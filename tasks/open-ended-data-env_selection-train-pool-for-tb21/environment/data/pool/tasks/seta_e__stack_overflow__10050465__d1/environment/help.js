"use strict";

var quickStart = `Use debugger; to pause execution in your code.
Open the Sources panel to step through line by line.
Set breakpoints by clicking on line numbers.
Use console.log() to inspect variables during development.`;

var helpSections = {
  tips: [
    "Set breakpoints in DevTools by clicking the line number gutter.",
    "Use the Network tab to inspect HTTP requests and responses.",
    "Filter requests by type: XHR, JS, CSS, Img, Media, Font.",
    "Right-click a request to copy it as a cURL command."
  ],
  performance: [
    "Use the Performance tab to record and analyze runtime behavior.",
    "Look for long tasks (over 50ms) that block the main thread.",
    "Use requestAnimationFrame for smooth visual updates.",
    "Avoid forced synchronous layout by batching DOM reads and writes."
  ]
};

function getHelpText() {
  var lines = [];
  lines.push("=== Developer Tools Quick Start ===");
  lines.push(quickStart);
  lines.push("");
  var sections = Object.keys(helpSections);
  for (var i = 0; i < sections.length; i++) {
    var sectionName = sections[i];
    var items = helpSections[sectionName];
    lines.push("## " + sectionName.charAt(0).toUpperCase() + sectionName.slice(1));
    for (var j = 0; j < items.length; j++) {
      lines.push("  - " + items[j]);
    }
    lines.push("");
  }
  return lines.join("\n");
}

function getSection(name) {
  if (!helpSections[name]) {
    return "Section not found: " + name;
  }
  return helpSections[name].join("\n");
}

function listSections() {
  return Object.keys(helpSections);
}

module.exports = { getHelpText, getSection, listSections, quickStart };
