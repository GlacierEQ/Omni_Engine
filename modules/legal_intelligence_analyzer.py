"""Legal Intelligence Analyzer for comprehensive case analysis and evidence processing."""

from __future__ import annotations

import json
import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .memory_bridge import MemoryEntry, MemoryBridge

logger = logging.getLogger(__name__)


@dataclass
class CaseEntity:
    """Represents a legal entity extracted from case materials."""
    entity_type: str  # person, organization, location, document, date, etc.
    name: str
    aliases: List[str] = field(default_factory=list)
    confidence: float = 1.0
    source_entries: List[str] = field(default_factory=list)  # MemoryEntry IDs
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CaseEvent:
    """Represents a chronological event in a legal case."""
    date: datetime
    description: str
    participants: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    significance: str = "medium"  # low, medium, high, critical
    source_entries: List[str] = field(default_factory=list)
    event_type: str = "general"  # filing, hearing, correspondence, etc.


@dataclass
class LegalPattern:
    """Represents a legal pattern or trend identified in case materials."""
    pattern_type: str
    description: str
    frequency: int
    confidence: float
    examples: List[str] = field(default_factory=list)
    legal_significance: str = "unknown"


@dataclass
class LegalIntelligenceAnalyzer:
    """Advanced legal intelligence analyzer for comprehensive case analysis.
    
    Processes memory entries to extract legal entities, build case timelines,
    identify patterns, and generate strategic recommendations.
    """
    
    memory_bridge: MemoryBridge
    case_number: Optional[str] = None
    jurisdiction: Optional[str] = "Hawaii"
    court_level: Optional[str] = "Family Court"
    
    # Analysis configuration
    entity_extraction_enabled: bool = True
    timeline_analysis_enabled: bool = True
    pattern_recognition_enabled: bool = True
    risk_assessment_enabled: bool = True
    strategic_analysis_enabled: bool = True
    
    # Legal knowledge patterns
    legal_entity_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        "person": [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # Full names
            r'\b(Mr\.|Mrs\.|Ms\.|Dr\.) ([A-Z][a-z]+ [A-Z][a-z]+)\b',  # Titled names
            r'\b(plaintiff|defendant|witness|attorney|judge)\s+([A-Z][a-z]+ [A-Z][a-z]+)\b'
        ],
        "organization": [
            r'\b([A-Z][a-z]+ (?:Inc\.|LLC|Corp\.|Corporation|Company))\b',
            r'\b(Family Court of [A-Z][a-z]+)\b',
            r'\b([A-Z][a-z]+ Law Firm)\b'
        ],
        "document": [
            r'\b(Motion (?:for|to) [A-Za-z ]+)\b',
            r'\b(Order (?:on|granting|denying) [A-Za-z ]+)\b',
            r'\b(Petition for [A-Za-z ]+)\b',
            r'\b([A-Z][a-z]+ Declaration)\b'
        ],
        "case_number": [
            r'\b([0-9]{1,2}[A-Z]{1,3}-[0-9]{2,4}-[0-9]{7,10})\b',  # Hawaii format
            r'\bCase No\.?\s*([A-Z0-9-]+)\b',
            r'\bCV-[0-9]{4}-[0-9]+\b'
        ],
        "date": [
            r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})\b',
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
            r'\b(\d{4}-\d{2}-\d{2})\b'
        ]
    })
    
    def __post_init__(self):
        self.extracted_entities: Dict[str, List[CaseEntity]] = defaultdict(list)
        self.case_timeline: List[CaseEvent] = []
        self.identified_patterns: List[LegalPattern] = []
        self.analysis_results: Dict[str, Any] = {}
        
        logger.info(f"Legal Intelligence Analyzer initialized for case: {self.case_number or 'Unknown'}")

    def extract_entities_from_text(self, text: str, source_id: str = "") -> List[CaseEntity]:
        """Extract legal entities from text using pattern matching and NLP."""
        entities = []
        
        if not self.entity_extraction_enabled:
            return entities
        
        for entity_type, patterns in self.legal_entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group(1) if match.groups() else match.group(0)
                    
                    # Clean up entity text
                    entity_text = entity_text.strip()
                    if len(entity_text) < 2 or len(entity_text) > 100:
                        continue
                    
                    # Calculate confidence based on context
                    confidence = 0.7  # Base confidence
                    context = text[max(0, match.start()-50):match.end()+50].lower()
                    
                    # Boost confidence for legal contexts
                    legal_context_words = ['court', 'case', 'attorney', 'legal', 'judge', 'motion', 'order']
                    context_matches = sum(1 for word in legal_context_words if word in context)
                    confidence += min(context_matches * 0.1, 0.3)
                    
                    entity = CaseEntity(
                        entity_type=entity_type,
                        name=entity_text,
                        confidence=confidence,
                        source_entries=[source_id] if source_id else [],
                        metadata={"context": context, "pattern_used": pattern}
                    )
                    
                    entities.append(entity)
        
        return entities

    def analyze_entries_for_timeline(self, entries: List[MemoryEntry]) -> List[CaseEvent]:
        """Analyze memory entries to build case timeline."""
        events = []
        
        if not self.timeline_analysis_enabled:
            return events
        
        date_pattern = r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})\b'
        
        for entry in entries:
            # Extract dates from content
            date_matches = re.finditer(date_pattern, entry.content, re.IGNORECASE)
            
            for date_match in date_matches:
                date_str = date_match.group(1)
                
                # Parse date
                try:
                    if '/' in date_str:
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    elif '-' in date_str:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    else:
                        date_obj = datetime.strptime(date_str, '%B %d, %Y')
                except ValueError:
                    continue
                
                # Extract context around the date
                start = max(0, date_match.start() - 100)
                end = min(len(entry.content), date_match.end() + 100)
                context = entry.content[start:end]
                
                # Determine event type based on content
                event_type = "general"
                if any(word in context.lower() for word in ['filed', 'filing', 'motion', 'petition']):
                    event_type = "filing"
                elif any(word in context.lower() for word in ['hearing', 'court', 'appearance']):
                    event_type = "hearing"
                elif any(word in context.lower() for word in ['email', 'letter', 'correspondence']):
                    event_type = "correspondence"
                elif any(word in context.lower() for word in ['order', 'ruling', 'decision']):
                    event_type = "court_order"
                
                # Determine significance
                significance = "medium"
                if any(word in context.lower() for word in ['critical', 'urgent', 'emergency']):
                    significance = "critical"
                elif any(word in context.lower() for word in ['important', 'significant', 'key']):
                    significance = "high"
                elif any(word in context.lower() for word in ['minor', 'routine', 'administrative']):
                    significance = "low"
                
                event = CaseEvent(
                    date=date_obj,
                    description=context.strip(),
                    event_type=event_type,
                    significance=significance,
                    source_entries=[entry.content[:50]]  # Use content preview as ID
                )
                
                events.append(event)
        
        # Sort events chronologically
        events.sort(key=lambda e: e.date)
        
        return events

    def identify_legal_patterns(self, entries: List[MemoryEntry]) -> List[LegalPattern]:
        """Identify patterns and trends in legal case materials."""
        patterns = []
        
        if not self.pattern_recognition_enabled:
            return patterns
        
        # Combine all content for analysis
        all_content = " ".join([entry.content for entry in entries]).lower()
        
        # Legal pattern definitions
        pattern_definitions = {
            "communication_frequency": {
                "keywords": ['email', 'call', 'text', 'message', 'correspondence'],
                "significance": "Communication patterns may indicate cooperation or conflict levels"
            },
            "deadline_management": {
                "keywords": ['deadline', 'due date', 'filing date', 'response due'],
                "significance": "Deadline compliance affects case success probability"
            },
            "conflict_escalation": {
                "keywords": ['dispute', 'disagreement', 'conflict', 'oppose', 'object'],
                "significance": "Escalating conflict may require mediation or settlement discussions"
            },
            "cooperation_indicators": {
                "keywords": ['agree', 'cooperate', 'collaborate', 'work together', 'mutual'],
                "significance": "Cooperation indicators suggest potential for negotiated resolution"
            },
            "child_welfare_concerns": {
                "keywords": ['child safety', 'welfare', 'best interest', 'custody', 'visitation'],
                "significance": "Child welfare is primary consideration in family court decisions"
            },
            "financial_issues": {
                "keywords": ['support', 'financial', 'income', 'expense', 'asset', 'debt'],
                "significance": "Financial documentation affects support calculations and asset division"
            }
        }
        
        for pattern_name, pattern_data in pattern_definitions.items():
            keyword_matches = []
            total_frequency = 0
            
            for keyword in pattern_data["keywords"]:
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', all_content))
                if matches > 0:
                    keyword_matches.append((keyword, matches))
                    total_frequency += matches
            
            if total_frequency >= 2:  # Minimum threshold
                confidence = min(total_frequency / 10.0, 1.0)  # Scale to 0-1
                
                pattern = LegalPattern(
                    pattern_type=pattern_name,
                    description=f"Pattern analysis: {pattern_name}",
                    frequency=total_frequency,
                    confidence=confidence,
                    examples=[f"{kw} ({freq} occurrences)" for kw, freq in keyword_matches],
                    legal_significance=pattern_data["significance"]
                )
                
                patterns.append(pattern)
        
        return patterns

    def assess_case_risks(self, entries: List[MemoryEntry]) -> Dict[str, Any]:
        """Assess potential risks and opportunities in the case."""
        if not self.risk_assessment_enabled:
            return {}
        
        risk_assessment = {
            "timestamp": datetime.now().isoformat(),
            "risk_factors": [],
            "opportunities": [],
            "recommendations": [],
            "overall_risk_level": "medium"
        }
        
        all_content = " ".join([entry.content for entry in entries]).lower()
        
        # Risk factor analysis
        risk_indicators = {
            "communication_breakdown": [
                'no response', 'failed to communicate', 'unresponsive', 'ignored'
            ],
            "deadline_violations": [
                'missed deadline', 'late filing', 'overdue', 'expired'
            ],
            "conflict_escalation": [
                'emergency', 'urgent', 'dispute', 'violation', 'contempt'
            ],
            "documentation_gaps": [
                'missing', 'unavailable', 'lost', 'no record'
            ],
            "child_safety_concerns": [
                'safety concern', 'welfare issue', 'risk to child', 'inappropriate'
            ]
        }
        
        opportunity_indicators = {
            "cooperation_potential": [
                'willing to cooperate', 'open to discussion', 'reasonable', 'collaborative'
            ],
            "strong_documentation": [
                'well documented', 'comprehensive record', 'clear evidence', 'detailed'
            ],
            "favorable_precedents": [
                'similar case', 'precedent', 'favorable ruling', 'established law'
            ],
            "mediation_readiness": [
                'mediation', 'settlement', 'negotiation', 'compromise'
            ]
        }
        
        # Analyze risk factors
        total_risk_score = 0
        for risk_type, indicators in risk_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in all_content)
            if matches > 0:
                risk_factor = {
                    "type": risk_type,
                    "indicators_found": matches,
                    "severity": "high" if matches >= 3 else "medium" if matches >= 2 else "low"
                }
                risk_assessment["risk_factors"].append(risk_factor)
                total_risk_score += matches * (3 if risk_factor["severity"] == "high" else 2 if risk_factor["severity"] == "medium" else 1)
        
        # Analyze opportunities
        for opportunity_type, indicators in opportunity_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in all_content)
            if matches > 0:
                opportunity = {
                    "type": opportunity_type,
                    "indicators_found": matches,
                    "potential": "high" if matches >= 3 else "medium" if matches >= 2 else "low"
                }
                risk_assessment["opportunities"].append(opportunity)
        
        # Calculate overall risk level
        if total_risk_score >= 15:
            risk_assessment["overall_risk_level"] = "critical"
        elif total_risk_score >= 10:
            risk_assessment["overall_risk_level"] = "high"
        elif total_risk_score >= 5:
            risk_assessment["overall_risk_level"] = "medium"
        else:
            risk_assessment["overall_risk_level"] = "low"
        
        return risk_assessment

    def generate_strategic_recommendations(self, 
                                        entities: Dict[str, List[CaseEntity]], 
                                        timeline: List[CaseEvent],
                                        patterns: List[LegalPattern],
                                        risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on case analysis."""
        
        if not self.strategic_analysis_enabled:
            return []
        
        recommendations = []
        
        # Timeline-based recommendations
        if timeline:
            recent_events = [event for event in timeline if (datetime.now() - event.date).days <= 30]
            if recent_events:
                recommendations.append(f"Recent activity detected: {len(recent_events)} events in last 30 days - monitor for developments")
            
            critical_events = [event for event in timeline if event.significance == "critical"]
            if critical_events:
                recommendations.append(f"Critical events identified: {len(critical_events)} - prioritize immediate attention")
        
        # Entity-based recommendations
        total_entities = sum(len(entity_list) for entity_list in entities.values())
        if total_entities > 20:
            recommendations.append("High entity complexity - consider creating relationship mapping diagram")
        
        if "person" in entities and len(entities["person"]) > 5:
            recommendations.append("Multiple parties involved - ensure all parties properly served with documents")
        
        # Pattern-based recommendations
        high_confidence_patterns = [p for p in patterns if p.confidence > 0.8]
        if high_confidence_patterns:
            for pattern in high_confidence_patterns:
                if pattern.pattern_type == "conflict_escalation":
                    recommendations.append("Conflict escalation pattern detected - consider early intervention strategies")
                elif pattern.pattern_type == "cooperation_indicators":
                    recommendations.append("Cooperation indicators present - opportunity for negotiated resolution")
                elif pattern.pattern_type == "child_welfare_concerns":
                    recommendations.append("Child welfare patterns identified - ensure GAL involvement and documentation")
        
        # Risk-based recommendations
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        if risk_level == "critical":
            recommendations.append("CRITICAL RISK LEVEL - immediate escalation and protective measures required")
        elif risk_level == "high":
            recommendations.append("High risk detected - implement enhanced monitoring and rapid response protocols")
        
        # Documentation recommendations
        evidence_entries = sum(1 for entry in self.memory_bridge.get_layer_entries("legal_evidence") if "evidence" in entry.content.lower())
        if evidence_entries < 5:
            recommendations.append("Limited evidence documentation - prioritize evidence collection and preservation")
        
        return recommendations

    def perform_comprehensive_analysis(self) -> Dict[str, Any]:
        """Perform comprehensive legal intelligence analysis."""
        start_time = datetime.now()
        logger.info("Starting comprehensive legal intelligence analysis")
        
        # Get all memory entries
        all_entries = []
        for layer in self.memory_bridge.layers:
            all_entries.extend(self.memory_bridge.get_layer_entries(layer))
        
        logger.info(f"Analyzing {len(all_entries)} memory entries")
        
        # Extract entities
        all_extracted_entities = defaultdict(list)
        for entry in all_entries:
            entry_entities = self.extract_entities_from_text(entry.content, entry.content[:50])
            for entity in entry_entities:
                all_extracted_entities[entity.entity_type].append(entity)
        
        # Consolidate duplicate entities
        for entity_type, entity_list in all_extracted_entities.items():
            consolidated = self._consolidate_entities(entity_list)
            self.extracted_entities[entity_type] = consolidated
        
        # Build timeline
        self.case_timeline = self.analyze_entries_for_timeline(all_entries)
        
        # Identify patterns
        self.identified_patterns = self.identify_legal_patterns(all_entries)
        
        # Assess risks
        risk_assessment = self.assess_case_risks(all_entries)
        
        # Generate recommendations
        recommendations = self.generate_strategic_recommendations(
            self.extracted_entities,
            self.case_timeline,
            self.identified_patterns,
            risk_assessment
        )
        
        # Compile comprehensive analysis results
        end_time = datetime.now()
        analysis_time = (end_time - start_time).total_seconds()
        
        self.analysis_results = {
            "analysis_metadata": {
                "case_number": self.case_number,
                "jurisdiction": self.jurisdiction,
                "court_level": self.court_level,
                "analysis_timestamp": start_time.isoformat(),
                "analysis_duration": analysis_time,
                "entries_analyzed": len(all_entries)
            },
            "entity_analysis": {
                "total_entities": sum(len(entities) for entities in self.extracted_entities.values()),
                "entities_by_type": {k: len(v) for k, v in self.extracted_entities.items()},
                "high_confidence_entities": sum(
                    1 for entities in self.extracted_entities.values() 
                    for entity in entities if entity.confidence > 0.8
                )
            },
            "timeline_analysis": {
                "total_events": len(self.case_timeline),
                "event_types": dict(Counter(event.event_type for event in self.case_timeline)),
                "critical_events": len([e for e in self.case_timeline if e.significance == "critical"]),
                "recent_events": len([e for e in self.case_timeline if (datetime.now() - e.date).days <= 30])
            },
            "pattern_analysis": {
                "patterns_identified": len(self.identified_patterns),
                "high_confidence_patterns": len([p for p in self.identified_patterns if p.confidence > 0.8]),
                "pattern_types": list(set(p.pattern_type for p in self.identified_patterns))
            },
            "risk_assessment": risk_assessment,
            "strategic_recommendations": recommendations
        }
        
        logger.info(f"Legal intelligence analysis completed in {analysis_time:.2f}s")
        return self.analysis_results

    def _consolidate_entities(self, entities: List[CaseEntity]) -> List[CaseEntity]:
        """Consolidate duplicate entities based on similarity."""
        if not entities:
            return []
        
        consolidated = []
        processed_names = set()
        
        for entity in entities:
            # Simple similarity check (can be enhanced with fuzzy matching)
            name_normalized = entity.name.lower().strip()
            
            if name_normalized not in processed_names:
                # Find similar entities
                similar_entities = [
                    e for e in entities 
                    if e.name.lower().strip() == name_normalized and e not in consolidated
                ]
                
                if len(similar_entities) > 1:
                    # Merge entities
                    merged_entity = CaseEntity(
                        entity_type=entity.entity_type,
                        name=entity.name,
                        aliases=list(set(sum([e.aliases for e in similar_entities], []))),
                        confidence=max(e.confidence for e in similar_entities),
                        source_entries=list(set(sum([e.source_entries for e in similar_entities], []))),
                        metadata={"merged_from": len(similar_entities)}
                    )
                    consolidated.append(merged_entity)
                else:
                    consolidated.append(entity)
                
                processed_names.add(name_normalized)
        
        return consolidated

    def export_analysis_report(self, output_path: Path) -> None:
        """Export comprehensive analysis report to JSON file."""
        if not self.analysis_results:
            logger.warning("No analysis results to export")
            return
        
        # Prepare export data
        export_data = {
            "legal_intelligence_report": self.analysis_results,
            "entities": {
                entity_type: [
                    {
                        "name": entity.name,
                        "aliases": entity.aliases,
                        "confidence": entity.confidence,
                        "source_count": len(entity.source_entries),
                        "metadata": entity.metadata
                    }
                    for entity in entity_list
                ]
                for entity_type, entity_list in self.extracted_entities.items()
            },
            "timeline": [
                {
                    "date": event.date.isoformat(),
                    "description": event.description[:200],  # Truncate for export
                    "event_type": event.event_type,
                    "significance": event.significance,
                    "participant_count": len(event.participants)
                }
                for event in self.case_timeline
            ],
            "patterns": [
                {
                    "type": pattern.pattern_type,
                    "description": pattern.description,
                    "frequency": pattern.frequency,
                    "confidence": pattern.confidence,
                    "legal_significance": pattern.legal_significance,
                    "example_count": len(pattern.examples)
                }
                for pattern in self.identified_patterns
            ],
            "export_metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "case_number": self.case_number,
                "analyzer_version": "1.0.0"
            }
        }
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Legal intelligence report exported to {output_path}")


__all__ = ["LegalIntelligenceAnalyzer", "CaseEntity", "CaseEvent", "LegalPattern"]
