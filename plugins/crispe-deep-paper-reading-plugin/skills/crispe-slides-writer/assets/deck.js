"use strict";
const slides = [...document.querySelectorAll(".slide")];
const stage = document.querySelector("#deck-stage");
const toc = document.querySelector("#toc");
const viewer = document.querySelector("#image-view");
const prev = document.querySelector("#prev"), next = document.querySelector("#next");
let current = 0;
const autoplay = document.querySelector("#autoplay");
const speed = document.querySelector("#playback-speed");
const zh = document.documentElement.lang === "zh-CN";
let playing = false, timer = null;
function pause() {
  playing = false; clearTimeout(timer); timer = null;
  autoplay.setAttribute("aria-pressed", "false");
  autoplay.textContent = zh ? "自动播放" : "Autoplay";
}
function schedule() {
  clearTimeout(timer); timer = null;
  if (!playing) return;
  if (current === slides.length - 1) { pause(); return; }
  if (document.hidden || toc.open || viewer.open || slides[current].querySelector("details[open]")) return;
  timer = setTimeout(() => { if (!document.hidden && !toc.open && !viewer.open) show(current + 1); else schedule(); }, Number(speed.value));
}
autoplay.addEventListener("click", () => {
  if (playing) { pause(); return; }
  if (current === slides.length - 1) show(0);
  playing = true;
  autoplay.setAttribute("aria-pressed", "true");
  autoplay.textContent = zh ? "暂停播放" : "Pause";
  schedule();
});
speed.addEventListener("change", schedule);
document.addEventListener("visibilitychange", schedule);
document.querySelectorAll("dialog").forEach(dialog => {
  dialog.addEventListener("close", schedule);
  dialog.addEventListener("cancel", () => queueMicrotask(() => { if (dialog.open) dialog.close(); schedule(); }));
});
document.querySelectorAll(".steps details").forEach(details => details.addEventListener("toggle", schedule));
function fit() { stage.style.transform = `scale(${Math.max(.05, Math.min((innerWidth - 24) / 1600, (innerHeight - 24) / 900))})`; }
function hashIndex() { const n = slides.findIndex(s => "#" + s.id === location.hash); return n < 0 ? 0 : n; }
function show(index, updateHash = true) {
  const oldFocus = document.activeElement?.closest(".slide");
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((s, i) => { const active = i === current; s.classList.toggle("active", active); s.inert = !active; s.setAttribute("aria-hidden", String(!active)); });
  prev.disabled = current === 0; next.disabled = current === slides.length - 1;
  document.querySelector("#page").textContent = `${current + 1} / ${slides.length}`;
  const progress = document.querySelector("#progress"); progress.max = slides.length; progress.value = current + 1;
  if (updateHash) { try { history.replaceState(null, "", "#" + slides[current].id); } catch (_) {} }
  if (oldFocus && oldFocus !== slides[current]) document.querySelector("#contents").focus();
  schedule();
}
prev.addEventListener("click", () => show(current - 1));
next.addEventListener("click", () => show(current + 1));
document.querySelector("#contents").addEventListener("click", () => { toc.showModal(); schedule(); });
document.querySelectorAll("dialog .close").forEach(b => b.addEventListener("click", () => b.closest("dialog").close()));
toc.addEventListener("click", e => { const a = e.target.closest("a"); if (!a) return; e.preventDefault(); const target = slides.findIndex(s => "#" + s.id === a.hash); if (target >= 0) show(target); toc.close(); });
document.querySelectorAll(".slide a[href^='#slide-']").forEach(a => a.addEventListener("click", e => { const index = slides.findIndex(s => "#" + s.id === a.hash); if(index >= 0) {e.preventDefault(); show(index);} }));
document.querySelectorAll(".example").forEach(example => { const buttons = [...example.querySelectorAll(".step")]; function activate(button) { const numbers = JSON.parse(button.dataset.lines); buttons.forEach(b => b.setAttribute("aria-pressed", String(b === button))); example.querySelectorAll(":scope > .code-panel .code-line").forEach(line => line.classList.toggle("highlight", numbers.includes(Number(line.dataset.line)))); } buttons.forEach(b => b.addEventListener("click", () => activate(b))); if(buttons.length) activate(buttons[0]); });
document.querySelectorAll(".zoom").forEach(button => button.addEventListener("click", () => { const source = button.querySelector("img"), target = viewer.querySelector("img"); target.src = source.src; target.alt = source.alt; viewer.showModal(); schedule(); }));
addEventListener("keydown", e => { if (toc.open || viewer.open || e.altKey || e.ctrlKey || e.metaKey || /INPUT|TEXTAREA|SELECT|PRE|CODE/.test(e.target.tagName) || e.target.isContentEditable) return; const map = {ArrowRight:current+1,ArrowDown:current+1,ArrowLeft:current-1,ArrowUp:current-1,Home:0,End:slides.length-1}; if(e.key in map) {e.preventDefault(); show(map[e.key]);} });
addEventListener("hashchange", () => show(hashIndex(), false));
addEventListener("resize", fit); fit(); show(hashIndex());

// Keep the corresponding translated slide when changing locale.
document.querySelectorAll(".language-switch").forEach(link => link.addEventListener("click", () => { link.hash = slides[current].id; }));
