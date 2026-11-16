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
