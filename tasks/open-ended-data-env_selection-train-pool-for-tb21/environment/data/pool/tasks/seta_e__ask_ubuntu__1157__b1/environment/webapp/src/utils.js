// Utility functions using Node 20+ features

// structuredClone for deep copying
export function deepCopy(obj) {
  return structuredClone(obj);
}

// Native fetch wrapper
export async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// Array.groupBy (available via Object.groupBy in Node 21+, but we use a manual approach)
export function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    const group = item[key];
    acc[group] = acc[group] || [];
    acc[group].push(item);
    return acc;
  }, {});
}

// Using String.replaceAll (Node 15+)
export function sanitize(input) {
  return input.replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}
