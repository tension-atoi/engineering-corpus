/* Docs adapter for the ratified GNU6 cross-domain geometric handoff.
 * The transport, timing, fragment and colour remain owned by g6-motion.js. */
(() => {
  "use strict";
  function reveal() {
    const root = document.documentElement;
    const motion = window.G6Motion;
    if (root.dataset.g6Domain !== "docs" || !motion?.bridge?.arriving) return;
    const anchor = document.querySelector(".g6-brand");
    const r = anchor?.getBoundingClientRect();
    const point = r
      ? { x: r.left + r.width / 2, y: r.top + r.height / 2 }
      : { x: 22, y: 22 };
    void motion.bridge.reveal(point).catch(() => {
      // Never leave the content under an opaque overlay on an aborted reveal.
      root.removeAttribute("data-g6-bridge");
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", reveal, { once: true });
  } else {
    reveal();
  }
})();
