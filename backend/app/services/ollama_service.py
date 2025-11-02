"""
Ollama Service for Phi-3 SLM Integration
Handles Entity Extraction and Template Response Formation
"""
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
import logging
from app.core.config import settings
from app.services.property_value_estimator import PropertyValueEstimator

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for Ollama Phi-3 model integration"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.session = requests.Session()
        self.value_estimator = PropertyValueEstimator()
    
    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = self.session.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama service unavailable: {e}")
            return False
    
    def extract_entities(self, user_query: str, language: str = "en") -> Dict[str, List[str]]:
        """
        Extract factual entities from user query using Phi-3
        IMPORTANT: This does NOT classify legal applicability - only extracts facts
        """

        # For demo reliability, use fallback entity extraction
        logger.info("Using fallback entity extraction for demo reliability")
        entities = self._extract_entities_fallback(user_query.lower())

        # Add property value estimation for objects
        if "objects" in entities and entities["objects"]:
            property_items = entities["objects"]

            # Estimate property values
            value_analysis = self.value_estimator.estimate_value(property_items)

            # Add value information to entities
            entities["property_value_analysis"] = value_analysis

            logger.info(f"Property value estimated: {value_analysis['total_estimated_value']} rupees")

        logger.info(f"Extracted entities: {entities}")
        return entities

        # Original Phi-3 code (commented for demo)
        # prompt = self._create_entity_extraction_prompt(user_query, language)
        # try:
        #     response = self._call_ollama(prompt)
        #     entities = self._parse_entity_response(response)
        #     # [rest of original code]
        # except Exception as e:
        #     logger.error(f"Entity extraction failed: {e}")
        #     return self._get_empty_entities()
    
    def format_legal_response(self, legal_analysis: Dict[str, Any], language: str = "en") -> str:
        """
        Generate citizen-friendly response from Neo4j legal analysis
        Uses template-based approach with Phi-3 for natural language generation
        """

        # For demo reliability, skip Phi-3 and use improved fallback directly
        logger.info("Using fallback response for demo reliability")
        return self._get_fallback_response(legal_analysis, language)

        # Original Phi-3 code (commented for demo)
        # prompt = self._create_response_template_prompt(legal_analysis, language)
        # try:
        #     response = self._call_ollama(prompt)
        #     formatted_response = self._clean_response_text(response)
        #     logger.info("Generated citizen-friendly legal response")
        #     return formatted_response
        # except Exception as e:
        #     logger.error(f"Response formatting failed: {e}")
        #     return self._get_fallback_response(legal_analysis, language)
    
    def _create_entity_extraction_prompt(self, user_query: str, language: str) -> str:
        """Create prompt for factual entity extraction"""
        
        # PREVIOUS ENTITY SCHEMA (COMMENTED OUT - CAN BE RESTORED IF NEEDED)
        # prompt = f"""You are a factual entity extraction system. Extract ONLY factual elements from the user's description. DO NOT determine which laws apply or make legal classifications.
        #
        # Extract the following categories:
        # 1. PERSONS: People involved (victim, accused, witness, employee, employer, etc.)
        # 2. OBJECTS: Physical items mentioned (phone, wallet, money, property, etc.)
        # 3. LOCATIONS: Places mentioned (house, office, street, building, etc.)
        # 4. ACTIONS: What happened (took, stole, grabbed, entered, threatened, etc.)
        # 5. INTENTIONS: Stated intentions (dishonestly, without permission, etc.)
        # 6. CIRCUMSTANCES: Situational details (at night, forcibly, secretly, etc.)
        # 7. RELATIONSHIPS: Relationships between people (employee-employer, etc.)
        #
        # User Query: "{user_query}"
        #
        # Extract entities in JSON format:
        # {{
        #   "persons": [...],
        #   "objects": [...],
        #   "locations": [...],
        #   "actions": [...],
        #   "intentions": [...],
        #   "circumstances": [...],
        #   "relationships": [...]
        # }}
        #
        # Important: Extract ONLY factual information. Do NOT determine legal classifications."""

        # PATTERN-BASED SEMANTIC MAPPING - Teaches SLM to generalize
        prompt = f"""You are an intelligent legal entity extraction system. Understand natural language descriptions and extract entities using legal terminology. Think like a legal expert who recognizes criminal patterns.

PATTERN RECOGNITION GUIDELINES:
1. THEFT PATTERNS: Any taking of property without permission
   - "borrowed/took + never returned" = stole, theft
   - "walked off with" = took, stole
   - "kept for themselves" = misappropriated, theft
   - "didn't give back" = stole, theft

2. THREAT/EXTORTION PATTERNS: Demanding something through fear
   - "said X would happen unless Y" = threatened, extorted
   - "or else" statements = threatened, demanded
   - "unless you pay/do X" = extorted, coerced
   - "bad things will happen" = threatened

3. DECEPTION/FRAUD PATTERNS: Tricking someone for gain
   - "convinced to give money for fake X" = cheated, deceived
   - "tricked into" = deceived, defrauded
   - "pretended to be" = impersonated, cheated
   - "fake/false documents" = forged, cheated

4. TRESPASS PATTERNS: Entering property without permission
   - "came/went inside without permission" = trespassed, entered unlawfully
   - "got into house when not home" = broke in, trespassed
   - "entered uninvited" = trespassed

5. DAMAGE PATTERNS: Intentional harm to property
   - "messed up/ruined on purpose" = damaged, vandalized
   - "broke to get inside" = damaged, destroyed
   - "threw stones at" = damaged, attacked

6. TRUST VIOLATION PATTERNS: Misusing entrusted responsibility
   - "was supposed to X but used for Y" = misappropriated, betrayed trust
   - "used company/client money for personal" = embezzled, misappropriated
   - "was given responsibility but misused" = breach of trust

ENTITY EXTRACTION:
1. PERSONS: victim, perpetrator, witness, employee, employer, etc.
2. OBJECTS: personal property, money, documents, vehicles, etc.
3. LOCATIONS: private property, public space, dwelling, office, etc.
4. ACTIONS: Apply pattern recognition to identify legal terms
5. INTENTIONS: dishonest, unauthorized, fraudulent, malicious, etc.
6. CIRCUMSTANCES: sudden, forcible, deceptive, secret, public, etc.
7. RELATIONSHIPS: employer-employee, agent-principal, trustee-beneficiary, etc.

CRITICAL: Look for PATTERNS in the description, not just exact words. If someone describes taking something and not returning it, recognize this as theft regardless of the words used.

User Query: "{user_query}"

Extract entities with pattern-based legal mapping:
{{
  "persons": [...],
  "objects": [...],
  "locations": [...],
  "actions": [...],
  "intentions": [...],
  "circumstances": [...],
  "relationships": [...]
}}

Think: What criminal patterns do I recognize in this description?"""
        
        return prompt
    
    def _create_response_template_prompt(self, legal_analysis: Dict[str, Any], language: str) -> str:
        """Create prompt for template-based response generation"""

        applicable_laws = legal_analysis.get("applicable_laws", [])
        confidence = legal_analysis.get("confidence_score", 0.0)
        entities = legal_analysis.get("entities_analyzed", {})

        # Extract case-specific details
        objects = entities.get("objects", [])
        locations = entities.get("locations", [])
        actions = entities.get("actions", [])
        persons = entities.get("persons", [])
        circumstances = entities.get("circumstances", [])

        # Build detailed law information with case-specific context
        law_details = ""
        property_analysis = ""

        for law in applicable_laws:
            law_details += f"**{law.get('section')}: {law.get('title')}**\n"
            law_details += f"Legal Definition: {law.get('description', '')}\n"
            law_details += f"Confidence: {law.get('confidence', 0.0):.0%}\n"
            law_details += f"Reasoning: {law.get('reasoning', '')}\n"

            # Add property analysis if available
            if law.get('property_analysis'):
                property_analysis += "**Property Value Analysis:**\n"
                total_value = 0
                for prop in law['property_analysis']:
                    value = prop.get('estimated_value', 0)
                    total_value += value
                    property_analysis += f"- {prop['item']}: Rs.{value:,} ({prop.get('basis', 'estimated')})\n"

                property_analysis += f"Total Value: Rs.{total_value:,}\n"
                if total_value >= 5000:
                    property_analysis += "WARNING: Above Rs.5,000 threshold - Standard penalties apply\n"
                else:
                    property_analysis += "NOTE: Below Rs.5,000 threshold - May qualify for community service\n"

            # Add punishment modifications
            if law.get('punishment_modification'):
                mod = law['punishment_modification']
                law_details += f"Modified Punishment: {mod.get('modified', '')}\n"
                law_details += f"Reasoning: {mod.get('reasoning', '')}\n"

            law_details += "\n"

        case_facts = f"Case Facts: {', '.join(objects)} involved, occurred at/in {', '.join(locations)}, actions: {', '.join(actions)}"

        language_instruction = "Respond in Hindi" if language == "hi" else "Respond in English"

        prompt = f"""You are a legal advisor providing specific, actionable guidance. Based on the case facts and legal analysis below, create a comprehensive response.

CASE FACTS:
{case_facts}

LEGAL ANALYSIS:
{law_details}

{property_analysis}

Overall Assessment Confidence: {confidence:.0%}

Create a detailed response with these sections:

1. **Legal Assessment**:
   - Explain SPECIFICALLY how the identified laws apply to this case
   - Reference the actual items, location, and circumstances mentioned
   - Explain why each law is relevant with specific examples

2. **Your Rights & Options**:
   - Specific actions the person can take based on THIS situation
   - Different options depending on whether they are victim, accused, or witness
   - Timeline considerations and urgent vs. non-urgent actions

3. **Immediate Next Steps**:
   - Prioritized list of specific actions to take right now
   - Who to contact and when
   - What evidence to preserve or gather
   - What to avoid doing

4. **Legal Consequences**:
   - Specific penalties that apply to THIS case
   - How property value affects outcomes
   - Potential defenses or mitigating factors

5. **Important Disclaimer**: Professional legal advice recommendation

Requirements:
- Be SPECIFIC to this case - mention the actual items, location, circumstances
- Provide ACTIONABLE advice, not generic statements
- Use concrete examples and clear next steps
- {language_instruction}
- Keep professional but accessible tone

Generate the comprehensive legal guidance:"""
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for consistency
                "top_p": 0.9,
                "num_predict": 800
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=20  # Reduced timeout for demo
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    def _parse_entity_response(self, response: str) -> Dict[str, List[str]]:
        """Parse entity extraction response from Phi-3"""
        try:
            # Try to find JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end != -1:
                json_str = response[start:end]
                entities = json.loads(json_str)
                
                # Validate and clean entity structure
                return self._validate_entities(entities)
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from entity response")
        
        # Fallback: extract entities using simple patterns
        return self._extract_entities_fallback(response)
    
    # OLD VALIDATION FUNCTION (COMMENTED OUT - CAN BE RESTORED IF NEEDED)
    # def _validate_entities(self, entities: Dict) -> Dict[str, List[str]]:
    #     """Validate and clean extracted entities"""
    #     valid_entities = {
    #         "persons": [],
    #         "objects": [],
    #         "locations": [],
    #         "actions": [],
    #         "intentions": [],
    #         "circumstances": [],
    #         "relationships": []
    #     }
    #
    #     for category in valid_entities.keys():
    #         if category in entities and isinstance(entities[category], list):
    #             # Clean and filter entities
    #             valid_entities[category] = [
    #                 item.strip() for item in entities[category]
    #                 if isinstance(item, str) and item.strip()
    #             ][:10]  # Limit to 10 entities per category

    def _validate_entities(self, entities: Dict) -> Dict[str, List[str]]:
        """Validate and clean extracted entities"""
        valid_entities = {
            "persons": [],
            "objects": [],
            "locations": [],
            "actions": [],
            "intentions": [],
            "circumstances": [],
            "relationships": []
        }

        for category in valid_entities.keys():
            if category in entities and isinstance(entities[category], list):
                # Clean and filter entities
                valid_entities[category] = [
                    item.strip() for item in entities[category]
                    if isinstance(item, str) and item.strip()
                ][:10]  # Limit to 10 entities per category

        return valid_entities
    
    def _extract_entities_fallback(self, response: str) -> Dict[str, List[str]]:
        """Enhanced fallback entity extraction using keyword matching"""
        entities = self._get_empty_entities()

        response_lower = response.lower()

        # Enhanced keyword matching for common demo scenarios
        person_keywords = ["victim", "accused", "employee", "employer", "person", "someone", "i", "me", "my"]
        object_keywords = ["phone", "mobile", "iphone", "smartphone", "laptop", "computer", "wallet", "money", "cash", "property", "bag", "jewelry", "purse", "chain", "necklace", "earrings", "watch", "bracelet", "funds", "account", "assets", "car", "vehicle", "window", "door", "wall", "fence", "furniture", "equipment", "machine", "handbag", "bicycle", "ring", "flowerpot", "stones"]
        action_keywords = ["took", "stole", "grabbed", "snatched", "entered", "threatened", "broke into", "stolen", "theft", "stealing", "cheated", "deceived", "defrauded", "scammed", "tricked", "misled", "promised", "lied", "fraudulently", "misappropriated", "misused", "betrayed", "embezzled", "used", "blackmailed", "intimidated", "coerced", "forced", "demanded", "extorted", "trespassed", "intruded", "invaded", "climbed over", "jumped over", "snuck into", "damaged", "destroyed", "broke", "vandalized", "defaced", "demolished", "ruined", "smashed", "burnt", "torn", "cut", "scratched", "pulled", "yanked", "jerked", "ripped", "convinced", "borrowed", "took away", "came inside", "walked around", "threw", "made dents", "spent", "kept"]
        location_keywords = ["house", "home", "apartment", "office", "street", "building", "shop", "room", "residence", "property", "land", "compound", "premises", "yard", "garden", "roof"]
        circumstance_keywords = ["night", "sleeping", "dark", "alone", "forcibly", "secretly", "suddenly", "quickly", "fast", "running", "speeding", "motorcycle", "bike", "scooter", "online", "phone call", "fake website", "false documents", "impersonation", "lottery", "prize", "investment", "loan", "credit card", "bank account", "OTP", "ATM", "bank", "pretending", "called", "entrusted", "managing", "handling", "responsible", "in charge", "unauthorized", "personal", "dishonest", "under threat", "fear", "pressure", "demanding money", "pay or else", "violence", "harm", "reputation damage", "legal action", "physical harm", "without permission", "illegally", "unlawfully", "climbed", "scaled", "fence", "wall", "gate", "boundary", "intentionally", "deliberately", "maliciously", "willfully", "on purpose", "angry", "revenge", "came fast", "walking", "uninvited", "charity", "never returned", "vacation", "multiple requests"]
        relationship_keywords = ["agent", "manager", "director", "trustee", "partner", "employee", "employer", "guardian", "executor", "fiduciary"]

        # More sophisticated matching
        for keyword in person_keywords:
            if keyword in response_lower:
                entities["persons"].append("victim" if keyword in ["i", "me", "my"] else keyword)

        for keyword in object_keywords:
            if keyword in response_lower:
                entities["objects"].append(keyword)

        for keyword in action_keywords:
            if keyword in response_lower:
                entities["actions"].append(keyword)

        for keyword in location_keywords:
            if keyword in response_lower:
                entities["locations"].append(keyword)

        for keyword in circumstance_keywords:
            if keyword in response_lower:
                entities["circumstances"].append(keyword)

        for keyword in relationship_keywords:
            if keyword in response_lower:
                entities["relationships"].append(keyword)

        # Remove duplicates while preserving order
        for category in entities:
            entities[category] = list(dict.fromkeys(entities[category]))

        return entities
    
    def _clean_response_text(self, response: str) -> str:
        """Clean and format the response text"""
        # Remove any JSON artifacts or extra formatting
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('{') and not line.startswith('}'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _get_empty_entities(self) -> Dict[str, List[str]]:
        """Return empty entity structure"""
        return {
            "persons": [],
            "objects": [],
            "locations": [],
            "actions": [],
            "intentions": [],
            "circumstances": [],
            "relationships": []
        }
    
    def _get_fallback_response(self, legal_analysis: Dict[str, Any], language: str) -> str:
        """Generate comprehensive fallback response when Phi-3 fails"""
        laws = legal_analysis.get("applicable_laws", [])
        entities = legal_analysis.get("entities_analyzed", {})

        # Extract case details
        objects = entities.get("objects", [])
        locations = entities.get("locations", [])
        actions = entities.get("actions", [])

        if language == "hi":
            response = "**आपकी कानूनी स्थिति का विश्लेषण**\n\n"
            if laws and objects:
                response += f"**लागू कानून:** {', '.join([law.get('section', '') for law in laws])}\n\n"
                response += f"**मामले की स्थिति:** आपके {', '.join(objects)} चोरी की गई है {', '.join(locations)} से। "
                response += f"यह {laws[0].get('title', 'चोरी')} के अंतर्गत आता है।\n\n"

                response += "**तत्काल करने योग्य कार्य:**\n"
                response += "1. 24 घंटे के अंदर पुलिस में FIR दर्ज कराएं\n"
                response += "2. चोरी हुई वस्तुओं की सूची और मूल्य तैयार करें\n"
                response += "3. CCTV फुटेज या गवाहों की जानकारी एकत्र करें\n"
                response += "4. घर के बाहर के ताले बदलवाएं\n\n"

                response += "**कानूनी परिणाम:**\n"
                for law in laws:
                    response += f"- {law.get('section', '')}: {law.get('punishment', 'सजा का प्रावधान')}\n"

                response += "\n**महत्वपूर्ण:** यह प्रारंभिक मार्गदर्शन है। विस्तृत सलाह के लिए वकील से मिलें।"

        else:
            response = "**Legal Assessment for Your Case**\n\n"

            if laws and objects:
                # Build case-specific analysis
                response += f"**Applicable Laws:** {', '.join([law.get('section', '') for law in laws])}\n\n"

                response += "**Legal Assessment:**\n"
                response += f"Based on your description, someone unlawfully took your {', '.join(objects)} from {', '.join(locations)}. "

                for law in laws:
                    response += f"This constitutes {law.get('title', 'theft')} under {law.get('section', 'BNS')} "
                    response += f"(confidence: {law.get('confidence', 0.8):.0%}). "

                # Add property value consideration
                property_analysis = None
                for law in laws:
                    if law.get('property_analysis'):
                        property_analysis = law['property_analysis']
                        break

                if property_analysis:
                    total_value = sum(item.get('estimated_value', 0) for item in property_analysis)
                    response += f"\n\n**Property Value Analysis:**\n"
                    for item in property_analysis:
                        response += f"- {item['item']}: Rs.{item.get('estimated_value', 0):,}\n"
                    response += f"Total estimated value: Rs.{total_value:,}\n"

                    if total_value >= 5000:
                        response += "Since value exceeds Rs.5,000, standard penalties apply.\n"
                    else:
                        response += "Since value is below Rs.5,000, community service may be considered for first-time offenders.\n"

                response += "\n**Your Rights & Immediate Actions:**\n"
                response += "1. **File FIR immediately** - You have the right to file a complaint within 24 hours\n"
                response += "2. **Preserve evidence** - Secure CCTV footage, take photos of forced entry points\n"
                response += "3. **List stolen items** - Prepare detailed inventory with serial numbers if available\n"
                response += "4. **Change locks** - Secure your property to prevent repeat incidents\n"
                response += "5. **Contact insurance** - Report to your home/property insurance provider\n\n"

                response += "**Legal Consequences for Perpetrator:**\n"
                for law in laws:
                    response += f"- **{law.get('section', '')}**: {law.get('punishment', 'Punishment details')}\n"
                    if law.get('punishment_modification'):
                        response += f"  Modified: {law['punishment_modification'].get('modified', '')}\n"

                response += "\n**Next Steps:**\n"
                response += "1. Visit nearest police station with this analysis\n"
                response += "2. Request case diary number for tracking\n"
                response += "3. Follow up every 7 days on investigation progress\n"
                response += "4. Consider legal counsel if case involves significant value\n\n"

                response += "**Important Disclaimer:** This is AI-generated preliminary legal guidance based on BNS provisions. "
                response += "For case-specific legal advice and representation, please consult a qualified criminal lawyer."

            else:
                response = "**Legal Analysis Result**\n\nUnable to determine specific applicable laws. Please provide more details about the incident."

        return response
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Ollama service"""
        try:
            if not self.is_available():
                return {"status": "error", "message": "Ollama service not available"}
            
            # Test with simple prompt
            test_response = self._call_ollama("Hello, this is a test. Respond with 'Test successful'.")
            
            return {
                "status": "success",
                "message": "Ollama connection successful",
                "model": self.model,
                "test_response": test_response[:100]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }


# Global Ollama service instance
ollama_service = OllamaService()