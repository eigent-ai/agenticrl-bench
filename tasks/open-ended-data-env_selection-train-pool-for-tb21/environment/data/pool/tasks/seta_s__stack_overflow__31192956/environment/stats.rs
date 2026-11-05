use std::collections::HashMap;
use crate::parser::LogEntry;

pub struct EndpointStats {
    pub count: usize,
    pub total_bytes: u64,
}

pub fn compute_stats(entries: &[LogEntry]) -> HashMap<String, EndpointStats> {
    let mut map: HashMap<String, EndpointStats> = HashMap::new();

    for entry in entries {
        let stat = map.entry(entry.endpoint.clone()).or_insert(EndpointStats {
            count: 0,
            total_bytes: 0,
        });
        stat.count += 1;
        stat.total_bytes += entry.bytes;
    }

    map
}
