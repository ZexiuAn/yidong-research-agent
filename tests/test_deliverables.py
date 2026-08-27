"""交付物抽取与品牌常量测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from app.branding import COMPANY_FULL, PRODUCT_NAME

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_webapp():
    path = ROOT / "app.py"
    spec = importlib.util.spec_from_file_location("yidong_webapp_deliverables", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_branding_company():
    assert COMPANY_FULL == "北京易动纷享科技有限责任公司"
    assert PRODUCT_NAME == "易动调研助手"
    assert "用友" not in COMPANY_FULL


def test_collect_deliverable_snippets(tmp_path, monkeypatch):
    webapp = _load_webapp()
    ws = tmp_path / "workspace"
    ws.mkdir()
    brief = ws / "research_brief_demo.md"
    brief.write_text(
        "# demo\n\n## 关键发现\n- 飞书偏协作 AI\n- 钉钉偏组织协同\n",
        encoding="utf-8",
    )
    (tmp_path / "app.py").write_text("# stub\n", encoding="utf-8")
    monkeypatch.setattr(webapp, "__file__", str(tmp_path / "app.py"))

    text, rels = webapp._collect_deliverable_snippets(
        "saved workspace/research_brief_demo.md"
    )
    assert any("research_brief_demo.md" in r for r in rels)
    assert "关键发现" in text or "飞书" in text
