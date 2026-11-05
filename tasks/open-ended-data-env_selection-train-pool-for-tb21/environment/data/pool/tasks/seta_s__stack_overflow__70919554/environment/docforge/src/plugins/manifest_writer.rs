use std::collections::HashSet;
use std::path::PathBuf;

use serde::Serialize;

use crate::config::OutputConfig;
use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;

#[derive(Serialize)]
struct ProcessedEntry {
    title: String,
    filename: String,
    #[serde(skip)]
    word_count: usize,
    timestamp: String,
    applied_transformations: HashSet<String>,
}

pub struct ManifestWriterPlugin;

impl Plugin for ManifestWriterPlugin {
    fn name(&self) -> &str {
        "ManifestWriter"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        let output_dir = resources
            .get::<OutputConfig>()
            .map(|c| c.output_dir.clone())
            .unwrap_or_default();

        log::info!("ManifestWriter output directory: {:?}", output_dir);

        if !output_dir.as_os_str().is_empty() {
            std::fs::create_dir_all(&output_dir)?;
        }

        let entities = store.all_entities();
        let mut manifest_entries = Vec::new();

        for id in &entities {
            if let Some(doc) = store.get_component::<Document>(*id) {
                let html = render_markdown(&doc.content);
                let html_filename = doc.filename.replace(".md", ".html");
                let html_path = resolve_path(&output_dir, &html_filename);

                std::fs::write(&html_path, &html)?;
                log::debug!("Wrote HTML file: {:?}", html_path);

                let title = doc
                    .metadata
                    .get("title")
                    .cloned()
                    .unwrap_or_else(|| "Untitled".to_string());
                let word_count = doc
                    .metadata
                    .get("word_count")
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(0usize);

                manifest_entries.push(ProcessedEntry {
                    title,
                    filename: html_filename,
                    word_count,
                    timestamp: chrono::Local::now()
                        .format("%Y-%m-%dT%H:%M:%S")
                        .to_string(),
                    applied_transformations: doc
                        .applied_transformations
                        .iter()
                        .cloned()
                        .collect(),
                });
            }
        }

        let manifest_path = resolve_path(&output_dir, "manifest.json");
        let manifest_json = serde_json::to_string_pretty(&manifest_entries)?;
        std::fs::write(&manifest_path, &manifest_json)?;
        log::info!(
            "Wrote manifest with {} entries to {:?}",
            manifest_entries.len(),
            manifest_path
        );

        Ok(entities)
    }
}

fn resolve_path(base: &PathBuf, filename: &str) -> PathBuf {
    if base.as_os_str().is_empty() {
        PathBuf::from(filename)
    } else {
        base.join(filename)
    }
}

fn render_markdown(content: &str) -> String {
    use pulldown_cmark::{html, Options, Parser};
    let options = Options::all();
    let parser = Parser::new_ext(content, options);
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);
    html_output
}
