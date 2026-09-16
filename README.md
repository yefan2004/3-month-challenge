# Open Duck Mini 推理 Demo

在匹配的仿真（[Open Duck Playground](https://github.com/apirrone/Open_Duck_Playground)）和匹配的真机（[Open Duck Mini Runtime v2](https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2)）上，播放同一份官方策略 `BEST_WALK_ONNX_2.onnx`（观测 101 维，动作 14 维）。

第三人按本文应能：在 Linux / WSL2 + GPU 上启动仿真推理；在检查清单通过后的真机上启动 Runtime 行走。

本仓库是运行说明、启动脚本和项目计划，不含上游仿真器源码，不含其它业务系统。

项目计划：[docs/project-plan.md](docs/project-plan.md)  
Week 1 清单：[docs/week-01.md](docs/week-01.md) · [Issue #1](https://github.com/yefan2004/3-month-challenge/issues/1)  
接口说明：[docs/model-match.md](docs/model-match.md)  
真机步骤：[docs/hardware.md](docs/hardware.md)

**不要**把该 ONNX 接到 `Open_Duck_Mini/.../scene.xml`（16 个力矩执行器）。

---

## 当前状态（2026-09-17）

| 阶段 | 状态 |
|---|---|
| D1.1 仿真零指令站立 | 已验证（约 10 s） |
| D1.2 仿真前进行走 | 已有录像（13 s 屏录）。日志：`command[0]=0.15` 仅 3–6 s；Playground + `BEST_WALK_ONNX_2.onnx`，obs 101 / act 14 |
| D1.3 接口文档 | [docs/model-match.md](docs/model-match.md) 已有初稿 |
| D2 启动脚本 | `scripts/run_infer.sh` 可启动；维数断言与运行日志未完成 |
| HW 真机 | 未到件。路径：**买零件 + 自主组装**，不买成品整机。零件付款截止 2026-10-06；未付款则 HW 冻结 |

---

## 仿真

### 要求

| 项 | 最低要求 |
|---|---|
| 系统 | Linux，或 Windows 下的 WSL2 |
| GPU | NVIDIA，`nvidia-smi` 可用 |
| 磁盘 | ≥ 20 GB 给 Playground 依赖 |
| 软件 | `git`、`curl`、Python 3.11+、`uv` |
| 显示 | MuJoCo 查看器需要 `DISPLAY`（WSLg 通常为 `:0`） |

未验证：macOS、无 GPU、Docker、Isaac Sim。本项目不把 Isaac 当主栈。

### 安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/apirrone/Open_Duck_Mini.git ~/Open_Duck_Mini
git clone https://github.com/apirrone/Open_Duck_Playground.git ~/Open_Duck_Playground

cd ~/Open_Duck_Playground
uv sync
```

策略文件：`~/Open_Duck_Mini/BEST_WALK_ONNX_2.onnx`（若仓库未带，按 Mini README 下载。本仓库不收录 ONNX）。

```bash
git clone https://github.com/yefan2004/3-month-challenge.git
cd 3-month-challenge
chmod +x scripts/run_infer.sh
```

### 运行

```bash
./scripts/run_infer.sh
```

等价：

```bash
cd ~/Open_Duck_Playground
uv run playground/open_duck_mini_v2/mujoco_infer.py \
  -o ~/Open_Duck_Mini/BEST_WALK_ONNX_2.onnx
```

`./scripts/run_infer.sh --help` 查看路径环境变量。

| 操作 | 预期 |
|---|---|
| 启动后、零指令 | 站立不倒 |
| 查看器上箭头 | `command[0] = +0.15`，应迈步 |
| 下 / 左 / 右箭头 | 后退 / 左移 / 右移（以 Playground 按键为准） |

查看器关闭时进程可能非零退出（WSLg/GLFW）。站立阶段无 Python traceback 则不视为策略加载失败。

已测：观测 `(101,)`，动作 `(14,)`，MJCF `scene_flat_terrain.xml`，50 Hz，`action_scale=0.25`。零指令 10 s 站立，XY 位移约 1 cm（符合零速度）。

---

## 真机

**买零件，自己打印、焊接、接线、装 Pi。** 不买成品整机。

- 装配 / BOM / 打印： [飞书知识库](https://zihao-ai.feishu.cn/wiki/space/7488517034406625281)
- 英文 BOM：[官方表格](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc)（上游口径：全套零件低于 400 美元）
- 软件：Runtime v2。同一 ONNX。

上策略前必须完成电机检查、IMU、关节偏移，见 [docs/hardware.md](docs/hardware.md)。不要开头控。D1 行走录像未完成前，不上真机策略。

检查通过后，在树莓派上：

```bash
cd ~/Open_Duck_Mini_Runtime/scripts
python v2_rl_walk_mujoco.py --onnx_model_path ~/BEST_WALK_ONNX_2.onnx
```

该脚本走串口与传感器，不是桌面仿真。

---

## 仓库内容

```text
README.md                 本说明
docs/project-plan.md      项目计划书（D1 / D2 / 实机）
docs/week-01.md           Week 1 任务清单
docs/model-match.md       14 执行器 vs 16 执行器
docs/hardware.md          真机检查清单与命令
scripts/run_infer.sh      仿真播放入口
```

不包含：其它业务系统、Isaac 工程、训练权重、飞书全文镜像。

---

## 许可

运行脚本与本文以本仓库 LICENSE 为准。模型、策略、Playground、Runtime 遵循各自上游许可。
