# CSV File Structure for Enhanced BNS Knowledge Graph

## Overview

To build the enhanced knowledge graph with legal elements, we need **7 CSV files** that define nodes and relationships.

---

## 1. sections.csv (Enhanced Section Information)

**Purpose:** Define BNS sections with enhanced properties

**Columns:**
- `section_id` - Unique identifier (e.g., "BNS-303")
- `section_number` - Numeric section number (e.g., 303)
- `title` - Section title (e.g., "Theft")
- `text` - Full legal text of the section
- `chapter` - Chapter number (e.g., "XVII")
- `category` - Category (e.g., "property_offences")
- `cognizable` - Is it cognizable? (true/false)
- `bailable` - Is it bailable? (true/false)

**Example:**
```csv
section_id,section_number,title,text,chapter,category,cognizable,bailable
BNS-303,303,Theft,"Whoever intends to take dishonestly any movable property...",XVII,property_offences,true,false
BNS-304,304,Snatching,"Whoever snatches movable property from a person...",XVII,property_offences,true,false
BNS-305,305,Theft in dwelling house,"Whoever commits theft in a building used as a dwelling...",XVII,property_offences,true,false
```

---

## 2. offences.csv (Offence Definitions)

**Purpose:** Define types of offences

**Columns:**
- `offence_id` - Unique identifier (e.g., "theft")
- `name` - Offence name (e.g., "Theft")
- `section_number` - Related section number (e.g., 303)
- `category` - Category (e.g., "dishonest_misappropriation")
- `severity` - Severity level (e.g., "moderate", "severe", "minor")
- `description` - Brief description

**Example:**
```csv
offence_id,name,section_number,category,severity,description
theft,Theft,303,dishonest_misappropriation,moderate,Dishonest taking of movable property
snatching,Snatching,304,dishonest_misappropriation,moderate,Sudden taking of property from person
dwelling_theft,Theft in dwelling house,305,dishonest_misappropriation,severe,Theft committed in residential building
employee_theft,Theft by employee,306,dishonest_misappropriation,severe,Theft by person in position of trust
extortion,Extortion,308,extortion_robbery,severe,Obtaining property by threat
robbery,Robbery,309,extortion_robbery,severe,Theft with violence or fear
breach_of_trust,Criminal breach of trust,316,criminal_breach_of_trust,severe,Dishonest misappropriation of entrusted property
cheating,Cheating,318,fraud_deception,moderate,Deception to induce delivery of property
mischief,Mischief,324,property_damage,moderate,Intentional damage to property
criminal_trespass,Criminal trespass,329,trespass,minor,Unlawful entry with intent to commit offence
```

---

## 3. legal_elements.csv (Legal Elements - Mens Rea, Actus Reus, Circumstances)

**Purpose:** Define legal elements required to prove an offence

**Columns:**
- `element_id` - Unique identifier (e.g., "dishonest_intent")
- `type` - Element type: "mens_rea", "actus_reus", or "circumstance"
- `name` - Human-readable name
- `description` - Detailed description
- `keywords` - Comma-separated keywords (for basic matching)

**Example:**
```csv
element_id,type,name,description,keywords
dishonest_intent,mens_rea,Dishonest Intent,Intention to cause wrongful gain or loss,"dishonestly,dishonest,wrongfully,wrongful"
taking_property,actus_reus,Taking Property,Taking or moving movable property,"took,taken,taking,stole,stolen,grabbed"
without_consent,circumstance,Without Consent,Without owner's consent or permission,"without permission,without consent,unauthorized,unlawfully"
sudden_taking,actus_reus,Sudden Taking,Suddenly taking property from person or their possession,"snatched,grabbed,yanked,pulled away"
in_dwelling,circumstance,In Dwelling House,Committed in building used as human dwelling,"in house,in home,in dwelling,in residence,from house"
position_of_trust,circumstance,Position of Trust,Offender in position of trust or employed by victim,"employee,clerk,servant,trusted person,working for"
threat_of_harm,actus_reus,Threat of Harm,Putting person in fear of injury,"threatened,intimidated,scared,put in fear"
obtaining_property,actus_reus,Obtaining Property,Obtaining or attempting to obtain property,"obtained,took,acquired,got"
violence_or_fear,circumstance,Violence or Fear,Using violence or putting in fear of instant death or hurt,"violence,assault,fear,hurt"
entrusted_property,circumstance,Entrusted Property,Property entrusted to the accused,"entrusted,trusted with,given custody,responsibility"
dishonest_misappropriation,actus_reus,Dishonest Misappropriation,Using or disposing of entrusted property dishonestly,"misappropriated,misused,converted,used for self"
deception,actus_reus,Deception,Deceiving someone fraudulently or dishonestly,"deceived,tricked,cheated,lied,defrauded"
inducing_delivery,actus_reus,Inducing Delivery,Inducing person to deliver property,"induced to give,made to hand over,convinced to deliver"
damage_property,actus_reus,Damage to Property,Destroying or damaging property,"damaged,destroyed,broke,vandalized,ruined"
intent_to_cause_loss,mens_rea,Intent to Cause Loss,Intent to cause wrongful loss or damage,"intending to damage,intending to cause loss,with intent"
unlawful_entry,actus_reus,Unlawful Entry,Entering property unlawfully,"entered,trespassed,broke in,climbed over,entered without permission"
intent_to_commit_offence,mens_rea,Intent to Commit Offence,Intent to commit an offence or intimidate,"intending to commit offence,to intimidate,to insult,to annoy"
```

---

## 4. action_patterns.csv (Action Pattern Variations)

**Purpose:** Map natural language action variations to legal terminology

**Columns:**
- `pattern_id` - Unique identifier
- `canonical` - Canonical/standard form (e.g., "theft")
- `variation` - Natural language variation
- `confidence` - Confidence level (0.0 to 1.0)

**Example:**
```csv
pattern_id,canonical,variation,confidence
theft_1,theft,stole,1.0
theft_2,theft,stolen,1.0
theft_3,theft,took,0.95
theft_4,theft,taken,0.95
theft_5,theft,taking,0.95
theft_6,theft,borrowed and never returned,0.9
theft_7,theft,walked off with,0.85
theft_8,theft,kept for themselves,0.85
snatch_1,snatching,snatched,1.0
snatch_2,snatching,grabbed suddenly,0.95
snatch_3,snatching,yanked,0.9
snatch_4,snatching,pulled away,0.9
threat_1,threatening,threatened,1.0
threat_2,threatening,intimidated,0.95
threat_3,threatening,scared into,0.9
threat_4,threatening,put in fear,0.95
threat_5,threatening,blackmailed,0.9
deceive_1,deception,cheated,1.0
deceive_2,deception,deceived,1.0
deceive_3,deception,tricked,0.95
deceive_4,deception,defrauded,0.95
deceive_5,deception,lied to obtain,0.9
deceive_6,deception,fooled into giving,0.85
damage_1,damage,damaged,1.0
damage_2,damage,destroyed,1.0
damage_3,damage,vandalized,0.95
damage_4,damage,broke,0.9
damage_5,damage,ruined,0.9
damage_6,damage,smashed,0.95
entry_1,entry,entered,1.0
entry_2,entry,trespassed,1.0
entry_3,entry,broke in,0.95
entry_4,entry,climbed over,0.9
entry_5,entry,entered without permission,1.0
misuse_1,misappropriation,misappropriated,1.0
misuse_2,misappropriation,misused,0.95
misuse_3,misappropriation,converted to own use,0.9
misuse_4,misappropriation,used for personal benefit,0.85
misuse_5,misappropriation,embezzled,0.95
```

---

## 5. punishments.csv (Punishment Details)

**Purpose:** Define punishments for each section

**Columns:**
- `punishment_id` - Unique identifier
- `section_id` - Related section (e.g., "BNS-303")
- `description` - Punishment description
- `punishment_type` - Type (e.g., "imprisonment", "fine", "both")
- `min_duration` - Minimum duration (e.g., "6 months")
- `max_duration` - Maximum duration (e.g., "3 years")
- `fine_amount` - Fine amount or "as per court"

**Example:**
```csv
punishment_id,section_id,description,punishment_type,min_duration,max_duration,fine_amount
p_303,BNS-303,Imprisonment up to 3 years or fine or both,both,0,3 years,as per court
p_304,BNS-304,Imprisonment up to 3 years and fine,both,0,3 years,mandatory
p_305,BNS-305,Imprisonment up to 7 years and fine,both,0,7 years,mandatory
p_306,BNS-306,Imprisonment up to 7 years and fine,both,0,7 years,mandatory
p_308,BNS-308,Imprisonment up to 3 years or fine or both,both,0,3 years,as per court
p_309,BNS-309,Imprisonment up to 10 years and fine,both,0,10 years,mandatory
p_316,BNS-316,Imprisonment up to 3 years or fine or both,both,0,3 years,as per court
p_318,BNS-318,Imprisonment up to 3 years or fine or both,both,0,3 years,as per court
p_324,BNS-324,Imprisonment up to 3 months or fine or both,both,0,3 months,as per court
p_329,BNS-329,Imprisonment up to 3 months or fine up to Rs 3000 or both,both,0,3 months,3000
```

---

## 6. offence_elements.csv (Offence → Legal Elements Relationships)

**Purpose:** Define which legal elements are required for each offence

**Columns:**
- `offence_id` - Offence identifier
- `element_id` - Legal element identifier
- `relationship_type` - Type: "REQUIRES_MENS_REA", "REQUIRES_ACTUS_REUS", "REQUIRES_CIRCUMSTANCE"
- `mandatory` - Is this element mandatory? (true/false)
- `weight` - Weight/importance (0.0 to 1.0)

**Example:**
```csv
offence_id,element_id,relationship_type,mandatory,weight
theft,dishonest_intent,REQUIRES_MENS_REA,true,1.0
theft,taking_property,REQUIRES_ACTUS_REUS,true,1.0
theft,without_consent,REQUIRES_CIRCUMSTANCE,true,1.0
snatching,dishonest_intent,REQUIRES_MENS_REA,true,1.0
snatching,sudden_taking,REQUIRES_ACTUS_REUS,true,1.0
snatching,without_consent,REQUIRES_CIRCUMSTANCE,true,1.0
dwelling_theft,dishonest_intent,REQUIRES_MENS_REA,true,1.0
dwelling_theft,taking_property,REQUIRES_ACTUS_REUS,true,1.0
dwelling_theft,without_consent,REQUIRES_CIRCUMSTANCE,true,1.0
dwelling_theft,in_dwelling,REQUIRES_CIRCUMSTANCE,true,1.0
employee_theft,dishonest_intent,REQUIRES_MENS_REA,true,1.0
employee_theft,taking_property,REQUIRES_ACTUS_REUS,true,1.0
employee_theft,without_consent,REQUIRES_CIRCUMSTANCE,true,1.0
employee_theft,position_of_trust,REQUIRES_CIRCUMSTANCE,true,1.0
extortion,dishonest_intent,REQUIRES_MENS_REA,true,1.0
extortion,threat_of_harm,REQUIRES_ACTUS_REUS,true,1.0
extortion,obtaining_property,REQUIRES_ACTUS_REUS,true,1.0
robbery,dishonest_intent,REQUIRES_MENS_REA,true,1.0
robbery,taking_property,REQUIRES_ACTUS_REUS,true,1.0
robbery,without_consent,REQUIRES_CIRCUMSTANCE,true,1.0
robbery,violence_or_fear,REQUIRES_CIRCUMSTANCE,true,1.0
breach_of_trust,dishonest_intent,REQUIRES_MENS_REA,true,1.0
breach_of_trust,entrusted_property,REQUIRES_CIRCUMSTANCE,true,1.0
breach_of_trust,dishonest_misappropriation,REQUIRES_ACTUS_REUS,true,1.0
cheating,dishonest_intent,REQUIRES_MENS_REA,true,1.0
cheating,deception,REQUIRES_ACTUS_REUS,true,1.0
cheating,inducing_delivery,REQUIRES_ACTUS_REUS,true,1.0
mischief,intent_to_cause_loss,REQUIRES_MENS_REA,true,1.0
mischief,damage_property,REQUIRES_ACTUS_REUS,true,1.0
criminal_trespass,intent_to_commit_offence,REQUIRES_MENS_REA,true,1.0
criminal_trespass,unlawful_entry,REQUIRES_ACTUS_REUS,true,1.0
```

---

## 7. pattern_satisfies.csv (Action Pattern → Legal Element Relationships)

**Purpose:** Map which action patterns satisfy which legal elements

**Columns:**
- `pattern_id` - Action pattern identifier
- `element_id` - Legal element identifier
- `confidence` - Confidence level (0.0 to 1.0)

**Example:**
```csv
pattern_id,element_id,confidence
theft_1,taking_property,1.0
theft_2,taking_property,1.0
theft_3,taking_property,0.95
theft_4,taking_property,0.95
theft_5,taking_property,0.95
theft_6,taking_property,0.9
theft_7,taking_property,0.85
theft_8,taking_property,0.85
snatch_1,sudden_taking,1.0
snatch_2,sudden_taking,0.95
snatch_3,sudden_taking,0.9
snatch_4,sudden_taking,0.9
threat_1,threat_of_harm,1.0
threat_2,threat_of_harm,0.95
threat_3,threat_of_harm,0.9
threat_4,threat_of_harm,0.95
threat_5,threat_of_harm,0.9
deceive_1,deception,1.0
deceive_2,deception,1.0
deceive_3,deception,0.95
deceive_4,deception,0.95
deceive_5,deception,0.9
deceive_6,deception,0.85
damage_1,damage_property,1.0
damage_2,damage_property,1.0
damage_3,damage_property,0.95
damage_4,damage_property,0.9
damage_5,damage_property,0.9
damage_6,damage_property,0.95
entry_1,unlawful_entry,1.0
entry_2,unlawful_entry,1.0
entry_3,unlawful_entry,0.95
entry_4,unlawful_entry,0.9
entry_5,unlawful_entry,1.0
misuse_1,dishonest_misappropriation,1.0
misuse_2,dishonest_misappropriation,0.95
misuse_3,dishonest_misappropriation,0.9
misuse_4,dishonest_misappropriation,0.85
misuse_5,dishonest_misappropriation,0.95
```

---

## Graph Structure Visualization

```
(Section:BNS-303) -[:DEFINES]-> (Offence:theft)

(Offence:theft) -[:REQUIRES_MENS_REA {mandatory:true, weight:1.0}]-> (LegalElement:dishonest_intent)
(Offence:theft) -[:REQUIRES_ACTUS_REUS {mandatory:true, weight:1.0}]-> (LegalElement:taking_property)
(Offence:theft) -[:REQUIRES_CIRCUMSTANCE {mandatory:true, weight:1.0}]-> (LegalElement:without_consent)

(ActionPattern:theft_1 {variation:"stole"}) -[:SATISFIES {confidence:1.0}]-> (LegalElement:taking_property)
(ActionPattern:theft_6 {variation:"borrowed and never returned"}) -[:SATISFIES {confidence:0.9}]-> (LegalElement:taking_property)

(Section:BNS-303) -[:PRESCRIBES]-> (Punishment:p_303)
```

---

## How the Graph Reasoning Works

1. **User Query:** "Someone borrowed my bike and never returned it"
2. **Entity Extraction:** actions = ["borrowed", "never returned"]
3. **Pattern Matching:**
   - "borrowed and never returned" matches ActionPattern:theft_6
4. **Element Satisfaction:**
   - ActionPattern:theft_6 SATISFIES LegalElement:taking_property (confidence: 0.9)
5. **Offence Detection:**
   - LegalElement:taking_property is REQUIRED by Offence:theft
6. **Section Identification:**
   - Offence:theft is DEFINED by Section:BNS-303
7. **Result:** BNS-303 (Theft) applies with 90% confidence

---

## File Locations

Save all CSV files in:
```
data/csv_enhanced_graph/
├── sections.csv
├── offences.csv
├── legal_elements.csv
├── action_patterns.csv
├── punishments.csv
├── offence_elements.csv
└── pattern_satisfies.csv
```

---

## Next Steps

1. Create sample CSV files for 10 BNS sections (303, 304, 305, 306, 308, 309, 316, 318, 324, 329)
2. Verify CSV format and data integrity
3. Create Python script to import these CSVs into Neo4j
4. Test graph queries with sample data
