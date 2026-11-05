use std::collections::HashMap;
use std::path::Path;

use crate::ecs::EntityStore;

#[derive(Clone, Debug)]
pub struct Document {
    pub filename: String,
    pub content: String,
    pub metadata: HashMap<String, String>,
    pub applied_transformations: Vec<String>,
}

impl Document {
    pub fn new(filename: String, content: String) -> Self {
        Document {
            filename,
            content,
            metadata: HashMap::new(),
            applied_transformations: Vec::new(),
        }
    }
}

pub fn load_documents(
    input_dir: &Path,
    store: &mut EntityStore,
) -> Result<(), Box<dyn std::error::Error>> {
    let mut entries: Vec<_> = std::fs::read_dir(input_dir)?
        .filter_map(|e| e.ok())
        .filter(|e| {
            e.path()
                .extension()
                .and_then(|s| s.to_str())
                .map(|s| s == "md")
                .unwrap_or(false)
        })
        .collect();

    entries.sort_by_key(|e| e.file_name());

    for entry in entries {
        let path = entry.path();
        let content = std::fs::read_to_string(&path)?;
        let filename = path.file_name().unwrap().to_string_lossy().to_string();
        log::debug!("Loading document: {}", filename);

        let id = store.spawn();
        store.insert_component(id, Document::new(filename, content));
    }

    Ok(())
}
