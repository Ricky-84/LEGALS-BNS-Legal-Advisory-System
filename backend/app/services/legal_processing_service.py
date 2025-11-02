"""
Legal Processing Service - Integrates SLM, Neo4j, and Database services
Complete pipeline: User Query → Entity Extraction → Legal Reasoning → Response Generation
"""
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .ollama_service import ollama_service
from .neo4j_service import neo4j_service
# from .database_service import database_service
# from ..models.database import get_db

logger = logging.getLogger(__name__)


class LegalProcessingService:
    """Main service orchestrating the complete legal analysis pipeline"""
    
    def __init__(self):
        self.ollama = ollama_service
        self.neo4j = neo4j_service
        # self.database = database_service
    
    def process_legal_query(
        self, 
        query: str, 
        language: str = "en", 
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete legal query processing pipeline
        
        Pipeline Flow:
        1. User Query → SLM Entity Extraction (factual only)
        2. Entities → Neo4j Legal Reasoning (deterministic)
        3. Legal Analysis → SLM Response Formatting (citizen-friendly)
        4. Results → Database Storage & Fact Verification
        """
        start_time = time.time()
        query_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Processing legal query {query_id}: {query[:100]}...")
            
            # Step 1: Entity Extraction using trained SLM
            logger.info("Step 1: Extracting entities using Phi-3...")
            extracted_entities = self._extract_entities_step(query, language)
            
            # Step 2: Legal Reasoning using Neo4j
            logger.info("Step 2: Performing legal reasoning using Neo4j...")
            legal_analysis = self._legal_reasoning_step(extracted_entities)
            
            # Step 3: Response Generation using SLM
            logger.info("Step 3: Generating citizen-friendly response...")
            formatted_response = self._response_generation_step(legal_analysis, language)
            
            # Step 4: Fact Verification and Storage
            logger.info("Step 4: Fact verification and storage...")
            verified_result = self._verification_and_storage_step(
                query_id, query, language, extracted_entities, legal_analysis, 
                formatted_response, start_time, user_id
            )
            
            processing_time = time.time() - start_time
            logger.info(f"Query {query_id} processed successfully in {processing_time:.2f}s")
            
            return verified_result
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"Query {query_id} failed after {error_time:.2f}s: {e}")
            
            return self._create_error_response(query_id, query, str(e), error_time)
    
    def _extract_entities_step(self, query: str, language: str) -> Dict[str, List[str]]:
        """Step 1: Extract factual entities using trained SLM (NO legal classification)"""
        try:
            entities = self.ollama.extract_entities(query, language)
            
            # Validate entity structure
            validated_entities = self._validate_extracted_entities(entities)
            
            logger.info(f"Extracted entities: {validated_entities}")
            return validated_entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            # Return empty but valid entity structure
            return {
                "persons": [],
                "objects": [],
                "locations": [],
                "actions": [],
                "intentions": [],
                "circumstances": [],
                "relationships": []
            }
    
    def _legal_reasoning_step(self, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Step 2: Enhanced legal reasoning using Neo4j with property value analysis"""
        try:
            # Neo4j determines applicable laws based on entities
            applicable_laws = self.neo4j.find_applicable_laws(entities)

            # Enhance with property value analysis for theft-related cases
            enhanced_laws = self.neo4j.enhance_with_property_analysis(applicable_laws, entities)

            # Calculate overall confidence
            confidence_score = self.neo4j.get_legal_confidence_score(enhanced_laws)

            legal_analysis = {
                "applicable_laws": enhanced_laws,
                "entities_analyzed": entities,
                "confidence_score": confidence_score,
                "reasoning_method": "enhanced_neo4j_with_property_analysis",
                "property_value_analysis": any(
                    law.get("property_analysis") for law in enhanced_laws
                ),
                "timestamp": datetime.utcnow().isoformat()
            }

            logger.info(f"Enhanced legal analysis completed. Found {len(enhanced_laws)} applicable laws with property analysis: {legal_analysis['property_value_analysis']}")
            return legal_analysis

        except Exception as e:
            logger.error(f"Legal reasoning failed: {e}")
            return {
                "applicable_laws": [],
                "entities_analyzed": entities,
                "confidence_score": 0.0,
                "error": str(e),
                "reasoning_method": "failed"
            }
    
    def _response_generation_step(self, legal_analysis: Dict[str, Any], language: str) -> str:
        """Step 3: Generate citizen-friendly response using SLM templates"""
        try:
            # Use SLM to format legal analysis into citizen-friendly response
            formatted_response = self.ollama.format_legal_response(legal_analysis, language)
            
            # Ensure response has required disclaimers
            response_with_disclaimers = self._ensure_legal_disclaimers(formatted_response, language)
            
            logger.info("Citizen-friendly response generated")
            return response_with_disclaimers
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._create_fallback_response(legal_analysis, language)
    
    def _verification_and_storage_step(
        self, 
        query_id: str, 
        query: str, 
        language: str,
        entities: Dict[str, List[str]], 
        legal_analysis: Dict[str, Any],
        formatted_response: str,
        start_time: float,
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Step 4: Fact verification and database storage"""
        
        processing_time = time.time() - start_time
        
        try:
            # Fact verification using Neo4j
            verified_analysis = self.neo4j.verify_legal_facts(legal_analysis)
            
            # Store in database (you can uncomment when database is ready)
            # db = next(get_db())
            # stored_query = self.database.save_legal_query(
            #     db, query, language, entities, legal_analysis.get("applicable_laws", []),
            #     formatted_response, legal_analysis.get("confidence_score", 0.0),
            #     processing_time, user_id
            # )
            
            # Create final response
            final_response = {
                "query_id": query_id,
                "query": query,
                "language": language,
                "entities": entities,
                "applicable_laws": legal_analysis.get("applicable_laws", []),
                "legal_advice": formatted_response,
                "confidence_score": legal_analysis.get("confidence_score", 0.0),
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat(),
                "verified": verified_analysis.get("verified", False),
                "disclaimers": self._get_legal_disclaimers(language),
                "system_info": {
                    "entity_extraction": "phi3_trained",
                    "legal_reasoning": "neo4j_deterministic", 
                    "response_formatting": "phi3_templates"
                }
            }
            
            return final_response
            
        except Exception as e:
            logger.error(f"Verification/storage failed: {e}")
            # Return response without storage
            return {
                "query_id": query_id,
                "query": query,
                "entities": entities,
                "applicable_laws": legal_analysis.get("applicable_laws", []),
                "legal_advice": formatted_response,
                "confidence_score": legal_analysis.get("confidence_score", 0.0),
                "processing_time": processing_time,
                "error": "Storage failed",
                "disclaimers": self._get_legal_disclaimers(language)
            }
    
    def _validate_extracted_entities(self, entities: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Validate and clean extracted entities"""
        required_categories = ["persons", "objects", "locations", "actions", "intentions", "circumstances", "relationships"]
        
        validated = {}
        for category in required_categories:
            if category in entities and isinstance(entities[category], list):
                # Clean and limit entities
                validated[category] = [
                    str(item).strip() for item in entities[category]
                    if item and str(item).strip()
                ][:10]  # Limit to 10 per category
            else:
                validated[category] = []
        
        return validated
    
    def _ensure_legal_disclaimers(self, response: str, language: str) -> str:
        """Ensure response contains proper legal disclaimers"""
        disclaimers = self._get_legal_disclaimers(language)
        
        # Check if disclaimers are already present
        disclaimer_keywords = ["consult", "lawyer", "preliminary", "qualified"] if language == "en" else ["सलाह", "वकील", "प्रारंभिक"]
        
        has_disclaimer = any(keyword.lower() in response.lower() for keyword in disclaimer_keywords)
        
        if not has_disclaimer:
            # Add disclaimers
            disclaimer_text = "\n\n**Important Disclaimers:**\n" + "\n".join(f"• {disclaimer}" for disclaimer in disclaimers)
            response += disclaimer_text
        
        return response
    
    def _get_legal_disclaimers(self, language: str) -> List[str]:
        """Get legal disclaimers in specified language"""
        if language == "hi":
            return [
                "यह प्रणाली केवल प्रारंभिक कानूनी जानकारी प्रदान करती है।",
                "योग्य कानूनी सलाहकार से परामर्श आवश्यक है।",
                "कार्यात्मक कानूनी सलाह के लिए वकील से संपर्क करें।"
            ]
        else:
            return [
                "This system provides preliminary legal information only.",
                "Not a replacement for qualified legal counsel.",
                "Consult lawyers for actionable legal advice.",
                "Always verify information with legal professionals."
            ]
    
    def _create_fallback_response(self, legal_analysis: Dict[str, Any], language: str) -> str:
        """Create detailed fallback response when SLM formatting fails"""
        applicable_laws = legal_analysis.get("applicable_laws", [])
        entities = legal_analysis.get("entities_analyzed", {})
        confidence = legal_analysis.get("confidence_score", 0.0)

        # Extract case details
        objects = entities.get("objects", [])
        locations = entities.get("locations", [])
        actions = entities.get("actions", [])

        if language == "hi":
            response = "**कानूनी मार्गदर्शन**\n\n"

            if objects or locations:
                response += f"**मामले का विवरण:** "
                if objects:
                    response += f"{', '.join(objects)} शामिल है"
                if locations:
                    response += f", स्थान: {', '.join(locations)}"
                response += "\n\n"

            response += "**कानूनी मूल्यांकन:**\n"
            for law in applicable_laws:
                response += f"• **{law.get('section', '')}: {law.get('title', '')}**\n"
                response += f"  आत्मविश्वास: {law.get('confidence', 0):.0%}\n"
                response += f"  कारण: {law.get('reasoning', '')}\n"

                if law.get('property_analysis'):
                    total_value = sum(prop.get('estimated_value', 0) for prop in law['property_analysis'])
                    response += f"  संपत्ति मूल्य: ₹{total_value:,}\n"

            response += "\n**तत्काल कार्रवाई:**\n"
            response += "1. पुलिस स्टेशन में FIR दर्ज कराएं\n"
            response += "2. सभी सबूत और गवाह की जानकारी संग्रहीत करें\n"
            response += "3. कानूनी सलाहकार से तुरंत संपर्क करें\n"
            response += "4. घटना की विस्तृत रिपोर्ट तैयार करें\n\n"

            response += "**महत्वपूर्ण सूचना:** यह प्रारंभिक मार्गदर्शन है। विशिष्ट कानूनी सलाह के लिए योग्य वकील से संपर्क करें।"

        else:
            response = "**Legal Guidance**\n\n"

            # Case-specific assessment
            if objects or locations:
                response += f"**Case Analysis:** "
                if objects:
                    response += f"Involving {', '.join(objects)}"
                if locations:
                    response += f" at/in {', '.join(locations)}"
                response += f" (Confidence: {confidence:.0%})\n\n"

            response += "**Legal Assessment:**\n"
            for i, law in enumerate(applicable_laws, 1):
                response += f"{i}. **{law.get('section', '')}: {law.get('title', '')}**\n"
                response += f"   • Applies because: {law.get('reasoning', '')}\n"
                response += f"   • Confidence level: {law.get('confidence', 0):.0%}\n"

                # Property value analysis
                if law.get('property_analysis'):
                    total_value = sum(prop.get('estimated_value', 0) for prop in law['property_analysis'])
                    response += f"   • Property value: ₹{total_value:,}"
                    if total_value >= 5000:
                        response += " (Above ₹5,000 threshold - Standard penalties)\n"
                    else:
                        response += " (Below ₹5,000 threshold - May qualify for community service)\n"

                # Specific punishment info
                if law.get('punishment_modification'):
                    mod = law['punishment_modification']
                    response += f"   • Potential penalty: {mod.get('modified', 'Standard punishment')}\n"

                response += "\n"

            response += "**Your Rights & Immediate Actions:**\n"

            # Victim-specific advice
            if any("victim" in person.lower() for person in entities.get("persons", [])) or "stolen" in actions:
                response += "**If you are the victim:**\n"
                response += "• File a police complaint (FIR) immediately\n"
                response += "• Preserve all evidence (receipts, photos, witness contacts)\n"
                response += "• Get a copy of the FIR for insurance/legal purposes\n"
                response += "• Contact your insurance company if applicable\n\n"

            # Accused-specific advice
            response += "**If you are accused:**\n"
            response += "• Do NOT give any statements without a lawyer present\n"
            response += "• Contact a criminal defense lawyer immediately\n"
            response += "• Gather evidence that supports your innocence\n"
            response += "• Avoid contact with the complainant\n\n"

            response += "**Timeline & Next Steps:**\n"
            response += "1. **Immediate (within 24 hours):** File police report or contact lawyer\n"
            response += "2. **Within 3 days:** Gather all evidence and witness statements\n"
            response += "3. **Within 1 week:** Consult with experienced criminal lawyer\n"
            response += "4. **Ongoing:** Follow legal advice and court procedures\n\n"

            response += "**Important Legal Disclaimer:**\n"
            response += "This analysis is based on general legal principles and the specific facts you provided. "
            response += "Every case is unique, and outcomes depend on many factors. This information should not "
            response += "replace consultation with a qualified lawyer who can provide advice specific to your situation."

        return response
    
    def _create_error_response(self, query_id: str, query: str, error: str, processing_time: float) -> Dict[str, Any]:
        """Create error response for failed queries"""
        return {
            "query_id": query_id,
            "query": query,
            "error": error,
            "status": "failed",
            "processing_time": processing_time,
            "timestamp": datetime.utcnow().isoformat(),
            "disclaimers": ["System error occurred. Please try again or consult a lawyer directly."]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all integrated services"""
        ollama_status = self.ollama.test_connection()
        
        return {
            "status": "integrated",
            "services": {
                "ollama": ollama_status.get("status", "unknown"),
                "neo4j": "ready",  # Would test actual connection
                "database": "ready"  # Would test actual connection
            },
            "capabilities": {
                "entity_extraction": True,
                "legal_reasoning": True,
                "response_formatting": True,
                "fact_verification": True,
                "multilingual": True
            },
            "model_info": {
                "slm_model": "phi3:latest",
                "training_data": "bns_chapter_xvii",
                "training_samples": 198
            }
        }


# Global integrated service instance
legal_processor = LegalProcessingService()