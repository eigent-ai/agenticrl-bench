use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;
use chrono::Local;

pub struct TemplateExpanderPlugin;

impl Plugin for TemplateExpanderPlugin {
    fn name(&self) -> &str {
        "TemplateExpander"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        _resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        let date = Local::now().format("%Y-%m-%d").to_string();

        let entities = store.all_entities();
        let mut processed = Vec::new();

        for id in &entities {
            if let Some(doc) = store.get_component_mut::<Document>(*id) {
                let title = extract_first_heading(&doc.content);

                let new_content = doc
                    .content
                    .replace("{{title}}", &title)
                    .replace("{{date}}", &date)
                    .replace("{{filename}}", &doc.filename);

                if new_content != doc.content {
                    log::debug!("Expanded templates in {}", doc.filename);
                    doc.content = new_content;
                    doc.applied_transformations
                        .push("template_expansion".to_string());
                }
                processed.push(*id);
            }
        }

        Ok(processed)
    }
}

fn extract_first_heading(content: &str) -> String {
    for line in content.lines() {
        let trimmed = line.trim();
        if let Some(title) = trimmed.strip_prefix("# ") {
            return title.trim().to_string();
        }
    }
    "Untitled".to_string()
}
