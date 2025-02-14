import json


def predict_NuExtract(model, tokenizer, text, schema, example=["", "", ""]):
    schema = json.dumps(json.loads(schema), indent=4)
    input_llm = "<|input|>\n### Template:\n" + schema + "\n"
    for i in example:
        if i != "":
            input_llm += "### Example:\n" + json.dumps(json.loads(i), indent=4) + "\n"

    input_llm += "### Text:\n" + text + "\n<|output|>\n"
    input_ids = tokenizer(
        input_llm, return_tensors="pt", truncation=True, max_length=4000
    )

    output = tokenizer.decode(model.generate(**input_ids)[0], skip_special_tokens=True)
    return output.split("<|output|>")[1].split("<|end-output|>")[0]


def text_to_number(text):
    """Convert text representation of numbers to integers."""
    if text == "":
        return "0"

    # Handle word numbers
    number_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
    }

    text = text.lower().strip()
    if text in number_map:
        return number_map[text]

    # Try to extract first number from text
    import re

    numbers = re.findall(r"\d+", text)
    return str(numbers[0]) if numbers else "0"


def text_to_boolean(text):
    """Convert text to boolean based on specific rules."""
    if not text:
        return "False"

    text = text.lower().strip()
    # cortext and medulla
    if "cortex" in text:
        return "True"
    if "medulla" in text:
        return "True"
    if text == "present":
        return "True"

    # transplant
    if "transplant" in text:
        return "True"

    # cortex/medulla/transplant
    if text == "yes":
        return "True"

    return "False"


def abnormal_transform(text):
    if "no " in text or text == "":
        return "False"
    else:
        return "True"


def extract_percentage(text):
    """Extract percentage from text, defaulting to 0."""
    import re

    match = re.search(r"(\d+)%", text)
    return str(match.group(1)) if match else ""


def transform_nuextract_report(report):
    """Transform a single report according to specified rules."""

    # Define key mappings
    key_mappings = {
        "Cortex presence": "cortex_present",
        "Medulla presence": "medulla_present",
        "Number of total glomeruli": "n_total",
        "Number of segmentally-sclerosed glomeruli": "n_segmental",
        "number of globally-sclerosed glomeruli": "n_global",
        "Presence of abnormal glomeruli": "abnormal_glomeruli",
        "Percentage of chronic change": "chronic_change_per",
        "Severity of chronic change": "chronic_change_adj",
        "Is it a transplant biopsy?": "transplant",
        "Grade of rejection": "rejection",
        "Final diagnosis": "diagnosis",
    }

    transformed = {}

    for old_key, new_key in key_mappings.items():
        value = report.get(old_key, "")

        # Apply transformations based on field type
        if new_key in ["cortex_present", "medulla_present", "transplant"]:
            transformed[new_key] = text_to_boolean(value)
        elif new_key in ["abnormal_glomeruli"]:
            transformed[new_key] = abnormal_transform(value)
        elif new_key in ["n_total", "n_segmental", "n_global"]:
            transformed[new_key] = text_to_number(value)
        elif new_key == "chronic_change_per":
            transformed[new_key] = extract_percentage(value)
        else:
            transformed[new_key] = value if value else ""

    transformed["chronic_change"] = (
        transformed["chronic_change_per"]
        if transformed["chronic_change_per"] != ""
        else transformed["chronic_change_adj"]
    )
    if transformed["chronic_change"] == "":
        transformed["chronic_change"] == 0

    return transformed


def transform_nuextract_reports(reports):
    """Transform a list of reports."""
    return [transform_nuextract_report(report) for report in reports]
