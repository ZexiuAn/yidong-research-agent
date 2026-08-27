# 易动调研助手 · 产品说明

## 业务背景（包装口径）

| 项 | 内容 |
|----|------|
| 实习公司 | **北京易动纷享科技有限责任公司** |
| 落地部门 | **研发中心（R&D）** |
| 产品定位 | **易动调研助手**：竞品 / 技术调研简报 Agent 原型 |
| 起点叙事 | 先服务「调研简报」小目标，验证工具闭环后抽象为可泛化效能基座 |
| 泛化验证 | 「内部文档任务整理」第二条演示任务 |
| 项目性质 | **实习作品 / 课程综合实训原型**（非对外商用交付） |

## 简历可写（一句话）

> 在北京易动纷享科技有限责任公司 R&D 场景下，完成调研简报 Agent 原型：多步工具编排（检索→归纳→落盘），步骤可观测；并验证可泛化到文档整理任务。

## 功能亮点

1. **多步 Tool Calling**：规划 → web_search / fetch_url / 文件读写 / python → terminate  
2. **MCP 业务工具**：自研 `yidong_research`（竞品 / 术语 / 模板）标准热插拔  
3. **步骤可观测**：Web UI 展开思考与工具轨迹（SSE）  
4. **任务结束再总结**：额外 LLM 调用生成面向用户的调研结论  
5. **国产模型**：DashScope `qwen-plus` OpenAI 兼容接口  

## 技术栈

- Agent：OpenManus（ToolCallAgent）  
- LLM：通义千问（DashScope）  
- 工具：WebSearch、FetchURL、ResearchKB、StrReplaceEditor、PythonExecute、MCP  
- UI：FastAPI + Jinja2 + SSE + 前端轨迹可视化  

## 诚实边界

- 默认关闭浏览器自动化（`ENABLE_BROWSER=1` 可开）  
- 公开网页检索需人工复核；本地知识库为演示 mock 数据  
- 百度等搜索结果噪声较大，演示以「链路可跑通 + 结构完整」为主  

## 快速启动

```bash
cd OpenManus-cy
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-demo.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
cp .env.example .env   # 填入 DASHSCOPE_API_KEY
python app.py          # http://127.0.0.1:5172
pytest tests/ -q
```
