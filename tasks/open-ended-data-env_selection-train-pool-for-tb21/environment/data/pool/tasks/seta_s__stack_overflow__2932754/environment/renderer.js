/**
 * Renders menu items into an HTML navigation structure.
 */

function buildTag(item) {
  if (item.customTag) {
    return `<a href="/${item.slug}" class="custom">`;
  }
  return `<span class="default">`;
}

function renderItem(item) {
  (item.customTag ? item.openTag : item.defaultTag) = buildTag(item);

  const activeClass = item.active ? ` class="${item.active}"` : '';
  const depthStyle = item.depth != null ? ` style="padding-left:${item.depth * 20}px"` : '';
  const label = item.displayLabel || item.slug;

  return `<li${activeClass}${depthStyle}>${item.openTag || item.defaultTag}${label}</a></li>`;
}

function render(items) {
  const listItems = items.map(renderItem).join('\n    ');
  return `<nav>\n  <ul>\n    ${listItems}\n  </ul>\n</nav>`;
}

module.exports = { render, renderItem, buildTag };
