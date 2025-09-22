from modules.mcp_catalog.main import build_catalog


def test_catalog_contents():
    catalog = build_catalog()
    assert "filesystem" in catalog
    assert "api-supermemory-ai" in catalog
    assert "read_file" in catalog["filesystem"]["functions"]
    assert catalog["api-supermemory-ai"]["status"] == "installed"
