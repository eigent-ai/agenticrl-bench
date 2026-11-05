#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { applyDefaults } = require('./defaults');
const { countSlugs } = require('./slugCounter');
const { markActive } = require('./utils');
const { render } = require('./renderer');

function main() {
  const configPath = process.argv[2];
  if (!configPath) {
    console.error('Usage: node src/index.js <menu-config.json>');
    process.exit(1);
  }

  const fullPath = path.resolve(configPath);
  if (!fs.existsSync(fullPath)) {
    console.error(`File not found: ${fullPath}`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(fullPath, 'utf8'));

  let items = config.items;
  const defaults = config.defaults;
  const currentPath = config.currentPath;

  items = applyDefaults(items, defaults);

  const slugCounts = countSlugs(items);
  items = items.map(item => ({
    ...item,
    slugCount: slugCounts[item.slug] || 0
  }));

  items = markActive(items, currentPath);

  const html = render(items);
  console.log(html);
}

main();
