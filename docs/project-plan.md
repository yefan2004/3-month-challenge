# Open Duck Mini 项目计划书（D1 + D2 + 实机）

| 项 | 内容 |
|---|---|
| 项目名称 | Open Duck Mini 推理闭环与实机部署 |
| 版本 | v0.3（2026-09-17：HW = **买零件 + 自主组装**，不买成品整机） |
| 负责人 | Leo.zhang |
| 周期 | 2026-09-16 ～ 2026-12-16 |
| 工时 | 工作日晚 2 小时只做 D1/D2；周末才打印 / 焊接 / 装配 |
| 装配 / 采购 SOP | 中文：[飞书知识库](https://zihao-ai.feishu.cn/wiki/space/7488517034406625281) |
| 英文 BOM | [官方表格](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc)（上游口径：全套零件低于 400 美元） |
| 仿真 SOP | [Open Duck Playground](https://github.com/apirrone/Open_Duck_Playground) |
| 实机 SOP | [Open_Duck_Mini_Runtime v2](https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2) + [sim2real.md](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md) |

本仓库只含本项目。

---

## 1. 要解决什么问题

把官方行走策略 `BEST_WALK_ONNX_2.onnx`（观测 101、动作 14）接到 **匹配的仿真** 和 **匹配的真机 Runtime**，并保证过程可复现、可检查。

已完成：Playground 零指令站立约 10 s。未完成：仿真行走录像、工程化检查、真机。

---

## 2. 目标与非目标

### 2.1 目标

| ID | 输出 | 完成定义 |
|---|---|---|
| D1 | 仿真行走 + 接口契约 | 第三人能按仓库启动 Playground；前进指令下鸭子行走并有录像；文档写清 101/14、50 Hz、`action_scale=0.25`、为何不能接 Mini 仓库 16 执行器 `scene.xml` |
| D2 | 可复现运行器 | `scripts/run_infer.sh` 可启动；启动前断言 ONNX 维数与 MJCF `nu==14`；一次运行写出 obs / action / command 日志 |
| HW | 实机 | 同一 ONNX 在树莓派 Runtime 上跑；官方 checklist（关节偏移、IMU、足底）通过后再上策略；手柄遥控行走并录像 |

### 2.2 非目标

- 从零训练新策略、刷 reward、域随机化论文
- 迁移 Isaac Lab / Isaac Sim 作为本项目主栈
- 头控（Runtime 明确不推荐，易损坏）
- 把其它业务系统写进本仓库
- 未过 checklist 就在真机上跑策略
- 买成品整机 / 代工组装。只买零件，自己打印、焊接、接线、装 Pi

---

## 3. 输入（基线）

| 项 | 现状 |
|---|---|
| 仿真 | WSL2 + Playground + `BEST_WALK_ONNX_2.onnx`，零指令站立已验证 |
| 主机 | 消费级笔记本 GPU 8 GB，只做仿真与打包，不做大规模训练 |
| 真机 | 尚未到件。路径：**按飞书 BOM 买零件，自主组装。** 下单截止 2026-10-06；**未付款则 HW 冻结**（口头确认不算） |
| 策略 | 全程同一文件 `BEST_WALK_ONNX_2.onnx`，仿真与实机不换模型 |

---

## 4. 工作分解

### 阶段 D1 — 仿真行走与契约（约 1.5 周）

| 任务 | 内容 | 验收 |
|---|---|---|
| D1.1 | 基线复现站立 | 现有命令可重复 |
| D1.2 | 查看器上箭头或等价 `command[0]=+0.15` | ≥10 s 行走录像 |
| D1.3 | 写完 `docs/model-match.md` | 含 16 vs 14、观测构成、频率、缩放 |

门禁：**D1 未关闭，不上真机策略。** 零件采购 / 打印可与 D1 并行，串口策略必须等 D1。

### 阶段 D2 — 运行器与检查（约 2 周，可与采购并行）

| 任务 | 内容 | 验收 |
|---|---|---|
| D2.1 | 固化 `scripts/run_infer.sh`（环境变量、缺文件退出） | 他人按 README 能启动或得到明确 error |
| D2.2 | 启动前检查：ONNX 输入 `[1,101]`、输出 `[1,14]`；XML `model.nu==14` | 故意指向 Mini `scene.xml` 时必须失败并退出 |
| D2.3 | 运行日志：每控制周期记录 command、obs shape、action shape | 一次行走过程可回放对齐按键 |

门禁：**D2.2 未通过，不认为工程可交付。**

### 阶段 HW — 实机

飞书负责：零件清单、购买、3D 打印、外壳、焊接、舵机接线。  
Runtime 负责：镜像或源码安装、I2C、串口、IMU、电机检查、关节偏移、`duck_config.json`、同一 ONNX 行走。

| 任务 | 内容 | 验收 |
|---|---|---|
| HW.0 | 冻结 BOM 并下单零件（舵机、Pi Zero 2W、IMU、结构件耗材等） | 型号+数量清单 + **订单号 / 付款记录**；未付款则 HW 整段冻结，D1/D2 照常 |
| HW.1 | 按飞书完成机械电气装配 | 上电后 `check_motors.py` 全关节应答 |
| HW.2 | Pi Zero 2W：官方预构建镜像 **或** README 手工安装，checkout `v2` | SSH 可用；I2C 开；可 `pip install -e .` |
| HW.3 | IMU 方向、`find_soft_offsets.py`、写入 `~/duck_config.json` | 与 Runtime checklist 一致 |
| HW.4 | Xbox 手柄配对（可选但推荐遥控） | `xbox_controller.py` 能读到按键 |
| HW.5 | **仅当 HW.1–HW.3 通过**：`python v2_rl_walk_mujoco.py --onnx_model_path …BEST_WALK_ONNX_2.onnx` | 暂停键可用；平地行走录像；**不开启头控 Y** |
| HW.6 | （加分）仿真日志与真机 `--save_obs` 各一段，对比维数与 command 是否同构 | 不必数值一致，必须维数一致 |

真机脚本文件名含 `mujoco`，实际打开 `/dev/ttyACM0`、IMU、足底，**不是**桌面 MuJoCo 查看器。禁止用 Mini 仓库的 `scene.xml` 播放脚本冒充实机。

---

## 5. 时间表

| 周 | 日期（约） | 主交付 | 并行 |
|---|---|---|---|
| 1 | 09-16 ～ 09-22 | D1.2 行走录像 | 周末：对照飞书导出零件清单（仍可不付款） |
| 2–3 | 09-23 ～ 10-06 | D2.1–D2.3 | HW.0：付款买零件；有打印机则开始打结构件 |
| 4–6 | 10-07 ～ 10-27 | 装配、Pi、电机、偏移 HW.1–HW.3 | D2 文档收口 |
| 7–9 | 10-28 ～ 11-16 | HW.4–HW.5 同一 ONNX 真机走 | 补 README 实机章节 |
| 10–13 | 11-17 ～ 12-16 | HW.6 可选；仓库只留可复现步骤与脱敏录像说明 | 缓冲翻车（舵机、串口、偏移） |

HW.0 = 10-06 前把零件付清。未付款则 HW 冻结。D1+D2 仍按期验收，不改仿真栈。自主组装只在周末进行。

---

## 6. 公开仓库里最终应有什么

第三人打开 GitHub 应能做到：

1. 按 README 在 Linux / WSL + GPU 上跑仿真推理（D1+D2）。
2. 按「真机」章节：飞书装配 + Runtime 安装 + checklist + 同一 ONNX 命令（HW）。

不存放飞书全文镜像、训练权重、其它业务代码。

---

## 7. 风险

| 风险 | 应对 |
|---|---|
| 飞书与上游步骤不一致 | 装配跟飞书；软件跟 Runtime `v2` README；冲突写进 `docs/` 一条「以谁为准」 |
| 未检查就上策略，舵机失控 | HW.5 强制依赖 HW.3；头控默认禁止 |
| 16 执行器模型混用 | D2.2 启动失败；实机侧只用 Runtime 14 DOF 策略接口 |
| 采购 / 打印拖期 | D1+D2 仍可独立交付；HW 降级为「未上机」 |
| 8 GB 显卡 | 不训练；只播放官方 ONNX |
| 经费 | 官方 BOM 低于 400 美元；国内按飞书报价核对。未付款则 HW.0 不通过 |
| 自组翻车（焊点、舵机 ID、打印公差） | 周末只做装配；策略仍等 HW.3。D1/D2 不替装配顶锅 |

---

## 8. 验收总表

**及格（没有真机也可以）：** D1 行走录像 + D2 断言与日志。

**完整通过：** 及格项 + HW.5 真机行走录像（同一 ONNX）。

**优秀：** 再加 HW.6 仿真 / 真机观测维数对照。

---

## 9. 已确认（2026-09-17）

1. 真机路径：买零件 + 自主组装，不买成品整机。
2. 2026-10-06 前零件付款才算 HW.0；口头「要买」不算。
3. 工作日晚 2 小时 = D1/D2；装配只在周末。
4. 运行说明见 [README.md](../README.md)，真机检查见 [hardware.md](hardware.md)。
