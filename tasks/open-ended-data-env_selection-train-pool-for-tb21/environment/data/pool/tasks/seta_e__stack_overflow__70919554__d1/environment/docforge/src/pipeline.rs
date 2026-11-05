use crate::ecs::{EntityId, EntityStore, ResourceMap};

pub trait Plugin {
    fn name(&self) -> &str;
    fn run(
        &mut self,
        store: &mut EntityStore,
        resources: &ResourceMap,
    ) -> Result<Vec<EntityId>, Box<dyn std::error::Error>>;
}

pub struct PipelineRunner {
    plugins: Vec<Box<dyn Plugin>>,
}

impl PipelineRunner {
    pub fn new() -> Self {
        PipelineRunner {
            plugins: Vec::new(),
        }
    }

    pub fn add_plugin(&mut self, plugin: Box<dyn Plugin>) {
        self.plugins.push(plugin);
    }

    pub fn run(
        &mut self,
        store: &mut EntityStore,
        resources: &ResourceMap,
    ) -> Result<(), Box<dyn std::error::Error>> {
        for plugin in &mut self.plugins {
            log::info!("Running plugin: {}", plugin.name());
            let results = plugin.run(store, resources)?;
            log::debug!(
                "Plugin '{}' processed {} entities",
                plugin.name(),
                results.len()
            );
            if results.is_empty() {
                log::warn!(
                    "Plugin '{}' produced no results, stopping pipeline",
                    plugin.name()
                );
                return Ok(());
            }
        }
        Ok(())
    }
}
