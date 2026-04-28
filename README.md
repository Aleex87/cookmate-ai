# Cookmate-ai.

## Project Structure (Working Map)

This section describes the purpose of each file and folder.  
Each team member can update this file from their own branch to document their work.  
This map will be removed before final submission.
## Git Workflow (Team Guidelines)

Follow this workflow to avoid conflicts and keep the project clean.

---

### 1. Always start from an updated main

```bash
git checkout main
git pull origin main
```
### 2. Create a new branch for your task

git checkout -b feature/your-task-name

### 3. 3. Work on your code
classic 
git add .
git commit -m "..."
git push origin feature/your-task-name 

### 4.  Create a Pull Request (PR)
On GitHub:
Click "Compare & pull request"

### 5. Review

### 6. Merge

### 7. After merge (IMPORTANT) 
git checkout main
git pull origin main

---

### Root
create a 
.env → environment variables 
COHERE_API_KEY=...personal key
OPENROUTER_API_KEY= ... personal key

then:
uv sync
I have installed the same dependences of the cours icnliding python 3.13

---

### data/

data/raw/ → raw datasets 
data/processed/ → cleaned dataset ready for ingestion  
data/evaluation/ → evaluation samples for testing the system  

---

### db/

db/recipes.lance/ → LanceDB vector database (embedded recipes)  

---

### notebooks/

notebooks/data_curation.ipynb → dataset filtering and preprocessing  
notebooks/exploration.ipynb → experiments and testing ideas  

---

### prompts/

prompts/recipe_agent_system_prompt.md → main system prompt for the agent  
prompts/retrieval_evaluation_prompt.md → prompt for evaluation/testing  

---

### mlruns/

mlruns/ → MLflow tracking data (runs, logs, experiments)  

---

### src/cookmate/

__init__.py → package initialization  

---

#### backend/

api.py → FastAPI endpoints  
agents.py → PydanticAI agent + retrieval tool  
data_models.py → request/response models + LanceDB schema  
constants.py → paths, model names, configuration  
middleware.py → logging and MLflow tracing

---

#### frontend/

app.py → Streamlit UI (user input and output display)  

---

#### setup/

prepare_dataset.py → prepare and format cleaned dataset  
ingestion.py → create embeddings and store data in LanceDB  

---

#### monitoring/

evaluation_dataset.json → test queries for evaluation  
monitoring.ipynb → evaluation and MLflow analysis  

---

#### utils/

config.py → environment loading and shared configuration  

---

### tests/

test_api.py → basic API tests  

