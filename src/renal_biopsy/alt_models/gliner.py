import re


gliner_label_mapping = {
    "total number of glomeruli": "n_total",
    "number of segmentally-sclerosed glomeruli": "n_segmental",
    "number of globally-sclerosed glomeruli": "n_global",
    "abnormal glomeruli present": "abnormal_glomeruli",
    "chronic change details": "chronic_change",
    "is it a transplant?": "transplant",
    "final diagnosis": "diagnosis",
    "cortex_present": "cortex_present",  # These stay the same
    "medulla_present": "medulla_present",
}


def reorganise_annotations(annotations, gliner_label_mapping):
    # Initialise output dictionary with all possible labels as empty lists
    output = {k: [] for k in gliner_label_mapping.keys()}

    # Process each annotation
    for ann in annotations:
        new_ann = {"start": ann["start"], "end": ann["end"], "label": ann["text"]}
        output[ann["label"]].append(new_ann)

    return output


def process_entry(entry):
    def extract_number(text):
        digits = "".join(filter(str.isdigit, text))
        return int(digits) if digits else 0

    result = {}

    result["cortex_present"] = len(entry["cortex_present"]) > 0
    result["medulla_present"] = len(entry["medulla_present"]) > 0

    if entry["n_total"]:
        # Extract number from text using string operations
        # number_text = entry["n_total"][0]["label"]
        result["n_total"] = extract_number(entry["n_total"][0]["label"])
    else:
        result["n_total"] = 0

    result["n_segmental"] = (
        extract_number(entry["n_segmental"][0]["label"]) if entry["n_segmental"] else 0
    )
    result["n_global"] = (
        extract_number(entry["n_global"][0]["label"]) if entry["n_global"] else 0
    )

    # Process abnormal_glomeruli via regex
    abnormal_pattern = r"""(?ix)
    (?:glomerul(?:ar|i))?
    \s*
    (?:(?P<count>\d+)\s+)?
    (?:scarring|
        isch(?:a)?emic\s+changes|
        thickening\s+of\s+bowman(?:'s)?\s+capsule|
        thickening\s+of\s+(?:capillary\s+)?basement\s+membrane|
        mesangial\s+(?:expansion|thickening)|
        changes?\s+in\s+(?:size|shape)|
        irregular\s+(?:size|shape))
    """
    if entry["abnormal_glomeruli"]:
        text = " ".join(item["label"] for item in entry["abnormal_glomeruli"])
        result["abnormal_glomeruli"] = bool(re.search(abnormal_pattern, text))
    else:
        result["abnormal_glomeruli"] = False

    # Process chronic_change
    if entry["chronic_change"]:
        text = " ".join(item["label"] for item in entry["chronic_change"])
        numbers = "".join(filter(str.isdigit, text))
        result["chronic_change"] = int(numbers) if numbers else 0
    else:
        result["chronic_change"] = 0

    # Process transplant (True if empty, False if present)
    result["transplant"] = len(entry["transplant"]) == 0

    # Process diagnosis (concatenate all text)
    if entry["diagnosis"]:
        result["diagnosis"] = " ".join(item["label"] for item in entry["diagnosis"])
    else:
        result["diagnosis"] = None
    return result


def transform_gliner_annotations(annotated_reports, label_mapping):
    final_annotated_reports = []
    processed_annotated_reports = []
    for annotated_report in annotated_reports:
        final_annotated_report_temp = reorganise_annotations(
            annotated_report, label_mapping
        )
        final_annotated_report = {
            label_mapping[k]: v for k, v in final_annotated_report_temp.items()
        }
        final_annotated_reports.append(final_annotated_report)
        processed_annotated_reports.append(process_entry(final_annotated_report))
    return final_annotated_reports, processed_annotated_reports
