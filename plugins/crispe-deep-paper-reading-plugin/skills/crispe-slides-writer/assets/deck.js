"use strict";
const slides = [...document.querySelectorAll("section.slide")];
const stage = document.querySelector("#deck-stage");
const printMode = new URLSearchParams(location.search).has("print-pdf");
let revealReady = false;
function initialIndex() { const id = location.hash.replace(/^#\/?/, ""); const index = slides.findIndex(s=>s.id===id); return index<0?0:index; }
const startupIndex = initialIndex();
const toc = document.querySelector("#toc");
const viewer = document.querySelector("#image-view");
const prev = document.querySelector("#prev"), next = document.querySelector("#next");
let current = 0;
const autoplay = document.querySelector("#autoplay");
const speed = document.querySelector("#playback-speed");
const zh = document.documentElement.lang === "zh-CN";
let playing = false, timer = null, deadline = 0;
const playbackStatus = document.createElement("span");
playbackStatus.id = "playback-status";
playbackStatus.setAttribute("role", "status");
playbackStatus.setAttribute("aria-live", "off");
autoplay.insertAdjacentElement("afterend", playbackStatus);
function duration() {
  const value = Number(speed.value);
  return [5000, 15000, 30000, 60000].includes(value) ? value : 15000;
}
function holdReason() {
  if (document.hidden) return zh ? "等待返回页面" : "Waiting for visible tab";
  if (toc.open || viewer.open) return zh ? "等待关闭弹窗" : "Waiting for dialog";
  if (slides[current]?.querySelector("details[open]")) return zh ? "等待收起详情" : "Waiting for details";
  return "";
}
function updatePlaybackStatus(reason = holdReason()) {
  autoplay.setAttribute("aria-pressed", String(playing));
  autoplay.textContent = playing ? (zh ? "暂停播放" : "Pause") : (zh ? "自动播放" : "Autoplay");
  if (!playing) {
    playbackStatus.textContent = "";
    autoplay.dataset.state = "paused";
  } else if (reason) {
    playbackStatus.textContent = reason;
    autoplay.dataset.state = "waiting";
  } else {
    const seconds = Math.max(0, Math.ceil((deadline - performance.now()) / 1000));
    playbackStatus.textContent = zh ? `${seconds}s 后翻页` : `Next in ${seconds}s`;
    autoplay.dataset.state = "playing";
  }
}
function clearPlaybackTimer() { clearTimeout(timer); timer = null; }
function pause() {
  playing = false; clearPlaybackTimer(); deadline = 0;
  updatePlaybackStatus("");
}
function tickPlayback() {
  timer = null;
  if (!playing) return;
  if (current === slides.length - 1) { pause(); return; }
  const reason = holdReason();
  if (reason) {
    // Poll as a fallback: dynamically added details/dialogs cannot strand playback.
    deadline = 0; updatePlaybackStatus(reason);
    timer = setTimeout(tickPlayback, 250);
    return;
  }
  if (!deadline) deadline = performance.now() + duration();
  const remaining = deadline - performance.now();
  if (remaining <= 0) { show(current + 1); return; }
  updatePlaybackStatus("");
  timer = setTimeout(tickPlayback, Math.min(250, remaining));
}
function schedule() {
  clearPlaybackTimer(); deadline = 0;
  if (!playing) { updatePlaybackStatus(""); return; }
  if (!holdReason()) deadline = performance.now() + duration();
  tickPlayback();
}
autoplay.addEventListener("click", () => {
  if (playing) { pause(); return; }
  if (current === slides.length - 1) show(0);
  playing = true;
  schedule();
});
function reconcilePlayback() {
  // Duplicate/late close events must not keep restarting a live countdown.
  clearPlaybackTimer();
  tickPlayback();
}
speed.addEventListener("change", schedule);
document.addEventListener("visibilitychange", reconcilePlayback);
addEventListener("pagehide", clearPlaybackTimer);
addEventListener("pageshow", schedule);
document.querySelectorAll("dialog").forEach(dialog => {
  dialog.addEventListener("close", reconcilePlayback);
  dialog.addEventListener("cancel", () => queueMicrotask(() => { if (dialog.open) dialog.close(); reconcilePlayback(); }));
});
// toggle does not bubble; capture covers every current/future details element.
document.addEventListener("toggle", event => {
  if (event.target.matches?.("details") && slides[current]?.contains(event.target)) reconcilePlayback();
}, true);
function hashIndex() { return initialIndex(); }
function updateReadingUI(index, updateHash = true) {
  const oldFocus = document.activeElement?.closest(".slide");
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((s, i) => { const active = i === current; s.classList.toggle("active", active); s.inert = !active; s.setAttribute("aria-hidden", String(!active)); });
  document.title = slides[current].dataset.slideHeading || slides[current].getAttribute("aria-label");
  prev.disabled = current === 0; next.disabled = current === slides.length - 1;
  const digits=String(slides.length).length;
  const pageNumber=String(current+1).padStart(digits,"0"), total=String(slides.length);
  document.querySelector("#page").textContent = `${pageNumber} / ${total}`;
  slides[current].querySelector("header > span:last-child").textContent = `${pageNumber} / ${total}`;
  const progress = document.querySelector("#progress"); progress.max = slides.length; progress.value = current + 1;
  if (updateHash) { try { history.replaceState(null, "", "#" + slides[current].id); } catch (_) {} }
  if (oldFocus && oldFocus !== slides[current]) document.querySelector("#contents").focus();
  window.fitPaperMath?.(slides[current]);
  window.fitPaperFigures?.(slides[current]);
  schedule();
}
function show(index, updateHash = true) {
  const target = Math.max(0, Math.min(slides.length - 1, index));
  if (!revealReady) { updateReadingUI(target, updateHash); return; }
  if(target!==current)prettyPlayers.filter(p=>p.root.closest("section")===slides[target]).forEach(p=>p.activate(0));
  Reveal.slide(target);
  // Re-selecting a page (or a legacy hash) still refreshes focus/status.
  updateReadingUI(target, updateHash);
}
prev.addEventListener("click", () => show(current - 1));
next.addEventListener("click", () => show(current + 1));
document.querySelector("#contents").addEventListener("click", () => { toc.showModal(); schedule(); });
document.querySelectorAll("dialog .close").forEach(b => b.addEventListener("click", () => b.closest("dialog").close()));
toc.addEventListener("click", e => { const a = e.target.closest("a"); if (!a) return; e.preventDefault(); const target = slides.findIndex(s => "#" + s.id === a.hash); if (target >= 0) show(target); toc.close(); });
document.querySelectorAll(".slide a[href]").forEach(a => a.addEventListener("click", e => {
  const target = new URL(a.href, location.href);
  if (target.origin !== location.origin || target.pathname !== location.pathname || !target.hash.startsWith("#slide-")) return;
  const index = slides.findIndex(s => "#" + s.id === target.hash);
  if (index >= 0) { e.preventDefault(); show(index); }
}));
const prettyPlayers = [];
function activatePrettyFragment(fragment) {
  if (!fragment?.matches?.(".pretty-fragment")) return;
  const player = prettyPlayers.find(p=>p.root===fragment.closest(".example"));
  if (player) player.activate(Number(fragment.dataset.step));
}
document.querySelectorAll(".example").forEach(root => {
  const buttons = [...root.querySelectorAll(".step")];
  const code = root.querySelector(":scope > .code-panel");
  let step = 0;
  const state = document.createElement("span");state.className="pretty-status";state.setAttribute("role","status");
  function activate(index) {
    step = Math.max(0,Math.min(buttons.length-1,index));
    const numbers = JSON.parse(buttons[step].dataset.lines);
    buttons.forEach((b,i)=>b.setAttribute("aria-pressed",String(i===step)));
    root.querySelectorAll(":scope > .code-panel .code-line").forEach(line=>line.classList.toggle("highlight",numbers.includes(Number(line.dataset.line))));
    const pre = code.querySelector("pre"), line = code.querySelector(`.code-line[data-line="${numbers[0]}"]`);
    if (line) pre.scrollTop = Math.max(0,line.offsetTop - pre.offsetTop - pre.clientHeight/3);
    state.textContent = zh ? `第 ${step+1}/${buttons.length} 步` : `Step ${step+1}/${buttons.length}`;
  }
  function seek(index) {
    const target=Math.max(0,Math.min(buttons.length-1,index));
    const first=root.querySelector(".pretty-fragment");
    if(revealReady && first)Reveal.navigateFragment(Number(first.dataset.fragmentIndex)+target-1);
    activate(target);
  }
  buttons.forEach((b,i)=>b.addEventListener("click",()=>seek(i)));
  const controls=document.createElement("div");controls.className="pretty-controls";
  for(const [delta,label] of [[-1,zh?"上一步":"Previous step"],[1,zh?"下一步":"Next step"]]) {
    const b=document.createElement("button");b.type="button";b.textContent=label;b.addEventListener("click",()=>seek(step+delta));controls.append(b);
  }
  controls.append(state);root.querySelector(".steps").append(controls);
  const fragments=document.createElement("span");fragments.className="pretty-fragments";fragments.setAttribute("aria-hidden","true");
  buttons.slice(1).forEach((_,i)=>{const fragment=document.createElement("span");fragment.className="fragment pretty-fragment";fragment.dataset.step=i+1;fragments.append(fragment);});root.append(fragments);
  prettyPlayers.push({root,activate});if(buttons.length)activate(0);
});
// Page timing stays page-based; fragments never add hidden extra autoplay delays.
window.paperSlidesPreparePrint = () => {
  pause();
  document.querySelectorAll(".fragment").forEach(fragment=>fragment.classList.add("visible"));
  window.fitPaperMath?.();window.fitPaperFigures?.();
  window.paperSlidesPrintReady=true;
};
document.querySelectorAll(".zoom").forEach(button => button.addEventListener("click", () => { const source = button.querySelector("img"), target = viewer.querySelector("img"); target.src = source.src; target.alt = source.alt; viewer.showModal(); schedule(); }));
addEventListener("keydown", e => {
  if (toc.open || viewer.open || e.altKey || e.ctrlKey || e.metaKey || /INPUT|TEXTAREA|SELECT|PRE|CODE/.test(e.target.tagName) || e.target.isContentEditable) return;
  if (e.key === "Home" || e.key === "End") { e.preventDefault(); show(e.key === "Home" ? 0 : slides.length - 1); }
});
addEventListener("hashchange", () => show(hashIndex(), false));
Reveal.initialize({
  width:1600,height:900,margin:0.014,minScale:0.05,maxScale:8,
  controls:false,progress:false,slideNumber:false,center:false,hash:false,history:false,respondToHashChanges:false,
  transition:"none",backgroundTransition:"none",navigationMode:"linear",touch:true,scrollActivationWidth:0,
  autoSlide:0,loop:false,overview:false,help:false,pause:false,
  pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,pdfPageHeightOffset:0,
  keyboardCondition: event => !toc.open && !viewer.open && !/INPUT|TEXTAREA|SELECT|PRE|CODE/.test(event.target.tagName),
  plugins:[] // Prism and KaTeX are deliberately independent of RevealHighlight.
}).then(async () => {
  revealReady = true;
  Reveal.on("slidechanged", event => {
    Reveal.navigateFragment(-1);
    prettyPlayers.filter(p=>p.root.closest("section")===slides[event.indexh]).forEach(p=>p.activate(0));
    updateReadingUI(event.indexh);
  });
  Reveal.on("fragmentshown", event => activatePrettyFragment(event.fragment));
  Reveal.on("fragmenthidden", event => {
    const root=event.fragment.closest(".example");const player=prettyPlayers.find(p=>p.root===root);
    if(player)player.activate(Math.max(0,Number(event.fragment.dataset.step)-1));
  });
  show(startupIndex);
  await document.fonts.ready;
  await Promise.all([...document.images].map(image => image.complete ? Promise.resolve() : new Promise(resolve => {image.addEventListener("load",resolve,{once:true});image.addEventListener("error",resolve,{once:true});})));
  window.fitPaperMath?.();window.fitPaperFigures?.();
  window.paperSlidesReady = true;
  if (printMode) { pause(); window.paperSlidesPreparePrint?.(); }
});

// Keep the corresponding translated slide when changing locale.
document.querySelectorAll(".language-switch").forEach(link => link.addEventListener("click", () => { link.hash = slides[current].id; }));
