# ZSK Coding Plugins Marketplace

[English](./README.md) | [中文](./README_CN.md)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

A collection of Claude Code plugins developed by zhangshikang to enhance coding productivity and development experience.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| **[session-export](plugins/session-export/)** | List, search, and export Claude Code sessions to Markdown/JSON format |

## Quick Start

### Prerequisites

- Node.js 18 or higher
- Claude Code CLI

### Method A: Install via Plugin Marketplace (Recommended)

```bash
# Add plugin marketplace
claude plugin marketplace add https://raw.githubusercontent.com/zhangshikang067/zsk-coding-plugins/main/.claude-plugin/marketplace.json

# Install plugin
claude plugin install session-export@zhangshikang067
```

### Method B: Manual Installation

```bash
# Clone repository
git clone https://github.com/zhangshikang067/zsk-coding-plugins.git ~/.claude/plugins/repos/zsk-coding-plugins

# Restart Claude Code
```

## Using Plugins

After installation, use directly in Claude Code:

```
"List my recent sessions"
"Export session ab5715bf to file"
```

## Plugin Development

### Adding New Plugins

1. Create a new plugin directory under `plugins/`
2. Organize your plugin with the following structure:

```
plugins/your-plugin/
├── agents/           # Agent definitions (optional)
├── commands/         # Command definitions (optional)
├── skills/           # Skill definitions (optional)
│   └── your-skill/
│       └── SKILL.md
├── scripts/          # Helper scripts (optional)
└── README.md         # Plugin documentation
```

3. Register new plugin in `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "category": "development",
  "description": "Plugin description"
}
```

### Plugin Structure Guidelines

Each plugin should include:

- **SKILL.md** - Skill definition describing when to activate
- **commands/** - Command files (if any commands)
- **agents/** - Agent definitions (if any agents)
- **scripts/** - Python/Node scripts (if needed)
- **README.md** - Plugin usage documentation

## Contributing

Contributions are welcome! Feel free to submit Issues or Pull Requests.

### Contribution Guide

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-plugin`)
3. Commit changes (`git commit -m 'Add amazing plugin'`)
4. Push to branch (`git push origin feature/amazing-plugin`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details

## Author

**zhangshikang**

- GitHub: [@zhangshikang067](https://github.com/zhangshikang067)
- Email: zhangshikang067@gmail.com
