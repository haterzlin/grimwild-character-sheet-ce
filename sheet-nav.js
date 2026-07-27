document.addEventListener("keydown", (event) => {
  if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.target instanceof Element && event.target.closest("input, textarea, select, [contenteditable='true']")) return;

  const rel = event.key === "ArrowLeft" ? "prev" : event.key === "ArrowRight" ? "next" : "";
  if (!rel) return;

  const link = document.querySelector('.sheet-nav-link[rel="' + rel + '"]');
  if (!link) return;

  event.preventDefault();
  link.click();
});
