# How to Create Enhanced CSV from Existing CSV

## Your Current CSV Structure

**File:** `data/csv_friend/bns_ch17_final_cleaned.csv`

**Current Columns:**
```
c_number, c_title, s_section_number, s_section_title, s_section_text, explain, illustration, punishment
```

**Example Row (BNS-303):**
```csv
XVII,Of Offences Against Property,303,Theft,Whoever intending to take dishonestly any movable property...,<explanation>,<illustration>,Imprisonment for 3 years...
```

---

## What Needs to Be Added

### New Columns (6 additional columns):

1. **offence_type** - Simple identifier (e.g., "theft", "snatching", "robbery")
2. **category** - Broader category (e.g., "property_offences")
3. **mens_rea** - Mental elements (pipe-separated)
4. **actus_reus** - Physical acts (pipe-separated)
5. **circumstances** - Contextual requirements (pipe-separated)
6. **basic_keywords** - Fallback keywords (pipe-separated)

### New CSV Structure:

```
c_number, c_title, s_section_number, s_section_title, s_section_text, explain, illustration, punishment,
offence_type, category, mens_rea, actus_reus, circumstances, basic_keywords
```

---

## Where Does This New Data Come From?

### Answer: Legal Analysis of the Section Text

You need to **read each section's legal text** and identify:

1. **Mens Rea (Mental State):** What intent is required?
   - "dishonestly" → `dishonest_intent`
   - "intentionally" → `intentional`
   - "knowing" → `knowledge`

2. **Actus Reus (Physical Act):** What action must be done?
   - "takes property" → `taking_property`
   - "suddenly seizes" → `sudden_taking`
   - "threatens" → `threat_of_harm`
   - "damages property" → `damage_property`

3. **Circumstances (Context):** What conditions must exist?
   - "without consent" → `without_consent`
   - "in dwelling house" → `in_dwelling`
   - "being an employee" → `position_of_trust`

4. **Basic Keywords:** Common words people use
   - Simple words for fallback matching
   - Derived from common usage

---

## Complete Mapping for 10 Main Sections

### BNS-303: Theft

**Section Text Analysis:**
- "intending to take **dishonestly**" → mens_rea: `dishonest_intent`
- "take... movable property" → actus_reus: `taking_property`
- "**without that persons consent**" → circumstances: `without_consent`
- "movable property" → circumstances: `movable_property`

**Add These Values:**
```csv
offence_type: theft
category: property_offences
mens_rea: dishonest_intent
actus_reus: taking_property|moving_property
circumstances: without_consent|movable_property
basic_keywords: stole|stolen|took|taken|taking|theft
```

---

### BNS-304: Snatching

**Section Text Analysis:**
- "Theft is snatching if... **suddenly or quickly or forcibly seizes**"
- Same mens rea as theft (dishonest)
- Special actus reus: sudden taking

**Add These Values:**
```csv
offence_type: snatching
category: property_offences
mens_rea: dishonest_intent
actus_reus: sudden_taking|forcible_seizing
circumstances: without_consent|from_person
basic_keywords: snatched|grabbed|yanked|pulled away|seized
```

---

### BNS-305: Theft in dwelling house

**Section Text Analysis:**
- "commits theft in any building... **used as human dwelling**"
- Same as theft + additional circumstance

**Add These Values:**
```csv
offence_type: dwelling_theft
category: property_offences
mens_rea: dishonest_intent
actus_reus: taking_property
circumstances: without_consent|in_dwelling|human_dwelling
basic_keywords: stole from house|took from home|theft in dwelling|from residence
```

---

### BNS-306: Theft by clerk or servant

**Section Text Analysis:**
- "being a **clerk or servant** or being **employed**"
- Same as theft + position of trust

**Add These Values:**
```csv
offence_type: employee_theft
category: property_offences
mens_rea: dishonest_intent
actus_reus: taking_property
circumstances: without_consent|position_of_trust|employment_relationship
basic_keywords: employee stole|servant took|clerk theft|worker took
```

---

### BNS-308: Extortion

**Section Text Analysis:**
- "**intentionally puts any person in fear**"
- "**dishonestly induces** the person... to **deliver** property"

**Add These Values:**
```csv
offence_type: extortion
category: extortion_robbery
mens_rea: dishonest_intent|intent_to_induce_fear
actus_reus: putting_in_fear|inducing_delivery
circumstances: fear_of_injury|obtaining_property
basic_keywords: threatened|intimidated|blackmailed|extorted|scared into giving
```

---

### BNS-309: Robbery

**Section Text Analysis:**
- "Theft is robbery if... offender **voluntarily causes or attempts to cause death or hurt**"

**Add These Values:**
```csv
offence_type: robbery
category: extortion_robbery
mens_rea: dishonest_intent
actus_reus: taking_property|causing_hurt
circumstances: without_consent|violence_or_fear|threat_of_injury
basic_keywords: robbed|forcefully took|stole with violence|threatened and took
```

---

### BNS-316: Criminal breach of trust

**Section Text Analysis:**
- "being in any manner **entrusted with property**"
- "**dishonestly misappropriates** or **converts to his own use**"

**Add These Values:**
```csv
offence_type: breach_of_trust
category: criminal_breach_of_trust
mens_rea: dishonest_intent
actus_reus: dishonest_misappropriation|converting_to_own_use
circumstances: entrusted_property|dominion_over_property
basic_keywords: misappropriated|embezzled|misused trust|converted|took entrusted property
```

---

### BNS-318: Cheating

**Section Text Analysis:**
- "by **deceiving** any person **fraudulently or dishonestly**"
- "**induces** the person... to **deliver** any property"

**Add These Values:**
```csv
offence_type: cheating
category: fraud_deception
mens_rea: dishonest_intent|fraudulent_intent
actus_reus: deception|inducing_delivery
circumstances: fraudulent_deception|delivery_of_property
basic_keywords: cheated|deceived|tricked|defrauded|lied to get|fake promise
```

---

### BNS-324: Mischief

**Section Text Analysis:**
- "with **intent to cause** wrongful loss or damage"
- "causes the **destruction** of any property or any **change**... as **destroys or diminishes its value**"

**Add These Values:**
```csv
offence_type: mischief
category: property_damage
mens_rea: intent_to_cause_loss|intent_to_damage
actus_reus: destruction_of_property|damage_to_property
circumstances: wrongful_loss|diminution_of_value
basic_keywords: damaged|destroyed|vandalized|broke|ruined|smashed|defaced
```

---

### BNS-329: Criminal trespass

**Section Text Analysis:**
- "**enters into or upon property**"
- "with **intent to commit an offence** or to **intimidate insult or annoy**"
- "in the possession of another" (without permission implied)

**Add These Values:**
```csv
offence_type: criminal_trespass
category: trespass
mens_rea: intent_to_commit_offence|intent_to_intimidate
actus_reus: unlawful_entry|entering_property
circumstances: without_permission|property_of_another
basic_keywords: entered|trespassed|broke in|climbed over|entered without permission
```

---

## How to Create the Enhanced CSV

### Option 1: Manual (Simple, Recommended)

1. **Open** `bns_ch17_final_cleaned.csv` in Excel/Google Sheets
2. **Add 6 new columns** at the end
3. **For each of the 10 sections above**, copy the values I provided
4. **For the other 22 sections**, you can:
   - Leave blank for now (focus on 10 main sections first)
   - Or add basic values later

### Option 2: Python Script (Automated)

I can create a Python script that:
1. Reads your current CSV
2. Has a mapping dictionary with all the new data
3. Adds the new columns automatically
4. Saves as `bns_ch17_enhanced.csv`

---

## Do We Need Additional Research?

### No External Research Needed!

All the data comes from **analyzing the section text** that's already in your CSV:

- **Mens Rea**: Look for words like "dishonestly", "intentionally", "knowingly", "fraudulently"
- **Actus Reus**: Look for action verbs - "takes", "moves", "damages", "enters", "deceives"
- **Circumstances**: Look for conditions - "without consent", "in dwelling", "entrusted with"
- **Keywords**: Think about how regular people would describe these actions in conversation

**I've already done this analysis for the 10 main sections** (see mappings above).

---

## Sample Enhanced CSV Row

**Before (Current):**
```csv
XVII,Of Offences Against Property,303,Theft,Whoever intending to take dishonestly...,<explain>,<illustration>,Imprisonment 3 years...
```

**After (Enhanced):**
```csv
XVII,Of Offences Against Property,303,Theft,Whoever intending to take dishonestly...,<explain>,<illustration>,Imprisonment 3 years...,theft,property_offences,dishonest_intent,taking_property|moving_property,without_consent|movable_property,stole|stolen|took|taken|taking|theft
```

---

## Next Steps

**Tell me which option you prefer:**

1. **Manual:** I'll create a formatted table with all values for 10 sections, you copy-paste into your CSV
2. **Script:** I'll create a Python script that does it automatically

**Which would you prefer?**
