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

### 怎么让它走

策略吃的是 **7 维 command**。零指令（全 0）只站着；**`command[0] = +0.15` 是前进**。这就是录像里鸭子迈步的原因，不是换模型、也不是按错仿真器。

D1.2 那条录像用的是定时指令，不是手按上箭头：

| 仿真时间 | command | 预期 |
|---|---|---|
| 0–3 s | `[0, 0, 0, 0, 0, 0, 0]` | 站立 |
| 3–6 s | **`[0.15, 0, 0, 0, 0, 0, 0]`** | 前进迈步 |
| 6–8 s | 全 0 | 再站住，然后结束 |

在 WSL2（已装好 Playground + 官方 ONNX）里：

```bash
cd ~/3-month-challenge   # 或本仓库路径
chmod +x scripts/run_walk.sh
./scripts/run_walk.sh
```

等价于录像里的命令（把仓库路径换成你的）：

```bash
export DISPLAY=:0 MUJOCO_GL=glfw
export OPEN_DUCK_PLAYGROUND=~/Open_Duck_Playground
export OPEN_DUCK_MINI=~/Open_Duck_Mini
~/env_duck_playground/bin/python ~/3-month-challenge/scripts/run_openduck_eval.py
```

终端应打印 `obs shape: (101,)`、`action shape: (14,)`、`actuator count: 14`，以及上面那张 schedule。日志默认写到 `~/openduck_eval.csv`。

**不要**用 `Open_Duck_Mini/.../scene.xml` 播这份 ONNX（16 个执行器，对不上）。

交互试玩（不写死 schedule）仍可用官方查看器，上箭头一般对应前进，以 Playground 按键为准：

```bash
./scripts/run_infer.sh
```

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
scripts/run_infer.sh      交互查看器入口
scripts/run_walk.sh       D1.2 行走（定时 command[0]=0.15）
scripts/run_openduck_eval.py
```

不包含：其它业务系统、Isaac 工程、训练权重、飞书全文镜像。

---

## 许可

运行脚本与本文以本仓库 LICENSE 为准。模型、策略、Playground、Runtime 遵循各自上游许可。
