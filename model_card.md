*Changed to describe our pipeline instead of a model.*

# Pipeline Card: GOSH Histopathology QA Pipeline

## Pipeline Details

The implementation of the GOSH Histopathology NER project within this repository was created as part of an NHS England PhD internship project undertaken by Avish Vijayaraghavan. This model card describes the updated version of the model, released 09/01/24. **We note that the description below corresponds to the entire annotation pipeline, not just the LLM models used.**

## Pipeline Use

### Intended Use

This pipeline is intended for annotating entities in medical reports using small language models (order of 0.5B-4B parameters).

### Out-of-Scope Use Cases

- This pipeline should not be used as an medical device.
- This pipeline should not be used in a production environment.
- This pipeline has been tested on histopathology reports for paediatric renal biopsies at Great Ormond Street Hospital. High-quality generalisation to other report datasets in different areas of medicine, different patient cohorts, and different hospitals is not guaranteed. 

## Data Used

- Histopathology reports for paediatric renal biopsies from Great Ormond Street Hospital. A sample of this data was manually annotated and compared to LLM annotation. This dataset is private.
- Synthetic few-shot samples and guidelines have been created from the reports and are used in input prompts.
- No data is used for "training" - all models used within the pipeline are natural.

## Performance and Limitations

- Full precision models preferred to avoid parsing issues in the output JSON.
- Results will not be perfect. Our best-performing models had ~80% average on our entity schema and performance differs per entity.
