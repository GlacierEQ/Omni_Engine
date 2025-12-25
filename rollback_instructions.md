# Rollback Instructions - VLEX Integration

In case of failure or API breaking changes:

1. **Remove Code**: Delete the `skills/integrations/vlex` directory.
2. **Revert CI/CD**: Delete `.github/workflows/vlex_test.yml`.
3. **Clean Environment**: Unset or remove `VLEX_API_KEY` from environment files.
4. **Previous State**: If this was part of a larger update, revert to the previous git commit.
   ```bash
   git revert <commit-hash>
   ```
