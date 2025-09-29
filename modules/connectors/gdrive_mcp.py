"""Google Drive MCP (Maximum Control Point) Connector for cloud evidence management."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    logging.warning("Google Drive dependencies not installed. Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    Request = Credentials = InstalledAppFlow = build = HttpError = None

from ..memory_bridge import MemoryEntry
from . import Connector

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]


@dataclass(slots=True)
class GoogleDriveMCPConnector(Connector):
    """Maximum Control Point connector for Google Drive evidence management.
    
    Provides comprehensive file analysis, metadata extraction, and automated
    evidence collection from Google Drive for legal case building.
    """

    name: str
    credentials_path: str
    token_path: str = "gdrive_token.json"
    layer: str = "cloud_evidence"
    source: str = "GDRIVE_MCP"
    include_metadata: bool = True
    include_permissions: bool = True
    include_revisions: bool = False
    max_files: int = 1000
    days_back: int = 30
    file_types: List[str] = field(default_factory=lambda: [
        'application/pdf',
        'application/vnd.google-apps.document',
        'application/vnd.google-apps.spreadsheet',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'image/jpeg',
        'image/png'
    ])
    folder_ids: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Drive API using OAuth 2.0."""
        if not all([Request, Credentials, InstalledAppFlow, build]):
            raise ImportError("Google Drive dependencies not installed")
            
        creds = None
        
        # Load existing token
        if Path(self.token_path).exists():
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    creds = None
            
            if not creds:
                if not Path(self.credentials_path).exists():
                    raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Successfully authenticated with Google Drive API")
        except Exception as e:
            logger.error(f"Failed to build Drive service: {e}")
            raise

    def _get_drive_info(self) -> Dict[str, Any]:
        """Get Google Drive account information."""
        try:
            about = self.service.about().get(fields='user,storageQuota').execute()
            return about
        except HttpError as e:
            logger.error(f"Failed to get drive info: {e}")
            return {}

    def _search_files(self, query: str = None, folder_id: str = None) -> List[Dict[str, Any]]:
        """Search for files in Google Drive."""
        try:
            # Build query
            query_parts = []
            
            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")
            
            if self.file_types:
                mime_query = " or ".join([f"mimeType='{mime}'" for mime in self.file_types])
                query_parts.append(f"({mime_query})")
            
            # Filter by modification date
            if self.days_back > 0:
                cutoff_date = (datetime.now() - timedelta(days=self.days_back)).isoformat() + 'Z'
                query_parts.append(f"modifiedTime >= '{cutoff_date}'")
            
            # Add trashed filter
            query_parts.append("trashed=false")
            
            if query:
                query_parts.append(query)
            
            final_query = " and ".join(query_parts)
            
            # Execute search
            fields = (
                'nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime,'
                'lastModifyingUser,parents,webViewLink,webContentLink,owners,'
                'permissions,shared,version,headRevisionId,md5Checksum,'
                'imageMediaMetadata,videoMediaMetadata,description)'
            )
            
            results = self.service.files().list(
                q=final_query,
                pageSize=min(self.max_files, 1000),
                fields=fields,
                orderBy='modifiedTime desc'
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as e:
            logger.error(f"Failed to search files: {e}")
            return []

    def _get_file_permissions(self, file_id: str) -> List[Dict[str, Any]]:
        """Get file permissions and sharing information."""
        try:
            permissions = self.service.permissions().list(
                fileId=file_id,
                fields='permissions(id,type,emailAddress,role,displayName,domain)'
            ).execute()
            return permissions.get('permissions', [])
        except HttpError as e:
            logger.error(f"Failed to get permissions for file {file_id}: {e}")
            return []

    def _get_file_revisions(self, file_id: str) -> List[Dict[str, Any]]:
        """Get file revision history."""
        try:
            revisions = self.service.revisions().list(
                fileId=file_id,
                fields='revisions(id,modifiedTime,lastModifyingUser,size,md5Checksum)'
            ).execute()
            return revisions.get('revisions', [])
        except HttpError as e:
            logger.error(f"Failed to get revisions for file {file_id}: {e}")
            return []

    def _analyze_file(self, file_data: Dict[str, Any]) -> MemoryEntry:
        """Analyze a single file and create memory entry."""
        file_id = file_data.get('id')
        
        # Basic file analysis
        analysis = {
            "type": "file_analysis",
            "file_id": file_id,
            "name": file_data.get('name'),
            "mime_type": file_data.get('mimeType'),
            "size": file_data.get('size'),
            "created_time": file_data.get('createdTime'),
            "modified_time": file_data.get('modifiedTime'),
            "last_modifying_user": file_data.get('lastModifyingUser', {}).get('emailAddress'),
            "owners": [owner.get('emailAddress') for owner in file_data.get('owners', [])],
            "web_view_link": file_data.get('webViewLink'),
            "shared": file_data.get('shared', False),
            "version": file_data.get('version'),
            "md5_checksum": file_data.get('md5Checksum'),
            "description": file_data.get('description')
        }
        
        # Add media metadata for images/videos
        if 'imageMediaMetadata' in file_data:
            analysis['image_metadata'] = file_data['imageMediaMetadata']
        if 'videoMediaMetadata' in file_data:
            analysis['video_metadata'] = file_data['videoMediaMetadata']
        
        # Get permissions if enabled
        if self.include_permissions and file_id:
            permissions = self._get_file_permissions(file_id)
            analysis['permissions'] = permissions
            analysis['permission_count'] = len(permissions)
            analysis['public_access'] = any(
                perm.get('type') == 'anyone' for perm in permissions
            )
        
        # Get revisions if enabled
        if self.include_revisions and file_id:
            revisions = self._get_file_revisions(file_id)
            analysis['revisions'] = revisions[:5]  # Limit to recent revisions
            analysis['revision_count'] = len(revisions)
        
        # Risk assessment
        risk_factors = []
        if analysis.get('shared'):
            risk_factors.append('shared_file')
        if analysis.get('public_access'):
            risk_factors.append('public_access')
        if analysis.get('permission_count', 0) > 10:
            risk_factors.append('many_permissions')
        
        analysis['risk_factors'] = risk_factors
        analysis['risk_level'] = 'high' if len(risk_factors) >= 2 else 'medium' if risk_factors else 'low'
        
        return MemoryEntry(
            layer=self.layer,
            content=f"Google Drive File Analysis: {file_data.get('name')}\n{json.dumps(analysis, indent=2, default=str)}",
            source=f"{self.source}_FILE_INTEL",
            metadata={
                "file_id": file_id,
                "file_name": file_data.get('name'),
                "analysis_type": "file",
                "risk_level": analysis['risk_level']
            }
        )

    def _analyze_folder_structure(self) -> List[MemoryEntry]:
        """Analyze folder structure and organization."""
        entries = []
        
        # If specific folders provided, analyze them
        if self.folder_ids:
            for folder_id in self.folder_ids:
                try:
                    folder_info = self.service.files().get(
                        fileId=folder_id,
                        fields='id,name,createdTime,modifiedTime,owners,shared,permissions'
                    ).execute()
                    
                    folder_analysis = {
                        "type": "folder_analysis",
                        "folder_id": folder_id,
                        "name": folder_info.get('name'),
                        "created_time": folder_info.get('createdTime'),
                        "modified_time": folder_info.get('modifiedTime'),
                        "owners": [owner.get('emailAddress') for owner in folder_info.get('owners', [])],
                        "shared": folder_info.get('shared', False)
                    }
                    
                    # Count files in folder
                    files_in_folder = self._search_files(folder_id=folder_id)
                    folder_analysis['file_count'] = len(files_in_folder)
                    folder_analysis['file_types'] = list(set(f.get('mimeType') for f in files_in_folder))
                    
                    entries.append(MemoryEntry(
                        layer=self.layer,
                        content=f"Folder Structure Analysis: {folder_info.get('name')}\n{json.dumps(folder_analysis, indent=2, default=str)}",
                        source=f"{self.source}_FOLDER_INTEL",
                        metadata={
                            "folder_id": folder_id,
                            "folder_name": folder_info.get('name'),
                            "analysis_type": "folder"
                        }
                    ))
                    
                except HttpError as e:
                    logger.error(f"Failed to analyze folder {folder_id}: {e}")
        
        return entries

    def gather(self) -> Iterable[MemoryEntry]:
        """Gather Google Drive intelligence and evidence."""
        if not self.service:
            logger.error("Google Drive service not initialized")
            return []
        
        entries = []
        
        # Drive account information
        drive_info = self._get_drive_info()
        if drive_info:
            user_info = drive_info.get('user', {})
            storage_info = drive_info.get('storageQuota', {})
            
            account_analysis = {
                "type": "account_analysis",
                "user_email": user_info.get('emailAddress'),
                "display_name": user_info.get('displayName'),
                "storage_limit": storage_info.get('limit'),
                "storage_usage": storage_info.get('usage'),
                "storage_usage_in_drive": storage_info.get('usageInDrive'),
                "storage_usage_in_trash": storage_info.get('usageInDriveTrash')
            }
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Google Drive Account Analysis\n{json.dumps(account_analysis, indent=2, default=str)}",
                source=f"{self.source}_ACCOUNT",
                metadata={"analysis_type": "account"}
            ))
        
        # Analyze folder structure
        folder_entries = self._analyze_folder_structure()
        entries.extend(folder_entries)
        
        # Search and analyze files
        try:
            # Search in specific folders or entire drive
            all_files = []
            
            if self.folder_ids:
                for folder_id in self.folder_ids:
                    folder_files = self._search_files(folder_id=folder_id)
                    all_files.extend(folder_files)
            else:
                all_files = self._search_files()
            
            logger.info(f"Found {len(all_files)} files to analyze")
            
            # Analyze each file
            for file_data in all_files:
                try:
                    file_entry = self._analyze_file(file_data)
                    entries.append(file_entry)
                except Exception as e:
                    logger.error(f"Failed to analyze file {file_data.get('name')}: {e}")
            
            # Summary analysis
            if all_files:
                summary = {
                    "type": "drive_summary",
                    "total_files_analyzed": len(all_files),
                    "file_types_found": list(set(f.get('mimeType') for f in all_files)),
                    "shared_files_count": sum(1 for f in all_files if f.get('shared')),
                    "recent_activity_count": len(all_files),  # All files are recent by our filter
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"Google Drive Summary Analysis\n{json.dumps(summary, indent=2)}",
                    source=f"{self.source}_SUMMARY",
                    metadata={"analysis_type": "summary"}
                ))
            
        except Exception as e:
            logger.error(f"Failed to gather Google Drive intelligence: {e}")
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Google Drive Analysis Error: {str(e)}",
                source=f"{self.source}_ERROR",
                metadata={"analysis_type": "error"}
            ))
        
        logger.info(f"Google Drive MCP gathered {len(entries)} intelligence entries")
        return entries


__all__ = ["GoogleDriveMCPConnector"]
