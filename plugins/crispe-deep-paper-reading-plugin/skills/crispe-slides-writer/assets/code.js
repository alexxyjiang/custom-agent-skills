"use strict";
(() => {
  const zh = document.documentElement.lang === "zh-CN";
  document.querySelectorAll(".copy-code").forEach(button => {
    button.addEventListener("click", async () => {
      const panel = button.closest(".code-panel");
      const source = [...panel.querySelectorAll("code > .code-line")].map(line => line.textContent).join("\n");
      const status = panel.querySelector(".copy-status");
      try {
        if (navigator.clipboard?.writeText) {
          try { await navigator.clipboard.writeText(source); }
          catch (_) { fallback(source); }
        } else fallback(source);
        status.textContent = zh ? "已复制" : "Copied";
      } catch (_) { status.textContent = zh ? "请选中代码复制" : "Select code to copy"; }
    });
  });
  function fallback(source) {
    const area = document.createElement("textarea");
    area.value = source; area.style.cssText = "position:fixed;left:-10000px;top:0";
    document.body.append(area);
    const focus = document.activeElement;
    try { area.select(); if (!document.execCommand("copy")) throw new Error("Copy unavailable"); }
    finally { area.remove(); focus?.focus({preventScroll:true}); }
  }
})();
