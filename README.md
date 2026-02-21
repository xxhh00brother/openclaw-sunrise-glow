# 🌅 Sunrise Glow - 早霞晚霞预测系统

专业的朝霞/晚霞拍摄条件预测工具，帮助摄影师捕捉最佳光线时刻。

![GitHub](https://img.shields.io/github/license/xxhh00brother/openclaw-sunrise-glow)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)

---

## ✨ 功能特点

- **1-10 分评分系统** - 直观的拍摄条件评分
- **颜色预测** - 预测朝霞/晚霞的颜色（金红、橙粉、紫红等）
- **最佳时间窗口** - 精确到分钟的拍摄时间建议
- **多地点支持** - 任意城市名或经纬度
- **完全免费** - 使用 Open-Meteo + Sunrise-Sunset.org 免费 API

---

## 🎯 预测算法

基于专业摄影师经验的智能评分：

| 因素 | 影响 | 说明 |
|------|------|------|
| **高云（6000m+）** | ⭐⭐⭐ 大幅加分 | 高层云反射阳光效果最佳 |
| **中云（2000-6000m）** | ⭐⭐ 加分 | 中层云散射光线，增加色彩层次 |
| **低云（0-2000m）** | ⚠️ 扣分 | 低云遮挡阳光，影响拍摄效果 |
| **湿度（60-80%）** | ⭐ 加分 | 适当湿度使颜色更红艳 |
| **日落后 15-20 分钟** | ⭐⭐ 黄金时间 | 最佳拍摄窗口 |

---

## 📋 输出示例

```
📍 Oakville - 2026 年 2 月 20 日

🌅 早霞预测：7/10 ⭐⭐⭐⭐⭐
颜色：金红色
最佳时间：06:42-07:05
原因：高云覆盖率 45%，湿度 72%，条件优秀

🌇 晚霞预测：5/10 ⭐⭐⭐
颜色：橙粉色
最佳时间：18:15-18:35
原因：低云较多，可能遮挡部分阳光
```

---

## 🚀 快速开始

### 前置要求

- Python 3.6+
- OpenClaw 运行环境
- 网络连接（调用天气 API）

### 安装与启动

```bash
# 克隆仓库
git clone https://github.com/xxhh00brother/openclaw-sunrise-glow.git
cd openclaw-sunrise-glow

# 一键启动（需要 OpenClaw 环境）
./start-sunrise-glow.sh
```

### 作为 OpenClaw Skill 使用

```bash
# 将 skill 复制到 OpenClaw workspace
cp -r sunrise-glow /path/to/your/openclaw/workspace/skills/

# 在 OpenClaw 中启动
cd /path/to/your/openclaw/workspace/skills/sunrise-glow
./start-sunrise-glow.sh
```

---

## 📁 项目结构

```
sunrise-glow/
├── README.md               # 本文件
├── SKILL.md               # OpenClaw Skill 定义
├── start-sunrise-glow.sh  # 一键启动脚本
├── src/
│   ├── __init__.py
│   ├── predictor.py       # 预测算法核心
│   └── display.py         # 展示输出模块
├── data/                  # 历史预测数据
└── tests/                 # 测试用例
```

---

## 🤖 多 Agent 架构

本系统使用 OpenClaw 多 Agent 框架自动协作：

| Agent | 角色 | 职责 |
|-------|------|------|
| **Athena** 🦉 | 协调者 | 监督进度、汇报用户、处理问题 |
| **Titan** 🏛️ | 后端开发 | API 集成、预测算法、数据处理 |
| **Luna** 🌙 | 前端展示 | 人类可读输出、多地点对比 |

---

## 📡 数据源

| API | 用途 | 费用 |
|-----|------|------|
| [Open-Meteo](https://open-meteo.com/) | 分层云量、湿度、气压、风速 | 免费 |
| [Sunrise-Sunset.org](https://sunrise-sunset.org/) | 日出日落时间 | 免费 |

---

## 📊 评分说明

| 分数 | 等级 | 拍摄建议 |
|------|------|----------|
| 9-10 | 极佳 | 必须出门，绝佳拍摄机会 |
| 7-8 | 优秀 | 强烈推荐，条件很好 |
| 5-6 | 良好 | 可以尝试，有一定机会 |
| 3-4 | 一般 | 条件一般，不建议专门前往 |
| 1-2 | 较差 | 不建议，可能失望 |

---

## 🛠️ 开发

### 添加新地点

```python
from src.predictor import GlowPredictor

predictor = GlowPredictor()
result = predictor.predict(location="Beijing", days=3)
print(result)
```

### 自定义输出格式

编辑 `src/display.py` 修改输出模板。

---

## 📝 更新日志

### v1.0.0 (2026-02-21)
- ✅ 初始版本发布
- ✅ 基础预测算法
- ✅ 多 Agent 自动协作
- ✅ OpenClaw Skill 集成

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Open-Meteo](https://open-meteo.com/) - 免费天气 API
- [Sunrise-Sunset.org](https://sunrise-sunset.org/) - 日出日落时间 API
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架

---

**📸 祝你捕捉到完美的朝霞晚霞！**
