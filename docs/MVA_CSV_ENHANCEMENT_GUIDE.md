# MVA Chapter 13 CSV Enhancement Guide

## Purpose
This guide helps enhance `mva13.csv` from 6 columns to 14 columns (matching BNS format) for Neo4j graph-based legal reasoning.

---

## Current Structure (6 columns)
```
Chapter No. | Chapter Name | Section No. | Section Name | Description | Punishment
```

## Target Structure (14 columns)
```
Chapter No. | Chapter Name | Section No. | Section Name | Description | Punishment | offence_type | category | mens_rea | actus_reus | circumstances | basic_keywords
```

---

## Column Enhancement Guide

### 1. `offence_type` (Single value - lowercase with underscores)

**Purpose:** Specific classification of the offence for quick matching

**MVA Chapter 13 Offence Types (Recommended list):**

| Section(s) | offence_type | Description |
|-----------|--------------|-------------|
| 177 | general_violation | Catch-all for unspecified violations |
| 178(1) | travel_without_ticket | Passenger without valid pass/ticket |
| 178(2) | conductor_dereliction | Conductor failing duties |
| 178(3) | refusal_to_ply | Contract carriage refusing service |
| 179(1) | disobedience_obstruction | Obstructing officers or disobeying orders |
| 179(2) | false_information | Withholding/providing false info |
| 180 | allowing_unlicensed_driver | Permitting unlicensed person to drive |
| 181 | driving_without_license | Operating vehicle without valid license |
| 182(1) | driving_while_disqualified | Driving with suspended/revoked license |
| 182(2) | acting_without_conductor_license | Conductor without valid license |
| 182A | construction_maintenance_violation | Non-compliant vehicle standards |
| 183(1) | overspeeding | Exceeding speed limits |
| 183(2) | causing_overspeeding | Employer forcing driver to overspeed |
| 184 | dangerous_driving | Reckless/dangerous manner of driving |
| 185 | drunk_driving | Driving under influence of alcohol/drugs |
| 186 | driving_while_unfit | Driving with physical/mental disability |
| 187 | hit_and_run | Failing to report/assist in accident |
| 188 | abetment_of_offence | Assisting in commission of MVA offence |
| 189 | illegal_racing | Racing/speed trials on public roads |
| 190(1) | unsafe_vehicle | Driving defective/unsafe vehicle |
| 190(2) | pollution_violation | Violating emission/noise standards |
| 190(3) | dangerous_goods_violation | Improper transport of hazardous materials |
| 191 | selling_altered_vehicle | Dealer selling non-compliant vehicles |
| 192 | driving_without_registration | Operating unregistered vehicle |
| 192A | driving_without_permit | Operating without valid permit |
| 193 | unauthorized_agent | Acting as unlicensed agent/canvasser |
| 194(1) | overloading | Exceeding permissible vehicle weight |
| 194(2) | refusing_weighment | Refusing to stop for weight inspection |
| 196 | driving_without_insurance | Operating uninsured vehicle |
| 197(1) | unauthorized_vehicle_taking | Taking vehicle without owner consent |
| 197(2) | vehicle_seizure | Forcibly seizing control of vehicle |
| 198 | vehicle_tampering | Unauthorized interference with vehicle |
| 199 | corporate_offence | Offences by companies/directors |
| 201 | obstruction_of_traffic | Blocking traffic flow with disabled vehicle |
| 202(1), 202(2) | arrestable_offence | Offences allowing arrest without warrant |

---

### 2. `category` (Broader grouping - lowercase with underscores)

**Purpose:** Group related offences for filtering and analysis

**MVA Chapter 13 Categories:**

| Category | Sections Covered | Description |
|----------|------------------|-------------|
| **licensing_offences** | 180, 181, 182(1), 182(2), 193 | License-related violations |
| **vehicle_compliance** | 182A, 190(1), 190(2), 191, 192, 196 | Vehicle registration, insurance, standards |
| **traffic_violations** | 177, 183(1), 183(2), 201 | Speed limits, general traffic rules |
| **dangerous_conduct** | 184, 185, 186, 189 | Reckless, drunk, unfit driving |
| **accident_related** | 187, 188 | Hit-and-run, accident procedures |
| **commercial_vehicle_offences** | 178(1), 178(2), 178(3), 192A, 194(1), 194(2) | Commercial transport violations |
| **vehicle_security** | 197(1), 197(2), 198 | Theft, unauthorized use, tampering |
| **weight_safety** | 190(3), 194(1), 194(2) | Overloading, hazardous goods |
| **procedural_violations** | 179(1), 179(2) | Non-compliance with authority |
| **corporate_liability** | 199 | Company/director offences |
| **enforcement** | 200, 202 | Composition, arrest powers |

---

### 3. `mens_rea` (Mental element - pipe-separated)

**Purpose:** Legal mental state required for the offence

**MVA-specific mens_rea values:**

| mens_rea Value | When to Use | Example Sections |
|----------------|-------------|------------------|
| `wilfully` | Intentional/deliberate acts | 179(1), 179(2), 197(1) |
| `negligently` | Careless/reckless conduct | 178(2), 190(1) |
| `knowingly` | Aware of the condition | 186, 190(1) |
| `none` | Strict liability (no mental element required) | 192, 192A, 196, 194(1) |
| `dishonest_intent` | Intent to deceive | 179(2) false info |
| `recklessly` | Disregard for consequences | 184, 189 |

**How to determine:**
- **Strict liability offences:** Most compliance violations (registration, insurance, permits) = `none`
- **Look for keywords in description:**
  - "wilfully" → `wilfully`
  - "negligently" → `negligently`
  - "knows" or "knowledge" → `knowingly`
  - "intending" → `intent_to_[action]`
- **Dangerous conduct:** Usually `recklessly` or `negligently`

**Examples:**
- Section 185 (drunk driving): `none` (strict liability - blood alcohol level is objective)
- Section 179(2) (false info): `wilfully|knowingly`
- Section 184 (dangerous driving): `recklessly`
- Section 192 (no registration): `none`

---

### 4. `actus_reus` (Physical act - pipe-separated)

**Purpose:** The actual prohibited action

**MVA-specific actus_reus patterns:**

| actus_reus Value | Description | Example Sections |
|------------------|-------------|------------------|
| `driving_vehicle` | Operating a motor vehicle | 181, 184, 185, 186, 192 |
| `causing_vehicle_to_be_driven` | Allowing others to drive | 180, 192, 192A |
| `exceeding_speed_limit` | Driving above prescribed speed | 183(1) |
| `refusing_to_comply` | Disobeying lawful orders | 179(1), 194(2) |
| `withholding_information` | Not providing required info | 179(2) |
| `failing_to_stop` | Not stopping at accident scene | 187 |
| `taking_vehicle_without_consent` | Unauthorized vehicle use | 197(1) |
| `tampering_with_vehicle` | Interfering with vehicle mechanism | 198 |
| `selling_vehicle` | Commercial sale of vehicle | 191 |
| `travelling_in_vehicle` | Being a passenger | 178(1) |
| `conducting_stage_carriage` | Acting as conductor | 178(2) |
| `overloading_vehicle` | Exceeding weight limits | 194(1) |
| `blood_alcohol_over_30mg` | Physical state condition | 185 |
| `causing_obstruction` | Blocking traffic | 201 |
| `racing_vehicles` | Speed competitions | 189 |

**Combination examples:**
- Section 185: `driving_vehicle|blood_alcohol_over_30mg`
- Section 180: `causing_vehicle_to_be_driven|allowing_unlicensed_driver`
- Section 192: `driving_vehicle|causing_vehicle_to_be_driven` (both prohibited)
- Section 197(1): `taking_vehicle_without_consent|driving_away_vehicle`

---

### 5. `circumstances` (Contextual elements - pipe-separated)

**Purpose:** Conditions that must exist for the offence

**MVA-specific circumstances:**

| circumstances Value | Description | Example Sections |
|--------------------|-------------|------------------|
| `in_public_place` | On public road/area | Most sections (184, 185, 186, 190, 192) |
| `without_license` | No valid driving license | 181 |
| `without_registration` | No RC book/registration | 192 |
| `without_permit` | No commercial permit | 192A |
| `without_insurance` | No valid insurance policy | 196 |
| `without_ticket` | No valid pass/ticket | 178(1) |
| `blood_alcohol_over_30mg` | Alcohol exceeds legal limit | 185 |
| `speed_exceeds_limit` | Above Section 112 limits | 183(1) |
| `while_disqualified` | During license suspension | 182(1), 182(2) |
| `vehicle_has_defects` | Known mechanical issues | 190(1) |
| `during_accident` | At accident scene | 187 |
| `weight_exceeds_limit` | Overloaded vehicle | 194(1) |
| `dangerous_to_public` | Creates public danger | 184, 190(1) |
| `in_stage_carriage` | On public transport | 178(1), 178(2) |
| `violates_standards` | Non-compliant with prescribed standards | 182A, 190(2) |
| `without_owner_consent` | No authorization from owner | 197(1) |
| `using_force_or_threat` | Through intimidation | 197(2) |

**Examples:**
- Section 185: `in_public_place|blood_alcohol_over_30mg`
- Section 192: `in_public_place|without_registration`
- Section 184: `in_public_place|dangerous_to_public`
- Section 197(1): `without_owner_consent`

---

### 6. `basic_keywords` (Matching terms - pipe-separated)

**Purpose:** Natural language phrases users might type in queries

**Keyword Strategy:**

1. **Include common phrases** (how citizens talk, not legal jargon)
2. **Include synonyms and variations**
3. **Include Hindi-English mix** (optional: "challan", "RC book")
4. **Include abbreviations** (DUI, RC, PUC)
5. **Include typos/common mistakes** (optional: "lisence")

**Section-by-Section Keyword Examples:**

| Section | basic_keywords |
|---------|----------------|
| 177 | `violation\|broke rule\|traffic rule\|general offence\|MVA violation` |
| 178(1) | `no ticket\|without ticket\|ticketless\|no pass\|travel without paying\|free ride` |
| 178(2) | `conductor refused\|conductor didn't give ticket\|conductor misbehavior` |
| 178(3) | `auto refused\|taxi refused\|driver refused ride\|refused to go\|refusal to ply` |
| 179(1) | `didn't obey\|disobeyed officer\|obstruction\|blocking officer\|refused to comply` |
| 179(2) | `false information\|lied to officer\|fake details\|wrong information\|refused information` |
| 180 | `let someone drive\|allowed unlicensed\|gave keys to\|permitted without license` |
| 181 | `no license\|without license\|driving without DL\|no driving license\|unlicensed driving` |
| 182(1) | `suspended license\|disqualified\|license cancelled\|banned from driving` |
| 182(2) | `conductor without license\|unlicensed conductor` |
| 182A | `modified vehicle\|illegal modification\|non-compliant vehicle\|modified exhaust` |
| 183(1) | `overspeeding\|speeding\|speed limit\|driving too fast\|exceeded speed\|racing` |
| 183(2) | `forced to speed\|employer made me speed\|company forced speeding` |
| 184 | `dangerous driving\|reckless driving\|rash driving\|negligent driving\|endangering public` |
| 185 | `drunk driving\|DUI\|drink and drive\|drinking and driving\|alcohol\|intoxicated\|breathalyzer\|30mg\|drunk\|under influence\|drug driving` |
| 186 | `unfit to drive\|medical condition\|disability driving\|epilepsy driving\|health issue` |
| 187 | `hit and run\|accident ran away\|didn't stop after accident\|fled accident scene\|left accident spot` |
| 188 | `helped someone\|assisted offence\|abetment\|aiding offence` |
| 189 | `racing\|street racing\|speed trial\|illegal race\|drag racing` |
| 190(1) | `defective vehicle\|unsafe vehicle\|faulty brakes\|broken lights\|vehicle in bad condition` |
| 190(2) | `pollution\|smoke\|emission\|loud exhaust\|noise pollution\|PUC expired\|pollution certificate` |
| 190(3) | `carrying explosives\|dangerous goods\|hazardous materials\|chemical transport\|inflammable goods` |
| 191 | `sold illegal vehicle\|dealer sold modified\|showroom sold non-compliant` |
| 192 | `no registration\|unregistered\|no RC\|RC book expired\|registration expired\|no number plate` |
| 192A | `no permit\|without permit\|commercial without permit\|taxi without permit\|permit expired` |
| 193 | `unauthorized agent\|illegal broker\|unlicensed agent` |
| 194(1) | `overloaded\|overloading\|excess weight\|too much weight\|loaded above limit` |
| 194(2) | `refused weighing\|didn't stop for weight check\|avoided weight bridge` |
| 196 | `no insurance\|without insurance\|insurance expired\|uninsured vehicle\|no policy` |
| 197(1) | `took vehicle without permission\|stole car\|took vehicle\|unauthorized use\|joy ride` |
| 197(2) | `hijacked\|vehicle hijack\|forcibly took vehicle\|seized vehicle by force` |
| 198 | `tampered with vehicle\|messed with car\|touched vehicle\|interfered with vehicle` |
| 199 | `company offence\|director liability\|corporate violation` |
| 201 | `blocking road\|vehicle blocking traffic\|obstruction\|parked wrong\|disabled vehicle on road` |
| 202 | `arrested without warrant\|police arrest\|arrest power` |

**Tips for keyword creation:**
- Think: "How would someone describe this situation to a friend?"
- Include both formal ("driving under influence") and informal ("drunk driving")
- Add location-specific terms if relevant ("auto refused" for Indian context)
- Test against real user queries from logs

---

## Enhancement Workflow

### Step 1: Setup
1. Make a backup copy of `mva13.csv`
2. Open in Excel/Google Sheets (easier than text editor)
3. Add 6 new column headers: `offence_type`, `category`, `mens_rea`, `actus_reus`, `circumstances`, `basic_keywords`

### Step 2: Enhance in Batches
**Do 10 sections at a time** to avoid fatigue:

**Batch 1:** Sections 177-183 (basic violations)
**Batch 2:** Sections 184-189 (dangerous conduct)
**Batch 3:** Sections 190-194 (vehicle compliance)
**Batch 4:** Sections 196-202 (serious offences)

### Step 3: For Each Section
1. **Read the description carefully**
2. **Choose offence_type** from the recommended list above
3. **Assign category** based on the grouping table
4. **Identify mens_rea:**
   - Look for "wilfully", "negligently", "knowingly" in description
   - If none found, check if it's strict liability → use "none"
5. **Extract actus_reus:**
   - What is the person physically doing?
   - Use pipe-separated values if multiple acts
6. **Determine circumstances:**
   - What conditions must exist?
   - Always include "in_public_place" if section mentions public place
   - Add specific conditions (without_license, blood_alcohol_over_30mg, etc.)
7. **Brainstorm basic_keywords:**
   - How would a citizen describe this situation?
   - Include 5-10 variations
   - Pipe-separate all keywords

### Step 4: Quality Check
After completing all rows:
- [ ] All 51 sections have values in all 14 columns
- [ ] No empty cells (use "none" if truly not applicable)
- [ ] Pipe separation used correctly (no spaces around pipes)
- [ ] Keywords are lowercase and practical
- [ ] Mens_rea values match the standard list
- [ ] Offence_types are consistent and unique enough

### Step 5: Validation
Test a few rows:
```
Query: "I was caught drunk driving"
Expected match: Section 185
Check: Does "drunk driving|DUI|drink and drive" cover this?

Query: "My RC book is expired"
Expected match: Section 192
Check: Does "no registration|RC book expired" cover this?

Query: "Auto driver refused to take me"
Expected match: Section 178(3)
Check: Does "auto refused|refused to go" cover this?
```

---

## Special Cases

### Procedural Provisions (183(3), 192(2), 195(2), etc.)
These sections don't define offences but explain procedures:
- **offence_type:** Use "procedural_provision"
- **category:** Keep original category
- **mens_rea:** "none"
- **actus_reus:** "none"
- **circumstances:** "procedural_context"
- **basic_keywords:** "procedure|court process|not applicable"

### Subsections (e.g., 190(1), 190(2), 190(3))
Treat each subsection as a separate row with unique values:
- Different offence_types for each
- May share same category
- Different keywords for each

### Sections with "First/Second Offence" Distinction
Keep as single row, mention in keywords:
```
Section 177: "first offence|second offence|repeat violation"
```

---

## Common Pitfalls to Avoid

1. **Don't use spaces around pipes:**
   - ❌ `drunk | driving | DUI`
   - ✅ `drunk|driving|DUI`

2. **Don't leave cells empty:**
   - Use `none` for mens_rea if strict liability
   - Use `not_applicable` if truly doesn't apply

3. **Don't make keywords too formal:**
   - ❌ `contravention of section 112 speed limits`
   - ✅ `overspeeding|driving too fast|speed limit`

4. **Don't duplicate offence_types:**
   - Make each section's offence_type unique and descriptive
   - Use section number suffix if needed: `theft_dwelling` vs `theft_servant`

5. **Don't forget user perspective:**
   - Think: "How would someone report this to police?"
   - Not: "What does the law technically say?"

---

## Testing the Enhanced CSV

After completion, test with these queries:

| User Query | Expected Section | Test Keywords |
|------------|------------------|---------------|
| "I was driving drunk last night" | 185 | drunk\|driving\|DUI |
| "My car doesn't have insurance" | 196 | no insurance\|without insurance |
| "Auto driver refused to take me" | 178(3) | auto refused\|refusal to ply |
| "I was overspeeding on highway" | 183(1) | overspeeding\|speed limit |
| "My vehicle is overloaded" | 194(1) | overloaded\|excess weight |
| "Someone stole my bike" | 197(1) | stole\|took vehicle without permission |
| "Hit and run case" | 187 | hit and run\|fled accident scene |
| "Driving without license" | 181 | no license\|without license |

---

## Final Output Format

```csv
Chapter No.,Chapter Name,Section No.,Section Name,Description,Punishment,offence_type,category,mens_rea,actus_reus,circumstances,basic_keywords
13,"Offences,Penalties and Procedure",185,Driving by a drunken person...,Whoever while driving...,First offence: Imprisonment...,drunk_driving,dangerous_conduct,none,driving_vehicle|blood_alcohol_over_30mg,in_public_place|blood_alcohol_over_30mg,drunk driving|DUI|drink and drive|drinking and driving|alcohol|intoxicated|breathalyzer|30mg|drunk|under influence
```

---

## Estimated Time
- **10 sections:** 1-1.5 hours
- **51 sections total:** 4-6 hours
- **Quality check:** 30 minutes

---

## Questions?
If unsure about any classification:
1. Look at BNS examples in `bns_32_sections_enhanced.csv`
2. Check if similar offences exist in BNS (e.g., theft concepts)
3. When in doubt, be descriptive in offence_type and generous with keywords
4. Remember: More keywords = better matching = happier users

---

## Success Criteria
✅ All 51 rows have 14 columns filled
✅ Keywords cover natural language queries
✅ Offence types are unique and meaningful
✅ Can import into Neo4j using `neo4j_import_enhanced.cypher` (with path updates)
✅ User queries successfully match to correct sections
