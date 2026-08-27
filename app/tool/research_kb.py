from __future__ import annotations

import json
from pathlib import Path

from app.tool.base import BaseTool

ASSETS = Path(__file__).resolve().parents[2] / "data" / "research_assets.json"


class ResearchKB(BaseTool):
    """本地调研知识库（术语 / 竞品清单 / 任务模板）。也可经 MCP 同名能力访问。"""

    name: str = "research_kb"
    description: str = (
        "查询易动调研本地知识：competitors（竞品清单）、glossary（术语）、"
        "template（任务模板）。在联网搜索前可先用它对齐范围与输出结构。"
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["competitors", "glossary", "template"],
                "description": "要执行的查询类型。",
            },
            "query": {
                "type": "string",
                "description": "glossary 时为术语；template 时为 research/docs。",
            },
        },
        "required": ["action"],
    }

    async def execute(self, action: str, query: str = "") -> str:
        data = json.loads(ASSETS.read_text(encoding="utf-8"))
        action = (action or "").strip().lower()
        query = (query or "").strip()

        if action == "competitors":
            lines = ["易动纷享常见对标竞品（本地知识库）："]
            for item in data.get("competitors", []):
                lines.append(
                    f"- {item['name']}｜重点：{item['focus']}｜备注：{item.get('notes', '')}"
                )
            return "\n".join(lines)

        if action == "glossary":
            glossary = data.get("glossary", {})
            if not query:
                return "请提供 query 术语。已知：" + "、".join(glossary.keys())
            if query in glossary:
                return f"{query}：{glossary[query]}"
            for k, v in glossary.items():
                if query.lower() in k.lower() or k.lower() in query.lower():
                    return f"{k}：{v}"
            return f"未找到「{query}」。已知：" + "、".join(glossary.keys())

        if action == "template":
            templates = data.get("templates", {})
            tid = query or "research"
            tpl = templates.get(tid) or templates.get("research")
            outline = "\n".join(
                f"  {i+1}. {x}" for i, x in enumerate(tpl.get("outline", []))
            )
            return (
                f"模板：{tpl.get('title')}（id={tpl.get('id')}）\n"
                f"建议输出：{tpl.get('output_file')}\n"
                f"大纲：\n{outline}"
            )

        return "action 仅支持 competitors / glossary / template"
