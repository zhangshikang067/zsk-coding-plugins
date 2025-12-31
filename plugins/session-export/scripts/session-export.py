#!/usr/bin/env python3
"""Export Claude Code session to markdown document."""

import argparse
import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def export_session_to_markdown(session_id: str, output_path: str | None = None) -> None:
    """
    Export session to markdown file.

    Args:
        session_id: Session UUID to export.
        output_path: Output file path. If None, uses session_id.md.
    """
    history_path = Path.home() / ".claude" / "history.jsonl"

    if not history_path.exists():
        print(f"Error: {history_path} not found")
        return

    # Read and filter session messages
    messages = []
    with open(history_path) as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("sessionId") == session_id:
                    messages.append(data)
            except json.JSONDecodeError:
                continue

    if not messages:
        print(f"No messages found for session: {session_id}")
        return

    # Sort by timestamp
    messages.sort(key=lambda x: x.get("timestamp", 0))

    # Generate markdown
    output_file = Path(output_path or f"session_{session_id[:8]}.md")

    with open(output_file, "w") as f:
        # Header
        f.write(f"# Claude Code Session\n\n")
        f.write(f"**Session ID**: `{session_id}`\n\n")
        f.write(f"**Date**: {datetime.fromtimestamp(messages[0].get('timestamp', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Project**: `{messages[0].get('project', 'N/A')}`\n\n")
        f.write("---\n\n")

        # Messages
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            display = msg.get("display", "")

            if display:
                f.write(f"## {role.capitalize()}\n\n")
                f.write(f"{display}\n\n")
            elif content:
                f.write(f"## {role.capitalize()}\n\n")
                f.write(f"{content}\n\n")

            f.write("---\n\n")

    print(f"Session exported to: {output_file}")
    print(f"Total messages: {len(messages)}")


def format_relative_time(timestamp_ms: int) -> str:
    """Format timestamp as relative time."""
    now = datetime.now().timestamp()
    delta_sec = now - (timestamp_ms / 1000)

    if delta_sec < 60:
        return f"{int(delta_sec)}秒前"
    elif delta_sec < 3600:
        return f"{int(delta_sec / 60)}分钟前"
    elif delta_sec < 86400:
        hours = int(delta_sec / 3600)
        return f"{hours}小时前" if hours < 24 else "昨天"
    elif delta_sec < 172800:
        return "昨天"
    elif delta_sec < 604800:
        days = int(delta_sec / 86400)
        return f"{days}天前"
    else:
        return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")


def truncate_path(path: str, max_len: int = 40) -> str:
    """Truncate path with ellipsis."""
    if len(path) <= max_len:
        return path
    # Keep directory name and filename
    parts = path.split("/")
    if len(parts) > 3:
        return f".../{parts[-2]}/{parts[-1]}"
    return path


def truncate_preview(text: str, max_len: int = 50) -> str:
    """Truncate preview text with ellipsis."""
    if not text:
        return ""
    # Remove newlines and extra whitespace
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def get_session_preview(history_path: Path, session_id: str) -> tuple[str, bool]:
    """
    Get first meaningful message as preview.

    Returns:
        Tuple of (preview_text, is_command_only)
    """
    try:
        # Read all messages for this session
        messages = []
        with open(history_path) as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get("sessionId") == session_id:
                        messages.append(data)
                except json.JSONDecodeError:
                    continue

        # Separate commands and regular messages
        commands = []
        regular_messages = []

        for msg in messages:
            display = msg.get("display", "")
            if display.startswith("/"):
                # Extract command name
                cmd = display.split()[0].replace("/", "")
                commands.append(cmd)
            elif display and len(display) > 3:
                regular_messages.append(display)

        # Return first regular message if exists
        if regular_messages:
            return truncate_preview(regular_messages[0], 70), False

        # Return commands list if only commands
        if commands:
            unique_cmds = list(dict.fromkeys(commands))  # Preserve order, remove duplicates
            if len(unique_cmds) <= 3:
                cmd_list = " ".join(f"/{c}" for c in unique_cmds)
                return f"[dim cyan]命令: {cmd_list}[/dim cyan]", True
            else:
                return f"[dim cyan]命令: /{' /'.join(unique_cmds[:3])} ... (+{len(unique_cmds)-3})[/dim cyan]", True

    except Exception:
        pass
    return "", False


def list_recent_sessions(limit: int = 15) -> None:
    """List recent sessions with rich table and preview."""
    history_path = Path.home() / ".claude" / "history.jsonl"

    if not history_path.exists():
        console.print("[red]Error: history.jsonl not found[/red]")
        return

    # Collect sessions and messages
    sessions = {}
    session_messages = {}

    with open(history_path) as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                sid = data.get("sessionId")
                if sid:
                    # Initialize session if not exists
                    if sid not in sessions:
                        sessions[sid] = {
                            "id": sid,
                            "timestamp": data.get("timestamp", 0),
                            "project": data.get("project", "N/A"),
                        }
                        session_messages[sid] = []

                    # Collect messages for preview
                    session_messages[sid].append(data)
            except json.JSONDecodeError:
                continue

    # Sort by timestamp
    sorted_sessions = sorted(sessions.values(), key=lambda x: x["timestamp"], reverse=True)[:limit]

    # Create table
    table = Table(
        title=f"[bold cyan]最近 {len(sorted_sessions)} 个会话[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        padding=(0, 1),
        collapse_padding=True,
    )
    table.add_column("ID", style="cyan", width=10)
    table.add_column("时间", style="green", width=10)
    table.add_column("对话预览", style="white", no_wrap=False)
    table.add_column("路径", style="dim", width=22)

    for i, s in enumerate(sorted_sessions, 1):
        sid = s["id"]
        sid_short = sid[:8]
        relative_time = format_relative_time(s["timestamp"])
        msg_count = len(session_messages.get(sid, []))
        project_path = truncate_path(s["project"] or "N/A", 22)

        # Get preview from first user message
        preview, is_cmd = get_session_preview(history_path, sid)
        if not preview:
            preview = f"[dim]({msg_count} 条消息)[/dim]"

        # Color code recent sessions
        time_style = "green" if "分钟前" in relative_time or "小时前" in relative_time else "dim"

        table.add_row(
            Text(sid_short, style="bold cyan"),
            Text(relative_time, style=time_style),
            Text.from_markup(preview),
            Text(project_path, style="dim"),
        )

    console.print(table)
    console.print(f"\n[dim]提示: 使用 python3 export_session.py --session <ID> 导出会话[/dim]\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Claude Code session to markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 export_session.py --list              # 列出最近15个会话
  python3 export_session.py --list --limit 20   # 列出最近20个会话
  python3 export_session.py --session ab5715bf  # 导出指定会话
  python3 export_session.py -s ab5715bf -o doc.md # 导出到指定文件
        """
    )
    parser.add_argument("--list", "-l", action="store_true", help="列出最近的会话")
    parser.add_argument("--session", "-s", help="要导出的会话ID")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--limit", type=int, default=15, help="显示的会话数量 (默认: 15)")

    args = parser.parse_args()

    if args.list:
        list_recent_sessions(args.limit)
    elif args.session:
        export_session_to_markdown(args.session, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
