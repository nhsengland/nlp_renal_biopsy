from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline


class MedicalReportQA:
    def __init__(self, model_name="dmis-lab/biobert-large-cased-v1.1-squad"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.qa_pipeline = pipeline(
            "question-answering", model=self.model, tokenizer=self.tokenizer
        )

        self.questions = {
            "cortex_present": "Is cortex present in the sample?",
            "medulla_present": "Is medulla present in the sample?",
            "n_total": "How many total glomeruli are there?",
            "n_segmental": "How many segmentally sclerosed glomeruli are there?",
            "n_global": "How many globally sclerosed glomeruli are there?",
            "abnormal_glomeruli": """Are there any abnormal glomeruli features like
                scarring, thickening, or irregular shape?""",
            "chronic_change": """What percentage or degree of chronic changes
                are present?""",
            "transplant": """Is this a transplant case or are there
                infiltrates/infection?""",
            "diagnosis": "What is the final diagnosis?",
        }

    def process_answer(self, answer, entity_type):
        if answer["score"] < 0.1:  # Confidence threshold
            return self._get_default_value(entity_type)

        text = answer["answer"].lower().strip()

        if entity_type.startswith("n_"):
            numbers = "".join(c for c in text if c.isdigit())
            return int(numbers) if numbers else 0

        elif entity_type == "chronic_change":
            if "%" in text:
                return float("".join(c for c in text if c.isdigit() or c == "."))
            elif any(
                adj in text
                for adj in [
                    "mild",
                    "moderate",
                    "severe",
                    "minimal",
                    "marked",
                    "extensive",
                ]
            ):
                return text
            return None

        elif entity_type in [
            "cortex_present",
            "medulla_present",
            "abnormal_glomeruli",
            "transplant",
        ]:
            return not any(neg in text for neg in ["no", "not", "absent", "missing"])

        return text

    def _get_default_value(self, entity_type):
        defaults = {
            "cortex_present": True,
            "medulla_present": False,
            "n_total": 0,
            "n_segmental": 0,
            "n_global": 0,
            "abnormal_glomeruli": False,
            "chronic_change": 0,
            "transplant": False,
            "diagnosis": None,
        }
        return defaults[entity_type]

    def process_report(self, text):
        results = {}
        for entity, question in self.questions.items():
            qa_result = self.qa_pipeline(question=question, context=text)
            results[entity] = self.process_answer(qa_result, entity)
        return results

    def process_reports(self, texts):
        return [self.process_report(text) for text in texts]


# Example usage
def run_bertqa(reports, model_name="dmis-lab/biobert-large-cased-v1.1-squad"):
    qa_model = MedicalReportQA(model_name=model_name)
    results = qa_model.process_reports(reports)
    # print(json.dumps(results, indent=2))
    return results
