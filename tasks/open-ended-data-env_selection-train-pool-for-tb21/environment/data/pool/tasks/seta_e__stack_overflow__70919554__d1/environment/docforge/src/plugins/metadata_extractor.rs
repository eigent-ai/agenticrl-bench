use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;

pub struct MetadataExtractorPlugin;

impl Plugin for MetadataExtractorPlugin {
    fn name(&self) -> &str {
        "MetadataExtractor"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        _resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        let entities = store.all_entities();
        let mut processed = Vec::new();

        for id in &entities {
            if let Some(doc) = store.get_component_mut::<Document>(*id) {
                let title = extract_title(&doc.content);
                let word_count = count_words(&doc.content);

                log::debug!(
                    "Extracted metadata for {}: title='{}', words={}",
                    doc.filename,
                    title,
                    word_count
                );

                doc.metadata.insert("title".to_string(), title);
                doc.metadata
                    .insert("word_count".to_string(), word_count.to_string());
                doc.applied_transformations
                    .push("metadata_extraction".to_string());

                processed.push(*id);
            }
        }

        Ok(processed)
    }
}

fn extract_title(content: &str) -> String {
    for line in content.lines() {
        let trimmed = line.trim();
        if let Some(title) = trimmed.strip_prefix("# ") {
            return title.trim().to_string();
        }
    }
    "Untitled".to_string()
}

fn count_words(content: &str) -> usize {
    content.split_whitespace().count()
}
