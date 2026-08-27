"""FastAPI 健康检查与演示接口测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.branding import COMPANY_FULL, PRODUCT_NAME

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_webapp():
    """根目录 app.py 与包名 app/ 冲突，按文件路径加载。"""
    path = ROOT / "app.py"
    spec = importlib.util.spec_from_file_location("yidong_webapp", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


webapp = _load_webapp()
client = TestClient(webapp.app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert "ok" in data
    assert "message" in data


def test_demo_tasks_branding():
    res = client.get("/api/demo-tasks")
    assert res.status_code == 200
    data = res.json()
    assert data["product"] == PRODUCT_NAME
    assert COMPANY_FULL in data["org"]
    assert "用友" not in data["org"]
    ids = {t["id"] for t in data["tasks"]}
    assert {"research", "docs"} <= ids


def test_capabilities_endpoint():
    res = client.get("/api/capabilities")
    assert res.status_code == 200
    data = res.json()
    assert "features" in data
    assert "tools" in data


def test_index_html_branding():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text
    assert PRODUCT_NAME in html
    assert COMPANY_FULL in html
    assert "用友" not in html
    assert "友企" not in html
