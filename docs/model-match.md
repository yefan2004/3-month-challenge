# 模型与策略匹配

官方行走 ONNX（`BEST_WALK_ONNX_2.onnx`）与 **Open Duck Mini 仓库里的 `scene.xml` 不是同一套接口**。

| | `Open_Duck_Mini/.../scene.xml` | Playground `scene_flat_terrain.xml` + 该 ONNX |
|---|---|---|
| 执行器 | 16 个 torque motor（含左右天线） | 14 个 position actuator（无天线） |
| 策略输入 | 不匹配 | 101 |
| 策略输出 | 14，不能直接写入 16 维 `data.ctrl` | 14，与 `model.nu` 一致 |
| 用途 | 模型查看 / 非本策略播放 | 本 Demo 的播放环境 |

观测 101 维在 `mujoco_infer.py` 的 `get_obs()` 中拼装（gyro、加速度、7 维 command、关节位置相对默认姿态、关节速度、历史动作、电机目标、足底接触、步态相位）。控制频率为 50 Hz，动作为默认站立姿态 + `action * 0.25`。

本 Demo 仿真只启动 Playground 入口。真机使用 Runtime，同一 14 维策略，不提供把 14 维动作插入 16 维 ctrl 的适配层。
