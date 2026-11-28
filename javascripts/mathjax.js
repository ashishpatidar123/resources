window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// If using Material for MkDocs, this ensures equations render on page navigation
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    MathJax.typesetPromise()
  })
}