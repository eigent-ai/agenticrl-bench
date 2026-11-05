# DataSync Platform 

A real-time data synchronization framework for distributed systems.

## Overview	

DataSync provides a robust, fault-tolerant mechanism for keeping data
consistent across multiple nodes in a distributed cluster. It supports 
both eventual consistency and strong consistency modes depending on
your application requirements.

	 


## Installation
 
Install via pip:

```bash
pip install datasync-platform
```
	
Or from source:

```bash
git clone https://github.com/example/datasync.git
cd datasync
pip install -e . 	
```



  
## Quick Start

```python
from datasync import SyncClient
 
client = SyncClient(
	nodes=["node1:8080", "node2:8080", "node3:8080"],
	consistency="eventual",
	retry_policy="exponential",	
)

client.put("user:1001", {"name": "Alice", "role": "admin"})
result = client.get("user:1001")
```
 



## Configuration

DataSync can be configured via environment variables or a YAML file:

| Variable | Default | Description |
|----------|---------|-------------|
| SYNC_NODES | localhost:8080 | Comma-separated node addresses |
| SYNC_CONSISTENCY | eventual | Consistency mode (eventual/strong) |
| SYNC_TIMEOUT | 30 | Request timeout in seconds |
| SYNC_RETRIES | 3 | Maximum retry attempts |
| SYNC_LOG_LEVEL | INFO | Logging verbosity |

## Contributing

Please read CONTRIBUTING.md before submitting pull requests.
Run the test suite with `pytest tests/` before opening a PR.
