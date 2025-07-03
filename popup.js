document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("checkBtn").addEventListener("click", async () => {
    const input = document.getElementById("urlInput").value.trim();
    const resultElement = document.getElementById("result");

    if (!input) {
      resultElement.textContent = "❌ 请输入内容！";
      return;
    }

    resultElement.textContent = "识别中，请稍候...";

    const prompt = `请判断以下内容中是否包含一个官方网站的链接或描述，并说明该链接是否是某个知名公司的主站或子站。如果不是，请指出是否有钓鱼或广告风险。\n\n内容：${input}`;

    try {
      const response = await fetch("http://localhost:5005/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
      });

      const text = await response.text();
      let reply = text;

      try {
        const json = JSON.parse(text);
        reply = json.error || json.choices?.[0]?.message?.content || "无响应内容";
      } catch (e) {
        reply = text;
      }

      resultElement.textContent = reply;
    } catch (err) {
      console.error("❌ 请求失败：", err);
      resultElement.textContent = "识别失败，请检查网络或后端状态";
    }
  });
});