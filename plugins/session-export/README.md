# Session Export

列出、搜索和导出 Claude Code 会话到 Markdown/JSON 格式的插件。

## 功能

- 📋 **列出会话** - 查看最近的对话历史
- 🔍 **对话预览** - 显示每个会话的首条消息或命令
- 💾 **导出会话** - 导出为 Markdown 格式
- 🎨 **美化输出** - 使用 Rich 库提供彩色表格显示
- ⏰ **相对时间** - 显示"2小时前"、"昨天"等友好时间

## 使用

### 列出会话

```
"列出我最近的会话"
```

或直接使用脚本：

```bash
python3 scripts/session-export.py --list
```

### 导出会话

```
"导出会话 ab5715bf"
```

或：

```bash
python3 scripts/session-export.py --session ab5715bf -o output.md
```

## 显示效果

```
┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID         ┃时间       ┃对话预览                     ┃路径                   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ ab5715bf   │52分钟前   │开发K8s部署工具              │.../my/ops_copilot     │
└────────────┴───────────┴─────────────────────────────┴───────────────────────┘
```

## 依赖

- Python 3.11+
- rich (`pip install rich`)

## 脚本参数

```bash
# 列出会话
python3 scripts/session-export.py --list [--limit N]

# 导出会话
python3 scripts/session-export.py --session <ID> [--output FILE]
```

## 作者

zhangshikang
