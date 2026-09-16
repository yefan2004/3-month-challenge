# 3-month-challenge

> 挑战者：**Leo.zhang**  
> 周期：2026-09-16 至 2026-12-16  
> 公开仓库只记证据。私人材料不进这个仓库。

**目标只有一句：**  
做出两件能离开 AI 讲 15 分钟的东西，然后投机器人应用 / ROS2 集成岗。不是继续把 FAE 当终点，也不是再装一套仿真环境。

---

## 锁死（2026-09-17）

| 战场 | 做什么 | 证据长什么样 |
|---|---|---|
| 1. 英达视 AI AGV | 只选一个模块做到可验证：视觉对齐 / 手眼标定 / 规划耗时拆解，**三选一，不换** | 新数据或录像；能讲接口、坐标系、失败怎么恢复 |
| 2. OpenDuck | **已通路**：WSL2 + Open Duck Playground + `BEST_WALK_ONNX_2.onnx` | 鸭子能走，有录像。已有：Playground 里预训练策略站住约 10 秒 |

求职方向：机器人应用软件 / ROS2 系统集成 / MoveIt 机械臂应用。  
报价：税前 16–18K 可面议。12 月再投。

---

## 明确不做

- 双系统、Isaac Sim 4.5 / 5 / 6、Isaac Lab、Isaac Gym 当本季度主线
- NVIDIA 证书、再写一套 13 周大表、并行接单、买真鸭、把口头承诺当钱
- 把公司源码、客户、IP、内部文档传到这个仓库
- 同一套 AGV 系统拆成四张项目卡；守不住的精度 / 成功率数字

失败长这样：又在装环境，又在改计划。

---

## 三个月交付

| 阶段 | 截止 | 必须交出来 | 失败 |
|---|---|---|---|
| 月 1 | 10/16 | 工作模块有新数据或录像；鸭子能走并录像；诚实简历冻结，先不投 | 还在装环境、改路线 |
| 月 2 | 11/16 | 同一模块补失败与恢复；OpenDuck 加深一层或脱敏小 Demo | 再开第二战场 |
| 月 3 | 12/16 | 两段 15 分钟口述；投 20–30 个应用岗 | 还在装环境、改人设 |

每周：白天只推工作那一个模块；晚上 2 小时只做 OpenDuck 或脱敏 Demo。  
周五交三行证据。周日闭卷讲一遍。  
演示和截止日期前：**冻结，只检查，不加新功能。**

成功不看打卡漂不漂亮，只看：鸭子有没有走起来；工作模块有没有新证据。

---

## 当前进度（诚实）

**OpenDuck**

- 通路已核对：WSL2 + Playground + `BEST_WALK_ONNX_2.onnx`（101→14）
- 已做到：Playground 里站住约 10 秒
- 下一步：同一条命令再跑，**录走路视频**。不换仿真器

**AI AGV**

- 模块尚未从三选一里钉死
- 下一步：选定一个，写清「今晚检查什么」，开始留证据
- 端到端真机验证按 **3 次** 写，不写成稳定量产

**公开仓库**

- 9/16–9/17 曾把 Week 1 写成 Ubuntu / Isaac Gym / Isaac Sim 4.5。那是路线抖动，**作废**
- 本文件从 2026-09-17 起以本节为准

---

## 今晚 / 下一步（只一件）

不装 Isaac。不改系统。

OpenDuck 下一刀：在已有 WSL2 环境里用 Playground 播放 `BEST_WALK_ONNX_2.onnx`，录一段能看清鸭子在走的视频。  
AGV 那一刀放到选定模块之后，白天做。

---

## 资源（只保留在用的）

- [Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)
- [Open Duck Playground](https://github.com/apirrone/Open_Duck_Playground)
- 本机 Playground 推断入口（已核对过，不改原仓库）：  
  `uv run playground/open_duck_mini_v2/mujoco_infer.py -o /home/ubuntu/Open_Duck_Mini/BEST_WALK_ONNX_2.onnx`

Issue：[Week 1 任务清单 #1](https://github.com/yefan2004/3-month-challenge/issues/1) 仍是旧的双系统/Isaac 清单，作废，待网络恢复后改成与本文一致。
