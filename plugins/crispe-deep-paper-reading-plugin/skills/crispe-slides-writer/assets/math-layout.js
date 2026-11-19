"use strict";
(() => {
  function overflowExpressions(slide) {
    return [...slide.querySelectorAll(".katex")].filter(math => {
      const container = math.closest(".katex-display") || math.closest("p,.lead,.takeaway,h1") || math.parentElement;
      return container.scrollWidth > container.clientWidth + 2
        || math.scrollWidth > math.clientWidth + 2
        || math.getBoundingClientRect().width > container.getBoundingClientRect().width + 1
        || [...math.querySelectorAll(".katex-html > .base,.katex-html > .tag")].some(base => {
          const box = base.getBoundingClientRect(), outer = container.getBoundingClientRect();
          return box.right > outer.right + 1 || box.left < outer.left - 1;
        });
    });
  }
  function hasVerticalOverflow(slide) {
    const body = slide.querySelector(".slide-body");
    if (!body) return false;
    const bottom = body.getBoundingClientRect().bottom;
    return [...body.querySelectorAll(".card,.card p,.katex-display")].some(element => element.getBoundingClientRect().bottom > bottom + 1);
  }
  function fit(slide) {
    if (!slide.querySelector(".katex")) return;
    slide.querySelectorAll(".math-wrap").forEach(element => element.classList.remove("math-wrap"));
    slide.querySelectorAll(".math-stacked").forEach(element => element.classList.remove("math-stacked"));
    const formulas = [...slide.querySelectorAll(".katex-display")];
    // KaTeX base spans are complete semantic units with supported breakpoints;
    // do not split TeX strings, fractions, roots or alignment internals.
    formulas.forEach(display => {
      if (display.scrollWidth > display.clientWidth + 2) display.classList.add("math-wrap");
    });
    let bad = overflowExpressions(slide);
    if (bad.length) {
      const groups = new Set(bad.map(math => math.closest(".cards")).filter(group => group && !group.closest(".figure-layout")));
      groups.forEach(group => group.classList.add("math-stacked"));
      // A wider card may no longer require wrapping.
      formulas.forEach(display => {
        display.classList.remove("math-wrap");
        if (display.scrollWidth > display.clientWidth + 2) display.classList.add("math-wrap");
      });
      bad = overflowExpressions(slide);
    }
    slide.dataset.mathLayoutStatus = bad.length || hasVerticalOverflow(slide) ? "overflow" : "fit";
    slide.dataset.mathOverflowCount = bad.length;
    slide.dataset.mathWrappedCount = slide.querySelectorAll(".math-wrap").length;
    slide.dataset.mathStackedCount = slide.querySelectorAll(".math-stacked").length;
  }
  window.fitPaperMath = (scope = document) => {
    if (scope.matches?.(".slide")) fit(scope);
    else scope.querySelectorAll(".slide").forEach(fit);
  };
  document.fonts.ready.then(() => requestAnimationFrame(() => {
    window.fitPaperMath();
    window.fitPaperFigures?.();
  }));
  addEventListener("resize", () => requestAnimationFrame(() => {
    window.fitPaperMath();
    window.fitPaperFigures?.();
  }));
})();
