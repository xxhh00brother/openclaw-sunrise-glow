#!/bin/bash
# 早霞晚霞预测项目 - 一键启动脚本
# 执行此脚本启动所有 Agent

echo "🌅 早霞晚霞预测项目 - 启动器"
echo "================================"

# 项目配置
PROJECT_ID="7521215b"
SESSION_PREFIX="sunrise-glow"

# 启动 Athena (协调者)
echo ""
echo "1️⃣ 启动 Athena（协调者）..."
openclaw agent \
  --session-id "${SESSION_PREFIX}-athena" \
  --message "你是早霞晚霞预测系统的协调者。你的任务是：
1. 监督 Titan 后端开发
2. 协调 Luna 前端设计
3. 定期向用户汇报进度
4. 处理开发中的问题

技术栈：Python + Open-Meteo API + Sunrise-Sunset API

开始工作吧！"

# 等待一下
sleep 3

# 启动 Titan (后端)
echo ""
echo "2️⃣ 启动 Titan（后端开发）..."
openclaw agent \
  --session-id "${SESSION_PREFIX}-titan" \
  --message "你是早霞晚霞预测系统的后端开发者。

任务：
1. 集成 Open-Meteo API（获取分层云量、湿度、气压、风速）
2. 集成 Sunrise-Sunset.org API（获取日出日落时间）
3. 实现预测算法（基于专业摄影师经验）：
   - 高云（6000m+）反射最佳 → 加分
   - 中云（2000-6000m）散射 → 加分
   - 低云（0-2000m）遮挡 → 扣分
   - 湿度高（60-80%）颜色更红 → 加分
   - 日落后 15-20 分钟最佳
4. 输出 JSON 格式（包含 weather + glow_prediction）
5. 保存历史预测记录

开始开发后端！"

sleep 3

# 启动 Luna (前端)
echo ""
echo "3️⃣ 启动 Luna（前端展示）..."
openclaw agent \
  --session-id "${SESSION_PREFIX}-luna" \
  --message "你是早霞晚霞预测系统的前端展示工程师。

任务：
1. 设计人类可读输出格式（与 JSON 内容一致）
2. 实现多地点对比展示
3. 设计解读模板（JSON → 人类可读文字）
4. 准备 Skill 集成

输出格式示例：
📍 Oakville - 2026年2月20日

🌅 早霞预测：7/10 ⭐⭐⭐⭐⭐
颜色：金红色
原因：高云覆盖率 45%...

等待 Titan 后端完成后对接。

开始设计！"

echo ""
echo "================================"
echo "✅ 启动命令已执行！"
echo ""
echo "查看进度："
echo "  cd /home/admin/.openclaw/workspace/skills/multi-agent/scripts"
echo "  ./ma status ${PROJECT_ID}"
