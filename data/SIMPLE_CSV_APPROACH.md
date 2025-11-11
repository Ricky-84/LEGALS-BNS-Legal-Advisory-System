# Simplified Approach: 1 Enhanced CSV File

## The Simple Way

Instead of 7 CSV files, we'll **extend your existing CSV** with a few new columns.

---

## Single CSV File: bns_enhanced.csv

### Columns (extending your current structure):

**Existing columns (keep these):**
- `section_id` - e.g., "BNS-303"
- `section_number` - e.g., 303
- `title` - e.g., "Theft"
- `text` - Full legal text
- `offence_type` - e.g., "theft"
- `punishment` - Punishment description

**New columns (add these):**
- `category` - e.g., "property_offences"
- `mens_rea` - Pipe-separated: "dishonest_intent|wrongful_gain"
- `actus_reus` - Pipe-separated: "taking_property|moving_property"
- `circumstances` - Pipe-separated: "without_consent|movable_property"
- `action_patterns` - Pipe-separated: "stole|stolen|took|taken|borrowed and never returned|walked off with"
- `cognizable` - true/false
- `bailable` - true/false

---

## Example CSV Structure

```csv
section_id,section_number,title,text,offence_type,punishment,category,mens_rea,actus_reus,circumstances,action_patterns,cognizable,bailable

BNS-303,303,Theft,"Whoever intends to take dishonestly...",theft,"Imprisonment up to 3 years or fine or both",property_offences,dishonest_intent,taking_property|moving_property,without_consent|movable_property,stole|stolen|took|taken|taking|borrowed and never returned|walked off with|kept for themselves,true,false

BNS-304,304,Snatching,"Whoever snatches movable property...",snatching,"Imprisonment up to 3 years and fine",property_offences,dishonest_intent,sudden_taking,without_consent|movable_property,snatched|grabbed suddenly|yanked|pulled away,true,false

BNS-305,305,Theft in dwelling house,"Whoever commits theft in a building...",dwelling_theft,"Imprisonment up to 7 years and fine",property_offences,dishonest_intent,taking_property,without_consent|in_dwelling,stole|stolen|took|taken|from house|from home|in dwelling,true,false

BNS-306,306,Theft by employee,"Whoever commits theft in respect of property...",employee_theft,"Imprisonment up to 7 years and fine",property_offences,dishonest_intent,taking_property,without_consent|position_of_trust,stole|stolen|took|misused position|employee took,true,false

BNS-308,308,Extortion,"Whoever intentionally puts any person in fear...",extortion,"Imprisonment up to 3 years or fine or both",extortion_robbery,dishonest_intent,threat_of_harm|obtaining_property,fear_of_injury,threatened|intimidated|scared into|put in fear|blackmailed|extorted,true,false

BNS-309,309,Robbery,"Whoever commits theft...",robbery,"Imprisonment up to 10 years and fine",extortion_robbery,dishonest_intent,taking_property,without_consent|violence_or_fear,robbed|stole with violence|forcefully took|threatened and took,true,false

BNS-316,316,Criminal breach of trust,"Whoever being in any manner entrusted...",breach_of_trust,"Imprisonment up to 3 years or fine or both",criminal_breach_of_trust,dishonest_intent,dishonest_misappropriation,entrusted_property,misappropriated|misused|embezzled|converted|used entrusted property|borrowed and never returned|took company money,true,false

BNS-318,318,Cheating,"Whoever by deceiving any person...",cheating,"Imprisonment up to 3 years or fine or both",fraud_deception,dishonest_intent,deception|inducing_delivery,fraudulent_intent,cheated|deceived|tricked|defrauded|lied to obtain|fooled into giving|fake promise,true,false

BNS-324,324,Mischief,"Whoever with intent to cause damage...",mischief,"Imprisonment up to 3 months or fine or both",property_damage,intent_to_cause_loss,damage_property,intentional_damage,damaged|destroyed|vandalized|broke|ruined|smashed|defaced,true,true

BNS-329,329,Criminal trespass,"Whoever enters into or upon property...",criminal_trespass,"Imprisonment up to 3 months or fine up to Rs 3000 or both",trespass,intent_to_commit_offence,unlawful_entry,without_permission,entered|trespassed|broke in|climbed over|entered without permission|unauthorized entry,true,true
```

---

## How It Works

### Step 1: Import Script Reads CSV
```python
import pandas as pd

df = pd.read_csv('data/bns_enhanced.csv')

for _, row in df.iterrows():
    section_id = row['section_id']

    # Create Section node
    # Create Offence node

    # Parse action patterns
    patterns = row['action_patterns'].split('|')
    for pattern in patterns:
        # Create ActionPattern node
        # Link: (ActionPattern)-[:MATCHES]->(Section)

    # Parse legal elements
    mens_rea_list = row['mens_rea'].split('|')
    actus_reus_list = row['actus_reus'].split('|')
    circumstances_list = row['circumstances'].split('|')

    # Create LegalElement nodes and relationships
```

### Step 2: Graph Structure Created Automatically

From 1 CSV row, the script creates:
```
(Section:BNS-303) -[:DEFINES]-> (Offence:theft)

(Offence:theft) -[:REQUIRES_MENS_REA]-> (LegalElement:dishonest_intent)
(Offence:theft) -[:REQUIRES_ACTUS_REUS]-> (LegalElement:taking_property)
(Offence:theft) -[:REQUIRES_CIRCUMSTANCE]-> (LegalElement:without_consent)

(ActionPattern {text:"stole"}) -[:SATISFIES]-> (LegalElement:taking_property)
(ActionPattern {text:"borrowed and never returned"}) -[:SATISFIES]-> (LegalElement:taking_property)
```

---

## Benefits of 1 CSV Approach

1. **Simple** - Just 1 file, easy to edit
2. **Familiar** - Similar to what you're already using
3. **Complete** - All info in one place
4. **Flexible** - Easy to add new patterns (just edit the cell)
5. **No complexity** - No need to manage 7 files and their relationships

---

## What Changed from Your Current CSV?

**Added 5 new columns:**
1. `category` - For grouping offences
2. `mens_rea` - Legal mental elements (pipe-separated)
3. `actus_reus` - Legal physical actions (pipe-separated)
4. `circumstances` - Required circumstances (pipe-separated)
5. `action_patterns` - Natural language variations (pipe-separated)

**Plus 2 optional columns:**
6. `cognizable` - Is it cognizable? (true/false)
7. `bailable` - Is it bailable? (true/false)

That's it! Just add 7 columns to your existing CSV.

---

## Key Innovation: Action Patterns Column

This is where the magic happens:

```csv
action_patterns
"stole|stolen|took|taken|borrowed and never returned|walked off with"
```

Now these all work:
- "Someone stole my phone" ✓
- "Someone took my phone" ✓
- "Someone borrowed my phone and never returned it" ✓
- "Someone walked off with my phone" ✓

All map to BNS-303 (Theft)!

---

## Next Step

I can create a sample `bns_enhanced.csv` file with:
- 10 BNS sections (303, 304, 305, 306, 308, 309, 316, 318, 324, 329)
- All the new columns filled in
- Comprehensive action patterns for each

Then you can just:
1. Review it
2. Edit if needed
3. Use it!

Much simpler than 7 files, right?
