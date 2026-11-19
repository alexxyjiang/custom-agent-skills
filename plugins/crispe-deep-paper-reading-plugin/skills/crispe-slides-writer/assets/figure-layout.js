"use strict";
(() => {
  const modes = ["left", "right", "top", "bottom"];
  function measure(root, mode) {
    root.dataset.layout = mode;
    const image = root.querySelector("img");
    const zoom = root.querySelector(".zoom");
    const notes = root.querySelector(".figure-notes");
    image.style.width = "0px";
    image.style.height = "0px";
    const style = getComputedStyle(zoom);
    const width = Math.max(0, zoom.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight));
    const height = Math.max(0, zoom.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom));
    const scale = Math.min(width / image.naturalWidth, height / image.naturalHeight);
    const renderedWidth = image.naturalWidth * scale;
    const renderedHeight = image.naturalHeight * scale;
    image.style.width = `${Math.max(0, renderedWidth)}px`;
    image.style.height = `${Math.max(0, renderedHeight)}px`;
    const box = root.getBoundingClientRect();
    const tolerance = Math.max(0.5, box.width / root.offsetWidth * 2);
    const visible = [...root.querySelectorAll(".paper-figure,figcaption,.figure-notes,.card,.card h3,.card p")]
      .filter(e => getComputedStyle(e).display !== "none");
    let overflow = 0;
    if (mode !== "full" && root.dataset.hasNotes === "true") {
      const imageRegion = root.querySelector(".paper-figure").getBoundingClientRect();
      const noteRegion = notes.getBoundingClientRect();
      const horizontal = mode === "left" || mode === "right";
      const span = horizontal ? box.width : box.height;
      const shares = horizontal ? [imageRegion.width / span, noteRegion.width / span] : [imageRegion.height / span, noteRegion.height / span];
      root.dataset.regionShares = JSON.stringify(shares);
      if (shares.some(share => share < .30 - .002)) overflow += 100000;
    } else root.dataset.regionShares = "[1]";
    for (const element of visible) {
      const rect = element.getBoundingClientRect();
      overflow += Math.max(0, rect.bottom - box.bottom - tolerance) + Math.max(0, rect.right - box.right - tolerance)
        + Math.max(0, box.top - rect.top - tolerance) + Math.max(0, box.left - rect.left - tolerance);
      if (element.scrollHeight > element.clientHeight + 2) overflow += element.scrollHeight - element.clientHeight;
      if (element.scrollWidth > element.clientWidth + 2) overflow += element.scrollWidth - element.clientWidth;
    }
    // Painted text must fit its card, not merely the card's layout box.
    notes.querySelectorAll(".card p,.card h3").forEach(element => {
      const range = document.createRange(); range.selectNodeContents(element);
      const card = element.closest(".card").getBoundingClientRect();
      for (const rect of range.getClientRects()) overflow += Math.max(0, rect.bottom - card.bottom - tolerance) + Math.max(0, rect.right - card.right - tolerance);
    });
    return {mode, overflow, area:renderedWidth * renderedHeight, width:renderedWidth, height:renderedHeight};
  }
  function fit(root) {
    const image = root.querySelector("img");
    if (!image.complete || !image.naturalWidth || !root.clientHeight) return;
    const hasNotes = root.dataset.hasNotes === "true";
    const ratio = image.naturalWidth / image.naturalHeight;
    const count = root.querySelectorAll(".card").length;
    const chars = root.querySelector(".figure-notes").textContent.length;
    // Wide/short artwork uses horizontal notes; portrait artwork uses a side rail.
    const preferred = ratio >= 1.9 && chars < 700 ? ["top", "bottom", "left", "right"] : ["left", "right", "top", "bottom"];
    const requested = root.dataset.preference || "auto";
    const ordered = !hasNotes ? ["full"] : [requested, ...preferred].filter((mode, i, all) => modes.includes(mode) && all.indexOf(mode) === i);
    root.style.setProperty("--figure-note-count", Math.max(1, count));
    const candidates = ordered.map(mode => measure(root, mode));
    const fits = candidates.filter(c => c.overflow <= 2 && c.width >= 1 && c.height >= 1);
    let selected;
    if (requested !== "auto" && fits.some(c => c.mode === requested)) selected = fits.find(c => c.mode === requested);
    else if (fits.length) selected = fits.reduce((best, c) => c.area > best.area * 1.04 ? c : best);
    else selected = candidates.reduce((best, c) => c.overflow < best.overflow ? c : best);
    if (!selected) return;
    measure(root, selected.mode);
    root.dataset.layoutStatus = fits.length ? "fit" : "overflow";
    root.dataset.imageRatio = ratio.toFixed(3);
    root.dataset.noteCharacters = chars;
    root.dataset.layoutCandidates = JSON.stringify(candidates.map(c => ({mode:c.mode,overflow:Math.round(c.overflow),area:Math.round(c.area)})));
    root.setAttribute("aria-label", root.closest("section").getAttribute("aria-label"));
  }
  window.fitPaperFigures = (scope = document) => scope.querySelectorAll(".figure-layout").forEach(fit);
  document.querySelectorAll(".figure-layout img").forEach(image => image.addEventListener("load", () => fit(image.closest(".figure-layout"))));
  document.fonts.ready.then(() => requestAnimationFrame(() => window.fitPaperFigures()));
  addEventListener("resize", () => requestAnimationFrame(() => window.fitPaperFigures()));
})();
