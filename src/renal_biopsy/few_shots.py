few_shots_list = [
    """--- EXAMPLE REPORT 1 ---
    \"MICROSCOPY SECTION: Biopsy composed of cortex and medulla with 45 glomeruli, all of which show no morphological abnormality. 
    The tubules, interstitium and vessels appear normal. Immunohistochemical staining is negative for CMV. 
    CONCLUSION SECTION: RENAL BIOPSY: NO EVIDENCE OF REJECTION\" 
    {\"cortex_present\": \"True\", \"medulla_present\": \"True\",
    \"n_total\": \"45\", \"n_segmental\": \"0\", \"n_global\": \"0\", \"abnormal_glomeruli\": \"False\",
    \"chronic_change\": \"0\", \"transplant\": \"True\", \"diagnosis\": \"No rejection\"}
    """,

    """--- EXAMPLE REPORT 2 ---
    \"MICROSCOPY SECTION: Biopsy composed of cortex and medulla with 38 glomeruli, most of which show no morphological abnormality. 
    One glomerulus has global sclerosis, while one has segmental sclerosis. One glomerulus is crushed but there is no infiltrate.
    There are areas of tubular atrophy and interstitial fibrosis over 30% of the biopsy.
    CONCLUSION SECTION: RENAL BIOPSY: SEVERE CHRONIC VASCULAR DAMAGE\" 
    {\"cortex_present\": \"True\", \"medulla_present\": \"True\",
    \"n_total\": \"38\", \"n_segmental\": \"1\", \"n_global\": \"1\", \"abnormal_glomeruli\": \"True\",
    \"chronic_change\": \"30\", \"transplant\": \"False\", \"diagnosis\": \"Severe chronic vascular damage\"}
    """,

    """--- EXAMPLE REPORT 3 ---
    \"MICROSCOPY SECTION: Renal biopsy comprising cortex and containing 25 glomeruli, 3 of which 
    are globally sclerosed. There are minimal irreversible chronic changes of tubular atrophy and interstitial 
    fibrosis. The glomeruli show no significant histological abnormalities. The arteries show no thickening. 
    There is multifocal tubulitis, ranging from mild to severe. A mononuclear cell infiltrate is present 
    within the interstitium, affecting less than 10% of the parenchyma. Neutrophils are not present in peritubular 
    capillaries. The morphological features are those of acute T-cell-mediated rejection, grade 2a.
    CONCLUSION SECTION:  PERCUTANEOUS RENAL BIOPSY (TRANSPLANT): ACUTE T-CELL-MEDIATED REJECTION, GRADE 2a \" 
    {\"cortex_present\": \"True\", \"medulla_present\": \"False\",
    \"n_total\": \"25\", \"n_segmental\": \"0\", \"n_global\": \"3\", \"abnormal_glomeruli\": \"False\",
    \"chronic_change\": \"Minimal\", \"transplant\": \"True\", \"diagnosis\": \"T-cell-mediated rejection, Grade 2A\"}
    """,
]