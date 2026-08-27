const DEMO_PROMPTS = {
  research: `请完成一份竞品/技术调研简报（R&D 演示任务）。
主题：国内企业协作 / 知识效能工具中的 AI 助手能力趋势（聚焦飞书、钉钉、企业微信等公开信息）。
要求：
1) 先用 research_kb 查看 competitors 与 template；
2) web_search 检索，并对 1 条关键链接 fetch_url 精读；
3) 用中文写 5–8 条关键发现 + 简要对比表；
4) 写入 workspace/research_brief_collab_ai.md，文末列来源；
5) 不要询问人工；完成后 terminate。`,
  docs: `请完成一次「内部文档任务整理」泛化演示。
1) 可用 research_kb 的 template=docs 对齐结构；
2) 阅读 workspace/internal_memo_rd_tasks.txt；
3) 整理为待办清单，输出 workspace/task_digest_rd.md；
4) 不要询问人工；完成后 terminate。`,
};

async function fillDemoPrompt(promptId) {
  if (DEMO_PROMPTS[promptId]) {
    document.getElementById("messageInput").value = DEMO_PROMPTS[promptId];
    document.getElementById("messageInput").focus();
    return;
  }
  try {
    const res = await fetch("/api/demo-tasks");
    const data = await res.json();
    const hit = (data.tasks || []).find((t) => t.id === promptId);
    if (hit) {
      document.getElementById("messageInput").value = hit.prompt;
      document.getElementById("messageInput").focus();
    }
  } catch (e) {
    console.error(e);
  }
}

window.fillDemoPrompt = fillDemoPrompt;

async function refreshModelStatus() {
  const el = document.getElementById("modelStatus");
  if (!el) return;
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    if (data.ok) {
      el.textContent = `${data.provider} · ${data.model}`;
      el.classList.add("is-ok");
      el.classList.remove("is-bad");
    } else {
      el.textContent = data.message || "未连接模型";
      el.classList.add("is-bad");
      el.classList.remove("is-ok");
    }
  } catch (e) {
    el.textContent = "服务未就绪";
    el.classList.add("is-bad");
    el.classList.remove("is-ok");
  }
}

async function refreshCapabilities() {
  const list = document.getElementById("capabilityList");
  if (!list) return;
  try {
    const res = await fetch("/api/capabilities");
    const data = await res.json();
    const features = data.features || [];
    if (!features.length) {
      list.innerHTML = '<li class="is-muted">暂无能力信息</li>';
      return;
    }
    list.innerHTML = features
      .map((f) => {
        const cls = f.on ? "is-on" : "is-off";
        const mark = f.on ? "" : "（未启用）";
        return `<li class="${cls}">${f.label}${mark}</li>`;
      })
      .join("");
  } catch (e) {
    list.innerHTML = '<li class="is-muted">能力状态加载失败</li>';
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-prompt-id]").forEach((el) => {
    el.addEventListener("click", () => {
      fillDemoPrompt(el.getAttribute("data-prompt-id"));
    });
  });
  refreshModelStatus();
  refreshCapabilities();
});
