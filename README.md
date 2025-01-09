# Resource-Constrained Annotation Workflows for Paediatric Histopathology Reports

## 🚀 Introduction

This package contains the source code for an automated entity annotation pipeline for medical reports using local LLMs. 

Workflow Steps:

1. Preparation of annotation guidelines - clinical expert to provide guidelines (see entity_guidelines.xlsx)

2. Annotation of sample reports by the clinical expert using Streamlit application - this is used for evaluation purpose

3. Run the script for automated entity annotation

Optional Steps:

4. Disagreement modelling - To compare two different models for further manual reviewing.

5. Second Streamlit application for comparing and commenting on results from disagreement modelling


## 📚 Installations

### Setting up new conda environment and package installations

*This takes roughly 30 minutes.*

```bash
# 1. Clone the repository
git clone [repository_url]
cd [repository_name]

# 2. Create and setup conda environment
conda create --name gosh-llm python=3.12.6
conda activate gosh-llm
conda install ipykernel
python -m ipykernel install --user --name=gosh-llm --display-name "gosh-llm (ipython)"

# 3. First pip installations 
pip install python-Levenshtein pandas streamlit

# 4. Install ollama and models
pip install ollama
ollama pull [model_name] # qwen2.5:1.5b-instruct-fp16 recommended as a good initial model
# If using llama-cpp:
mkdir models  # Create models directory
# Download GGUF models from HuggingFace and place in models/
# Ensure models/ is in .gitignore

# 5. Install ML and NLP packages
pip install matplotlib seaborn scikit-learn spacy gensim
python -m spacy download en_core_web_sm
# Note: If numpy dtype issues occur after gensim, restart notebook kernel

# 6. Final installations
pip install openpyxl streamlit-annotation-tools langchain langchain-community gliner llama-cpp-python
```

### Usage

```bash
# 1. Activate conda environment
conda activate gosh-llm

# 2. Run annotation app
streamlit run src/renal_biopsy/annotation_app.py src/renal_biopsy src/renal_biopsy/data/real_input.json

# 3. Run LLM annotation and evaluation
python rb_script.py --backend [ollama/llamacpp] \
   --root_dir src/renal_biopsy \
   --model_name [model_name] \
   --n_shots [n_few_shot_samples] \
   --n_prototype [n_annotated_samples] \
   --include_guidelines
# As a good initial test, we recommend the command below:
# python rb_script.py --backend ollama --root_dir src/renal_biopsy --model_name qwen2.5:1.5b-instruct-fp16 --n_shots 1 --n_prototype 1 --include_guidelines

# 4. Run disagreement modeling between two models 
python rb_disagreement_script.py --backend [ollama/llamacpp] \
   --root_dir src/renal_biopsy \
   --model_1_name [model_1_name] \
   --model_2_name [model_2_name] \
   --n_shots [n_few_shot_samples] \
   --n_prototype [n_annotated_samples] \
   --disagreement_threshold [threshold] \
   --include_guidelines
# As a good initial test, we recommend the two commands below:
# ollama pull gemma2:2b-instruct-fp16
# python rb_disagreement_script.py --backend ollama --root_dir src/renal_biopsy --model_1_name qwen2.5:1.5b-instruct-fp16 --model_2_name gemma2:2b-instruct-fp16 --n_shots 1 --n_prototype 1 --disagreement_threshold 0.3 --include_guidelines

# 5. View disagreements in comparison app
streamlit run src/renal_biopsy/comparison_app.py \
   src/renal_biopsy \
   data/runs/{timestamp} \
   [n_annotated_samples]
# Note: if there are no disagreements, this won't be able to run.
# TODO: comparison_comments.json currently saves to root directory, fix to save in timestamped folder.

# 6. Additional notebooks available:
# - renal_biopsy.ipynb: For exploratory data analysis and model debugging
# - alt_methods.ipynb: For standard NER-based methods
```

### Adapting this project to your own area of biomedicine

```bash
# 1. Create project directory
mkdir src/{project_folder}

# 2. Set up data folder and files
mkdir src/{project_folder}/data
# Add your guidelines.xlsx and sample_data files to data/
# Minimum columns needed in guidelines.xlsx:
# - Entity
# - Entity Question To Ask  
# - Entity Type
# - Entity Code
# Example available in src/project_files/

# 3. Create preprocessor
touch src/{project_folder}/preprocessor.py
# Create {Project}Processor class inheriting MedicalReportProcessor
# Implement:
# - create_input_json()
# - process_all_reports() 
# - segment_report()
# Note: Entity Code names in guidelines.xlsx cannot clash with section headings you need to extract in segment_report()

# 4. Create QA module
touch src/{project_folder}/qa.py
touch src/{project_folder}/few_shots.py
# Create {Project}QA class inheriting QABase (Ollama/LlamaCpp)
# Implement:
# - get_few_shot_list() (store list in few_shots.py)
# - get_report_string()

# 5. Create annotation app
touch src/{project_folder}/annotation_app.py
# Create {Project}StreamlitApp class inheriting StreamlitAppBase
# Implement write_report_string_for_streamlit()
# Copy main section from existing renal_biopsy/annotation_app.py and modify it to suit your project

# 6. Run the annotation app from root directory
streamlit run src/{project_folder}/annotation_app.py \
   src/{project_folder} \
   src/{project_folder}/data/{input_json_name}.json
```

##  🤝 Acknowledgements
*This project was a five month internship funded by NHSE and supervised by NHSE and GOSH DRIVE*
* GOSH DRIVE Digital Research Environment (DRE) Team
* NHSE Data Science Team

##  🤝 Contributors
* Avish Vijayaraghavan - PhD student @ Imperial College London (core contributor)
* Dr. Pavi Rajendran - NLP & Computer Vision Lead @ GOSH DRIVE
* Dr. Neil J. Sebire - Clinical Lead @ GOSH DRIVE
* Dr. Dan Schofield - AI Technical Specialist @ NHSE
* Dr. Jonathan Hope - Data Science Lead Manager @ NHSE
* Dr. Jonny Pearson - Lead Data Scientist @ NHSE

For any queries, please contact us via email pavithra.rajendran@gosh.nhs.uk.

##  🧑🏽‍🤝‍🧑🏽 Citing & Authors

To be updated

## 📃 Licenses

Code is this repository is covered by the GNU General Public License and for all documentation the [Open Government License (OGL)](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) is used.

Copyright (c) 2024 Crown Copyright

