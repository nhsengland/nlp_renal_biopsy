REM Create and activate environment
echo --- Create and activate conda environment
call conda env create -f project_files\environment.yml
call conda activate llm-annotation-env-test

REM Download ollama models (need 8.3GB)
echo --- Downloading two FP16 instruction-tuned models: Qwen2.5:1.5B and Gemma2:2B
ollama pull qwen2.5:1.5b-instruct-fp16 
ollama pull gemma2:2b-instruct-fp16

REM Create models directory
echo --- Creating model/ directory - model/ only used with llama-cpp
mkdir models
echo models/>> .gitignore

REM Create data directory and move guidelines in
echo --- Creating data/ directory and moving relevant files from project_files/ directory
mkdir src\renal_biopsy\data
mkdir src\renal_biopsy\data\runs
echo src/renal_biopsy/data/>> .gitignore
xcopy /y project_files\guidelines.xlsx src\renal_biopsy\data\
xcopy /y project_files\synthetic_data.xlsx src\renal_biopsy\data\
xcopy /y project_files\synthetic_annotations.json src\renal_biopsy\data\

REM Setup input JSON using Python script
echo Setting up input JSON...
python setup_input_json.py --guidelines guidelines.xlsx --raw_data synthetic_data.xlsx

echo --- Final steps of setup...

REM Install ipython kernel for notebooks
python -m ipykernel install --user --name=llm-annotation-env-test --display-name "llm-annotation-env-test (ipython)"

REM Download spacy model
python -m spacy download en_core_web_sm

REM Install pre-commit hooks
pre-commit install

echo --- Setup completed successfully!
