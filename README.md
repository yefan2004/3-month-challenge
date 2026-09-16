# 3个月机器人技术冲刺挑战 | 3-Month Robotics Challenge

> 📅 开始日期：2026-09-16  
> 📅 结束日期：2026-12-16  
> 👤 挑战者：Leo Zhang  
> 🎯 目标：从现场 FAE 转型为机器人软件工程师  
> 🔥 当前状态：**Week 1 Day 2**（2026-09-17）— 安装 Isaac Sim 4.5.0

仓库：[yefan2004/3-month-challenge](https://github.com/yefan2004/3-month-challenge)  
本周任务：[Issue #1](https://github.com/yefan2004/3-month-challenge/issues/1)  
本地路径：`D:\3-month-challenge`

---

## 已锁定的技术栈（2026-09-17）

| 项目 | 决定 |
|---|---|
| 系统 | **Windows 11 24H2 原生** |
| GPU | RTX 4060 Laptop **8 GB**（有光追，显存是短板） |
| 驱动 | 591.44（CUDA 13.1）。先不升级 |
| CPU / 内存 | i7-12650H（10 核 / 16 线程），32 GB |
| 仿真 | **Isaac Sim 4.5.0** Windows workstation zip → `D:\isaacsim` |
| 强化学习框架 | 4.5 能稳定打开后，再装 **Isaac Lab 2.1.x**（绑定 Sim 4.5） |
| 主项目 | [Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)（旧策略在 Isaac Gym；仓库已转向 MuJoCo Playground） |

**明确不做：**

- Ubuntu 双系统
- 在现有 WSL Ubuntu **26.04** 里装 Isaac Sim（官方只要 22.04 / 24.04）
- 一上来装 Isaac Sim **5.x / 6.x**（官方最低写成 RTX 4080 / 16 GB）
- 把已弃用的 Isaac Gym Preview 4 当 Week 1 主环境

**为什么选 4.5.0：** 这是仍写 **8 GB GPU** 的工作站版本，和这台笔记本匹配。5.0 起官方最低是 16 GB。8 GB 可以学界面、跑小场景；复杂场景和大规模训练会顶满显存。

---

## 进度追踪

**完成度：** 0%（0/13 周）

| 阶段 | 周数 | 核心任务 | 状态 | 计划日期 | 完成日期 |
|---|---|---|---|---|---|
| **Month 1** | Week 1 | Windows + Isaac Sim 4.5.0 环境 | 🔥 进行中 | 9/16–9/22 | - |
| | Week 2 | OpenDuck 预训练 / 遥控（以兼容性结论为准） | ⚪ 未开始 | 9/23–9/29 | - |
| | Week 3 | 自定义训练 + Reward 调优 | ⚪ 未开始 | 9/30–10/6 | - |
| | Week 4 | 总结发布 + 技术博客 | ⚪ 未开始 | 10/7–10/13 | - |
| **Month 2** | Week 5 | AI AGV 性能基线 | ⚪ 未开始 | 10/14–10/20 | - |
| | Week 6 | MoveIt 规划优化（上） | ⚪ 未开始 | 10/21–10/27 | - |
| | Week 7 | MoveIt 规划优化（下） | ⚪ 未开始 | 10/28–11/3 | - |
| | Week 8 | 自动化测试 | ⚪ 未开始 | 11/4–11/10 | - |
| **Month 3** | Week 9 | 整理作品集 + GitHub | ⚪ 未开始 | 11/11–11/17 | - |
| | Week 10 | 密集投递（第一轮） | ⚪ 未开始 | 11/18–11/24 | - |
| | Week 11 | 面试冲刺（第二轮） | ⚪ 未开始 | 11/25–12/1 | - |
| | Week 12 | 面试冲刺（第三轮） | ⚪ 未开始 | 12/2–12/8 | - |
| **收尾期** | Week 13 | 最终决策 + 复盘 | ⚪ 未开始 | 12/9–12/16 | - |

---

## Week 1（2026-09-16 至 2026-09-22）

### 本周目标

- [ ] 安装 Isaac Sim **4.5.0** 到 `D:\isaacsim`
- [ ] 跑 Compatibility Checker
- [ ] 启动 Isaac Sim，跑 Simple Room（必要时降到 1280×720 / Medium）
- [ ] `nvidia-smi` 截图：可见 RTX 4060，显存占用可控
- [ ] 写清 OpenDuck 真实依赖（Gym / MuJoCo Playground / 是否能接 Lab）
- [ ] （4.5 稳定后再做）安装 Isaac Lab 2.1.x，跑一个官方示例

### 验收

**最低标准（周日必须达到）：**

- [ ] Isaac Sim 4.5.0 能启动
- [ ] 至少一个小场景能渲染
- [ ] README 里写明 OpenDuck 兼容性结论
- [ ] 每天打卡未断

**理想标准：**

- [ ] Isaac Lab 2.1.x 至少一个示例能跑
- [ ] OpenDuck 代码已 clone，预训练权重能加载（不要求完全训通）

### 实际进展

**Day 1（2026-09-16 周三）**

- 正式启动挑战；本机当时未到位
- 方案从「Ubuntu 双系统 + Isaac Gym」改到「Windows + Isaac Lab」，再改到「Windows + Isaac Sim 4.5.0」
- 双系统准备（ISO / 启动盘 / 分区 / BIOS）**作废，不再执行**
- 投入时间：约 0.5 小时（调研，不是装系统）
- 打卡：[Issue #1 评论](https://github.com/yefan2004/3-month-challenge/issues/1#issuecomment-5687426580)

**Day 2（2026-09-17 周四）— 今天**

- [x] 公开仓库拉到本地：`D:\3-month-challenge`（不放 C 盘）
- [x] 锁定技术栈：Isaac Sim 4.5.0 Windows，不装双系统，不装 6.x
- [ ] 关闭占 GPU 的程序后，下载并解压 Isaac Sim 4.5.0 到 `D:\isaacsim`
- [ ] Compatibility Checker
- [ ] 首次启动 + Simple Room
- [ ] 晚上 21:30–22:00 打卡（截图 + 本 README + Issue 评论）

**Day 3（9/18）：** 驱动验收、显存策略、Isaac Lab 2.1.x 安装判断  
**Day 4（9/19）：** Lab 示例 或 OpenDuck 依赖核对  
**Day 5（9/20 周五）：** 中期检查，必须有 Isaac Sim 能跑的证据  
**Day 6–7（9/21–9/22）：** OpenDuck 结论 + Week 1 验收

### 遇到的问题

- **Day 1：** 硬件未到位 + 技术栈连改三轮，公开进度停在旧方案。应对：Day 2 先改仓库，再装 4.5.0。
- **持续风险：** [Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini) 旧策略在 Isaac Gym，当前训练转向 MuJoCo Playground，**不保证能直接跑在 Isaac Lab 上**。Day 5 前必须给出结论，再决定 Week 2 是接 Lab、走 Playground，还是先跑通预训练推理。

---

## Day 2 安装步骤（只装 4.5.0）

装之前：关掉浏览器 / Cursor AI 面板 / 其他占 GPU 的程序，尽量空出 8 GB 显存。建议装到 `D:\isaacsim`。

1. 打开 [Isaac Sim 下载页](https://developer.nvidia.com/isaac-sim)，登录 NVIDIA 账号，选 **4.5.0 Windows Workstation zip**，不要选 5.x / 6.x。
2. 解压到 `D:\isaacsim`。
3. 先跑 `D:\isaacsim\compatibility_checker.bat`。
4. 再跑 `D:\isaacsim\isaac-sim.bat`（首次会编译 shader，可能 5–10 分钟）。
5. 进界面后：`Create → Environment → Simple Room`，分辨率先用 1280×720，Quality Medium。
6. 截图：Compatibility Checker、主界面、Simple Room、`nvidia-smi`。

**翻车时：** 显存顶满就先关其他程序、再降画质；启动失败先看终端报错，补 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)。不要为此升级到 6.x。

---

## 打卡规则

- 每天 21:30 开始写，22:00 前更新本 README **和** [Issue #1](https://github.com/yefan2004/3-month-challenge/issues/1)
- 周五晚中期检查，周日晚周验收
- 连续 2 天未打卡 → 公开道歉；连续 3 天 → 视为放弃

---

## 资源

- [Isaac Sim](https://developer.nvidia.com/isaac-sim)
- [Isaac Lab](https://github.com/isaac-sim/IsaacLab)（4.5.0 对应 **v2.1.x**）
- [Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)
- [Open Duck Playground](https://github.com/apirrone/Open_Duck_Playground)

---

## 下周预告（Week 2）

取决于 Day 5 的 OpenDuck 兼容性结论：预训练推理 + 键盘/手柄遥控，或改到可运行的仿真栈。
