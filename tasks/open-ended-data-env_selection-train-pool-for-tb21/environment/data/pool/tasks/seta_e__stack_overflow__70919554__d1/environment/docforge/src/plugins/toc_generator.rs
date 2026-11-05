use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;

pub struct TocGeneratorPlugin;

impl Plugin for TocGeneratorPlugin {
    fn name(&self) -> &str {
        "TocGenerator"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        _resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        let entities = store.query_entities::<Document>();
        log::debug!("TocGenerator found {} document entities", entities.len());

        let mut processed = Vec::new();

        for id in &entities {
            if let Some(doc) = store.get_component_mut::<Document>(*id) {
                let headings = extract_headings(&doc.content);
                if headings.len() >= 2 {
                    let toc = generate_toc(&headings);
                    doc.content = format!("{}\n\n{}", toc, doc.content);
                    doc.applied_transformations
                        .push("toc_generation".to_string());
                    log::debug!(
                        "Generated ToC for {} ({} headings)",
                        doc.filename,
                        headings.len()
                    );
                }
                processed.push(*id);
            }
        }

        Ok(processed)
    }
}

fn extract_headings(content: &str) -> Vec<(usize, String)> {
    let mut headings = Vec::new();
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with('#') {
            let level = trimmed.chars().take_while(|c| *c == '#').count();
            let text = trimmed[level..].trim().to_string();
            if !text.is_empty() {
                headings.push((level, text));
            }
        }
    }
    headings
}

fn generate_toc(headings: &[(usize, String)]) -> String {
    let mut toc = String::from("## Table of Contents\n\n");
    for (level, text) in headings {
        let indent = "  ".repeat(level.saturating_sub(1));
        let anchor = text
            .to_lowercase()
            .replace(' ', "-")
            .chars()
            .filter(|c| c.is_alphanumeric() || *c == '-')
            .collect::<String>();
        toc.push_str(&format!("{}- [{}](#{})\n", indent, text, anchor));
    }
    toc
}
