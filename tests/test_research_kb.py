"""research_kb 与 MCP 工具数据一致性测试。"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "data" / "research_assets.json"


def test_research_assets_shape():
    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    assert "glossary" in data and "competitors" in data and "templates" in data
    assert len(data["competitors"]) >= 3
    assert "research" in data["templates"]
    # 品牌口径：不应再出现用友包装残留
    blob = ASSETS.read_text(encoding="utf-8")
    assert "用友" not in blob
    assert "YonBIP" not in blob


@pytest.mark.asyncio
async def test_research_kb_competitors_and_glossary():
    from app.tool.research_kb import ResearchKB

    tool = ResearchKB()
    comps = await tool.execute(action="competitors")
    assert "飞书" in comps
    assert "易动纷享" in comps

    term = await tool.execute(action="glossary", query="MCP")
    assert "Model Context Protocol" in term or "MCP" in term

    tpl = await tool.execute(action="template", query="research")
    assert "调研" in tpl


def test_mcp_tools_match_assets():
    """直接调用 MCP 模块内函数（不走 stdio），保证与 JSON 一致。"""
    import importlib.util

    path = ROOT / "mcp_servers" / "yidong_research_mcp.py"
    spec = importlib.util.spec_from_file_location("yidong_research_mcp", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)

    text = mod.list_competitors()
    assert "钉钉" in text
    assert "易动纷享" in text
    assert "MCP" in mod.lookup_glossary("MCP")
    assert "大纲" in mod.get_task_template("docs")
