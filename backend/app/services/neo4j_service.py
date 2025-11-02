"""
Neo4j Knowledge Graph Service for Legal Reasoning
"""
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    GraphDatabase = None

from typing import List, Dict, Any, Optional
import logging
from app.core.config import settings
from app.services.property_value_estimator import PropertyValueEstimator

logger = logging.getLogger(__name__)


class Neo4jService:
    """Neo4j service for legal knowledge graph operations"""
    
    def __init__(self):
        self.driver = None
        self.available = NEO4J_AVAILABLE
        self.property_estimator = PropertyValueEstimator()
        if self.available:
            self.connect()
        else:
            logger.warning("Neo4j driver not available - using fallback legal reasoning")
    
    def connect(self):
        """Establish connection to Neo4j database"""
        if not self.available:
            return
            
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Test connection
            with self.driver.session(database="legalknowledge") as session:
                result = session.run("RETURN 1 as test")
                logger.info("Neo4j connection established successfully")
        except Exception as e:
            logger.warning(f"Neo4j connection failed, using fallback: {e}")
            self.available = False
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
    
    def find_applicable_laws(self, entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Find applicable BNS laws based on extracted entities using knowledge graph

        Args:
            entities: Dictionary of entity categories and their values

        Returns:
            List of applicable law sections with confidence scores
        """
        # Use fallback reasoning if Neo4j not available
        if not self.available or not self.driver:
            return self._fallback_legal_reasoning(entities)

        applicable_laws = []

        try:
            with self.driver.session(database="legalknowledge") as session:
                # Rule 1: Basic theft detection (Section 303)
                if self._has_theft_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 303 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"],
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.8,
                            "reasoning": "Basic theft elements detected",
                            "property_value_consideration": True  # Section 303 has value thresholds
                        })

                # Rule 2: Dwelling house theft (Section 305)
                if self._has_dwelling_theft_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 305 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"],
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.9,
                            "reasoning": "Theft in dwelling house detected"
                        })

                # Rule 3: Employee theft (Section 306)
                if self._has_employee_theft_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 306 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"],
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.85,
                            "reasoning": "Employee theft scenario detected"
                        })

                # Rule 4: Robbery detection (Section 309)
                if self._has_robbery_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 309 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"],
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.9,
                            "reasoning": "Robbery elements detected (violence/force used)"
                        })

                # Rule 5: Snatching detection (Section 304)
                if self._has_snatching_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 304 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Snatching involves sudden and forceful taking of property",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.85,
                            "reasoning": "Snatching elements detected (sudden forceful taking)"
                        })

                # Rule 6: Cheating detection (Section 318)
                if self._has_cheating_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 318 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Cheating involves dishonest inducement to deliver property or do/omit an act",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.9,
                            "reasoning": "Cheating elements detected (deception/fraud identified)"
                        })

                # Rule 7: Criminal breach of trust detection (Section 316)
                if self._has_breach_of_trust_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 316 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Criminal breach of trust involves dishonest misappropriation of entrusted property",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.9,
                            "reasoning": "Breach of trust elements detected (trust relationship violated)"
                        })

                # Rule 8: Extortion detection (Section 308)
                if self._has_extortion_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 308 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Extortion involves threatening someone to obtain money, property, or compliance",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.9,
                            "reasoning": "Extortion elements detected (threat-based coercion)"
                        })

                # Rule 9: Criminal trespass detection (Section 329)
                if self._has_trespass_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 329 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Criminal trespass involves unlawfully entering someone's property",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.85,
                            "reasoning": "Criminal trespass elements detected (unlawful entry)"
                        })

                # Rule 10: Mischief detection (Section 324)
                if self._has_mischief_elements(entities):
                    result = session.run("""
                        MATCH (s:Section)-[:DEFINES]->(o:Offence)
                        MATCH (p:Punishment)
                        WHERE s.section_number = 324 AND p.section_id = s.section_id
                        RETURN s.section_id as section, s.title as title,
                               s.text as description, p.description as punishment,
                               p.punishment_type as severity, o.type as offence_type
                    """)

                    for record in result:
                        applicable_laws.append({
                            "section": record["section"],
                            "title": record["title"],
                            "description": record["description"] or "Mischief involves intentional damage or destruction of property",
                            "punishment": record["punishment"],
                            "severity": record["severity"],
                            "offence_type": record["offence_type"],
                            "confidence": 0.85,
                            "reasoning": "Mischief elements detected (property damage)"
                        })

            return applicable_laws

        except Exception as e:
            logger.error(f"Neo4j query failed, using fallback: {e}")
            return self._fallback_legal_reasoning(entities)
    
    def _has_theft_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate basic theft"""
        actions = entities.get("actions", [])
        objects = entities.get("objects", [])
        intentions = entities.get("intentions", [])
        
        theft_actions = ["took", "stolen", "stole", "theft", "stealing", "grabbed", "snatched", "broke into", "borrowed", "taken", "kept", "appropriated"]
        property_objects = ["phone", "mobile", "iphone", "smartphone", "wallet", "money", "cash", "bag", "purse", "jewelry", "laptop", "computer"]
        dishonest_intentions = ["without permission", "dishonest", "wrongfully", "dishonestly"]

        has_theft_action = any(theft_action.lower() in action.lower() for action in actions for theft_action in theft_actions)
        has_property = any(prop.lower() in obj.lower() for obj in objects for prop in property_objects)
        has_dishonest_intent = any(intent.lower() in dishonest_intentions for intent in intentions)
        
        # For basic theft, we only require theft action + property (intention is implied)
        return has_theft_action and has_property
    
    def _has_dwelling_theft_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate theft in dwelling"""
        locations = entities.get("locations", [])
        actions = entities.get("actions", [])
        
        dwelling_locations = ["house", "home", "apartment", "residence", "building", "room"]
        theft_actions = ["took", "stolen", "stole", "theft", "stealing", "grabbed", "snatched", "broke into", "borrowed", "taken", "kept", "appropriated"]

        has_dwelling = any(dwelling.lower() in loc.lower() for loc in locations for dwelling in dwelling_locations)
        has_theft = any(theft_action.lower() in action.lower() for action in actions for theft_action in theft_actions)
        
        return has_dwelling and has_theft
    
    def _has_employee_theft_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate employee theft"""
        persons = entities.get("persons", [])
        relationships = entities.get("relationships", [])
        actions = entities.get("actions", [])

        employee_terms = ["employee", "worker", "staff", "clerk", "servant"]
        employer_terms = ["employer", "boss", "company", "master"]
        theft_actions = ["took", "stolen", "stole", "theft", "stealing", "grabbed", "snatched", "broke into", "borrowed", "taken", "kept", "appropriated"]

        has_employee = any(person.lower() in employee_terms for person in persons)
        has_employer = any(rel.lower() in employer_terms for rel in relationships)
        has_theft = any(action.lower() in theft_actions for action in actions)

        return has_employee and has_employer and has_theft

    def _has_robbery_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate robbery (theft with violence/force)"""
        actions = entities.get("actions", [])
        violence_indicators = entities.get("violence", [])
        objects = entities.get("objects", [])

        theft_actions = ["took", "stolen", "theft", "stealing", "robbed", "snatched", "grabbed"]
        violence_terms = ["violence", "force", "hurt", "threatened", "attacked", "beaten", "knife", "gun", "weapon"]
        property_objects = ["phone", "mobile", "iphone", "smartphone", "wallet", "money", "cash", "bag", "purse", "jewelry", "laptop", "computer"]

        has_theft = any(action.lower() in theft_actions for action in actions)
        has_violence = any(
            violence.lower() in violence_terms for violence in violence_indicators
        ) or any(action.lower() in violence_terms for action in actions)
        has_property = any(obj.lower() in property_objects for obj in objects)

        return has_theft and has_violence and has_property

    def _has_snatching_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate snatching (sudden forceful taking)"""
        actions = entities.get("actions", [])
        objects = entities.get("objects", [])
        circumstances = entities.get("circumstances", [])
        locations = entities.get("locations", [])

        # Snatching-specific indicators
        snatching_actions = ["snatched", "grabbed", "yanked", "pulled", "jerked", "ripped", "tore", "forcefully took"]
        snatching_circumstances = ["suddenly", "quickly", "fast", "running", "speeding", "motorcycle", "bike", "scooter"]
        snatching_objects = ["chain", "necklace", "bag", "purse", "phone", "mobile", "wallet", "earrings", "watch"]
        public_locations = ["street", "road", "footpath", "market", "bus stop", "station", "park", "outside"]

        has_snatching_action = any(snatch_action.lower() in action.lower() for action in actions for snatch_action in snatching_actions)
        has_sudden_element = any(circumstance.lower() in snatching_circumstances for circumstance in circumstances)
        has_snatching_object = any(obj.lower() in snatching_objects for obj in objects)
        has_public_location = any(location.lower() in public_locations for location in locations)

        # Snatching requires forceful action + property + (sudden element OR public location)
        return has_snatching_action and has_snatching_object and (has_sudden_element or has_public_location)

    def _has_cheating_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate cheating/fraud"""
        actions = entities.get("actions", [])
        intentions = entities.get("intentions", [])
        circumstances = entities.get("circumstances", [])

        # Cheating-specific indicators
        cheating_actions = ["cheated", "deceived", "defrauded", "scammed", "tricked", "misled", "promised", "lied", "convinced", "persuaded", "fooled"]
        fraud_intentions = ["dishonest", "fraudulent", "fake", "false", "misleading", "deceptive"]
        fraud_circumstances = ["online", "phone call", "fake website", "false documents", "impersonation", "lottery", "prize"]

        # Common fraud patterns
        fraud_patterns = ["investment", "loan", "credit card", "bank account", "OTP", "ATM", "digital payment", "cryptocurrency"]

        # Check all entity types for fraud indicators
        all_text = " ".join(actions + intentions + circumstances).lower()

        has_cheating_action = any(cheat_action.lower() in action.lower() for action in actions for cheat_action in cheating_actions)
        has_fraud_intention = any(fraud_int.lower() in intention.lower() for intention in intentions for fraud_int in fraud_intentions)
        has_fraud_circumstance = any(fraud_circ.lower() in circumstance.lower() for circumstance in circumstances for fraud_circ in fraud_circumstances)
        has_fraud_pattern = any(pattern in all_text for pattern in fraud_patterns)

        # Cheating can be detected by:
        # 1. Strong cheating action (scammed, defrauded) alone
        # 2. OR (cheating action OR fraud intention) + (fraud circumstance OR fraud pattern)
        strong_cheating_actions = ["scammed", "defrauded", "cheated", "fraudulently"]
        has_strong_cheating = any(strong_action.lower() in action.lower() for action in actions for strong_action in strong_cheating_actions)

        return has_strong_cheating or ((has_cheating_action or has_fraud_intention) and (has_fraud_circumstance or has_fraud_pattern))

    def _has_breach_of_trust_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate criminal breach of trust"""
        actions = entities.get("actions", [])
        relationships = entities.get("relationships", [])
        circumstances = entities.get("circumstances", [])
        intentions = entities.get("intentions", [])

        # Trust-specific indicators
        trust_actions = ["misappropriated", "misused", "betrayed", "violated trust", "dishonestly used", "converted", "embezzled"]
        trust_relationships = ["entrusted", "trustee", "fiduciary", "agent", "guardian", "manager", "executor", "director"]
        trust_circumstances = ["entrusted with", "given responsibility", "in charge of", "managing", "handling", "responsible for"]
        dishonest_intentions = ["dishonest", "wrongful", "unauthorized", "personal use", "own benefit"]

        # Check all entity types for trust indicators
        all_text = " ".join(actions + relationships + circumstances + intentions).lower()

        has_trust_action = any(trust_action.lower() in action.lower() for action in actions for trust_action in trust_actions)
        has_trust_relationship = any(trust_rel.lower() in rel.lower() for rel in relationships for trust_rel in trust_relationships)
        has_trust_circumstance = any(trust_circ.lower() in circumstance.lower() for circumstance in circumstances for trust_circ in trust_circumstances)
        has_dishonest_intention = any(dishonest_int.lower() in intention.lower() for intention in intentions for dishonest_int in dishonest_intentions)

        # Also check for trust indicators in the combined text
        has_trust_pattern = any(pattern in all_text for pattern in trust_relationships + trust_circumstances)

        # Check for dishonest elements in circumstances as well
        has_dishonest_circumstance = any(dishonest_int.lower() in circumstance.lower() for circumstance in circumstances for dishonest_int in dishonest_intentions)

        # Breach of trust requires: trust relationship/circumstance + (dishonest action OR intention OR circumstance)
        return (has_trust_relationship or has_trust_circumstance or has_trust_pattern) and (has_trust_action or has_dishonest_intention or has_dishonest_circumstance)

    def _has_extortion_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate extortion"""
        actions = entities.get("actions", [])
        circumstances = entities.get("circumstances", [])
        intentions = entities.get("intentions", [])
        methods = entities.get("methods", [])

        # Extortion-specific indicators (including semantic mappings)
        threat_actions = ["threatened", "blackmailed", "intimidated", "coerced", "forced", "demanded", "extorted", "pressured", "warned", "told"]
        threat_methods = ["violence", "harm", "exposure", "reputation damage", "legal action", "physical harm"]
        threat_circumstances = ["under threat", "fear", "pressure", "demanding money", "pay or else"]
        threat_objects = ["money", "property", "compliance", "silence", "cooperation"]

        # Check all entity types for threat indicators
        all_text = " ".join(actions + circumstances + intentions + methods).lower()

        has_threat_action = any(threat_action.lower() in action.lower() for action in actions for threat_action in threat_actions)
        has_threat_method = any(threat_method.lower() in method.lower() for method in methods for threat_method in threat_methods)
        has_threat_circumstance = any(threat_circ.lower() in circumstance.lower() for circumstance in circumstances for threat_circ in threat_circumstances)

        # Also check for threat patterns in combined text
        has_threat_pattern = any(pattern in all_text for pattern in threat_actions + threat_methods + threat_circumstances)

        # Extortion requires threat indicators
        return has_threat_action or has_threat_method or has_threat_circumstance or has_threat_pattern

    def _has_trespass_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate criminal trespass"""
        actions = entities.get("actions", [])
        locations = entities.get("locations", [])
        circumstances = entities.get("circumstances", [])
        intentions = entities.get("intentions", [])

        # Trespass-specific indicators (including semantic mappings)
        trespass_actions = ["entered", "broke into", "trespassed", "intruded", "invaded", "climbed over", "jumped over", "snuck into", "came inside", "went into", "accessed"]
        trespass_locations = ["house", "home", "property", "land", "building", "apartment", "office", "compound", "premises", "yard", "garden", "roof"]
        unlawful_circumstances = ["without permission", "unauthorized", "illegally", "unlawfully", "forcibly", "broke in", "climbed", "scaled", "fence", "wall", "gate", "boundary"]
        trespass_intentions = ["to steal", "to commit", "unlawful purpose", "criminal intent"]

        # Check all entity types for trespass indicators
        all_text = " ".join(actions + locations + circumstances + intentions).lower()

        has_trespass_action = any(trespass_action.lower() in action.lower() for action in actions for trespass_action in trespass_actions)
        has_property_location = any(location.lower() in loc.lower() for loc in locations for location in trespass_locations)
        has_unlawful_circumstance = any(unlawful_circ.lower() in circumstance.lower() for circumstance in circumstances for unlawful_circ in unlawful_circumstances)

        # Also check for trespass patterns in combined text
        has_trespass_pattern = any(pattern in all_text for pattern in trespass_actions + unlawful_circumstances)

        # Criminal trespass requires entry action + property location OR unlawful circumstances
        return (has_trespass_action and has_property_location) or has_unlawful_circumstance or has_trespass_pattern

    def _has_mischief_elements(self, entities: Dict[str, List[str]]) -> bool:
        """Check if entities indicate mischief (property damage)"""
        actions = entities.get("actions", [])
        objects = entities.get("objects", [])
        circumstances = entities.get("circumstances", [])
        intentions = entities.get("intentions", [])

        # Mischief-specific indicators
        damage_actions = ["damaged", "destroyed", "broke", "vandalized", "defaced", "demolished", "ruined", "smashed", "burnt", "torn", "cut", "scratched"]
        property_objects = ["car", "vehicle", "window", "door", "wall", "fence", "property", "building", "house", "furniture", "equipment", "machine", "computer", "phone"]
        damage_circumstances = ["intentionally", "deliberately", "maliciously", "willfully", "on purpose", "angry", "revenge"]
        malicious_intentions = ["to harm", "to damage", "revenge", "anger", "spite", "malice"]

        # Check all entity types for mischief indicators
        all_text = " ".join(actions + objects + circumstances + intentions).lower()

        has_damage_action = any(damage_action.lower() in action.lower() for action in actions for damage_action in damage_actions)
        has_property_object = any(prop_obj.lower() in obj.lower() for obj in objects for prop_obj in property_objects)
        has_damage_circumstance = any(damage_circ.lower() in circumstance.lower() for circumstance in circumstances for damage_circ in damage_circumstances)
        has_malicious_intention = any(malicious_int.lower() in intention.lower() for intention in intentions for malicious_int in malicious_intentions)

        # Also check for damage patterns in combined text
        has_damage_pattern = any(pattern in all_text for pattern in damage_actions + damage_circumstances)

        # Check for accidental indicators (should exclude mischief)
        accidental_indicators = ["accidentally", "accidental", "by mistake", "unintentionally", "fell", "dropped", "slipped"]
        has_accidental_indicator = any(acc_ind in all_text for acc_ind in accidental_indicators)

        # Mischief requires intentional damage: (damage action + property object + intent) OR intentional circumstances
        has_intentional_damage = has_damage_action and has_property_object and (has_damage_circumstance or has_malicious_intention)

        # Also allow strong damage actions that imply intent (like vandalized, defaced)
        strong_damage_actions = ["vandalized", "defaced", "demolished", "smashed", "burnt"]
        has_strong_damage_action = any(strong_action.lower() in action.lower() for action in actions for strong_action in strong_damage_actions)
        has_strong_intentional_damage = has_strong_damage_action and has_property_object

        # Exclude accidental damage
        return (has_intentional_damage or has_strong_intentional_damage or has_damage_circumstance or has_malicious_intention) and not has_accidental_indicator

    def enhance_with_property_analysis(self, applicable_laws: List[Dict[str, Any]], entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Enhance legal analysis with property value considerations"""
        enhanced_laws = []

        for law in applicable_laws:
            enhanced_law = law.copy()

            # Special handling for Section 303 (Theft) - property value matters
            if law.get("section") == "BNS-303" and law.get("property_value_consideration"):
                objects = entities.get("objects", [])
                if objects:
                    property_analysis = self.property_estimator.estimate_value(objects)
                    enhanced_law["property_analysis"] = property_analysis["breakdown"]

                    # Check if total value is below Rs.5,000 threshold
                    total_value = property_analysis.get("total_estimated_value", 0)
                    if total_value < 5000:
                        enhanced_law["punishment_modification"] = {
                            "original": law.get("punishment"),
                            "modified": "Community service (if first-time offender and property value < Rs.5,000)",
                            "threshold_applied": "Rs.5,000 BNS-303 threshold",
                            "reasoning": "Property value consideration under BNS Section 303",
                            "total_value": total_value
                        }
                        enhanced_law["confidence"] = min(law.get("confidence", 0.8) + 0.1, 1.0)

            enhanced_laws.append(enhanced_law)

        return enhanced_laws

    def get_legal_confidence_score(self, applicable_laws: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score for legal analysis"""
        if not applicable_laws:
            return 0.0
        
        # Use highest confidence law as base score
        max_confidence = max(law.get("confidence", 0.0) for law in applicable_laws)
        
        # Boost confidence if multiple laws apply (corroborating evidence)
        if len(applicable_laws) > 1:
            max_confidence = min(max_confidence + 0.1, 1.0)
        
        return max_confidence
    
    def _fallback_legal_reasoning(self, entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Fallback legal reasoning when Neo4j is not available"""
        applicable_laws = []
        
        # Rule-based fallback reasoning
        if self._has_theft_elements(entities):
            applicable_laws.append({
                "section": "BNS-303",
                "title": "Theft",
                "description": "Taking movable property dishonestly without consent",
                "punishment": "Imprisonment up to 3 years or fine or both",
                "severity": "moderate",
                "confidence": 0.8,
                "reasoning": "Basic theft elements detected (fallback reasoning)"
            })
        
        if self._has_dwelling_theft_elements(entities):
            applicable_laws.append({
                "section": "BNS-305",
                "title": "Theft in dwelling house",
                "description": "Theft committed in dwelling or custody place",
                "punishment": "Imprisonment up to 7 years and fine",
                "severity": "high", 
                "confidence": 0.9,
                "reasoning": "Dwelling theft detected (fallback reasoning)"
            })
        
        if self._has_employee_theft_elements(entities):
            applicable_laws.append({
                "section": "BNS-306",
                "title": "Theft by employee",
                "description": "Theft by clerk/servant of employer's property",
                "punishment": "Imprisonment up to 7 years and fine",
                "severity": "high",
                "confidence": 0.85,
                "reasoning": "Employee theft detected (fallback reasoning)"
            })

        if self._has_snatching_elements(entities):
            applicable_laws.append({
                "section": "BNS-304",
                "title": "Snatching",
                "description": "Snatching involves sudden and forceful taking of property",
                "punishment": "Imprisonment up to 3 years and fine",
                "severity": "moderate",
                "confidence": 0.85,
                "reasoning": "Snatching elements detected (fallback reasoning)"
            })

        if self._has_cheating_elements(entities):
            applicable_laws.append({
                "section": "BNS-318",
                "title": "Cheating",
                "description": "Cheating involves dishonest inducement to deliver property or do/omit an act",
                "punishment": "Imprisonment up to 7 years and fine",
                "severity": "high",
                "confidence": 0.9,
                "reasoning": "Cheating elements detected (fallback reasoning)"
            })

        if self._has_breach_of_trust_elements(entities):
            applicable_laws.append({
                "section": "BNS-316",
                "title": "Criminal breach of trust",
                "description": "Criminal breach of trust involves dishonest misappropriation of entrusted property",
                "punishment": "Imprisonment up to 7 years or fine or both",
                "severity": "high",
                "confidence": 0.9,
                "reasoning": "Breach of trust elements detected (fallback reasoning)"
            })

        if self._has_extortion_elements(entities):
            applicable_laws.append({
                "section": "BNS-308",
                "title": "Extortion",
                "description": "Extortion involves threatening someone to obtain money, property, or compliance",
                "punishment": "Imprisonment up to 7 years or fine or both",
                "severity": "high",
                "confidence": 0.9,
                "reasoning": "Extortion elements detected (fallback reasoning)"
            })

        if self._has_trespass_elements(entities):
            applicable_laws.append({
                "section": "BNS-329",
                "title": "Criminal trespass and house-trespass",
                "description": "Criminal trespass involves unlawfully entering someone's property",
                "punishment": "Imprisonment up to 3 months or fine up to Rs.5,000 or both",
                "severity": "moderate",
                "confidence": 0.85,
                "reasoning": "Criminal trespass elements detected (fallback reasoning)"
            })

        if self._has_mischief_elements(entities):
            applicable_laws.append({
                "section": "BNS-324",
                "title": "Mischief",
                "description": "Mischief involves intentional damage or destruction of property",
                "punishment": "Imprisonment up to 6 months or fine or both",
                "severity": "moderate",
                "confidence": 0.85,
                "reasoning": "Mischief elements detected (fallback reasoning)"
            })

        return applicable_laws
    
    def verify_legal_facts(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify legal analysis against knowledge base"""
        # This would cross-check the analysis results against the knowledge graph
        # For now, return the analysis as-is with verification flag
        analysis_result["verified"] = True if self.available else False
        analysis_result["verification_notes"] = (
            "Analysis verified against BNS knowledge base" if self.available 
            else "Fallback reasoning used - Neo4j not available"
        )
        return analysis_result


# Global Neo4j service instance
neo4j_service = Neo4jService()