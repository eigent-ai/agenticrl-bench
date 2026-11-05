import { readFileSync, mkdirSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { SpriteProcessor } from './sprite-processor.js';
import { AnimationSequencer } from './animation-sequencer.js';
import { MapCompiler } from './map-compiler.js';
import { Renderer } from './renderer.js';
import { ThemeParser } from './theme-parser.js';
import { CssGenerator } from './css-generator.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const appDir = join(__dirname, '..');

async function build() {
  console.log('=== Tile Map Build Pipeline ===');
  console.log('');

  const pipelineConfig = JSON.parse(readFileSync(join(appDir, 'config', 'pipeline.json'), 'utf-8'));
  const themeConfig = JSON.parse(readFileSync(join(appDir, 'config', 'theme.json'), 'utf-8'));

  const outputDir = join(appDir, pipelineConfig.output.directory);
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  console.log('[1/6] Processing sprite sheets...');
  const spriteProcessor = new SpriteProcessor(pipelineConfig);
  await spriteProcessor.loadAndSliceAll(join(appDir, 'assets'));
  console.log('  Sprite sheets loaded and sliced');

  console.log('[2/6] Initializing animation sequencer...');
  const animSequencer = new AnimationSequencer(pipelineConfig);
  console.log(`  ${Object.keys(pipelineConfig.animations).length} animations configured`);

  console.log('[3/6] Compiling tile maps...');
  const mapCompiler = new MapCompiler(pipelineConfig);
  const mapsDir = join(appDir, 'assets', 'maps');
  const mapFiles = readdirSync(mapsDir).filter(f => f.endsWith('.json'));
  const compiledMaps = {};

  for (const mapFile of mapFiles) {
    const mapPath = join(mapsDir, mapFile);
    const compiled = mapCompiler.loadMap(mapPath);
    compiledMaps[compiled.name] = compiled;
    console.log(`  Compiled: ${compiled.name} (${compiled.width}x${compiled.height})`);
  }

  console.log('[4/6] Rendering static maps...');
  const renderer = new Renderer(spriteProcessor, animSequencer, pipelineConfig);
  await renderer.init(join(appDir, 'assets'));

  for (const [name, compiled] of Object.entries(compiledMaps)) {
    const outputPath = join(outputDir, `${pipelineConfig.output.mapPrefix}${name}.png`);
    const result = renderer.renderStaticMap(compiled, outputPath);
    console.log(`  Rendered: ${name} → ${result.width}x${result.height}px`);
  }

  console.log('[5/6] Rendering animated preview...');
  const mainMap = compiledMaps['overworld'] || Object.values(compiledMaps)[0];
  const animOutputPath = join(outputDir, pipelineConfig.output.animatedPreview);
  const animResult = renderer.renderAnimatedPreview(mainMap, animOutputPath, 2000);
  console.log(`  Animated preview: ${animResult.frames} frames`);

  console.log('[6/6] Generating HUD CSS...');
  const themeParser = new ThemeParser(themeConfig);
  themeParser.resolveAll();
  const cssGenerator = new CssGenerator(themeParser);
  const css = cssGenerator.generate();
  const cssOutputPath = join(outputDir, pipelineConfig.output.hudCss);
  const { writeFileSync } = await import('fs');
  writeFileSync(cssOutputPath, css, 'utf-8');
  console.log(`  CSS generated: ${css.length} bytes`);

  console.log('');
  console.log('=== Build Complete ===');
  console.log(`Output directory: ${outputDir}`);

  animSequencer.stopAll();
}

build().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
