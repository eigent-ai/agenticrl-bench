# API Reference

Complete API reference for DocForge internals.

## Entity Store

The `EntityStore` manages all document entities in the pipeline.
Each document is represented as an entity with attached components.

### Methods

- `spawn()` - Create a new entity
- `insert_component<T>(id, component)` - Attach a component to an entity
- `get_component<T>(id)` - Retrieve a component from an entity
- `query_entities<T>()` - Find all entities with a specific component type

## Resource Map

The `ResourceMap` holds shared configuration resources accessible to all plugins.

## Plugin Trait

All pipeline stages implement the `Plugin` trait:

```rust
trait Plugin {
    fn name(&self) -> &str;
    fn run(&mut self, store: &mut EntityStore, resources: &ResourceMap)
        -> Result<Vec<EntityId>, Box<dyn Error>>;
}
```

For usage examples, see [[tutorial.md]] and [[guide.md]].

Document generated from: {{filename}}
