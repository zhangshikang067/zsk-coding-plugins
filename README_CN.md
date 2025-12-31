# ZSK 编程插件市场

[English](./README.md) | [中文](./README_CN.md)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

zhangshikang 开发的 Claude Code 插件集合，提升编码效率和开发体验。

## 可用插件

| 插件 | 描述 |
|------|------|
| **[session-export](plugins/session-export/)** | 列出、搜索和导出 Claude Code 会话到 Markdown/JSON 格式 |

## 快速开始

### 前置要求

- Node.js 18 或更高版本
- Claude Code CLI

### 方法 A：通过插件市场安装（推荐）

```bash
# 添加插件市场
claude plugin marketplace add https://raw.githubusercontent.com/zhangshikang067/zsk-coding-plugins/main/.claude-plugin/marketplace.json

# 安装插件
claude plugin install session-export@zhangshikang067
```

### 方法 B：手动安装

```bash
# 克隆仓库
git clone https://github.com/zhangshikang067/zsk-coding-plugins.git ~/.claude/plugins/repos/zsk-coding-plugins

# 重启 Claude Code
```

## 使用插件

安装后，在 Claude Code 中直接使用：

```
"列出我最近的会话"
"导出会话 ab5715bf 到文件"
```

## 插件开发

### 添加新插件

1. 在 `plugins/` 目录下创建新的插件目录
2. 按照以下结构组织插件：

```
plugins/your-plugin/
├── agents/           # Agent 定义（可选）
├── commands/         # 命令定义（可选）
├── skills/           # 技能定义（可选）
│   └── your-skill/
│       └── SKILL.md
├── scripts/          # 辅助脚本（可选）
└── README.md         # 插件说明
```

3. 在 `.claude-plugin/marketplace.json` 中注册新插件：

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "category": "development",
  "description": "插件描述"
}
```

### 插件结构规范

每个插件应包含：

- **SKILL.md** - 技能定义，描述何时触发
- **commands/** - 命令文件（如果有命令）
- **agents/** - Agent 定义（如果有 agent）
- **scripts/** - Python/Node 脚本（如果需要）
- **README.md** - 插件使用说明

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-plugin`)
3. 提交更改 (`git commit -m 'Add amazing plugin'`)
4. 推送到分支 (`git push origin feature/amazing-plugin`)
5. 开启 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 作者

**zhangshikang**

- GitHub: [@zhangshikang067](https://github.com/zhangshikang067)
- Email: zhangshikang067@gmail.com

## 相关链接

- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Claude Code 插件开发指南](https://docs.anthropic.com/claude-code/plugins)
- [示例插件](https://github.com/anthropics/claude-plugins-official)
