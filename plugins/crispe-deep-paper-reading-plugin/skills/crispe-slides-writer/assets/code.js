"use strict";
(() => {
  const zh = document.documentElement.lang === "zh-CN";
  // Tokenize complete blocks first: multiline Python strings/comments remain intact.
  document.querySelectorAll(".code-panel code").forEach(code => {
    const source = [...code.querySelectorAll(":scope > .code-line")].map(line => line.textContent).join("\n");
    const language = Prism.util.getLanguage(code);
    const grammar = Prism.languages[language];
    const rows = [document.createElement("span")];
    const row = () => rows[rows.length - 1];
    function append(value, classes = []) {
      if (typeof value === "string") {
        value.split("\n").forEach((part, i) => {
          if (i) rows.push(document.createElement("span"));
          let target = row();
          classes.forEach(names => { const span = document.createElement("span"); span.className = names; target.append(span); target = span; });
          target.append(document.createTextNode(part));
        });
      } else if (Array.isArray(value)) value.forEach(token => append(token, classes));
      else append(value.content, [...classes, ["token", value.type, ...(Array.isArray(value.alias) ? value.alias : value.alias ? [value.alias] : [])].join(" ")]);
    }
    append(grammar ? Prism.tokenize(source, grammar) : source);
    rows.forEach((line, i) => { line.className = "code-line"; line.dataset.line = i + 1; });
    code.replaceChildren(...rows);
    code.dataset.highlighter = grammar ? "prismjs" : "plain";
  });
  // Normalize paired single-dollar math without treating prices as delimiters.
  function normalizeInlineDollars(element) {
    const walker=document.createTreeWalker(element,NodeFilter.SHOW_TEXT);
    const nodes=[];
    while(walker.nextNode())if(!walker.currentNode.parentElement.closest("pre,code,script,style,.katex"))nodes.push(walker.currentNode);
    nodes.forEach(node=>{
      node.textContent=node.textContent.replace(/(?<![\\$])\$(?![$\d])([^$\n]+?)(?<!\\)\$(?![$\d])/g,(whole,tex)=>{
        if(tex!==tex.trim() || /^\d[\d,.]*(?:\s*(?:USD|EUR|CNY))?$/i.test(tex))return whole;
        return "\\("+tex+"\\)";
      });
    });
  }
  // Render only authored prose, never source code, JSON, controls or raw records.
  document.querySelectorAll(".slide h1,.slide .lead,.card p,.takeaway,.steps .step strong,.steps .step span,.paper-card p,.collection .intro").forEach(element => {
    normalizeInlineDollars(element);
    renderMathInElement(element, {
      delimiters: [{left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}],
      throwOnError:false, trust:false, strict:"ignore",
      ignoredTags:["script","noscript","style","textarea","pre","code","option"],
      errorCallback:() => { element.dataset.mathError = "true"; }
    });
  });
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
