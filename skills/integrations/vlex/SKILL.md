# VLEX Legal Research Integration

## Description
This skill provides a Python client and CLI interface for interacting with the vLex API. It allows searching for legal cases, statutes, and secondary sources, as well as retrieving full document metadata and text.

## Configuration
Requires an API key from vLex. Set the following environment variable:
- `VLEX_API_KEY`: Your vLex API Bearer token.

## Usage
### Python API
```python
from skills.integrations.vlex.vlex_client import VlexClient

client = VlexClient(api_key="your_key")
results = client.search("due process child custody")
doc = client.get_document(results['results'][0]['id'])
```

### CLI
```bash
export VLEX_API_KEY="your_key"
python3 skills/integrations/vlex/vlex_client.py "child custody jurisdiction"
```

## Integration Hooks
- **GUID Mapping**: When performing research tasks, map internal GUIDs to vLex Document IDs in the metadata store.
- **Auto-Update**: Use `upgrade_hooks.json` to track API version changes.
