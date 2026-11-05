use std::collections::HashMap;

use crate::document::Document;
use crate::ecs::{EntityId, EntityStore, ResourceMap};
use crate::pipeline::Plugin;

pub struct CrossRefPlugin {
    link_map: Option<HashMap<String, String>>,
}

impl CrossRefPlugin {
    pub fn new() -> Self {
        CrossRefPlugin { link_map: None }
    }

    fn build_link_map(&self, store: &EntityStore) -> HashMap<String, String> {
        let mut map = HashMap::new();
        for id in store.all_entities() {
            if let Some(doc) = store.get_component::<Document>(id) {
                let html_name = doc.filename.replace(".md", ".html");
                let display_name = doc.filename.replace(".md", "");
                map.insert(doc.filename.clone(), format!("{}|{}", html_name, display_name));
            }
        }
        map
    }
}

impl Plugin for CrossRefPlugin {
    fn name(&self) -> &str {
        "CrossRef"
    }

    fn run(
        &mut self,
        store: &mut EntityStore,
        _resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>> {
        if self.link_map.is_none() {
            self.link_map = Some(self.build_link_map(store));
        }

        let entities = store.all_entities();
        let mut processed = Vec::new();

        for id in &entities {
            if let Some(link_map) = self.link_map.take() {
                if let Some(doc) = store.get_component_mut::<Document>(*id) {
                    let mut new_content = doc.content.clone();
                    for (md_name, link_info) in &link_map {
                        let parts: Vec<&str> = link_info.split('|').collect();
                        let html_name = parts[0];
                        let display_name = parts[1];
                        let pattern = format!("[[{}]]", md_name);
                        let replacement =
                            format!("<a href=\"{}\">{}</a>", html_name, display_name);
                        new_content = new_content.replace(&pattern, &replacement);
                    }
                    if new_content != doc.content {
                        log::debug!("Resolved cross-references in {}", doc.filename);
                        doc.content = new_content;
                        doc.applied_transformations
                            .push("cross_reference".to_string());
                    }
                    processed.push(*id);
                }
            }
        }

        Ok(processed)
    }
}
