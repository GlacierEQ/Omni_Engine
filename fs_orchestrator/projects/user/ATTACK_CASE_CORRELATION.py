#!/usr/bin/env python3
"""
Attack → Case Outcome Correlation Engine
Case 1FDV-23-0001009
"""
import json
from datetime import datetime, timedelta
from collections import defaultdict

class AttackCorrelation:
    def __init__(self):
        self.attacks = []
        self.rulings = []
        self.correlations = []
    
    def add_attack(self, timestamp, ip, credential, action):
        self.attacks.append({
            'timestamp': timestamp,
            'ip': ip,
            'credential': credential,
            'action': action
        })
    
    def add_ruling(self, timestamp, judge, decision, case_id):
        self.rulings.append({
            'timestamp': timestamp,
            'judge': judge,
            'decision': decision,
            'case_id': case_id
        })
    
    def find_correlations(self, window_hours=48):
        correlations = []
        for attack in self.attacks:
            attack_time = datetime.fromisoformat(attack['timestamp'])
            for ruling in self.rulings:
                ruling_time = datetime.fromisoformat(ruling['timestamp'])
                time_diff = abs((attack_time - ruling_time).total_seconds()) / 3600
                
                if time_diff <= window_hours:
                    correlations.append({
                        'attack': attack,
                        'ruling': ruling,
                        'time_diff_hours': time_diff,
                        'correlation_score': self.calculate_score(attack, ruling)
                    })
        return sorted(correlations, key=lambda x: x['correlation_score'], reverse=True)
    
    def calculate_score(self, attack, ruling):
        score = 0
        if 'evidence' in attack['action'].lower() or 'notion' in attack['credential'].lower():
            score += 3
        if ruling['judge'] in ['JUDGE_X', 'JUDGE_Y']:  # Known biased judges
            score += 2
        if 'denied' in ruling['decision'].lower() or 'dismissed' in ruling['decision'].lower():
            score += 2
        return score

# Demo usage
correlator = AttackCorrelation()
correlator.add_attack('2025-11-20T14:30:00', '203.0.113.1', 'notion', 'evidence_access_attempt')
correlator.add_ruling('2025-11-21T09:15:00', 'JUDGE_X', 'motion_denied', '1FDV-23-0001009')

print("CORRELATIONS:", correlator.find_correlations())
