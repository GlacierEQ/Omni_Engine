# Kong Admin + Insomnia Integration

## Quick Setup

1. **Start Kong** (Docker Compose example):
```bash
docker run -d --name kong \
  -e "KONG_DATABASE=off" \
  -e "KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yml" \
  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
  -e "KONG_PROXY_LISTEN=0.0.0.0:8000" \
  -p 8000:8000 -p 8001:8001 \
  kong:latest
```

2. **Configure Insomnia Environment**:
```
kongAdminUrl: http://localhost:8001
kongAdminToken: your-secret-token-here
```

3. **Import Collection**:
   - File → Import → `kong-admin.json`

## Key Operations

- **Services**: List/Create/Update/Delete
- **Routes**: Map paths/hosts to services  
- **Plugins**: Rate limiting, auth, CORS, etc.
- **Consumers**: API key/users management

## Common Workflows

1. Create Service → Create Route → Add Plugin
2. Rate limiting per consumer
3. JWT/OAuth2 validation
4. Canary deployments

See Kong Admin API docs: https://docs.konghq.com/gateway/latest/admin-api/
