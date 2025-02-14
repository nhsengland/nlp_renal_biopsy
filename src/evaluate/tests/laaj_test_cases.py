# results here given for gemma2:2b
# TODO: update to be in appropriate format
comparison_phrases_pairs = [
    ("Mild chronic allograft nephropathy", "Mild chronic changes only"),  # true
    (
        "MARKED CHRONIC CHANGES WITH SEVERE CHRONIC VASCULAR CHANGE",
        "Marked chronic changes with severe chronic vasc   ular change",
    ),  # true
    (
        "No rejection, mild chronic allograft nephropathy",
        "Mild chronic allograft nephropathy",
    ),  # this is true... should it be?
    ("Borderline rejection", "Borderline rejection changes"),  # this is false... wrong
    (
        "Borderline rejection, mild chronic allograft nephropathy",
        "Borderline acute rejection and mild chronic allograft nephropathy",
    ),  # false... wrong
    (
        "CHRONIC ALLOGRAFT NEPHROPATHY",
        "Severe chronic allograft nephropathy",
    ),  # true... should it be?
    (
        "Acute rejection 1A",
        "Mild chronic changes with superimposed acute cellular rejection, grade 1A",
    ),  # true... correct
    (
        "No rejection, mild chronic allograft nephropathy",
        "mild chronic allograft nephropathy and mild cyclosporin effect",
    ),  # true... should it be?
    (
        "Very mild borderline rejection",
        "Very mild borderline acute rejection changes only",
    ),  # true
]

comparison_cases_small = {
    "exact": [("0", "0"), ("moderate", "moderate")],
    "same_concept": [
        ("zero", "0"),
        ("none", "0"),
    ],
    "similar_enough": [
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
    ],
    "different": [
        ("severe CAN", "mild CAN"),
        ("acute rejection", "chronic rejection"),
    ],
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
        ("CMV", "CMV"),
        ("glomerulitis", "glomerulitis"),
    ],
    "same_concept": [
        ("zero", "0"),
        ("False", "Not present"),
        ("True", "Present"),
        ("normal", "unremarkable"),
        ("TCMR", "Acute T-cell-mediated rejection"),
        ("CMV", "Cytomegalovirus infection"),
        ("CAN", "Chronic allograft nephropathy"),
        ("Grade 0 rejection", "No rejection"),
        ("renal tissue", "kidney tissue"),
        ("inflammation", "inflammatory changes"),
        ("no rejection", "no acute rejection"),
        ("borderline rejection", "borderline rejection changes"),
        (
            "borderline rejection, mild chronic allograft nephropathy",
            "borderline rejection changes and mild chronic allograft nephropathy",
        ),
        ("no rejection", "no significant rejection"),
        (
            "patchy renal cortical necrosis",
            "changes consistent with healing patchy renal cortical necrosis",
        ),
        ("borderline rejection", "borderline allograft rejection changes (Banff)"),
    ],
    "similar_enough": [
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
        ("transplant changes", "allograft changes"),
        ("double contours", "two-layer pattern"),
        ("tubular damage", "tubular injury"),
        ("Grade 1A rejection", "Mild rejection"),
        ("Grade 2A rejection", "Grade 2b rejection"),
        ("complete inflammation", "florid inflammation"),
        ("extensive fibrosis", "marked fibrosis"),
        ("notable chronic change", "marked chronic change"),
        (
            "No rejection, mild chronic allograft nephropathy",
            "mild chronic allograft nephropathy and no acute rejection",
        ),
        (
            "Very mild borderline rejection",
            "Very mild borderline acute rejection changes only",
        ),
        ("Severe", "greater than two thirds"),
        ("Severe", "two thirds"),
        ("Severe", "2/3"),
        ("small area", "mild to moderate"),
        ("minor", "slight"),
        ("some", "moderate"),
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
        ("T-cell mediated", "antibody-mediated"),
    ],
}

comparison_cases_large = {
    "exact": [
        # numbers
        ("0", "0"),
        ("15", "15"),
        ("18%", "18%"),
        # booleans
        ("True", "True"),
        ("False", "False"),
        # key concepts
        ("cortex", "cortex"),
        ("fibrosis", "fibrosis"),
        ("tubular atrophy", "tubular atrophy"),
        ("interstitial fibrosis", "interstitial fibrosis"),
        ("glomerulosclerosis", "glomerulosclerosis"),
        ("glomerulitis", "glomerulitis"),
        ("oedema", "oedema"),
        ("chronic infiltrate", "chronic infiltrate"),
        # severity
        ("moderate chronic change", "moderate chronic change"),
        ("No rejection", "No rejection"),
        ("severe tubular atrophy", "severe tubular atrophy"),
        ("focal sclerosis", "focal sclerosis"),
        # abbreviations
        ("CAN", "CAN"),
        ("CMV", "CMV"),
        ("EBV", "EBV"),
    ],
    "same_concept": [
        # numbers
        ("zero", "0"),
        ("none", "0"),
        ("nil", "0"),
        ("4", "four"),
        ("5", "5%"),
        # harder booleans that require inference
        ("False", "Not present"),
        ("True", "Present"),
        ("absent", "False"),
        # abbreviations
        ("TCMR", "Acute T-cell-mediated rejection"),
        ("CMV", "Cytomegalovirus infection"),
        ("CAN", "Chronic allograft nephropathy"),
        ("CTIN", "Chronic tubulointerstitial nephritis"),
        ("FSGS", "Focal segmental glomerulosclerosis"),
        ("MEST", "Cystic hamartoma of the renal pelvis"),
        ("severe chronic allograft nepropathy", "severe CAN"),
        # different phrases for same concept
        ("fibrosis", "fibrotic change"),
        ("the tissue is fibrosed", "there is fibrosis"),
        ("vascular disease", "vasculopathy"),
        ("tubular vacuolation", "vacuolated tubules"),
        ("Grade 0 rejection", "No rejection"),
        ("renal tissue", "kidney tissue"),
        ("inflammation", "inflammatory changes"),
        ("Borderline rejection", "Borderline rejection changes"),
        ("features suggestive of rejection", "there is rejection"),
        ("no rejection", "no acute rejection"),
        ("borderline rejection", "borderline rejection changes"),
        (
            "borderline rejection, mild chronic allograft nephropathy",
            "borderline rejection changes and mild chronic allograft nephropathy",
        ),
        ("no rejection", "no significant rejection"),
        (
            "patchy renal cortical necrosis",
            "changes consistent with healing patchy renal cortical necrosis",
        ),
        ("borderline rejection", "borderline allograft rejection changes (Banff)"),
        # misspellings and syntax differences
        ("chronic allograf neprhopathy", "Chronic allograft nephropathy"),
        ("vasclpathy", "vasculopathy"),
        ("inflammation", "inflammaton"),
        (
            "MARKED CHRONIC CHANGES WITH SEVERE CHRONIC VASCULAR CHANGE",
            "Marked chronic changes with severe chronic vasc   ular change",
        ),
        # challenging synonyms that requires prior knowledge
        ("uromodulin", "Tamm-Horsfall protein"),
        ("nuclear loss", "pyknosis"),
        # synonyms for normal clinical presentation
        ("normal", "unremarkable"),
        ("normal", "no change"),
        ("normal", "no abnormalities"),
        ("unremarkable", "morphologically normal"),
        ("normal morphology", "no abnormalities"),
    ],
    "similar_enough": [
        # similar enough
        ("glomerular change", "glomerulosclerosis"),
        ("rejection", "allograft rejection"),
        ("transplant changes", "allograft changes"),
        ("Fibroelastic initial hyperplasia", "fibrointimal hyperplasia"),
        ("fibrointimal thickening", "fibrointimal hyperplasia"),
        ("double contours", "two-layer pattern"),
        ("BK polyomavirus infection", "BK virus-associated nephropathy"),
        ("capsular crescents", "nephrotic lesions"),
        ("chronic allograft glomerulopathy", "chronic allograft nephropathy"),
        ("tubular damage", "tubular injury"),
        ("intimal change", "intimal thickening"),
        ("glomerular injury", "glomerular damage"),
        ("Grade 1A rejection", "Mild rejection"),
        ("rejection Grade 2A", "Moderate rejection"),
        ("Grade 3 rejection", "Severe acute rejection"),
        ("complete inflammation", "florid inflammation"),
        ("patchy infiltrate", "areas of infiltrate"),
        ("extensive fibrosis", "marked fibrosis"),
        ("florid change", "complete change"),
        ("considerable atrophy", "marked atrophy"),
        ("notable chronic change", "marked chronic change"),
        ("pronounced vasculitis", "marked vasculitis"),
        (
            "cellular rejection",
            "antibody-mediated rejection",
        ),  # these are different but we can treat as same
        ("small foci", "minor"),
        ("a lot", "a lot asakja;os;a"),
        ("no rejection", "no rejection, mild cyclosporin effect"),
        (
            "mild rejection",
            "Very mild acute rejection with a prominent interstitial infiltrate",
        ),
        # phrases that are close enough
        ("Mild chronic allograft nephropathy", "Mild chronic changes only"),
        # nested phrases
        (
            "No rejection, mild chronic allograft nephropathy",
            "Mild chronic allograft nephropathy",
        ),
        (
            "Acute rejection 1A",
            "Mild chronic changes with superimposed acute cellular rejection, grade 1A",
        ),
        (
            "No rejection, mild chronic allograft nephropathy",
            "mild chronic allograft nephropathy and no acute rejection",
        ),
        (
            "Very mild borderline rejection",
            "Very mild borderline acute rejection changes only",
        ),
        ("Severe", "greater than two thirds"),
        ("Severe", "two thirds"),
        ("small area", "mild to moderate"),
        ("minor", "slight"),
        ("some", "moderate"),
        ("extensive sclerosis", "global sclerosis"),
        # numerical ranges
        ("1", "<1%"),
        ("1%", "minimal, <1%"),
        ("1", "minimal, <1%"),
        ("Marked, more than 75%", "75%"),
        ("40", "40% and 50% for capillary loops"),
        ("5", "5% and 10% (mild to moderate)"),
        ("5", "less than 5"),
        ("3", "3-5"),
        # multiple adjectives
        ("mild and patchy", "mild"),
        ("mild and patchy", "patchy"),
        ("mild to moderate", "mild"),
        ("mild to moderate", "moderate"),
        ("mild to moderate", "mild and moderate"),
        ("5 (mild, patchy)", "mild"),
        ("5 (mild, patchy)", "patchy"),
        ("5 (mild, patchy)", "5"),
        ("mild to moderate", "moderate to severe"),
    ],
    "different": [
        # different concepts
        ("cortex", "medulla"),
        ("cortex", "infiltrate"),
        ("severe chronic changes", "mild cyclosporin effect"),
        # different concepts that could be mistaken for the same thing
        # (e.g. because similar adjective)
        ("focal sclerosis", "diffuse sclerosis"),
        ("T-cell mediated rejection", "antibody-mediated rejection"),
        ("cortical scarring", "medullary scarring"),
        ("tubular injury", "glomerular injury"),
        # varying severity
        ("severe allograft nephropathy", "mild allograft nephropathy"),
        ("moderate chronic change", "mild chronic change"),
        ("acute rejection", "chronic rejection"),
        ("global sclerosis", "segmental sclerosis"),
        ("acute inflammation", "chronic inflammation"),
        (
            "CHRONIC ALLOGRAFT NEPHROPATHY",
            "Severe chronic allograft nephropathy",
        ),  # unknown
        # different severity
        ("0%", "75%"),
        ("0", "75"),
        # rejection grades
        ("0", "Category IV"),
        ("0", "Grade 2"),
        ("Grade 1A", "Grade 2B"),
        ("Grade 1B rejection", "Rejection Grade 1A"),
        ("Grade 2A", "Grade 2b rejection"),
        # null values automatically wrong (ensures these are filled in
        # by doctors if needed)
        ("0", "null"),
        ("0", "NaN"),
        ("4", "None"),
        ("50", "NaN"),
        ("NaN", "None"),
        ("null", "null"),
        # numbers and words
        ("0", "patchy"),
        ("0", "mild"),
        ("mild to moderate", "50"),
        # random
        ("some", "interstitial fibrosis"),
        ("interstitial", "scattered"),
    ],
}
