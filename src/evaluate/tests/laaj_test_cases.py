# results here given for gemma2:2b
# TODO: update to be in appropriate format
comparison_phrases_pairs = [
    ("Mild chronic allograft nephropathy", "Mild chronic changes only"), # true
    ( "MARKED CHRONIC CHANGES WITH SEVERE CHRONIC VASCULAR CHANGE", "Marked chronic changes with severe chronic vasc   ular change"), # true
    ("No rejection, mild chronic allograft nephropathy", "Mild chronic allograft nephropathy"), # this is true... should it be?
    ("Borderline rejection", "Borderline rejection changes"), # this is false... wrong
    ( "Borderline rejection, mild chronic allograft nephropathy", "Borderline acute rejection and mild chronic allograft nephropathy"), # false... wrong
    ("CHRONIC ALLOGRAFT NEPHROPATHY", "Severe chronic allograft nephropathy"), # true... should it be?
    ("Acute rejection 1A", "Mild chronic changes with superimposed acute cellular rejection, grade 1A"), # true... correct
    ("No rejection, mild chronic allograft nephropathy", "mild chronic allograft nephropathy and mild cyclosporin effect"), # true... should it be?
    ("Very mild borderline rejection", "Very mild borderline acute rejection changes only") # true
]

comparison_cases_small = {
    "exact": [
        ("0", "0"),
        ("moderate", "moderate")
    ],
    "synonyms": [
        ("zero", "0"),
        ("none", "0"),
    ],
    "similar": [
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
    ],
    "different": [
        ("severe CAN", "mild CAN"),
        ("acute rejection", "chronic rejection"),
    ]
}

comparison_cases_medium = {
    "exact": [
        ("0", "0"),
        ("moderate", "moderate"),
        ("True", "True"),
        ("No rejection", "No rejection"),
        ("cortex", "cortex"),
        ("medulla", "medulla"),
        ("fibrosis", "fibrosis"),
        ("TCMR", "TCMR"),
        ("CMV", "CMV"),
        ("glomerulitis", "glomerulitis")
    ],
    
    "synonyms": [
        ("zero", "0"),
        ("False", "Not present"),
        ("True", "Present"),
        ("normal", "unremarkable"),
        ("TCMR", "Acute T-cell-mediated rejection"),
        ("CMV", "Cytomegalovirus infection"),
        ("CAN", "Chronic allograft nephropathy"),
        ("Grade 0", "No rejection"),
        ("renal tissue", "kidney tissue"),
        ("inflammation", "inflammatory changes")
    ],
    
    "similar": [
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
        ("transplant changes", "allograft changes"),
        ("double contours", "two-layer pattern"),
        ("tubular damage", "tubular injury"),
        ("Grade 1A", "Mild acute T-cell mediated rejection"),
        ("Grade 2A", "Grade 2b rejection"),
        ("complete inflammation", "florid inflammation"),
        ("extensive fibrosis", "marked fibrosis"),
        ("notable chronic change", "marked chronic change")
    ],
    
    "different": [
        ("severe CAN", "mild CAN"),
        ("acute rejection", "chronic rejection"),
        ("cellular rejection", "antibody-mediated rejection"),
        ("global sclerosis", "segmental sclerosis"),
        ("cortical scarring", "medullary scarring"),
        ("focal", "diffuse"),
        ("Grade 0", "Grade 3"),
        ("tubular injury", "glomerular injury"),
        ("vascular change", "interstitial change"),
        ("T-cell mediated", "antibody-mediated")
    ]
}

comparison_cases_large = {
    "exact": [
        ("0", "0"),
        ("moderate", "moderate"),
        ("True", "True"),
        ("False", "False"),
        ("No rejection", "No rejection"),
        ("15", "15"),
        ("severe", "severe"),
        ("focal", "focal"),
        ("cortex", "cortex"),
        ("medulla", "medulla"),
        ("fibrosis", "fibrosis"),
        ("hyalinosis", "hyalinosis"),
        ("TCMR", "TCMR"),
        ("CMV", "CMV"),
        ("glomerulitis", "glomerulitis"),
        ("endotheliatis", "endotheliatis"),
        ("oedema", "oedema"),
    ],
    
    "synonyms": [
        ("zero", "0"),
        ("none", "0"),
        ("nil", "0"),
        ("4", "four"),
        ("False", "Not present"),
        ("True", "Present"),
        ("absent", "False"),
        ("normal", "unremarkable"),
        ("normal", "no abnormalities"),
        ("unremarkable", "morphologically normal"),
        ("normal morphology", "no abnormalities"),
        ("TCMR", "Acute T-cell-mediated rejection"),
        ("CMV", "Cytomegalovirus infection"),
        ("CAN", "Chronic allograft nephropathy"),
        ("CTIN", "Chronic tubulointerstitial nephritis"),
        ("FSGS", "Focal segmental glomerulosclerosis"),
        ("MEST", "Cystic hamartoma of the renal pelvis"),
        ("uromodulin", "Tamm-Horsfall protein"),
        ("nuclear loss", "pyknosis"),
        ("vascular disease", "vasculopathy"),
        ("tubular vacuolation", "vacuolated tubules"),
        ("Grade 0", "No rejection"),
        ("renal tissue", "kidney tissue"),
        ("inflammation", "inflammatory changes"),
    ],
    
    "similar": [
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
        ("transplant changes", "allograft changes"),
        ("Fibroelastic initial hyperplasia", "fibrointimal hyperplasia"),
        ("fibrointimal thickening", "fibrointimal hyperplasia"),
        ("double contours", "two-layer pattern"),
        ("BK polyomavirus infection", "BK virus-associated nephropathy"),
        ("capsular crescents", "nephrotic lesions"),
        ("chronic allograft glomerulopathy", "CAN"),
        ("tubular damage", "tubular injury"),
        ("vascular disease", "vasculopathy"),
        ("intimal change", "intimal thickening"),
        ("glomerular injury", "glomerular damage"),
        ("Grade 1A", "Mild acute T-cell mediated rejection"),
        ("Grade 1B", "Rejection Grade 1A"),
        ("rejection Grade 2A", "Moderate-severe acute TCMR"),
        ("Grade 2A", "Grade 2b rejection"),
        ("Grade 3", "Severe acute TCMR with arteritis"),
        ("complete inflammation", "florid inflammation"),
        ("moderate chronic change", "mild chronic change"),
        ("patchy infiltrate", "areas of infiltrate"),
        ("extensive fibrosis", "marked fibrosis"),
        ("florid change", "complete change"),
        ("considerable atrophy", "marked atrophy"),
        ("extensive sclerosis", "global sclerosis"),
        ("notable chronic change", "marked chronic change"),
        ("pronounced vasculitis", "marked vasculitis"),
        ("substantial arteriopathy", "marked arteriopathy")
    ],
    
    "different": [
        ("severe CAN", "mild CAN"),
        ("acute rejection", "chronic rejection"),
        ("cellular rejection", "antibody-mediated rejection"),
        ("chronic infiltrate", "chronic allograft nephropathy"),
        ("global sclerosis", "segmental sclerosis"),
        ("cortical scarring", "medullary scarring"),
        ("acute inflammation", "chronic inflammation"),
        ("vascular rejection", "tubular rejection"),
        ("mild change", "severe change"),
        ("cortex", "medulla"),
        ("focal", "diffuse"),
        ("acute tubulitis", "chronic tubulitis"),
        ("T-cell mediated", "antibody-mediated"),
        ("acute vasculitis", "chronic vasculitis"),
        ("acute ischemia", "chronic ischemia"),
        ("acute fibrosis", "chronic fibrosis"),
        ("tubular injury", "glomerular injury"),
        ("vascular change", "interstitial change"),
        ("mild CAN", "severe CAN"),
        ("Grade 0", "Grade 3"),
        ("Grade 1A", "Grade 2B"),
        ("Grade 1B", "Grade 3"),
        ("No rejection", "Severe rejection"),
    ]
}