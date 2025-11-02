"""
Training Data Generator for SLM Entity Extraction and Template Response Formation
Using Official BNS Chapter XVII Data
"""
import json
import random
from typing import List, Dict, Any, Tuple
from pathlib import Path


class TrainingDataGenerator:
    """Generate training data for SLM from official BNS data"""
    
    def __init__(self, bns_data_path: str):
        with open(bns_data_path, 'r', encoding='utf-8') as f:
            self.bns_data = json.load(f)
        
        # Entity categories for factual extraction
        self.entity_categories = {
            "persons": ["accused", "victim", "witness", "owner", "employee", "employer", "clerk", "servant"],
            "objects": ["movable property", "phone", "mobile", "wallet", "money", "jewelry", "vehicle", "bag"],
            "locations": ["dwelling house", "building", "public place", "workplace", "home", "apartment", "office"],
            "actions": ["taking", "stealing", "snatching", "removing", "grabbing", "forcibly taking"],
            "intentions": ["dishonestly", "without consent", "with intent to deprive", "fraudulently"],
            "circumstances": ["at night", "during day", "in presence of others", "secretly", "forcibly"],
            "relationships": ["employee-employer", "owner-property", "victim-accused", "master-servant"]
        }
        
    def generate_entity_extraction_training_data(self, num_samples: int = 100) -> List[Dict[str, Any]]:
        """Generate training data for factual entity extraction (NO legal classification)"""
        training_data = []
        
        # Generate samples based on BNS sections
        for section in self.bns_data["sections"]:
            section_samples = self._generate_section_based_scenarios(section, num_samples // len(self.bns_data["sections"]))
            training_data.extend(section_samples)
        
        return training_data
    
    def _generate_section_based_scenarios(self, section: Dict, num_samples: int) -> List[Dict[str, Any]]:
        """Generate training scenarios based on specific BNS section"""
        scenarios = []
        section_num = section["section_number"]
        
        if section_num == 303:  # Basic Theft
            scenarios.extend(self._generate_theft_scenarios(num_samples))
        elif section_num == 304:  # Snatching
            scenarios.extend(self._generate_snatching_scenarios(num_samples))
        elif section_num == 305:  # Theft in dwelling
            scenarios.extend(self._generate_dwelling_theft_scenarios(num_samples))
        elif section_num == 306:  # Employee theft
            scenarios.extend(self._generate_employee_theft_scenarios(num_samples))
        elif section_num == 308:  # Extortion
            scenarios.extend(self._generate_extortion_scenarios(num_samples))
        elif section_num == 309:  # Robbery
            scenarios.extend(self._generate_robbery_scenarios(num_samples))
        
        return scenarios
    
    def _generate_theft_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate basic theft training scenarios"""
        scenarios = []
        templates = [
            "Someone took my {object} from my {location} without asking. I left it on the table and when I came back it was gone.",
            "A person removed my {object} from my bag while I was in the {location}. I did not give permission for this.",
            "My {object} was stolen from my {location}. The accused person took it dishonestly without my consent.",
            "I found that my {object} is missing from my {location}. Someone must have taken it without my knowledge."
        ]
        
        objects = ["mobile phone", "wallet", "money", "jewelry", "laptop", "bag", "watch"]
        locations = ["office", "bus", "market", "restaurant", "park", "home"]
        
        for i in range(num_samples):
            template = random.choice(templates)
            obj = random.choice(objects)
            location = random.choice(locations)
            
            user_query = template.format(object=obj, location=location)
            
            # Extract ONLY factual entities - NO legal classification
            entities = {
                "objects": [obj],
                "locations": [location],
                "actions": ["took", "stolen", "removed"],
                "intentions": ["without asking", "without permission", "dishonestly", "without consent"],
                "persons": ["accused", "victim"],
                "circumstances": ["from table", "from bag", "while away"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def _generate_snatching_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate snatching training scenarios"""
        scenarios = []
        templates = [
            "Someone suddenly grabbed my {object} from my hands in the {location} and ran away.",
            "A person quickly snatched my {object} while I was walking in {location}.",
            "My {object} was forcibly taken from me by someone in {location}. They seized it suddenly.",
        ]
        
        for i in range(num_samples):
            template = random.choice(templates)
            obj = random.choice(["purse", "chain", "phone", "bag"])
            location = random.choice(["street", "market", "bus stop"])
            
            user_query = template.format(object=obj, location=location)
            
            entities = {
                "objects": [obj],
                "locations": [location],
                "actions": ["grabbed", "snatched", "seized", "forcibly taken"],
                "circumstances": ["suddenly", "quickly", "ran away"],
                "persons": ["accused", "victim"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def _generate_dwelling_theft_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate dwelling house theft scenarios"""
        scenarios = []
        templates = [
            "Someone entered my {dwelling} and stole my {object}. I was not at home when this happened.",
            "My {object} was taken from inside my {dwelling} without my permission.",
            "A person broke into my {dwelling} and removed my {object}.",
        ]
        
        dwellings = ["house", "apartment", "home", "room", "building"]
        
        for i in range(num_samples):
            template = random.choice(templates)
            dwelling = random.choice(dwellings)
            obj = random.choice(["jewelry", "electronics", "money", "valuables"])
            
            user_query = template.format(dwelling=dwelling, object=obj)
            
            entities = {
                "objects": [obj],
                "locations": [dwelling, "dwelling house"],
                "actions": ["entered", "stole", "taken", "broke into", "removed"],
                "circumstances": ["not at home", "without permission"],
                "persons": ["accused", "victim"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def _generate_employee_theft_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate employee theft scenarios"""
        scenarios = []
        templates = [
            "My {employee_type} took {object} belonging to the company. As their {employer_type}, I trusted them with access.",
            "The {employee_type} working for me stole {object} from the workplace.",
            "An {employee_type} in my {workplace} dishonestly took {object} that belongs to the organization.",
        ]
        
        employee_types = ["employee", "worker", "clerk", "servant", "staff member"]
        employer_types = ["employer", "manager", "boss", "owner"]
        workplaces = ["office", "shop", "company", "store", "workplace"]
        
        for i in range(num_samples):
            template = random.choice(templates)
            employee = random.choice(employee_types)
            employer = random.choice(employer_types)
            workplace = random.choice(workplaces)
            obj = random.choice(["equipment", "money", "supplies", "property"])
            
            user_query = template.format(
                employee_type=employee,
                employer_type=employer,
                workplace=workplace,
                object=obj
            )
            
            entities = {
                "objects": [obj],
                "locations": [workplace],
                "actions": ["took", "stole", "dishonestly took"],
                "persons": ["employee", "employer", employee, employer],
                "relationships": ["employee-employer", "worker-boss"],
                "circumstances": ["trusted with access", "from workplace"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def _generate_extortion_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate extortion scenarios"""
        scenarios = []
        templates = [
            "Someone threatened me to give them {object} or they would {threat}.",
            "A person put me in fear by saying they would {threat} unless I gave them {object}.",
            "I was forced to give {object} because someone threatened to {threat}.",
        ]
        
        threats = ["harm my family", "damage my property", "spread false information", "cause hurt"]
        
        for i in range(num_samples):
            template = random.choice(templates)
            obj = random.choice(["money", "property", "valuables"])
            threat = random.choice(threats)
            
            user_query = template.format(object=obj, threat=threat)
            
            entities = {
                "objects": [obj],
                "actions": ["threatened", "forced", "put in fear"],
                "intentions": ["to give", "unless given"],
                "persons": ["accused", "victim"],
                "circumstances": [threat, "under threat"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def _generate_robbery_scenarios(self, num_samples: int) -> List[Dict[str, Any]]:
        """Generate robbery scenarios"""
        scenarios = []
        templates = [
            "Someone used {weapon} to threaten me and took my {object} in {location}.",
            "A person caused me {harm_type} while stealing my {object}.",
            "I was attacked and my {object} was taken by force in {location}.",
        ]
        
        weapons = ["knife", "gun", "stick", "weapon"]
        harm_types = ["hurt", "injury", "physical harm", "wrongful restraint"]
        
        for i in range(num_samples):
            template = random.choice(templates)
            weapon = random.choice(weapons)
            harm = random.choice(harm_types)
            obj = random.choice(["wallet", "phone", "bag", "jewelry"])
            location = random.choice(["street", "alley", "park", "road"])
            
            user_query = template.format(weapon=weapon, harm_type=harm, object=obj, location=location)
            
            entities = {
                "objects": [obj, weapon],
                "locations": [location],
                "actions": ["threatened", "took", "attacked", "stealing", "taken by force"],
                "persons": ["accused", "victim"],
                "circumstances": [harm, "under threat", "by force"]
            }
            
            scenarios.append({
                "user_query": user_query,
                "extracted_entities": entities,
                "task": "entity_extraction",
                "language": "en"
            })
        
        return scenarios
    
    def generate_template_response_training_data(self) -> List[Dict[str, Any]]:
        """Generate training data for template response formation"""
        training_data = []
        
        # Templates for different legal analysis results
        for section in self.bns_data["sections"]:
            section_num = section["section_number"]
            
            # Mock Neo4j legal analysis results
            legal_analysis = {
                "applicable_laws": [{
                    "section": f"BNS-{section_num}",
                    "title": section["section_title"],
                    "description": section["section_text"][:200] + "...",
                    "confidence": 0.85
                }],
                "entities": {"objects": ["property"], "actions": ["theft"]},
                "confidence_score": 0.85
            }
            
            # Generate citizen-friendly response template
            response_template = self._generate_response_template(section_num, legal_analysis)
            
            training_data.append({
                "legal_analysis": legal_analysis,
                "citizen_friendly_response": response_template,
                "task": "template_response_formation",
                "section": section_num
            })
        
        return training_data
    
    def _generate_response_template(self, section_num: int, analysis: Dict) -> str:
        """Generate citizen-friendly response templates"""
        
        if section_num == 303:  # Basic Theft
            return """Based on your description, this appears to involve theft under BNS Section 303. 

**What the law says:**
Taking someone's movable property without their consent with dishonest intention constitutes theft.

**Possible legal action:**
- File a police complaint (FIR)
- The offense is bailable and cognizable
- Punishment can include imprisonment up to 3 years and/or fine

**Next steps:**
1. Report to the nearest police station immediately
2. Gather any evidence (witnesses, CCTV, etc.)
3. Consult with a criminal lawyer for legal guidance

**Important:** This is preliminary legal information only. Please consult a qualified lawyer for actionable advice."""

        elif section_num == 304:  # Snatching
            return """Your situation appears to involve snatching under BNS Section 304.

**What the law says:**
Suddenly, quickly, or forcibly seizing property from a person constitutes snatching.

**Possible legal action:**
- File FIR for snatching
- The offense is cognizable
- Punishment includes imprisonment up to 3 years and fine

**Next steps:**
1. Report to police immediately with details
2. Provide description of the accused if possible
3. Seek medical attention if injured

**Important:** This is preliminary legal information only. Please consult a qualified lawyer for actionable advice."""
        
        # Add more templates for other sections...
        
        return f"""Based on your description, this may involve BNS Section {section_num}.

**Legal Analysis:**
The situation described contains elements that may fall under property offense laws.

**Recommended Actions:**
1. Report to police authorities
2. Gather supporting evidence
3. Consult with a qualified lawyer

**Important:** This is preliminary legal information only. Always consult a lawyer for actionable advice."""
    
    def save_training_data(self, output_dir: str):
        """Save all training data to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate and save entity extraction training data
        entity_data = self.generate_entity_extraction_training_data(200)
        with open(output_path / "entity_extraction_training.json", 'w', encoding='utf-8') as f:
            json.dump(entity_data, f, indent=2, ensure_ascii=False)
        
        # Generate and save template response training data
        template_data = self.generate_template_response_training_data()
        with open(output_path / "template_response_training.json", 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        
        print(f"Training data saved to {output_path}")
        print(f"Entity extraction samples: {len(entity_data)}")
        print(f"Template response samples: {len(template_data)}")


if __name__ == "__main__":
    # Generate training data from official BNS data
    generator = TrainingDataGenerator("../../data/bns_data/bns_ch17.json")
    generator.save_training_data("../../data/training_data/")