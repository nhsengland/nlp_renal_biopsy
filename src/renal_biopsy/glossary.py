# NOTE: everything here in renal context
# NOTE: types of definitions: conditions, anatomy of kidney
# TODO: automate this glossary creation

# {term : ([synonyms], definition, additional info)}
medical_terms = {
    "Acute cellular rejection": (
        [], 
        "Presents in transplant recipient with acute kidney injury and decreased urine output.", 
        ""
    ),
    "Acute pyelonephritis": (
        [], 
        "An infection of one or both kidneys usually caused by bacteria arising in the bladder.", 
        ""
    ),
    "Acute T-cell-mediated rejection": (
        ["TCMR"], 
        "A reaction that can occur after a transplant when the recipient's T cells attack the donor organ.", 
        ""
    ),
    "Acute tubular necrosis": (
        [], 
        "Medical condition involving the death of tubular epithelial cells that form the renal tubules of the kidneys.", 
        ""
    ),
    "Arteriolar hyalinosis": (
        [], 
        "Common vascular lesion seen in diseases involving the renal vasculature.", 
        ""
    ),
    "Arterioles": (
        [], 
        "A very small blood vessel that branches off from your artery and carries blood away from your heart to your tissues and organs.", 
        "Arterioles are small arteries that link up to capillaries, which are even smaller."
    ),
    "Basement membrane": (
        [], 
        "A thin, adhesive layer that attaches kidney tubule epithelial cells to interstitial connective tissue.", 
        "There are two types: glomerular basement membrane (GBM) and tubular basement membrane (TBM)."
    ),
    "BK polyomavirus infection": (
        ["BK virus-associated nephropathy"], 
        "Infection typically associated with patients who have had a kidney transplant. Presentation in immunocompromised patients is severe.", 
        ""
    ),
    "Calcineurin-inhibitor-induced effect": (
        [], 
        "Calcineurin inhibitors bind to cytoplasmic immunophilins to form complexes that inhibit calcineurin, blocking protein transcription.", 
        "It's a rare but debilitating complication of organ transplantation."
    ),
    "Capillary loops": (
        [], 
        "The loops that make up each glomerulus.", 
        ""
    ),
    "Capsule": (
        [], 
        "Thin membranous sheath that covers the outer surface (cortex) of each kidney.", 
        "Composed of tough fibres, chiefly collagen and elastin (fibrous proteins), that help support the kidney mass and \
        protect the vital tissue from injury."
    ),
    "Capsular crescents": (
        ["nephrotic lesions"], 
        "Hyperplastic lesions which are signs of severe glomerular injury.", 
        "Hallmark of inflammatory glomerulonephritis."
    ),
    "Chronic allograft nephropathy": (
        ["Chronic allograft glomerulopathy", "CAN"], 
        "Generic term to describe chronic interstitial fibrosis and tubular atrophy commonly seen in kidney transplants.", 
        "It's not a synonym for rejection."
    ),
    "Chronic tubulointerstitial nephritis": (
        ["CTIN"], 
        "Long-term, progressive condition that causes irreversible kidney damage.", 
        "Characterized by inflammation and scarring in the kidneys."
    ),
    "Cortex": (
        [], 
        "The outside of the kidney. Surrounds the medulla (inside of the kidney).", 
        "Covered by the renal capsule which is a layer of tougher protective tissue."
    ),
    "Cortical necrosis": (
        [], 
        "One of the causes of prerenal acute kidney injury, caused by a sudden drop in blood perfusion to the renal cortex.", 
        ""
    ),
    "Creatinine": (
        [], 
        "A waste product from muscle metabolism, used as a measure of kidney filtration function.", 
        "Rising levels can indicate kidney dysfunction."
    ),
    "Cyclosporine toxicity": (
        [], 
        "Constriction of afferent renal arteriole.", 
        ""
    ),
    "Cystic hamartoma of the renal pelvis": (
        ["Mixed epithelial and stromal tumor", "MEST"], 
        "A rare, benign tumor of the kidney.", 
        ""
    ),
    "Cytomegalovirus infection": (
        ["Cytomegalovirus", "CMV", "CMV infection"], 
        "Common infection from a herpes virus.", 
        ""
    ),
    "Double contours": (
        ["Two-layer pattern"], 
        "Type of histopathology pattern on the glomerular basement membrane.", 
        ""
    ),
    "DTPA": (
        [], 
        "A radioisotope used to measure function of the kidneys.", 
        "Used to see how the left and right kidney work comparatively."
    ),
    "Eccentric": (
        [], 
        "Adjective to describe thickening/hyperplasia inside the lumen which takes up space.", 
        ""
    ),
    "Endotheliatis": (
        [], 
        "Immune response within endothelium, where endothelial cells become inflamed.", 
        "Can cause oedema of the surrounding tissue. Note: endothelial cells line interior surface of blood vessels.\
        This seems to be more associated with arteries vs glomerulitis which is for glomeruli/capillaries."
    ),
    "Eosinophils": (
        [], 
        "White blood cell that combat against parasitic infections and participate in allergic reactions.", 
        ""
    ),
    "Eosinophilic casts": (
        [], 
        "Urinary casts (nmicroscopic cylindrical structures produced by kidney) that contain eosinophils.", 
        "Seen in tubulointerstitial nephritis."
    ),
    "Epithelial cell vacuolation": (
        [], 
        "formation of vacuoles or vacuole-like structures within or adjacent to cells.", 
        ""
    ),
    "Fibrinoid necrosis": (
        [], 
        "death of cells in small blood vessels due to antigen-antibody complexes and fibrin deposits in walls of blood vessels.", 
        ""
    ),
    "Fibrointimal hyperplasia": (
        ["Fibroelastic initial hyperplasia", "fibrointimal thickening"], 
        "Thickening of intima due to vascular smooth muscle cells, resulting in narrowing of lumen.", 
        "Fibrointimal thickening is not necessarily bad but hyperplasia implies it is unusual."
    ),
    "Fibroplasia": (
        [], 
        "Growth of fibrous tissue.", 
        ""
    ),
    "Fibrosis": (
        [], 
        "Formation of excess fibrous connective tissue in an organ or tissue as a reparative process.", 
        "Sclerosis is a specific type of fibrosis, foten related to autoimmune or chronic inflammatory conditions."
    ),
    "Florid": (
        [], 
        "Fully-developed.", 
        ""
    ),
    "Focal": (
        [], 
        "Adjective describing how much of the kidney core is affected. Focal means <50% covered; if >50%, say diffuse.", 
        "It is not realted to global/complete vs segemntal/partial."
    ),
    "Focal segmental glomerulosclerosis": (
        ["FSGS"], 
        "disease in which scar tissue develops on the glomeruli, resulting in poorer kidney filtration and protein presence\
        in the urine due to protein loss.", 
        ""
    ),
    "Glomerulitis": (
        [], 
        "term used when inflammation has restricted glomeruli.", 
        ""
    ),
    "Glomerulus": (
        [], 
        "Network of capillaries (also called a capillary tuft) at the beginning of nephron in kidney.", 
        "Blood enters glomerulus through afferent arterioles and exits via efferent arterioles."
    ),
    "Glomerulonephritis": (
        [], 
        "Inflammation and damage to the filtering part of the kidneys (glomeruli).", 
        ""
    ),
    "Haemosiderin deposition": (
        [], 
        "Issue caused by blood leaking out of capillaries, leaving residue of haemoglobin in tissues.", 
        ""
    ),
    "Hyaline": (
        [], 
        "Substance that is some combination of protein, collagen, and ECM, and provides cushioning for joints.", 
        ""
    ),
    "Hyalinosis": (
        [], 
        "Accumulation of hyaline in tissue.", 
        "Associated with damage to blood vessels or glomeruli."
    ),
    "Hydronephrosis": (
        [], 
        "Condition where one or both kidneys become stretched and swollen due to urine buildup.", 
        ""
    ),
    "Hypertensive vasculopathy": (
        [], 
        "Endothelial dysfunction and arterial remodeling.", 
        ""
    ),
    "Hypertrophy": (
        [], 
        "A consequence of sustained glomerular hypertension and hyperfiltration that often precedes the development of glomerulosclerosis.", 
        ""
    ),
    "Hypoperfusion": (
        [], 
        "(too) low blood flow through renal tissue.", 
        ""
    ),
    "Hypovolaemia": (
        [], 
        "low blood volume usually caused by dehydration or excessive bleeding.", 
        ""
    ),
    "Immunoreactant": (
        [], 
        "refers to an antigen or antibody.", 
        ""
    ),
    # NOTE: not sure when infiltrate is actually bad vs normal response to transplant
    "Infiltrate": (
        ["lymphocytic infiltrate"], 
        "cells that have come into areas of the kidney, indicating inflammation.", 
        "Refers to non-cancerous cell build-up."
    ),
    "Internal elastic lamina": (
        [], 
        "layer of elastic tissue that forms the outermost part of the tunic intima of blood vessels.", 
        ""
    ),
    "Interstitial": (
        [], 
        "the parts between blood vessels and kidney filters.", 
        ""
    ),
    "Interstitial fibrosis": (
        [], 
        "accumulation of collagen and related molecules in the interstitium.", 
        ""
    ),
    "Intima": (
        [], 
        "innermost coating/membrane of an organ, especially of a vein or artery.", 
        ""
    ),
    "Intimal endarteritis": (
        [], 
        "inflammation of the inner lining of the artery.", 
        ""
    ),
    "Intimal fibroplasia": (
        [], 
        "circumferential or eccentric deposition of collagen in intima with no lipid or inflammatory component.", 
        ""
    ),
    "Intimal fibrous thickening": (
        [], 
        "accumulation of endothelial cells, fibroblastic-like cells, and collagen.", 
        ""
    ),
    "Intimal proliferation": (
        [], 
        "associated with induced proliferation of fibroblasts and smooth muscle cells within subendothelial region i.e. precursor to thickening.", 
        ""
    ),
    "Ischemia": (
        [], 
        "less-than-normal amount of blood flow to part of your body.", 
        "Often a result of glomeruli sclerosing and tissue fibrosing."
    ),
    "Loop of Henle": (
        [], 
        "Part of kidney whose function is to recover water and sodium chloride from urine.", 
        ""
    ),
    "Lumen": (
        [], 
        "Refers to inside space of tubular structure. Used to describe inside of blood vessels.", 
        ""
    ),
    "Lupus nephritis": (
        [], 
        "inflammation of the kidneys caused by systemic lupus erythematosus, an autoimmune disease.", 
        "Type of glomerulonephritis (where glomeruli become inflamed)."
    ),
    "Lymphocytic infiltration": (
        [], 
        "Lots of WBCs have come into kidney indicating immune system activation in the kidney.", 
        "May suggest post-transplant response. Some response expected but too many cells is bad as body's rejecting."
    ),
    "Lymphoproliferative disorders": (
        [], 
        "a group of conditions where lymphocytes are produced in excessive quantities.", 
        ""
    ),
    "Medulla": (
        [], 
        "Inside of the kidney.", 
        ""
    ),
    "Mesangial expansion": (
        [], 
        "occurs due to increased deposition of ECM proteins into the mesangium.", 
        "Characteristic of diabetic nephropathy.\
        Mesangial expansion and the degree of fibrosis present correlate inversely with glomerular filtration rate. \
        So mesangial expansion and increased fibrosis mean worse filtration. "
        # NOTE: used as alternative phrase to global sclerosis hence it is not sclerosis
    ),
    "Mononuclear cells": (
        ["mononuclear inflammatory cells"], 
        "WBC with a single round nucleus, including lymphocytes and monocytes.", 
        "Often indicative of inflammtion in kidney. May relate to tubulitis but is not tubulitis itself (kind of a precursor)."
    ),
    "Morphological": (
        [], 
        "relates to the structure and form of things.", 
        ""
    ),
    "Mural": (
        [], 
        "Adjective which signifies noun is of the wall of a hollow organ or structure.", 
        ""
    ),
    "Myointimal": (
        [], 
        "relating to the smooth muscle cells of the intima of a blood vessel.", 
        ""
    ),
    "Neutrophils": (
        [], 
        "WBC that are the first line of the immune system.", 
        ""
    ),
    "Nodular glomerulosclerosis": (
        [], 
        "Condition where nodules of pink hyaline material form in glomerular capillary loops due to increase in mesangial matrix.", 
        ""
    ),
    "Oedema": (
        [], 
        "Condition characterized by excess watery fluid collecting in cavities or tissues of the body.", 
        ""
    ),
    "Parenchyma": (
        [], 
        "Functional part of the kidney that includes cortex and medulla.", 
        ""
    ),
    "Percutaneous renal biopsy": (
        [], 
        "A needle is placed through the skin that lies over the kidney and guided to the right place in kidney to obtain a sample.", 
        "Percutaneous means through the skin. Different from open biopsy where kidney sample \
        taken directly from kidney during surgery."
    ),
    "Perfusion": (
        [], 
        "blood flow that passes through a unit mass of renal tissue within a given time (mL/min/g).", 
        ""
    ),
    "Peritubular capillaries": (
        [], 
        "capillaries that wrap around the proximal convoluted tubule.", 
        "So, the blood comes in through the afferent arteriole and goes into the glomerulus. Some gets filtered \
        through the BC and into the proximal convoluted tubule. Some doesn't get filtered and goes to the \
        efferent arteriole and then the peritubular capillaries which wrap round the proximal convoluted tubule.  "
    ),
    "Pleomorphic": (
        [], 
        "having variation in the size and shape of cells or their nuclei.", 
        ""
    ),
    "Pyknosis": (
        ["nuclear loss", "nuclear pyknosis"], 
        "shedding/loss of lining epithelial cells indicative of patchy acute tubular necrosis.", 
        ""
    ),
    "Renal artery thrombosis": (
        [], 
        "formation of a clot in a renal artery, potentially causing kidney failure.", 
        ""
    ),
    "Renal infarction": (
        [], 
        "Rare ischaemic event caused by occlusion of the renal artery or its branches.", 
        ""
    ),
    "Sclerosis": (
        [], 
        "hardening of tissue, especially in the context of renal biopsies.", 
        "Can refer specifically to glomerulosclerosis. \
        Sclerosis is inside bit of glomerulus; fibrosis is bit of kidney outside of glomerulus. Sclerosis happesn to glomerulus itself."
    ),
    "Tamm-Horsfall protein": (
        ["uromodulin"], 
        "the most abundant protein excreted in ordinary urine, produced in the ascending limb of the loop of Henle.", 
        ""
    ),
    "T-lymphocytes": (
        [], 
        "WBC that play a central role in the adaptive immune response.", 
        ""
    ),
    "Thrombus": (
        [], 
        "A blood clot.", 
        ""
    ),
    "Tubular atrophy": (
        [], 
        "Describes patterns of chronic tubular injury with thickened tubular basement membranes.", 
        "A hallmark of chronic kidney disease that results in decreased glomerular filtration rate."
    ),
    "Tubular basement membranes": (
        [], 
        "Thin dense layer of ECM that lines most human tissues and supports epithelial tissue.", 
        ""
    ),
    "Tubulitis": (
        [], 
        "Presence of inflammatory cells in the tubular wall, often indicating acute renal allograft rejection.", 
        ""
    ),
    "Tubulointerstitial nephritis": (
        [], 
        "Inflammation of renal interstitium.", 
        ""
    ),
    "Tunic intima": (
        [], 
        "Innermost and narrowest layer of the artery.", 
        ""
    ),
    "Ureter": (
        [], 
        "Tube that carries urine from kidney to the urinary bladder.", 
        "There are two ureters, one attached to each kidney."
    ),
    "Vacuolated": (
        [], 
        "Formed into or containing vacuoles within a cell.", 
        "Tubular vacuolisation may cause gradual swelling that may lead to narrowing of lumens but not complete occlusion."
    ),
    "Vasculitis": (
        [], 
        "Describes conditions causing inflammation in blood vessels.", 
        ""
    ),
    "Vasculopathy": (
        ["vascular disease"], 
        "General term for any disease affecting blood vessels.", 
        ""
    ),
    "Venous radicles": (
        [], 
        "Blood vessels that carry blood from the GI tract to the liver.", 
        "These are portal veins i.e. blood vessels that carry blood from GI tract, gallbladder, pancreas, and spleen to the liver."
    ),
}