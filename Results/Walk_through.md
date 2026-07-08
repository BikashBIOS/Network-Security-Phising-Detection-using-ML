# 🔐 Network Security Project (Phishing Data) — Full Structured Guide

A complete, step-by-step walkthrough of the entire project — from environment setup to AWS EC2 deployment. Nothing from the original README is omitted; it's just organized into clear phases, numbered steps, and sub-steps so it's easy to follow and replicate.

---

## 📑 Table of Contents

| # | Phase | What Happens |
|---|-------|--------------|
| 1 | Requirements & GitHub Setup | Project scaffolding, venv, git repo |
| 2 | setup.py | Package building from requirements.txt |
| 3 | Logging & Exception Handling | Generic logging/exception modules |
| 4 | ETL Pipeline Concept | Extract → Transform → Load overview |
| 5 | MongoDB Connection | Atlas cluster + driver setup |
| 6 | ETL Script (push_data.py) | CSV → JSON → MongoDB insertion |
| 7 | Data Ingestion (Summary) | Concept overview |
| 8 | Data Ingestion Configuration | Config classes & folder structure |
| 9 | Data Ingestion Component | Read → Feature Store → Train/Test Split |
| 10 | Data Validation | Schema checks & data drift |
| 11 | Data Transformation | Imputation, cleaning, array storage |
| 12 | Model Trainer (MLflow + Dagshub) | Training, tuning, experiment tracking |
| 13 | Training Pipeline Orchestration | Stitching all stages together |
| 14 | app.py (FastAPI) | Training API |
| 15 | Batch Prediction Pipeline | Predict API + HTML output |
| 16 | Push Artifacts/Models to AWS S3 | Sync code |
| 17 | AWS S3 Setup | IAM, bucket, CLI config |
| 18 | Deployment to AWS ECR | Docker image via GitHub Actions |
| 19 | GitHub Actions (CI) | Dockerfile + workflow yaml |
| 20 | ECR Docker Image Creation (CI) | Build & push to ECR |
| 21 | ECR → EC2 (CD) | Self-hosted runner + deployment |
| 22 | Running the Project Finally | End-to-end local run |

---

## 1️⃣ Requirements & GitHub Setup

1. Create a new virtual environment: `python -m venv venv`
2. Create these files at project root:
   - `requirements.txt`
   - `.gitignore`
   - `setup.py`
   - `.github/workflows/main.yaml`
   - `Dockerfile`
   - `.env`
3. Create these folders as per project requirement:
   - **Network_Data** → for your data (e.g., `phisingdata.csv`)
   - **networksecurity** → for your main source code
   - **notebooks** → for Jupyter notebooks
4. Add your libraries to `requirements.txt`, then run:
   ```
   pip install -r requirements.txt
   ```
5. Add `venv` and `.env` to `.gitignore` so Git ignores them when pushing to GitHub.
6. Create a new GitHub repo (e.g., "Network Security") and push code:
   ```
   git init
   git add .
   git commit -m "First commit"
   git branch -M main
   git remote add origin https://github.com/BikashBIOS/Network-Security.git
   git push -u origin main
   ```
7. Add `__init__.py` in **all** folders, then push again.

---

## 2️⃣ setup.py

1. Write code in `setup.py` to pull libraries from `requirements.txt`.
2. Specify version and package info, retrieved via a `get_requirements()` function.
3. After running `pip install -r requirements.txt`, your package folder is created with all package info and requirements.

---

## 3️⃣ Logging and Exception Handling

1. Create logging and exception files using the generic logging/exception boilerplate code.
2. The `__main__` block in the exception file can be used to test whether the exception handling works correctly.

---

## 4️⃣ ETL Pipeline (Extract, Transform, Load) — Concept

1. There's a **Source** and a **Destination**, with **Transformation** happening in between.
2. Flow:
   - **Extract** → CSV dataset from local database (Source)
   - **Transform** → Convert CSV to JSON
   - **Load** → Insert JSON data into MongoDB (Destination)

---

## 5️⃣ MongoDB Connection Setup

1. Create a free account on **MongoDB Atlas**.
2. Create a default **Cluster0** cluster.
3. Keep the default username and password.
4. Click **Next → Choose a Connection Method → Drivers**.
5. Select **Driver: Python** and choose the version.
6. Add the `pymongo` library version to `requirements.txt`.
7. Click **Done** — Cluster0 gets created.
8. Click **Connect** on the cluster → copy the full code sample shown.
9. Create a new file `push_data.py` in the root folder and paste that code.
10. In the code, replace the placeholder `dbpassword` in the URI object with your actual password (retrieve/reset via **Quickstart** if forgotten).
11. Don't hardcode the URI — move it into your `.env` file instead.
12. Run:
    ```
    python push_data.py
    ```
    Success message: *"You successfully connected to MongoDB."*
13. Cut the `push_data.py` code into a new file `test_mongodb.py` (to be reused later).
14. Back in `push_data.py`, load the environment variable — fetch `MONGO_DB_URL` from `.env` and print it.

---

## 6️⃣ ETL Pipeline Setup — Inserting Records into MongoDB

1. Import `certifi` in `push_data.py`.
2. **certifi** = Python package providing root certificates, used for secure HTTPS connections.
3. Write a function to convert CSV data → JSON.
4. **JSON structure**: one row of data = one dict of key–value pairs (key = column name, value = row value).
5. `cv_to_json_converter()` → converts CSV data into JSON and stores the JSON records.
6. `insert_data_mongodb()` → creates the database, collection, and records; connects to the MongoDB client; inserts and returns the records.
7. `__main__()` block:
   - Pass in `FILE_PATH` for your dataset (`phisingData.csv`)
   - Assign a name to your dataset/collection
   - Call `NetworkDataExtract()` → converts data to JSON
   - Call `insert_data_mongodb()` → inserts data into the MongoDB cluster
8. Run:
   ```
   python push_data.py
   ```
   Data gets inserted into the MongoDB cluster. Open Cluster0 in the browser → open the database → verify your JSON data is there.

---

## 7️⃣ Data Ingestion — Summary (Concept Overview)

1. **Data Ingestion Config** → holds basic info: where data is stored, train/test split ratio, paths, etc.
2. Read data from MongoDB and convert it into a **Data Ingestion Artifact** based on the Config.
3. The artifact contains raw data plus train/test splits.
4. Feature engineering is then applied on train/test data before moving to **Data Transformation**.

---

## 8️⃣ Data Ingestion Configuration

1. Create a `training_pipeline` folder inside `constants` → add `__init__.py` to store common Data Ingestion Config values (raw data, train, test constants).
2. In MongoDB: **Network Access → IP Access List → Create New IP Address → Add `0.0.0.0/0`**.
3. Create `config_entity.py` in the `entity` folder:
   - **Goal**: Create `Artifact → [Date & Time folder] → Data Ingestion → feature store → data.csv`
   - `TrainingPipelineConfig()` → sets timestamp + main folder (`self.artifact_dir` joins "Artifact" folder name with timestamp).
   - `DataIngestionConfig()` → defines exactly where data goes during ingestion.
     - `self.data_ingestion_dir` → sub-folder inside the timestamped artifact folder, specific to ingestion.
     - `self.feature_store_file_path` → where raw data is saved.
     - `self.training_file_path` & `self.testing_file_path` → paths for split train/test data.
     - `self.train_test_split_ratio` → e.g., 0.2 (fraction reserved for testing).
     - `self.collection_name` & `database_name` → source MongoDB database/collection.

---

## 9️⃣ Data Ingestion Component / Initiate

**Flow:** Read Data from MongoDB → Create Feature Store → Split Test/Train Data → Save in Ingested Folder

### A. Read Data from MongoDB
1. Create `data_ingestion.py` in `components` folder:
   - `export_collection_as_dataframe()` → connects to MongoDB and converts data into a DataFrame.
     - `collection.find()` → grabs every record in the table.
     - `pd.DataFrame()` → converts to DataFrame.
     - Drop the `_id` column (always present in MongoDB data).
     - Replace NA values with NaN (null).
   - `initiate_data_ingestion()` → collects the DataFrame using the function above.

### B. Create Feature Store
- `export_data_into_feature_store()` → takes the DataFrame → saves it as CSV at `feature_store_file_path`.

### C. Split Training and Testing Data
- `split_data_as_train_test()` → splits the CSV data into train/test CSV.
- `os.makedirs(dir_path)` → creates the path (`Artifacts/timestamp/data_ingestion/ingested`).
- Saves training data → `training_file_path`; testing data → `testing_file_path`.
- Call `split_data_as_train_test()` inside `initiate_data_ingestion()` with the DataFrame.

### D. Artifacts & Execution
2. Create `artifact_entity.py` in `entity` folder → initialize `DataIngestionArtifact` dataclass to store trained/test data paths.
   - Call this dataclass inside `initiate_data_ingestion()` with train/test file paths.
3. Create `main.py` in root folder:
   - Call `TrainingPipelineConfig` and `DataIngestionConfig`.
   - Create a `DataIngestion()` object → call `initiate_data_ingestion()` to run the full ingestion process.
   - Run `python main.py` — success if it creates an `Artifacts` folder with `train.csv`/`test.csv` in `ingested`, and raw data in `feature_store`.
4. If successful, delete the `Artifacts` and `logs` folders, then commit the code.

---

## 🔟 Data Validation

### Configuration
Validate the data on:
- Same number of features/columns as expected.
- **Data Drift** → when today's data differs significantly (statistically) from training data.
- Validate number of columns and whether numerical columns exist.

**Steps:**
1. In `training_pipeline.py`, store common values (data validation, invalid, valid data, drift report, `preprocessing.pkl`) for the Data Validation Config.
2. In `config_entity.py`, use `DataValidation()` to define paths for valid/invalid data (train + test) and the data drift report.
3. Add the above values to the `DataValidationArtifact` dataclass in `artifact_entity.py`.
4. Create `data_schema` folder in root → create `schema.yaml` and paste schema code. Reference this path in `training_pipeline > __init__.py`.
5. Create `main_utils` folder inside `utils` → add `__init__.py` and `utils.py`. Add code in `utils.py` for reading the YAML file.
6. Create `data_validation.py`:
   - Initialize `dataingestionartifact` and `datavalidationartifact`, then read the schema file.

### Data Validation Initiation
1. Load training and test data using their file paths.
2. `status` → checks the number of columns (per schema) against training/testing data.
3. Check **data drift** → compares statistical distribution of test vs. training data → result stored as `True`/`False`.
4. Store validated data in a new folder path.
5. Save train/test DataFrames as CSVs at that path.
6. Create a **Data Validation Artifact** capturing status (based on train/test data); if drift is detected, store data in the specific path.
7. To run: In `main.py`, initialize Data Validation Config and Data Validation (passing the config + Data Ingestion Artifact).
8. Finally, initialize the Data Validation Artifact by calling `initiate_data_validation()`.

---

## 1️⃣1️⃣ Data Transformation

1. Add `DataTransformationConfig` class in `config_entity.py`.
2. Add `DataTransformationArtifact` dataclass in `artifact_entity.py`.
3. Add Data Transformation constants in `constants > training_pipeline > __pycache__ > __init__.py`.
4. Add new functions in `utils > utils.py`:
   - `save_numpy_array_data()`
   - `save_object()`
   - `load_object()`
   - `load_numpy_array_data()`
5. Create `data_transformation.py` and write the logic:
   6. **Load Validated Data** — Load train/test DataFrames using paths from `DataValidationArtifact`.
   7. **Feature/Target Separation** — Drop `TARGET_COLUMN` to separate features from target (train + test).
   8. **Target Label Cleaning** — Convert target label `-1` → `0` for standard formatting.
   9. **Initialize Preprocessing Object** — `get_data_transformer_object()` initializes a `KNNImputer` (params from constants) — handles missing values via nearest-neighbor estimation.
   10. **Fit and Transform**:
       - Fit the preprocessor on training features (learn imputation pattern).
       - Apply the transformation to both training and testing feature sets.
   11. **Data Recombination** — Combine transformed features with target columns using `np.c_` to build final train/test arrays.
   12. **Artifact Storage**:
       - Save transformed train/test arrays as `.npy` files in the designated folder.
       - Save the preprocessor object as a `.pkl` file (for reuse in prediction/deployment).
   13. **Create Data Transformation Artifact** — containing paths to transformed data + saved preprocessor object.
   14. **Execution via main.py** — Initialize `DataTransformationConfig` + `DataTransformation` class (with config + `DataValidationArtifact`), then call `initiate_data_transformation()`.

---

## 1️⃣2️⃣ Model Trainer (with MLflow and Dagshub)

1. Define `ModelTrainerConfig` class in `config_entity.py`.
2. Create Model Trainer constants (`DIR_NAME`) in `constants > training_pipeline > __init__.py`.
3. Add 2 dataclasses in `artifact_entity.py`: **Classification Metrics** and **Model Trainer Artifact**.
4. Create `load_object` and `load_numpy_array_data` functions in `utils.py`.
5. Create 2 folders inside `utils`: `metric` and `model`.
6. In `metric` folder, create `classification_metric` → function to compute recall, F1 score, precision score.
7. In `model` folder, create `estimator.py` → write prediction code (use `SAVED_MODEL` and `MODEL_FILE_NAME` from `__init__.py` constants).
8. Create `model_trainer.py` in `components`, and write the following:
   9. Create `ModelTrainer` class with model trainer config + data transformation artifact.
   10. Create `initiate_model_training()` — pass train/test data, split into X and y.
   11. Create `train_model()` — load models, apply hyperparameter tuning.
   12. Pass these values into `evaluate_model()` (configured in `utils.py`).
   13. Find the best model via this evaluation code.
   14. Get classification scores for both train and test.
   15. Load object/model at the designated path using `load_object()` and `load_numpy_array_data()`.
   16. Build a `NetworkModel` using the best model + preprocessor → save as `.pkl`. Then create and return `ModelTrainerArtifact`.
   17. Create `track_mlflow()` — logs classification score, F1 score, precision, and recall.
   18. Apply this function to the best model to log scores in MLflow.
   19. In terminal, run:
       ```
       mlflow ui
       ```
       → generates a link to view your MLflow dashboard.
   20. Set up **Dagshub**:
       - Go to Dagshub → Login via GitHub.
       - Create a repository from your existing GitHub repo → go to **Experiments** tab.
       - Copy the `import dagshub` line + repository connection code into `model_trainer.py`.
   21. Run:
       ```
       python main.py
       ```
       → executes the training process; results saved to Dagshub.
   22. In the **Experiments** tab, view the 2 models created → compare classification scores and graphs.
   23. Based on the best model: `model.pkl` saved in `final_model` folder; `preprocessing.pkl` also saved (from `data_transformation.py`).

---

## 1️⃣3️⃣ Pipeline of Model Training (Orchestration)

1. Create 2 Python files in the `pipeline` folder: `batch_prediction.py` and `training_pipeline.py`.
2. Start writing code in `training_pipeline.py`:
3. **Initialization (`__init__`)** — Sets up the base `TrainingPipelineConfig` (global config for the whole pipeline).
4. **Stage 1: Data Ingestion** (`start_data_ingestion`)
   - Action: Fetches/loads raw data.
   - Process: Initializes `DataIngestion` using its config.
   - Output: `DataIngestionArtifact` (train/test file paths).
5. **Stage 2: Data Validation** (`start_data_validation`)
   - Input: `DataIngestionArtifact` from Stage 1.
   - Action: Checks structural integrity and data drift.
   - Output: `DataValidationArtifact` (validated/clean data paths).
6. **Stage 3: Data Transformation** (`start_data_transformation`)
   - Input: `DataValidationArtifact` from Stage 2.
   - Action: Feature engineering, scaling, encoding.
   - Output: `DataTransformationArtifact` (transformed data + preprocessing object paths).
7. **Stage 4: Model Training** (`start_model_trainer`)
   - Input: `DataTransformationArtifact` from Stage 3.
   - Action: Trains the ML model.
   - Output: `ModelTrainerArtifact` (final model + performance metrics).
8. **Master Orchestration** (`run_pipeline`)
   - Main trigger function; runs Stages 1–4 sequentially.
   - Automatically passes each stage's artifact to the next.
   - Returns the final `model_trainer_artifact`.

---

## 1️⃣4️⃣ app.py — Exposing Everything via FastAPI

1. Create `app.py` in the root folder.
2. Install `fastapi` and `uvicorn`.
3. Start writing the code:
4. **Database Connection & Setup**
   - Initialize a MongoDB client (`pymongo.MongoClient`) with a secure DB URL + TLS certificate (`tlsCAFile=ca`) to encrypt the connection.
   - Target the specific database/collection using constants (`DATA_INGESTION_DATABASE_NAME`, `DATA_INGESTION_COLLECTION_NAME`).
5. **FastAPI App Initialization** — `app = FastAPI()`.
6. **CORS Middleware Configuration** — Register `CORSMiddleware` with `origins = ["*"]` (allows any domain to communicate with the API; all methods/headers permitted).
7. **Root Route Redirect (`/`)** — GET endpoint at `/` redirects to `/docs` (FastAPI's Swagger UI).
8. **Model Training Route (`/train`)**
   - Async GET endpoint to trigger the ML pipeline.
   - Instantiates `TrainingPipeline` object → calls `run_pipeline()` (runs ingestion, validation, transformation, training).
   - Success Response: `"Training is successful"`.
9. Initialize the main function to run `app.py`.
10. Run:
    ```
    uvicorn app:app --reload
    ```
11. Open localhost link → go to `/train` → execute.
12. After execution, training runs fully; new train/test experiments appear in Dagshub for comparison.

---

## 1️⃣5️⃣ Batch Prediction Pipeline

1. Create `templates` folder → add `tables.html` (prewritten HTML code).
2. Create `valid_data` folder → paste `test.csv` (the data you want predictions for).
3. Add the following `/predict` code in `app.py`:
4. **Template Engine Initialization** — Set up `Jinja2Templates` pointing to `./templates`, so FastAPI can render dynamic HTML.
5. **File Upload and Data Loading**
   - POST route at `/predict` accepting a user-uploaded file (`UploadFile`).
   - Reads the uploaded file into a Pandas DataFrame via `pd.read_csv(file.file)`.
6. **Model Loading and Wrapper Initialization**
   - Loads two components from `final_model/` using `load_object()`:
     - `preprocessor.pkl` (feature preprocessing object)
     - `model.pkl` (trained ML model)
   - Binds both into a custom wrapper class `NetworkModel`.
7. **Prediction Logic** — Passes the DataFrame into `network_model.predict(df)` to generate predictions (`y_pred`).
   - Appends results back into the original data as a new column: `predicted_column`.
8. **Output Persistence (File Saving)**
   - Ensures `prediction_output` folder exists via `os.makedirs(..., exist_ok=True)`.
   - Saves the updated DataFrame (with predictions) as `prediction_output/output.csv`, without the DataFrame index.
9. **HTML Presentation and Rendering**
   - Converts the DataFrame into an HTML table via `df.to_html()`, styled with Bootstrap classes (`table table-striped`).
   - Returns a `TemplateResponse` targeting `tables.html` (⚠️ note the "s" — must match exactly), injecting the request context + generated `table_html`.
10. Run:
    ```
    uvicorn app:app --reload
    ```
11. Navigate to the `/predict` section on the page.
12. Click **Try it out** → Upload `test.csv` → Click **Execute**.
    - On success: full data appears as a table on the page.
    - Verify: a `prediction_output` folder is created with `output.csv`, including the new `predicted_column`.

---

## 1️⃣6️⃣ Pushing Final Models & Artifacts to AWS S3

1. Create `s3_syncer.py` in `networksecurity > cloud` folder.
2. Write code for the AWS CLI sync commands.
3. Write 2 functions in `training_pipeline.py` to sync artifacts and saved models to S3:
4. **Artifact Directory Synchronization** (`sync_artifact_dir_to_s3`)
   - Purpose: Uploads the entire intermediate data history (ingested, validated, drift reports, transformation objects) to the cloud.
   - Logic: Builds an S3 URL pointing to `/artifact/` + the pipeline runtime timestamp.
   - Execution: Calls `s3_sync.sync_folder_to_s3()` to push the local `artifact_dir` to that S3 destination.
5. **Saved Model Synchronization** (`sync_saved_model_dir_to_s3`)
   - Purpose: Pushes final production-ready model files to S3 for later deployment/production use.
   - Logic: Builds an S3 URL pointing to `/final_model/` + runtime timestamp.
   - Execution: Copies contents of local `model_dir` to the S3 bucket.
   - Call both functions inside `run_pipeline()`.
6. Remember to initialize `TRAINING_BUCKET_NAME` in `__init__.py`.

---

## 1️⃣7️⃣ Push Data to AWS S3 (Account/CLI Setup)

1. Download the AWS CLI.
2. Open the AWS Console.
3. Go to **IAM**.
4. Create a new user (e.g., `testsecurity`).
5. Click **Next → Attach Policies Directly → Select Administrator Access**.
6. Create the user.
7. Open the user → **Access Keys → Security Credentials → Create Access Keys**.
8. Select **CLI** → **Next → Create access key**.
9. Copy the Key and Secret.
10. In your project terminal:
    ```
    aws configure
    ```
    → provide Access Key ID and Secret.
11. Go to **S3 → Create bucket** → give a name (⚠️ must match `TRAINING_BUCKET_NAME` in `__init__.py`) → Create bucket.
12. Run:
    ```
    uvicorn app:app --reload
    ```
13. On success, `artifacts` and `final_models` folders appear in the S3 bucket.
14. You can also run the program via `python main.py` — it will run the uvicorn command internally too.

---

## 1️⃣8️⃣ Deployment to AWS ECR

1. Goal: Deploy the full project into an EC2 instance.
2. Convert the NetworkSecurity project into a **Docker image**.
3. Upload this Docker image to **AWS ECR**.
4. Deploy it into the EC2 instance.

> **Note:** This whole process requires GitHub Actions via **CI/CD pipelines** and **App Runners**.

### GitHub Action Process
1. In the `Dockerfile`, write code specifying the Python 3 version and running `app.py`.
2. In `.github/workflows/main.yaml`, edit the workflow code.
3. Add `name:`, `on:`, and `jobs:` tags to `main.yaml` and push the code.
4. In the **Actions** tab of your GitHub repo, you'll see the CI action running with all functions executing.

### ECR AWS — Docker Image Creation
1. Go to **ECR → Create repository** → give it a name → Create.
2. Copy the URI.
3. Copy the build/push ECR image code from `main.yaml`.
4. Provide AWS Access Key ID and Secret (how to get this):
5. Go to **IAM User** → generate the access key ID and secret.
6. Go to **GitHub → Secrets and Variables → Actions → New repository secret**.
7. Add `AWS_ACCESS_KEY_ID` → paste the access key ID.
8. Add `AWS_SECRET_ACCESS_KEY` → paste the secret.
9. Add `AWS_REGION` → provide the region.
10. Add `AWS_ECR_LOGIN_URI` → paste the URI (⚠️ don't include the repo name in it).
11. Add `ECR_REPOSITORY_NAME` → the name of the ECR repository.
12. Add the "Build, tag, and push image to Amazon ECR" step to `main.yaml`.
13. Push the code to GitHub → go to **Actions** → watch the CI/CD pipeline run.
14. On success: green checkmarks appear, and the Docker image is visible in ECR AWS (tag: `latest`).

---

## 1️⃣9️⃣ Pushing ECR Image to EC2 Instance

1. Add **Continuous Deployment** code to `main.yaml`.
2. Go to **EC2 in Console → Launch an Instance** → give it a name → Select **Ubuntu** → Select instance type (e.g., **t3.micro**) → Create Instance.
3. After creation: click on the instance ID → **Connect → Connect via Public IP** (opens Amazon CLI/terminal).
4. Run these pre-installation Docker setup commands in EC2:
   ```
   sudo apt-get update -y
   sudo apt-get upgrade
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```
5. Go to your GitHub repo → **Settings → Actions → Runners**.
6. Click **New self-hosted runner**.
7. Select **Linux**.
8. Execute the 4 setup commands shown, one by one, in the EC2 CLI.
9. Then execute the next 2 commands shown below that.
10. When prompted, enter the runner name as `self-hosted` (matches what's referenced in the Continuous Deployment section of `main.yaml`).
11. Run:
    ```
    ./run.sh
    ```
12. Confirm the self-hosted runner shows as **Idle** in GitHub's Runners section.
13. Change the host to `"0.0.0.0"` in `app.py`.
14. Commit and push the code to GitHub.
15. Watch the pipeline progress: **Continuous Integration → Continuous Delivery → Continuous Deployment**.
16. On success, all 3 sections show green checkmarks.
17. Go to the EC2 instance's **Security Groups** → add a Custom TCP rule for `0.0.0.0` on **Port 8080**.
18. Save it, then open the instance and copy the **Public IPv4 address**, and open it in the browser.
19. Append `:8080` to the IP address and open it — the FastAPI screen appears, ready for training and prediction.

---

## 2️⃣0️⃣ Running This Project — Final End-to-End Steps

1. Open the project in **VS Code**.
2. Activate the `venv` environment.
3. Run:
   ```
   uvicorn app:app --reload
   ```
4. Open the localhost link in the browser.
5. Click **Train → Execute**.
6. Execution starts in VS Code.
7. After execution, you'll see a successful response for training in FastAPI.
8. Click **Predict → Try it out** → select the `test.csv` file from `valid_data`.
9. Click **Execute**.
10. Prediction runs in VS Code.
11. The same `test.csv` is regenerated with a new column `predicted_column` in `prediction_output/output.csv`.

---

### ✅ Quick Recap of the Overall Pipeline Flow

```
Setup (venv, git, folders)
   → MongoDB Connection & Data Push
   → Data Ingestion (MongoDB → Feature Store → Train/Test Split)
   → Data Validation (Schema + Drift Check)
   → Data Transformation (Imputation + Encoding → .npy + .pkl)
   → Model Training (Best model selection + MLflow/Dagshub tracking)
   → Training Pipeline Orchestration (Stitch all stages)
   → FastAPI app.py (/train and /predict routes)
   → Push Artifacts/Models to AWS S3
   → Dockerize → Push to AWS ECR (via GitHub Actions CI)
   → Deploy to EC2 (via self-hosted runner CD)
   → Access live FastAPI app via EC2 Public IP:8080
```
