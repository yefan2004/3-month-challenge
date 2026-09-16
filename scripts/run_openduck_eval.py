"""Scheduled ONNX playback: stand, then command[0]=0.15 walk, then stand.

This produced the D1.2 walk recording. See README section 怎么让它走.
"""
import csv
import os
import sys
from pathlib import Path

import mujoco
import numpy as np
import mujoco.viewer
import time

PLAYGROUND = Path(
    os.environ.get("OPEN_DUCK_PLAYGROUND", Path.home() / "Open_Duck_Playground")
).expanduser()
MINI = Path(os.environ.get("OPEN_DUCK_MINI", Path.home() / "Open_Duck_Mini")).expanduser()
sys.path.insert(0, str(PLAYGROUND))

from playground.common.onnx_infer import OnnxInfer
from playground.common.poly_reference_motion_numpy import PolyReferenceMotion
from playground.common.utils import LowPassActionFilter
from playground.open_duck_mini_v2.mujoco_infer_base import MJInferBase

USE_MOTOR_SPEED_LIMITS = True
MAX_SIM_SECONDS = 8.0
CSV_PATH = os.environ.get(
    "OPEN_DUCK_EVAL_CSV", str(Path.home() / "openduck_eval.csv")
)
FALL_HEIGHT_FRACTION = 0.5

DEFAULT_XML = str(
    PLAYGROUND / "playground/open_duck_mini_v2/xmls/scene_flat_terrain.xml"
)
DEFAULT_ONNX = os.environ.get(
    "OPEN_DUCK_ONNX", str(MINI / "BEST_WALK_ONNX_2.onnx")
)
DEFAULT_REFERENCE = str(
    PLAYGROUND / "playground/open_duck_mini_v2/data/polynomial_coefficients.pkl"
)
FORBIDDEN_XML = str(MINI / "mini_bdx/robots/open_duck_mini_v2/scene.xml")

COMMAND_SCHEDULE = [
    (0.0, 3.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    (3.0, 6.0, [0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    (6.0, 8.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
]


def command_at(sim_time: float) -> np.ndarray:
    for start, end, cmd in COMMAND_SCHEDULE:
        if start <= sim_time < end:
            return np.array(cmd, dtype=np.float32)
    return np.array(COMMAND_SCHEDULE[-1][2], dtype=np.float32)


def has_nan_or_inf(*arrays) -> bool:
    for arr in arrays:
        x = np.asarray(arr)
        if x.size == 0:
            continue
        if not np.isfinite(x).all():
            return True
    return False


class MjEval(MJInferBase):
    def __init__(self, model_path: str, reference_data: str, onnx_model_path: str):
        super().__init__(model_path)

        self.dof_vel_scale = 0.05
        self.action_scale = 0.25
        self.action_filter = LowPassActionFilter(50, cutoff_frequency=37.5)
        self.PRM = PolyReferenceMotion(reference_data)
        self.policy = OnnxInfer(onnx_model_path, awd=True)

        self.last_action = np.zeros(self.num_dofs)
        self.last_last_action = np.zeros(self.num_dofs)
        self.last_last_last_action = np.zeros(self.num_dofs)
        self.commands = np.zeros(7, dtype=np.float32)
        self.imitation_i = 0
        self.imitation_phase = np.array([0.0, 0.0])
        self.max_motor_velocity = 5.24
        self.phase_frequency_factor = 1.0

        home_qpos = np.array(self.model.keyframe("home").qpos)
        self.home_root_z = float(
            home_qpos[self._floating_base_qpos_addr + 2]
        )
        self.fall_z = FALL_HEIGHT_FRACTION * self.home_root_z
        self.control_freq = 1.0 / (self.sim_dt * self.decimation)
        self.xml_path = model_path
        self.onnx_path = onnx_model_path

    def get_obs(self, data, command):
        gyro = self.get_gyro(data)
        accelerometer = self.get_accelerometer(data)
        accelerometer[0] += 1.3
        joint_angles = self.get_actuator_joints_qpos(data.qpos)
        joint_vel = self.get_actuator_joints_qvel(data.qvel)
        contacts = self.get_feet_contacts(data)
        obs = np.concatenate(
            [
                gyro,
                accelerometer,
                command,
                joint_angles - self.default_actuator,
                joint_vel * self.dof_vel_scale,
                self.last_action,
                self.last_last_action,
                self.last_last_last_action,
                self.motor_targets,
                contacts,
                self.imitation_phase,
            ]
        )
        return obs

    def print_run_header(self):
        print("XML path:", self.xml_path)
        print("ONNX path:", self.onnx_path)
        print("obs shape:", (101,))
        print("action shape:", (self.num_dofs,))
        print("control frequency Hz:", self.control_freq)
        print("actuator count:", self.num_dofs)
        print("actuator names:", self.actuator_names)
        print("action_scale:", self.action_scale)
        print("home root_z (keyframe home):", self.home_root_z)
        print(
            "fall root_z threshold "
            f"({FALL_HEIGHT_FRACTION} * home root_z):",
            self.fall_z,
        )
        print("command schedule:")
        for start, end, cmd in COMMAND_SCHEDULE:
            print(f"  {start:.0f}–{end:.0f}s: {cmd}")

    def run(self):
        self.print_run_header()
        if self.xml_path == FORBIDDEN_XML:
            raise SystemExit("Refusing 16-actuator Open_Duck_Mini scene.xml")
        if self.num_dofs != 14:
            raise SystemExit(f"actuator count mismatch: {self.num_dofs}")

        csv_fields = (
            ["time"]
            + [f"command{i}" for i in range(7)]
            + ["root_x", "root_y", "root_z"]
            + ["root_qw", "root_qx", "root_qy", "root_qz"]
            + ["root_linvel_x", "root_linvel_y", "root_linvel_z"]
            + ["root_angvel_x", "root_angvel_y", "root_angvel_z"]
            + [f"action{i}" for i in range(14)]
            + ["nan_or_inf"]
        )

        stop_reason = "sim_time_reached"
        printed_shapes = False
        csv_parent = os.path.dirname(os.path.abspath(CSV_PATH))
        if csv_parent:
            os.makedirs(csv_parent, exist_ok=True)

        with open(CSV_PATH, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
            writer.writeheader()

            with mujoco.viewer.launch_passive(
                self.model,
                self.data,
                show_left_ui=False,
                show_right_ui=False,
            ) as viewer:
                counter = 0
                action = np.zeros(self.num_dofs)
                while True:
                    sim_time = float(self.data.time)
                    if sim_time >= MAX_SIM_SECONDS:
                        stop_reason = "sim_time_reached"
                        print(f"STOP after {MAX_SIM_SECONDS} seconds sim time")
                        break

                    step_start = time.time()
                    mujoco.mj_step(self.model, self.data)
                    counter += 1

                    if counter % self.decimation == 0:
                        sim_time = float(self.data.time)
                        self.commands = command_at(sim_time)

                        self.imitation_i += 1.0 * self.phase_frequency_factor
                        self.imitation_i = (
                            self.imitation_i % self.PRM.nb_steps_in_period
                        )
                        self.imitation_phase = np.array(
                            [
                                np.cos(
                                    self.imitation_i
                                    / self.PRM.nb_steps_in_period
                                    * 2
                                    * np.pi
                                ),
                                np.sin(
                                    self.imitation_i
                                    / self.PRM.nb_steps_in_period
                                    * 2
                                    * np.pi
                                ),
                            ]
                        )

                        obs = np.asarray(
                            self.get_obs(self.data, self.commands),
                            dtype=np.float32,
                        )
                        if obs.shape != (101,):
                            raise RuntimeError(
                                f"obs shape mismatch: {obs.shape}, expected (101,)"
                            )
                        action = np.asarray(self.policy.infer(obs), dtype=np.float32)
                        if action.shape != (14,):
                            raise RuntimeError(
                                f"action shape mismatch: {action.shape}, expected (14,)"
                            )
                        if not printed_shapes:
                            print("runtime obs shape", obs.shape)
                            print("runtime action shape", action.shape)
                            printed_shapes = True

                        nan_inf = has_nan_or_inf(
                            obs,
                            action,
                            self.data.qpos,
                            self.data.qvel,
                            self.data.ctrl,
                        )
                        qpos_addr = self._floating_base_qpos_addr
                        qvel_addr = self._floating_base_qvel_addr
                        root_z = float(self.data.qpos[qpos_addr + 2])

                        row = {
                            "time": sim_time,
                            "root_x": float(self.data.qpos[qpos_addr + 0]),
                            "root_y": float(self.data.qpos[qpos_addr + 1]),
                            "root_z": root_z,
                            "root_qw": float(self.data.qpos[qpos_addr + 3]),
                            "root_qx": float(self.data.qpos[qpos_addr + 4]),
                            "root_qy": float(self.data.qpos[qpos_addr + 5]),
                            "root_qz": float(self.data.qpos[qpos_addr + 6]),
                            "root_linvel_x": float(self.data.qvel[qvel_addr + 0]),
                            "root_linvel_y": float(self.data.qvel[qvel_addr + 1]),
                            "root_linvel_z": float(self.data.qvel[qvel_addr + 2]),
                            "root_angvel_x": float(self.data.qvel[qvel_addr + 3]),
                            "root_angvel_y": float(self.data.qvel[qvel_addr + 4]),
                            "root_angvel_z": float(self.data.qvel[qvel_addr + 5]),
                            "nan_or_inf": int(nan_inf),
                        }
                        for i in range(7):
                            row[f"command{i}"] = float(self.commands[i])
                        for i in range(14):
                            row[f"action{i}"] = float(action[i])
                        writer.writerow(row)
                        csv_file.flush()

                        if nan_inf:
                            stop_reason = "nan_or_inf"
                            print("STOP: NaN or Inf in obs/action/state")
                            break
                        if root_z < self.fall_z:
                            stop_reason = "fallen"
                            print(
                                "STOP: root_z "
                                f"{root_z} < fall threshold {self.fall_z} "
                                f"(home root_z={self.home_root_z})"
                            )
                            break

                        self.last_last_last_action = self.last_last_action.copy()
                        self.last_last_action = self.last_action.copy()
                        self.last_action = action.copy()
                        self.motor_targets = (
                            self.default_actuator + action * self.action_scale
                        )
                        if USE_MOTOR_SPEED_LIMITS:
                            self.motor_targets = np.clip(
                                self.motor_targets,
                                self.prev_motor_targets
                                - self.max_motor_velocity
                                * (self.sim_dt * self.decimation),
                                self.prev_motor_targets
                                + self.max_motor_velocity
                                * (self.sim_dt * self.decimation),
                            )
                            self.prev_motor_targets = self.motor_targets.copy()
                        self.data.ctrl = self.motor_targets.copy()

                    viewer.sync()
                    time_until_next_step = self.model.opt.timestep - (
                        time.time() - step_start
                    )
                    if time_until_next_step > 0:
                        time.sleep(time_until_next_step)

        print("stop_reason:", stop_reason)
        print("csv:", CSV_PATH)


if __name__ == "__main__":
    eval_runner = MjEval(DEFAULT_XML, DEFAULT_REFERENCE, DEFAULT_ONNX)
    eval_runner.run()
