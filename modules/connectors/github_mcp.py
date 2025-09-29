"""GitHub MCP (Maximum Control Point) Connector for repository intelligence."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import httpx

from ..memory_bridge import MemoryEntry
from . import Connector

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GitHubMCPConnector(Connector):
    """Maximum Control Point connector for GitHub repository intelligence.
    
    Provides comprehensive repository analysis, commit tracking, workflow monitoring,
    and automated evidence collection for legal case building.
    """

    name: str
    github_token: str
    repositories: List[str] = field(default_factory=list)
    layer: str = "github_intelligence"
    source: str = "GITHUB_MCP"
    include_commits: bool = True
    include_issues: bool = True
    include_workflows: bool = True
    include_branches: bool = True
    max_commits: int = 100
    days_back: int = 30
    base_url: str = "https://api.github.com"
    
    def __post_init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Omni-Engine-MCP/1.0"
            },
            timeout=30.0
        )

    async def _get_authenticated_user(self) -> Dict[str, Any]:
        """Get details about the authenticated GitHub user."""
        try:
            response = await self.client.get(f"{self.base_url}/user")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get authenticated user: {e}")
            return {}

    async def _get_repository_info(self, repo: str) -> Dict[str, Any]:
        """Get comprehensive repository information."""
        try:
            response = await self.client.get(f"{self.base_url}/repos/{repo}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get repository info for {repo}: {e}")
            return {}

    async def _get_commits(self, repo: str) -> List[Dict[str, Any]]:
        """Get recent commits from repository."""
        try:
            params = {
                "per_page": min(self.max_commits, 100),
                "since": (datetime.now().replace(microsecond=0) - 
                         datetime.timedelta(days=self.days_back)).isoformat()
            }
            response = await self.client.get(
                f"{self.base_url}/repos/{repo}/commits",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get commits for {repo}: {e}")
            return []

    async def _get_issues(self, repo: str) -> List[Dict[str, Any]]:
        """Get open issues from repository."""
        try:
            params = {
                "state": "all",
                "per_page": 100,
                "sort": "updated"
            }
            response = await self.client.get(
                f"{self.base_url}/repos/{repo}/issues",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get issues for {repo}: {e}")
            return []

    async def _get_workflows(self, repo: str) -> List[Dict[str, Any]]:
        """Get GitHub Actions workflows."""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{repo}/actions/workflows"
            )
            response.raise_for_status()
            return response.json().get("workflows", [])
        except Exception as e:
            logger.error(f"Failed to get workflows for {repo}: {e}")
            return []

    async def _get_workflow_runs(self, repo: str) -> List[Dict[str, Any]]:
        """Get recent workflow runs."""
        try:
            params = {"per_page": 50}
            response = await self.client.get(
                f"{self.base_url}/repos/{repo}/actions/runs",
                params=params
            )
            response.raise_for_status()
            return response.json().get("workflow_runs", [])
        except Exception as e:
            logger.error(f"Failed to get workflow runs for {repo}: {e}")
            return []

    async def _get_branches(self, repo: str) -> List[Dict[str, Any]]:
        """Get repository branches."""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{repo}/branches"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get branches for {repo}: {e}")
            return []

    async def _analyze_repository(self, repo: str) -> List[MemoryEntry]:
        """Perform comprehensive repository analysis."""
        entries = []
        
        # Repository overview
        repo_info = await self._get_repository_info(repo)
        if repo_info:
            content = {
                "type": "repository_overview",
                "repository": repo,
                "description": repo_info.get("description", ""),
                "language": repo_info.get("language"),
                "stars": repo_info.get("stargazers_count", 0),
                "forks": repo_info.get("forks_count", 0),
                "open_issues": repo_info.get("open_issues_count", 0),
                "created_at": repo_info.get("created_at"),
                "updated_at": repo_info.get("updated_at"),
                "size": repo_info.get("size", 0),
                "default_branch": repo_info.get("default_branch"),
                "visibility": repo_info.get("visibility", "unknown")
            }
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Repository Analysis: {repo}\n{json.dumps(content, indent=2)}",
                source=f"{self.source}_REPO_INTEL",
                metadata={"repo": repo, "analysis_type": "overview"}
            ))

        # Commit analysis
        if self.include_commits:
            commits = await self._get_commits(repo)
            for commit in commits[:20]:  # Limit to recent commits
                commit_data = {
                    "type": "commit_analysis",
                    "repository": repo,
                    "sha": commit.get("sha", "")[:7],
                    "message": commit.get("commit", {}).get("message", ""),
                    "author": commit.get("commit", {}).get("author", {}).get("name"),
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                    "additions": commit.get("stats", {}).get("additions", 0),
                    "deletions": commit.get("stats", {}).get("deletions", 0),
                    "files_changed": len(commit.get("files", []))
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Commit Intelligence: {repo}\n{json.dumps(commit_data, indent=2)}",
                    source=f"{self.source}_COMMIT_INTEL",
                    metadata={"repo": repo, "analysis_type": "commit", "sha": commit.get("sha", "")[:7]}
                ))

        # Issue analysis
        if self.include_issues:
            issues = await self._get_issues(repo)
            for issue in issues[:10]:  # Limit to recent issues
                issue_data = {
                    "type": "issue_analysis",
                    "repository": repo,
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "author": issue.get("user", {}).get("login"),
                    "created_at": issue.get("created_at"),
                    "updated_at": issue.get("updated_at"),
                    "labels": [label.get("name") for label in issue.get("labels", [])],
                    "comments": issue.get("comments", 0)
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Issue Intelligence: {repo}\n{json.dumps(issue_data, indent=2)}",
                    source=f"{self.source}_ISSUE_INTEL",
                    metadata={"repo": repo, "analysis_type": "issue", "issue_number": issue.get("number")}
                ))

        # Workflow analysis
        if self.include_workflows:
            workflows = await self._get_workflows(repo)
            workflow_runs = await self._get_workflow_runs(repo)
            
            for workflow in workflows:
                workflow_data = {
                    "type": "workflow_analysis",
                    "repository": repo,
                    "name": workflow.get("name"),
                    "state": workflow.get("state"),
                    "path": workflow.get("path"),
                    "created_at": workflow.get("created_at"),
                    "updated_at": workflow.get("updated_at")
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Workflow Intelligence: {repo}\n{json.dumps(workflow_data, indent=2)}",
                    source=f"{self.source}_WORKFLOW_INTEL",
                    metadata={"repo": repo, "analysis_type": "workflow", "workflow_id": workflow.get("id")}
                ))
            
            # Recent workflow runs
            for run in workflow_runs[:5]:
                run_data = {
                    "type": "workflow_run_analysis",
                    "repository": repo,
                    "workflow_name": run.get("name"),
                    "status": run.get("status"),
                    "conclusion": run.get("conclusion"),
                    "created_at": run.get("created_at"),
                    "updated_at": run.get("updated_at"),
                    "head_branch": run.get("head_branch"),
                    "run_number": run.get("run_number")
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Workflow Run Intelligence: {repo}\n{json.dumps(run_data, indent=2)}",
                    source=f"{self.source}_WORKFLOW_RUN_INTEL",
                    metadata={"repo": repo, "analysis_type": "workflow_run", "run_id": run.get("id")}
                ))

        # Branch analysis
        if self.include_branches:
            branches = await self._get_branches(repo)
            for branch in branches:
                branch_data = {
                    "type": "branch_analysis",
                    "repository": repo,
                    "name": branch.get("name"),
                    "protected": branch.get("protected", False),
                    "commit_sha": branch.get("commit", {}).get("sha", "")[:7]
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Branch Intelligence: {repo}\n{json.dumps(branch_data, indent=2)}",
                    source=f"{self.source}_BRANCH_INTEL",
                    metadata={"repo": repo, "analysis_type": "branch", "branch_name": branch.get("name")}
                ))

        return entries

    async def gather_async(self) -> Iterable[MemoryEntry]:
        """Asynchronously gather GitHub intelligence from all configured repositories."""
        entries = []
        
        # User authentication check
        user_info = await self._get_authenticated_user()
        if user_info:
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"GitHub Authentication: Connected as {user_info.get('login')}\n" +
                       f"Public Repos: {user_info.get('public_repos', 0)}\n" +
                       f"Private Repos: {user_info.get('total_private_repos', 0)}\n" +
                       f"Followers: {user_info.get('followers', 0)}",
                source=f"{self.source}_AUTH",
                metadata={"analysis_type": "authentication"}
            ))

        # Analyze each repository
        for repo in self.repositories:
            try:
                repo_entries = await self._analyze_repository(repo)
                entries.extend(repo_entries)
                logger.info(f"Analyzed repository {repo}: {len(repo_entries)} entries")
            except Exception as e:
                logger.error(f"Failed to analyze repository {repo}: {e}")
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Repository Analysis Error: {repo}\nError: {str(e)}",
                    source=f"{self.source}_ERROR",
                    metadata={"repo": repo, "analysis_type": "error"}
                ))

        await self.client.aclose()
        return entries

    def gather(self) -> Iterable[MemoryEntry]:
        """Synchronous wrapper for async gather method."""
        return asyncio.run(self.gather_async())


__all__ = ["GitHubMCPConnector"]
