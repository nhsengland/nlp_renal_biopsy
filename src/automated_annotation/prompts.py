### entity identification

ENTITY_IDENTIFICATION_TASK = f"""
You are a medical knowledge extraction system specialising in identifying important medical entities in clinical reports. Your task is to analyse medical reports and identify patterns of key medical entities that clinicians consistently document and rely on for diagnosis.

For the entire corpus of reports, please:

1. First identify the medical domain based on the report content

2. Create a structured analysis with:
- Primary Findings: Key pathological or anatomical features consistently documented
- Measurements: Any quantitative values or scales regularly mentioned
- Descriptive Terms: Common modifiers or qualifiers used
- Associated Terms: Related conditions or complications frequently noted
- Diagnostic Patterns: Combinations of findings that appear diagnostically significant

3. Organise these into suggested entity categories:
- Critical entities: Essential for diagnosis/treatment
- Supporting entities: Provide context but not critical
- Modifier entities: Describe severity/extent/quality
- Temporal entities: Indicate progression/changes

4. For each entity category provide:
- Example extracts from the reports
- Clinical significance
- Common variations in how it's documented

Format your response as a structured list with clear hierarchical organisation.

The reports will be provided after "REPORTS:" with one report per line.
"""

### section header identification

SECTION_HEADER_IDENTIFIER_TASK = f"""
You are a medical text analysis system. Your task is to identify any section headers in pathology reports.

For each report I share, output a dictionary with:
- "has_headers": true/false indicating if any section headers were detected
- "headers": list of identified headers (empty list if none found)
- "reasoning": brief explanation of how you determined if headers exist

Look for these common patterns:
- Capitalised sections followed by colons (e.g., "MICROSCOPIC DESCRIPTION:")
- Numbered or lettered sections (e.g., "1.", "A.")
- Headers in all caps (e.g., "GROSS DESCRIPTION")
- Underlined or emphasised text denoting sections
- Common medical report section names like:
  * Clinical History
  * Gross Description/Examination 
  * Microscopic Description/Examination
  * Diagnosis
  * Comments
  * Specimen

Report text will be provided after "REPORT:" on each line.
Output should be valid JSON.

Example output:
{{
    "has_headers": true,
    "headers": ["CLINICAL HISTORY", "GROSS DESCRIPTION", "MICROSCOPIC"],
    "reasoning": "Found capitalised sections with colons marking distinct report segments"
}}
"""

### guideline creation

GUIDELINE_CREATION_TASK = f"""
We have reports for different patients. Using the entities in the JSON template and the guideline rules,
go over the patient reports and produce a set of guidelines for each entity.
Do NOT produce a set of guidelines per report, do it for the whole report corpus: 

--- JSON TEMPLATE TO USE ---
[{{"cortex_present": {{"current_data_type": "binary", 
             "data_type_changes": "?"
             "entity_scope": "?"}} }},
{{"medulla_present": {{"current_data_type": "binary", 
             "data_type_changes": "?"
             "entity_scope": "?"}} }},
{{"chronic_or_fibrotic_change": {{"current_data_type": "numerical", 
             "data_type_changes": "?"
             "entity_scope": "?"}} }},
{{"diagnosis": {{"current_data_type": "string", 
             "data_type_changes": "?"
             "entity_scope": "?"}} }}]

--- GUIDELINE RULES ---
Your guidelines for the entities should be concise but discuss the following:
- Data type changes: Should the current data type change and why? Possible data types are: binary, categorical, numerical, string.
                     If categories are present, can they be mapped to numbers (e.g. as a severity score)?
- Entity scope: What phrases describe the entity and what phrases do not? If the entity is not mentioned, is their presence implied?
                For phrases that describe the entity, which are common and which are uncommon?
"""

GUIDELINE_EXAMPLE = f"""
--- EXAMPLE JSON FOR CORTEX_PRESENT ---
{{"cortex_present": {{"current_data_type": "binary", 
                    "data_type_changes": "No change is needed,"
                    "lack_of_mention": "If not mentioned, should be assumed not present."
                    "entity_scope": "Will usually mention 'cortex', or occasionally 'cortical area'. 
                                    It can be inferred as 'inner part of kidney'. It is the opposite of the 
                                    medulla which is the outer part of kidney."
                    "categorisation": "No categorisation needed since binary data type."}}
}}
"""

### few-shot creation

def create_few_shots_prompt(num_examples=3):
    prompt = f"""Generate {num_examples} synthetic kidney biopsy reports. Each report must follow this exact format and include all specified components:
    MICROSCOPY:
    - Must mention presence/absence of cortex and medulla
    - Must specify total number of glomeruli (range: 5-30)
    - Must specify number of segmentally sclerosed glomeruli (should be less than total)
    - Must specify number of globally sclerosed glomeruli (should be less than total)
    - Must note presence/absence of non-sclerotic glomerular abnormalities
    - Must describe chronic changes using terms: minimal, mild, moderate, or severe
    - Must mention if it's a transplant biopsy
    - Additional findings may be included if relevant

    CONCLUSION:
    - Final diagnosis including primary disease process
    - If transplant: must include rejection status and severity
    - Keep conclusions concise and clinically relevant

    Example format:
    MICROSCOPY: Cortex present, medulla absent. Total of 15 glomeruli identified, with 2 showing segmental sclerosis and 1 with global sclerosis. No other glomerular abnormalities noted. Moderate chronic changes with tubular atrophy and interstitial fibrosis. Transplant biopsy.

    CONCLUSION: Renal transplant biopsy showing moderate chronic allograft nephropathy without evidence of acute rejection.

    Requirements:
    1. Use only standard medical terminology
    2. Maintain internal consistency between findings and diagnosis
    3. Ensure numbers add up correctly (segmental + global ≤ total glomeruli)
    4. Include all required components while varying presentation
    5. Keep style formal and objective
    6. Avoid using specific dates, patient identifiers, or hospital details

    Generate {num_examples} different examples that vary in findings and diagnoses."""

    return prompt

### entity comparison analysis (in notebook)