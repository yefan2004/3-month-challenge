# 实机部署

装配、采购、打印、焊接、舵机接线以飞书为准：  
https://zihao-ai.feishu.cn/wiki/space/7488517034406625281

英文 BOM：  
https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc

路径：**买零件 + 自主组装**，不买成品整机。

树莓派系统、Runtime、检查脚本、行走命令以官方仓库为准：  
https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2

冲突时：**机械电气跟飞书，软件跟 Runtime v2。**

仿真与真机使用同一策略文件：`BEST_WALK_ONNX_2.onnx`（输入 101，输出 14）。

`scripts/v2_rl_walk_mujoco.py` 名称含 mujoco，实际打开 `/dev/ttyACM0`、IMU、足底传感器，**不是**桌面 MuJoCo 查看器。

---

## 上策略之前必须完成

按顺序，缺一不可：

1. 机械电气装配完成（飞书）。
2. Pi Zero 2W 可 SSH；I2C 已开；Runtime `v2` 已安装。
3. `python3 scripts/check_motors.py` 全关节应答。
4. IMU 方向正确（`raw_imu.py` / 官方 imu server）。
5. `find_soft_offsets.py` 结果写入 `~/duck_config.json`。

未完成不要运行行走策略。不要打开头控（手柄 Y，官方不推荐，易损坏头部）。

可选：Xbox 手柄蓝牙配对，用 `xbox_controller.py` 确认按键。

---

## Pi 上安装（摘要）

完整步骤见 Runtime README。两条路任选其一：

- 官方预构建镜像（Pi Zero 2W / Raspberry Pi OS Lite 64-bit），再按仓库 `docs/INSTALL.md` 写入配置。
- 或：烧录 Lite 64-bit → SSH/WiFi → 开 I2C → clone Runtime、`git checkout v2` → `pip install -e .`

然后：

```bash
cp example_config.json ~/duck_config.json
# 编辑关节偏移与 IMU 安装方向
cd scripts
python find_soft_offsets.py
python check_motors.py
```

将 `BEST_WALK_ONNX_2.onnx` 拷到板子上（与仿真同一文件）。

---

## 行走

仅在上一节检查通过后：

```bash
cd ~/Open_Duck_Mini_Runtime/scripts
python v2_rl_walk_mujoco.py --onnx_model_path ~/BEST_WALK_ONNX_2.onnx
```

手柄（官方默认）：

- A：暂停 / 继续
- 不要按 Y（头控）

平地行走并录像。需要对照仿真时，可加官方 `--save_obs`，与仿真日志比维数和 command 是否同构，不要求数值一致。

---

## 本仓库不包含

BOM 价格表以外的采购隐私、公司项目、飞书全文镜像、未脱敏的现场照片中的个人信息。
