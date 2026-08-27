"""易动调研 MCP 服务（stdio）。

提供：竞品词表、术语解释、任务模板 —— 演示「业务工具经 MCP 热插拔」。
启动方式由 config/mcp.json 配置，Agent 创建时自动连接。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "data" / "research_assets.json"

mcp = FastMCP("yidong_research")


def _load() -> dict:
    return json.loads(ASSETS.read_text(encoding="utf-8"))


@mcp.tool()
def list_competitors() -> str:
    """列出易动纷享常见对标竞品及关注点（本地知识，非实时网页）。"""
    data = _load()
    lines = ["易动纷享常见对标竞品（本地知识库）："]
    for item in data.get("competitors", []):
        lines.append(
            f"- {item['name']}｜重点：{item['focus']}｜备注：{item.get('notes', '')}"
        )
    return "\n".join(lines)


@mcp.tool()
def lookup_glossary(term: str) -> str:
    """查询 R&D 调研常用术语解释。"""
    data = _load()
    glossary = data.get("glossary", {})
    key = (term or "").strip()
    if not key:
        return "请提供要查询的术语。"
    if key in glossary:
        return f"{key}：{glossary[key]}"
    for k, v in glossary.items():
        if key.lower() in k.lower() or k.lower() in key.lower():
            return f"{k}：{v}"
    known = "、".join(glossary.keys())
    return f"未找到「{key}」。已知术语：{known}"


@mcp.tool()
def get_task_template(task_id: str = "research") -> str:
    """获取调研/文档整理任务模板（大纲与建议输出路径）。"""
    data = _load()
    templates = data.get("templates", {})
    tid = (task_id or "research").strip()
    tpl = templates.get(tid) or templates.get("research")
    if not tpl:
        return "无可用模板。"
    outline = "\n".join(f"  {i+1}. {x}" for i, x in enumerate(tpl.get("outline", [])))
    return (
        f"模板：{tpl.get('title')}（id={tpl.get('id')}）\n"
        f"建议输出：{tpl.get('output_file')}\n"
        f"大纲：\n{outline}"
    )


if __name__ == "__main__":
    # stdio：日志必须打到 stderr，避免污染 MCP 协议通道
    mcp.run(transport="stdio")
