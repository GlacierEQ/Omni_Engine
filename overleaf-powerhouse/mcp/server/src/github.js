const { execSync } = require('child_process');

mcp.tool('git_export_project', async ({ project_id, repo_url }) => {
  const projectDir = `/projects/${project_id}`;
  execSync(`git init ${projectDir}`);
  execSync(`cd ${projectDir} && git remote add origin ${repo_url}`);
  execSync(`cd ${projectDir} && git add . && git commit -m "Overleaf MCP export"`);
  execSync(`cd ${projectDir} && git push -u origin main`);
  return { success: true, repo: repo_url };
});
