/**
 * Applies default values to menu items based on the provided defaults config.
 */
function applyDefaults(items, defaults) {
  return items.map(item => {
    const result = { ...item };

    result.depth = result.depth || defaults.depth;

    result.defaultTag = result.defaultTag || defaults.defaultTag;

    const label = !result.label ? result.label = result.slug.replace(/-/g, ' ') : null;
    result.displayLabel = label.toUpperCase();

    return result;
  });
}

module.exports = { applyDefaults };
