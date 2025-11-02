"""
Property Value Estimation Service for Legal Processing
Estimates market value of stolen/damaged property when not explicitly mentioned
"""
from typing import Dict, Tuple, List
import re
from enum import Enum

class ValueConfidence(Enum):
    HIGH = "high"      # Specific model/brand mentioned
    MEDIUM = "medium"  # General item type with some details
    LOW = "low"        # Vague description

class PropertyValueEstimator:
    """Estimates property values for legal threshold determination"""

    def __init__(self):
        # Property value database (in rupees)
        self.value_database = {
            # Electronics
            "mobile_phone": {
                "iphone": {"14": 79000, "13": 65000, "12": 55000, "se": 35000},
                "samsung": {"s24": 75000, "s23": 60000, "a54": 35000, "a34": 25000},
                "generic": {"smartphone": 25000, "basic_phone": 5000}
            },
            "laptop": {
                "macbook": {"pro": 150000, "air": 100000},
                "dell": {"xps": 120000, "inspiron": 60000},
                "hp": {"pavilion": 50000, "elitebook": 90000},
                "generic": {"laptop": 45000, "gaming_laptop": 80000}
            },
            "tablet": {
                "ipad": {"pro": 80000, "air": 60000, "basic": 35000},
                "samsung": {"tab_s": 45000, "tab_a": 25000},
                "generic": {"tablet": 20000}
            },

            # Jewelry & Accessories
            "jewelry": {
                "gold": {"ring": 15000, "chain": 25000, "earrings": 12000},
                "silver": {"ring": 3000, "chain": 5000, "earrings": 2500},
                "watch": {"luxury": 50000, "branded": 15000, "basic": 3000}
            },

            # Vehicles
            "vehicle": {
                "car": {"luxury": 1500000, "sedan": 800000, "hatchback": 600000},
                "motorcycle": {"high_end": 200000, "standard": 80000, "scooter": 60000},
                "bicycle": {"mountain": 25000, "road": 40000, "basic": 8000}
            },

            # Cash & Documents
            "cash": {"mentioned_amount": "use_exact_value"},
            "documents": {
                "passport": 1500,  # replacement cost
                "driving_license": 500,
                "credit_card": 1000,  # replacement hassle value
                "important_documents": 2000
            },

            # Clothing & Personal Items
            "clothing": {
                "branded": {"shirt": 3000, "jeans": 4000, "shoes": 5000},
                "designer": {"dress": 15000, "suit": 25000, "shoes": 12000},
                "generic": {"shirt": 800, "jeans": 1500, "shoes": 2000}
            },

            # Household Items
            "household": {
                "appliances": {"tv": 35000, "refrigerator": 25000, "microwave": 8000},
                "furniture": {"sofa": 20000, "bed": 15000, "table": 8000}
            }
        }

        # Legal thresholds (in rupees)
        self.legal_thresholds = {
            "community_service": 5000,   # BNS-303: below this = community service
            "simple_theft": 50000,       # Above this might be considered serious
            "major_theft": 100000        # Might involve additional charges
        }

    def estimate_value(self, property_items: List[str], descriptions: List[str] = None) -> Dict:
        """
        Estimate total value of stolen/damaged property

        Args:
            property_items: List of property items mentioned
            descriptions: Optional detailed descriptions

        Returns:
            Dict with estimated value, confidence, and legal implications
        """
        total_value = 0
        confidence_scores = []
        breakdown = []

        descriptions = descriptions or []

        for i, item in enumerate(property_items):
            item_desc = descriptions[i] if i < len(descriptions) else ""
            value, confidence, details = self._estimate_single_item(item, item_desc)

            total_value += value
            confidence_scores.append(confidence)
            breakdown.append({
                "item": item,
                "description": item_desc,
                "estimated_value": value,
                "confidence": confidence.value,
                "basis": details
            })

        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(confidence_scores)

        # Determine legal implications
        legal_analysis = self._analyze_legal_thresholds(total_value)

        return {
            "total_estimated_value": total_value,
            "confidence": overall_confidence.value,
            "breakdown": breakdown,
            "legal_thresholds": legal_analysis,
            "value_category": self._categorize_value(total_value)
        }

    def _estimate_single_item(self, item: str, description: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate value of a single item"""
        item_lower = item.lower()
        desc_lower = description.lower()
        combined_text = f"{item_lower} {desc_lower}"

        # Check for explicit value mentions
        value_match = re.search(r'(?:worth|value|cost|price).*?(\d+(?:,\d+)*)', combined_text)
        if value_match:
            try:
                explicit_value = int(value_match.group(1).replace(',', ''))
                return explicit_value, ValueConfidence.HIGH, "User mentioned explicit value"
            except ValueError:
                pass

        # Electronics detection with brand/model
        if any(phone in combined_text for phone in ["iphone", "phone", "mobile"]):
            return self._estimate_phone(combined_text)
        elif any(laptop in combined_text for laptop in ["laptop", "macbook", "computer"]):
            return self._estimate_laptop(combined_text)
        elif "tablet" in combined_text or "ipad" in combined_text:
            return self._estimate_tablet(combined_text)

        # Jewelry and accessories
        elif any(jewelry in combined_text for jewelry in ["ring", "chain", "earring", "jewelry", "gold", "silver"]):
            return self._estimate_jewelry(combined_text)
        elif "watch" in combined_text:
            return self._estimate_watch(combined_text)

        # Vehicles
        elif any(vehicle in combined_text for vehicle in ["car", "bike", "motorcycle", "scooter", "bicycle"]):
            return self._estimate_vehicle(combined_text)

        # Cash
        elif "cash" in combined_text or "money" in combined_text or "rupees" in combined_text:
            return self._estimate_cash(combined_text)

        # Documents
        elif any(doc in combined_text for doc in ["passport", "license", "document", "card"]):
            return self._estimate_documents(combined_text)

        # Clothing
        elif any(cloth in combined_text for cloth in ["shirt", "dress", "shoe", "clothes", "jeans"]):
            return self._estimate_clothing(combined_text)

        # Default fallback
        return 10000, ValueConfidence.LOW, "Generic property estimation"

    def _estimate_phone(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate phone value based on description"""
        if "iphone" in text:
            if "14" in text or "14 pro" in text:
                return 79000, ValueConfidence.HIGH, "iPhone 14 market price"
            elif "13" in text:
                return 65000, ValueConfidence.HIGH, "iPhone 13 market price"
            elif "12" in text:
                return 55000, ValueConfidence.HIGH, "iPhone 12 market price"
            else:
                return 60000, ValueConfidence.MEDIUM, "Generic iPhone price"
        elif "samsung" in text:
            if "s24" in text or "s23" in text:
                return 65000, ValueConfidence.HIGH, "Samsung flagship price"
            else:
                return 30000, ValueConfidence.MEDIUM, "Samsung mid-range price"
        else:
            return 25000, ValueConfidence.LOW, "Generic smartphone price"

    def _estimate_laptop(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate laptop value"""
        if "macbook" in text:
            if "pro" in text:
                return 150000, ValueConfidence.HIGH, "MacBook Pro market price"
            else:
                return 100000, ValueConfidence.HIGH, "MacBook Air market price"
        elif any(brand in text for brand in ["dell", "hp", "lenovo"]):
            return 60000, ValueConfidence.MEDIUM, "Branded laptop average price"
        else:
            return 45000, ValueConfidence.LOW, "Generic laptop price"

    def _estimate_tablet(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate tablet value"""
        if "ipad" in text:
            if "pro" in text:
                return 80000, ValueConfidence.HIGH, "iPad Pro market price"
            else:
                return 45000, ValueConfidence.HIGH, "iPad standard market price"
        else:
            return 20000, ValueConfidence.LOW, "Generic tablet price"

    def _estimate_jewelry(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate jewelry value"""
        if "gold" in text:
            if "chain" in text:
                return 25000, ValueConfidence.MEDIUM, "Gold chain average price"
            elif "ring" in text:
                return 15000, ValueConfidence.MEDIUM, "Gold ring average price"
            else:
                return 20000, ValueConfidence.MEDIUM, "Gold jewelry average"
        elif "silver" in text:
            return 5000, ValueConfidence.MEDIUM, "Silver jewelry average"
        else:
            return 10000, ValueConfidence.LOW, "Generic jewelry price"

    def _estimate_watch(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate watch value"""
        luxury_brands = ["rolex", "omega", "tag", "breitling", "patek"]
        if any(brand in text for brand in luxury_brands):
            return 200000, ValueConfidence.HIGH, "Luxury watch brand"
        elif any(brand in text for brand in ["titan", "fossil", "casio"]):
            return 8000, ValueConfidence.MEDIUM, "Branded watch price"
        else:
            return 3000, ValueConfidence.LOW, "Generic watch price"

    def _estimate_vehicle(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate vehicle value"""
        if "car" in text:
            return 800000, ValueConfidence.MEDIUM, "Average car price"
        elif "motorcycle" in text or "bike" in text:
            return 80000, ValueConfidence.MEDIUM, "Motorcycle average price"
        elif "scooter" in text:
            return 60000, ValueConfidence.MEDIUM, "Scooter average price"
        elif "bicycle" in text:
            return 15000, ValueConfidence.MEDIUM, "Bicycle average price"
        else:
            return 100000, ValueConfidence.LOW, "Generic vehicle price"

    def _estimate_cash(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate cash value"""
        # Try to extract amount from text
        amount_match = re.search(r'(\d+(?:,\d+)*)\s*(?:rupees?|rs\.?|₹)', text)
        if amount_match:
            try:
                amount = int(amount_match.group(1).replace(',', ''))
                return amount, ValueConfidence.HIGH, "Explicit cash amount mentioned"
            except ValueError:
                pass

        # Look for descriptive amounts
        if any(word in text for word in ["thousand", "1000", "2000", "5000"]):
            return 3000, ValueConfidence.MEDIUM, "Approximate cash amount"
        else:
            return 2000, ValueConfidence.LOW, "Generic cash estimation"

    def _estimate_documents(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate document replacement value"""
        if "passport" in text:
            return 1500, ValueConfidence.HIGH, "Passport replacement cost"
        elif "license" in text:
            return 500, ValueConfidence.HIGH, "License replacement cost"
        elif "card" in text:
            return 1000, ValueConfidence.MEDIUM, "Card replacement hassle value"
        else:
            return 2000, ValueConfidence.LOW, "Document replacement average"

    def _estimate_clothing(self, text: str) -> Tuple[int, ValueConfidence, str]:
        """Estimate clothing value"""
        designer_brands = ["gucci", "prada", "louis", "chanel", "versace"]
        if any(brand in text for brand in designer_brands):
            return 15000, ValueConfidence.HIGH, "Designer brand clothing"
        elif any(brand in text for brand in ["nike", "adidas", "puma", "levis"]):
            return 4000, ValueConfidence.MEDIUM, "Branded clothing"
        else:
            return 1500, ValueConfidence.LOW, "Generic clothing price"

    def _calculate_overall_confidence(self, confidence_scores: List[ValueConfidence]) -> ValueConfidence:
        """Calculate overall confidence from individual scores"""
        if not confidence_scores:
            return ValueConfidence.LOW

        high_count = sum(1 for c in confidence_scores if c == ValueConfidence.HIGH)
        medium_count = sum(1 for c in confidence_scores if c == ValueConfidence.MEDIUM)

        if high_count >= len(confidence_scores) * 0.7:
            return ValueConfidence.HIGH
        elif high_count + medium_count >= len(confidence_scores) * 0.5:
            return ValueConfidence.MEDIUM
        else:
            return ValueConfidence.LOW

    def _analyze_legal_thresholds(self, total_value: int) -> Dict:
        """Analyze legal implications based on property value"""
        analysis = {
            "above_community_service_threshold": total_value >= self.legal_thresholds["community_service"],
            "theft_severity": "minor" if total_value < self.legal_thresholds["community_service"] else "major",
            "bns_303_implication": "community_service" if total_value < 5000 else "imprisonment_or_fine",
            "threshold_details": {
                "value": total_value,
                "threshold": self.legal_thresholds["community_service"],
                "difference": total_value - self.legal_thresholds["community_service"]
            }
        }

        return analysis

    def _categorize_value(self, value: int) -> str:
        """Categorize value for legal processing"""
        if value < 5000:
            return "minor_theft"  # Community service eligible
        elif value < 50000:
            return "moderate_theft"  # Standard theft punishment
        elif value < 100000:
            return "serious_theft"  # Higher penalties
        else:
            return "major_theft"  # Maximum penalties