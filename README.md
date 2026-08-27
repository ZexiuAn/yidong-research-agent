# 易动调研助手

> 北京易动纷享科技有限责任公司 · R&D 场景下的竞品/技术调研 Agent 原型  
> 基于 [OpenManus](https://github.com/FoundationAgents/OpenManus) 二次开发与产品化封装

## 能做什么

- 多步 Tool Calling：搜索 → 网页精读 → 本地知识库/MCP → Markdown 落盘
- 任务结束后二次 LLM 调用，生成**面向用户的调研结论**
- Web UI（SSE）可观测思考与工具轨迹
- 两条演示任务：调研简报 / 内部文档整理

## 快速开始

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-demo.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pytest pytest-asyncio httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
cp .env.example .env   # 填写 DASHSCOPE_API_KEY
python app.py          # http://127.0.0.1:5172
bash scripts/smoke.sh  # 单元测试冒烟
```

## 文档

- [产品说明](docs/PRODUCT_BRIEF.md)
- [演示话术](docs/PRESENT_SCRIPT.md)
- [简历要点](docs/RESUME_BULLETS.md)

## 说明

本地 `data/research_assets.json` 为演示用 mock 知识，非真实内部数据。公开网页结论需人工复核。
