use crate::config::FontConfig;
use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;
use regex::Regex;

pub struct FontNormalizerPlugin;

impl Plugin for FontNormalizerPlugin {
    fn name(&self) -> &str {
        "FontNormalizer"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        let config = resources.get::<FontConfig>().ok_or("FontConfig not found")?;

        if config.font_family.is_empty() {
            log::warn!("No font family configured, skipping font normalization");
            return Ok(store.all_entities());
        }

        let font_re = Regex::new(r#"font-family:\s*"[^"]*""#)?;
        let replacement = format!(r#"font-family: "{}""#, config.font_family);

        let entities = store.all_entities();
        let mut processed = Vec::new();

        for id in &entities {
            if let Some(doc) = store.get_component_mut::<Document>(*id) {
                let new_content = font_re
                    .replace_all(&doc.content, replacement.as_str())
                    .to_string();
                if new_content != doc.content {
                    log::debug!("Normalized fonts in {}", doc.filename);
                    doc.content = new_content;
                    doc.applied_transformations
                        .push("font_normalization".to_string());
                }
                processed.push(*id);
            }
        }

        Ok(processed)
    }
}
