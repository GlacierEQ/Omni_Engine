"""Notion AI MCP (Maximum Control Point) Connector for knowledge management."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
except ImportError:
    logging.warning("Notion client not installed. Install with: pip install notion-client")
    Client = APIResponseError = None

from ..memory_bridge import MemoryEntry
from . import Connector

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class NotionMCPConnector(Connector):
    """Maximum Control Point connector for Notion AI knowledge management.
    
    Provides comprehensive database analysis, page content extraction,
    and automated knowledge organization for legal case management.
    """

    name: str
    api_token: str
    layer: str = "knowledge_base"
    source: str = "NOTION_MCP"
    database_ids: List[str] = field(default_factory=list)
    page_ids: List[str] = field(default_factory=list)
    include_content: bool = True
    include_properties: bool = True
    include_blocks: bool = True
    max_pages: int = 100
    days_back: int = 30
    case_tracking_enabled: bool = True
    evidence_organization: bool = True
    
    def __post_init__(self):
        if not Client:
            raise ImportError("Notion client not installed. Install with: pip install notion-client")
        
        self.client = Client(auth=self.api_token)
        logger.info("Notion MCP connector initialized")

    def _get_database_info(self, database_id: str) -> Dict[str, Any]:
        """Get comprehensive database information."""
        try:
            database = self.client.databases.retrieve(database_id=database_id)
            return database
        except APIResponseError as e:
            logger.error(f"Failed to get database {database_id}: {e}")
            return {}

    def _query_database(self, database_id: str, filter_conditions: Dict = None) -> List[Dict[str, Any]]:
        """Query database for pages with optional filtering."""
        try:
            query_params = {
                "database_id": database_id,
                "page_size": min(self.max_pages, 100)
            }
            
            # Add date filter if days_back is specified
            if self.days_back > 0:
                cutoff_date = (datetime.now() - timedelta(days=self.days_back)).isoformat()
                query_params["filter"] = {
                    "property": "last_edited_time",
                    "date": {
                        "after": cutoff_date
                    }
                }
            
            # Add custom filter conditions
            if filter_conditions:
                if "filter" in query_params:
                    query_params["filter"] = {
                        "and": [query_params["filter"], filter_conditions]
                    }
                else:
                    query_params["filter"] = filter_conditions
            
            response = self.client.databases.query(**query_params)
            return response.get("results", [])
            
        except APIResponseError as e:
            logger.error(f"Failed to query database {database_id}: {e}")
            return []

    def _get_page_content(self, page_id: str) -> Dict[str, Any]:
        """Get page content including properties and blocks."""
        try:
            # Get page properties
            page = self.client.pages.retrieve(page_id=page_id)
            
            page_data = {
                "page_info": page,
                "blocks": [],
                "content_text": ""
            }
            
            # Get page blocks if enabled
            if self.include_blocks:
                blocks_response = self.client.blocks.children.list(block_id=page_id)
                blocks = blocks_response.get("results", [])
                page_data["blocks"] = blocks
                
                # Extract text content from blocks
                text_content = []
                for block in blocks:
                    if block.get("type") == "paragraph":
                        rich_text = block.get("paragraph", {}).get("rich_text", [])
                        for text_obj in rich_text:
                            if text_obj.get("type") == "text":
                                text_content.append(text_obj.get("text", {}).get("content", ""))
                    elif block.get("type") == "heading_1":
                        rich_text = block.get("heading_1", {}).get("rich_text", [])
                        for text_obj in rich_text:
                            if text_obj.get("type") == "text":
                                text_content.append(f"# {text_obj.get('text', {}).get('content', '')}")
                    elif block.get("type") == "heading_2":
                        rich_text = block.get("heading_2", {}).get("rich_text", [])
                        for text_obj in rich_text:
                            if text_obj.get("type") == "text":
                                text_content.append(f"## {text_obj.get('text', {}).get('content', '')}")
                    elif block.get("type") == "heading_3":
                        rich_text = block.get("heading_3", {}).get("rich_text", [])
                        for text_obj in rich_text:
                            if text_obj.get("type") == "text":
                                text_content.append(f"### {text_obj.get('text', {}).get('content', '')}")
                
                page_data["content_text"] = "\n".join(text_content)
            
            return page_data
            
        except APIResponseError as e:
            logger.error(f"Failed to get page content {page_id}: {e}")
            return {}

    def _extract_property_value(self, property_data: Dict[str, Any]) -> Any:
        """Extract value from Notion property data."""
        prop_type = property_data.get("type")
        
        if prop_type == "title":
            title_list = property_data.get("title", [])
            return " ".join([t.get("text", {}).get("content", "") for t in title_list])
        elif prop_type == "rich_text":
            rich_text_list = property_data.get("rich_text", [])
            return " ".join([t.get("text", {}).get("content", "") for t in rich_text_list])
        elif prop_type == "select":
            select_data = property_data.get("select")
            return select_data.get("name") if select_data else None
        elif prop_type == "multi_select":
            multi_select_data = property_data.get("multi_select", [])
            return [item.get("name") for item in multi_select_data]
        elif prop_type == "date":
            date_data = property_data.get("date")
            return date_data.get("start") if date_data else None
        elif prop_type == "number":
            return property_data.get("number")
        elif prop_type == "checkbox":
            return property_data.get("checkbox")
        elif prop_type == "url":
            return property_data.get("url")
        elif prop_type == "email":
            return property_data.get("email")
        elif prop_type == "phone_number":
            return property_data.get("phone_number")
        elif prop_type == "people":
            people_data = property_data.get("people", [])
            return [person.get("name") or person.get("id") for person in people_data]
        elif prop_type == "files":
            files_data = property_data.get("files", [])
            return [file.get("name") for file in files_data]
        elif prop_type == "relation":
            relation_data = property_data.get("relation", [])
            return [rel.get("id") for rel in relation_data]
        else:
            return str(property_data)

    def _analyze_database(self, database_id: str) -> List[MemoryEntry]:
        """Analyze a Notion database comprehensively."""
        entries = []
        
        # Get database structure
        database_info = self._get_database_info(database_id)
        if not database_info:
            return entries
        
        # Database schema analysis
        properties = database_info.get("properties", {})
        schema_analysis = {
            "type": "database_schema",
            "database_id": database_id,
            "title": database_info.get("title", [{}])[0].get("text", {}).get("content", "Untitled"),
            "property_count": len(properties),
            "properties": {}
        }
        
        # Analyze each property
        for prop_name, prop_data in properties.items():
            prop_analysis = {
                "type": prop_data.get("type"),
                "id": prop_data.get("id")
            }
            
            # Add type-specific analysis
            if prop_data.get("type") == "select":
                options = prop_data.get("select", {}).get("options", [])
                prop_analysis["option_count"] = len(options)
                prop_analysis["options"] = [opt.get("name") for opt in options]
            elif prop_data.get("type") == "multi_select":
                options = prop_data.get("multi_select", {}).get("options", [])
                prop_analysis["option_count"] = len(options)
                prop_analysis["options"] = [opt.get("name") for opt in options]
            
            schema_analysis["properties"][prop_name] = prop_analysis
        
        entries.append(MemoryEntry(
            layer=self.layer,
            content=f"Notion Database Schema: {schema_analysis['title']}\n{json.dumps(schema_analysis, indent=2)}",
            source=f"{self.source}_SCHEMA",
            metadata={"database_id": database_id, "analysis_type": "schema"}
        ))
        
        # Query and analyze pages
        pages = self._query_database(database_id)
        
        for page in pages[:20]:  # Limit to 20 pages for performance
            page_id = page.get("id")
            page_properties = page.get("properties", {})
            
            # Extract property values
            extracted_properties = {}
            for prop_name, prop_data in page_properties.items():
                extracted_properties[prop_name] = self._extract_property_value(prop_data)
            
            page_analysis = {
                "type": "page_analysis",
                "page_id": page_id,
                "database_id": database_id,
                "properties": extracted_properties,
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time"),
                "url": page.get("url")
            }
            
            # Get page content if enabled
            if self.include_content:
                content_data = self._get_page_content(page_id)
                if content_data:
                    page_analysis["content_preview"] = content_data.get("content_text", "")[:500]
                    page_analysis["block_count"] = len(content_data.get("blocks", []))
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Notion Page Analysis\n{json.dumps(page_analysis, indent=2, default=str)}",
                source=f"{self.source}_PAGE",
                metadata={
                    "page_id": page_id,
                    "database_id": database_id,
                    "analysis_type": "page"
                }
            ))
        
        # Database summary
        summary = {
            "type": "database_summary",
            "database_id": database_id,
            "title": schema_analysis["title"],
            "total_pages_analyzed": len(pages),
            "property_types": list(set(prop["type"] for prop in schema_analysis["properties"].values())),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        entries.append(MemoryEntry(
            layer=self.layer,
            content=f"Notion Database Summary\n{json.dumps(summary, indent=2)}",
            source=f"{self.source}_DB_SUMMARY",
            metadata={"database_id": database_id, "analysis_type": "database_summary"}
        ))
        
        return entries

    def _analyze_case_management_patterns(self) -> List[MemoryEntry]:
        """Analyze Notion databases for legal case management patterns."""
        entries = []
        
        if not self.case_tracking_enabled:
            return entries
        
        case_patterns = {
            "total_databases_analyzed": len(self.database_ids),
            "potential_case_databases": [],
            "evidence_tracking_found": False,
            "timeline_tracking_found": False,
            "contact_management_found": False,
            "document_organization_found": False
        }
        
        # Analyze each database for case management patterns
        for db_id in self.database_ids:
            db_info = self._get_database_info(db_id)
            if not db_info:
                continue
            
            properties = db_info.get("properties", {})
            prop_names = [name.lower() for name in properties.keys()]
            
            # Check for case management indicators
            case_indicators = {
                "database_id": db_id,
                "title": db_info.get("title", [{}])[0].get("text", {}).get("content", "Untitled"),
                "case_related_properties": [],
                "evidence_properties": [],
                "timeline_properties": [],
                "contact_properties": []
            }
            
            # Legal case keywords
            case_keywords = ['case', 'matter', 'client', 'lawsuit', 'litigation', 'legal']
            evidence_keywords = ['evidence', 'document', 'exhibit', 'proof', 'file']
            timeline_keywords = ['date', 'deadline', 'due', 'hearing', 'court', 'schedule']
            contact_keywords = ['attorney', 'lawyer', 'judge', 'witness', 'contact', 'person']
            
            for prop_name in prop_names:
                if any(keyword in prop_name for keyword in case_keywords):
                    case_indicators["case_related_properties"].append(prop_name)
                if any(keyword in prop_name for keyword in evidence_keywords):
                    case_indicators["evidence_properties"].append(prop_name)
                if any(keyword in prop_name for keyword in timeline_keywords):
                    case_indicators["timeline_properties"].append(prop_name)
                if any(keyword in prop_name for keyword in contact_keywords):
                    case_indicators["contact_properties"].append(prop_name)
            
            # Calculate case management score
            score = (
                len(case_indicators["case_related_properties"]) * 3 +
                len(case_indicators["evidence_properties"]) * 2 +
                len(case_indicators["timeline_properties"]) * 2 +
                len(case_indicators["contact_properties"]) * 1
            )
            
            case_indicators["case_management_score"] = score
            
            if score >= 3:  # Threshold for case-related database
                case_patterns["potential_case_databases"].append(case_indicators)
                
                if case_indicators["evidence_properties"]:
                    case_patterns["evidence_tracking_found"] = True
                if case_indicators["timeline_properties"]:
                    case_patterns["timeline_tracking_found"] = True
                if case_indicators["contact_properties"]:
                    case_patterns["contact_management_found"] = True
        
        entries.append(MemoryEntry(
            layer=self.layer,
            content=f"Notion Case Management Analysis\n{json.dumps(case_patterns, indent=2)}",
            source=f"{self.source}_CASE_ANALYSIS",
            metadata={"analysis_type": "case_management"}
        ))
        
        return entries

    def gather(self) -> Iterable[MemoryEntry]:
        """Gather Notion AI knowledge management intelligence."""
        entries = []
        
        try:
            # Analyze each configured database
            for database_id in self.database_ids:
                try:
                    db_entries = self._analyze_database(database_id)
                    entries.extend(db_entries)
                    logger.info(f"Analyzed Notion database {database_id}: {len(db_entries)} entries")
                except Exception as e:
                    logger.error(f"Failed to analyze database {database_id}: {e}")
                    entries.append(MemoryEntry(
                        layer=self.layer,
                        content=f"Notion Database Analysis Error: {database_id}\nError: {str(e)}",
                        source=f"{self.source}_ERROR",
                        metadata={"database_id": database_id, "analysis_type": "error"}
                    ))
            
            # Analyze individual pages
            for page_id in self.page_ids:
                try:
                    page_data = self._get_page_content(page_id)
                    if page_data:
                        entries.append(MemoryEntry(
                            layer=self.layer,
                            content=f"Notion Standalone Page Analysis\n{json.dumps(page_data, indent=2, default=str)}",
                            source=f"{self.source}_STANDALONE_PAGE",
                            metadata={"page_id": page_id, "analysis_type": "standalone_page"}
                        ))
                except Exception as e:
                    logger.error(f"Failed to analyze page {page_id}: {e}")
            
            # Case management pattern analysis
            case_entries = self._analyze_case_management_patterns()
            entries.extend(case_entries)
            
            # Overall Notion workspace summary
            workspace_summary = {
                "type": "workspace_summary",
                "databases_analyzed": len(self.database_ids),
                "pages_analyzed": len(self.page_ids),
                "total_entries_generated": len(entries),
                "analysis_timestamp": datetime.now().isoformat(),
                "case_tracking_enabled": self.case_tracking_enabled,
                "evidence_organization": self.evidence_organization
            }
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Notion Workspace Summary\n{json.dumps(workspace_summary, indent=2)}",
                source=f"{self.source}_WORKSPACE_SUMMARY",
                metadata={"analysis_type": "workspace_summary"}
            ))
            
        except Exception as e:
            logger.error(f"Notion MCP analysis failed: {e}")
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"Notion MCP Error: {str(e)}",
                source=f"{self.source}_ERROR",
                metadata={"analysis_type": "error"}
            ))
        
        logger.info(f"Notion MCP generated {len(entries)} knowledge entries")
        return entries


__all__ = ["NotionMCPConnector"]
