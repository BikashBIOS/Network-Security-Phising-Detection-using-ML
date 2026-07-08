# 🛡️ Network Security — Phishing Detection ML System

A **production-grade, end-to-end Machine Learning project** built for network security. The system ingests raw phishing data from **MongoDB**, runs it through a full **ETL + ML pipeline** (data ingestion → validation → transformation → model training), tracks experiments on **MLflow + DagHub**, serves predictions via a **FastAPI** web server, and deploys to **AWS EC2** via a fully automated **CI/CD pipeline** using GitHub Actions, Docker, and AWS ECR.

> 🧑‍💻 **Author:** [BikashBIOS](https://github.com/BikashBIOS)
> 📦 **Repo:** [Network-Security](https://github.com/BikashBIOS/Network-Security)

---

## 📌 What This Project Does

Given a CSV of network/URL features, the ML model classifies whether each record represents a **phishing attempt (1)** or a **legitimate connection (0)**. The full system flow is:

```
[PhishingData CSV]
      ↓
[MongoDB Atlas — cloud database]
      ↓
[Data Ingestion → Validation → Transformation → Model Training]
      ↓
[MLflow / DagHub — experiment tracking]
      ↓
[FastAPI Server — /train and /predict endpoints]
      ↓
[Docker Image → AWS ECR → AWS EC2 — production deployment]
```

---

## 📁 Repository Structure

```
Network-Security/
│
├── networksecurity/                     # Main source package (all pipeline logic lives here)
│   ├── __init__.py
│   ├── components/                      # Core pipeline stage implementations
│   │   ├── data_ingestion.py            # Pulls data from MongoDB, saves raw CSV
│   │   ├── data_validation.py           # Validates schema, detects data drift
│   │   ├── data_transformation.py       # KNN imputation, feature/target split, saves .npy
│   │   └── model_trainer.py             # Trains models, hyperparameter tuning, MLflow logging
│   │
│   ├── entity/                          # Config and Artifact dataclass definitions
│   │   ├── config_entity.py             # TrainingPipelineConfig, DataIngestionConfig, etc.
│   │   └── artifact_entity.py           # DataIngestionArtifact, ModelTrainerArtifact, etc.
│   │
│   ├── constants/
│   │   └── training_pipeline/
│   │       └── __init__.py              # All shared constant values (paths, ratios, names)
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py         # Orchestrates all 4 stages end-to-end
│   │   └── batch_prediction.py          # Batch inference pipeline
│   │
│   ├── exception/
│   │   └── exception.py                 # Custom NetworkSecurityException class
│   │
│   ├── logging/
│   │   └── logger.py                    # Centralised logging configuration
│   │
│   ├── cloud/
│   │   └── s3_syncer.py                 # AWS S3 sync utility (artifacts + models)
│   │
│   └── utils/
│       ├── main_utils/
│       │   └── utils.py                 # save/load object, save/load numpy arrays, read YAML
│       └── ml_utils/
│           ├── metric/
│           │   └── classification_metric.py   # F1, precision, recall scorer
│           └── model/
│               └── estimator.py               # NetworkModel wrapper (preprocessor + model)
│
├── data_schema/
│   └── schema.yaml                      # Expected column names and data types
│
├── Network_Data/
│   └── phisingData.csv                  # Raw phishing dataset (source of truth)
│
├── final_model/                         # Saved best model and preprocessor after training
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── prediction_output/                   # Prediction results saved here
│   └── output.csv
│
├── valid_data/                          # Test CSV files for /predict endpoint
│   └── test.csv
│
├── templates/
│   └── tables.html                      # Jinja2 HTML template for prediction output display
│
├── .github/workflows/
│   └── main.yaml                        # GitHub Actions CI/CD pipeline (CI → ECR → EC2)
│
├── app.py                               # FastAPI application — /train and /predict routes
├── main.py                              # Manual pipeline runner (step-by-step)
├── push_data.py                         # ETL: CSV → JSON → MongoDB Atlas
├── setup.py                             # Package builder (makes networksecurity importable)
├── Dockerfile                           # Container definition for AWS ECR/EC2 deployment
├── requirements.txt                     # All Python dependencies
├── mlflow.db                            # Local MLflow tracking database
└── .gitignore                           # Excludes venv, .env, __pycache__, artifacts
```

---

## ⚙️ Project Setup — Step by Step

### Step 1 — Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 2 — Create Required Files and Folders

Create these files in the project root:

```
requirements.txt
.gitignore
setup.py
Dockerfile
.env
.github/workflows/main.yaml
```

Create these folders:

```
Network_Data/       ← place phisingData.csv here
networksecurity/    ← main source package
notebooks/          ← optional Jupyter experiments
```

> **Critical:** Every folder inside `networksecurity/` must have an `__init__.py` file. Without it, Python does not recognise the folder as a package and all imports will fail.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create the `.env` File

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
MONGO_URL_KEY=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
```

> **Security:** Add `.env` and `venv/` to your `.gitignore` immediately. Never commit credentials.

### Step 5 — Install the Package Locally

```bash
pip install -e .
```

The `-e` (editable) flag installs `networksecurity` as a local Python package, making all internal imports like `from networksecurity.components.data_ingestion import DataIngestion` work correctly from any file in the project.

### Step 6 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/BikashBIOS/Network-Security.git
git push -u origin main
```

---

## 📄 File-by-File Code Walkthrough

---

### `setup.py` — Making the Project a Python Package

```python
from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            requirement = line.strip()
            if requirement and requirement != '-e .':
                requirement_list.append(requirement)
    except FileNotFoundError:
        print("Requirements file not found")
    return requirement_list

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Bikash",
    author_email="bikashojha101@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
```

`find_packages()` automatically scans all sub-folders that contain an `__init__.py` file and registers them as importable packages. This is why every sub-folder needs an `__init__.py`.

`get_requirements()` reads `requirements.txt` line by line and builds a list of dependencies. The `if requirement != '-e .'` guard removes the `-e .` self-referential install line if it appears in the file — installing a package as its own dependency would cause a circular error.

`install_requires=get_requirements()` tells pip to automatically install all listed packages whenever someone runs `pip install .` or `pip install -e .` on this project.

After running `pip install -r requirements.txt`, a `NetworkSecurity.egg-info/` folder is created — this is the package metadata directory confirming the package has been registered locally.

---

### `push_data.py` — ETL Pipeline (CSV → JSON → MongoDB)

This script implements the full **Extract → Transform → Load** pipeline to seed your MongoDB database with the phishing dataset.

```python
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()
```

`load_dotenv()` reads the `.env` file and injects all variables into the OS environment. `os.getenv("MONGO_DB_URL")` then retrieves the MongoDB connection string without ever hardcoding it in the source code — a critical security practice.

`certifi` is a Python package that bundles a set of trusted SSL/TLS root certificates. `certifi.where()` returns the file path to this certificate bundle. MongoDB Atlas requires a TLS-encrypted connection, and `ca` is later passed to `pymongo.MongoClient` so it can verify the server's SSL certificate.

```python
class NetworkDataExtract():
    def cv_to_json_converter(self, file_path):
        data = pd.read_csv(file_path)
        data.reset_index(drop=True, inplace=True)
        records = list(json.loads(data.T.to_json()).values())
        return records
```

`pd.read_csv(file_path)` loads the entire phishing CSV dataset into a Pandas DataFrame. Each row is a network connection sample; each column is a feature (URL length, presence of HTTPS, number of dots in URL, etc.).

`data.reset_index(drop=True, inplace=True)` reassigns row indices from 0 to N sequentially. `drop=True` prevents the old index from becoming a new column. `inplace=True` modifies the DataFrame in place rather than returning a copy.

`data.T` **transposes** the DataFrame — columns become rows and rows become columns. This is the key conversion trick: after transposing, each original row (one data sample) becomes a column, and `to_json()` converts each column into a JSON object like `{"feature1": val, "feature2": val, ...}`.

`json.loads(...).values()` parses the JSON string back into a Python dict and extracts just the values (the individual record dicts). `list(...)` converts the dict_values object into a plain Python list. The result is a list of dicts — exactly the format `pymongo.insert_many()` expects.

```python
    def insert_data_mongodb(self, records, database, collection):
        self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
        self.database = self.mongo_client[self.database]
        self.collection = self.database[self.collection]
        self.collection.insert_many(self.records)
        return len(self.records)
```

`pymongo.MongoClient(MONGO_DB_URL)` opens a persistent connection to your MongoDB Atlas cluster using the connection string from `.env`. MongoDB Atlas is a cloud-hosted NoSQL database — it stores your data as documents (JSON-like objects).

`self.mongo_client[self.database]` selects (or creates) a database named `BIKASHAI`. In MongoDB, databases and collections are created automatically on first write if they don't already exist — no schema definition required.

`self.collection.insert_many(self.records)` pushes all records at once in a single network call, which is far more efficient than calling `insert_one()` thousands of times in a loop. MongoDB assigns each record a unique `_id` field automatically.

```python
if __name__ == '__main__':
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "BIKASHAI"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json_converter(file_path=FILE_PATH)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)
```

**To run:**
```bash
python push_data.py
```
After execution, open MongoDB Atlas in the browser → Cluster0 → Collections → `BIKASHAI` database → `NetworkData` collection, and you will see all phishing records inserted as JSON documents.

---

### `networksecurity/constants/training_pipeline/__init__.py` — Shared Constants

This file acts as the **single source of truth** for all magic strings and numbers used across the pipeline. Centralising constants here means if you need to rename a folder or change a ratio, you change it in one place and it propagates everywhere.

Key constants include:

```python
# Pipeline artifact root
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"

# Data Ingestion constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "BIKASHAI"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

# Data Transformation constants
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

# Model Trainer constants
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_FILE_NAME = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05

# Target column
TARGET_COLUMN = "Result"
```

`DATA_TRANSFORMATION_IMPUTER_PARAMS` deserves special attention: `n_neighbors: 3` tells the KNN Imputer to look at the 3 nearest neighbours when estimating a missing value. `weights: "uniform"` means all 3 neighbours are weighted equally (alternative is `"distance"`, which gives closer neighbours more influence). These values are passed directly to sklearn's `KNNImputer`.

---

### `networksecurity/entity/config_entity.py` — Configuration Dataclasses

Config classes define **where everything is stored**. They are computed once at the start of a pipeline run and then threaded through every stage.

```python
@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, PIPELINE_NAME, timestamp)
    timestamp: str = timestamp
```

`TrainingPipelineConfig` establishes the **root artifact directory** for this specific run. The `timestamp` (formatted as `YYYY_MM_DD_HH_MM_SS`) ensures every training run gets its own uniquely-named folder. This means historical runs are never overwritten — you can always look back at artifacts from a previous execution.

```python
@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
    )
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
    )
    training_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
    )
    testing_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
    )
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name: str = DATA_INGESTION_COLLECTION_NAME
    database_name: str = DATA_INGESTION_DATABASE_NAME
```

This constructs a path structure like:
```
Artifacts/NetworkSecurity/2024_01_15_10_30_00/
  └── data_ingestion/
      ├── feature_store/
      │   └── phisingData.csv         ← raw full dataset
      └── ingested/
          ├── train.csv               ← 80% training split
          └── test.csv                ← 20% testing split
```

---

### `networksecurity/entity/artifact_entity.py` — Artifact Dataclasses

While config classes define **where to put things**, artifact classes define **what was produced**. After each pipeline stage, an artifact object is returned containing the actual file paths where outputs were saved. That artifact is then passed as input to the next stage.

```python
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str  # path to preprocessor.pkl
    transformed_train_file_path: str   # path to train.npy
    transformed_test_file_path: str    # path to test.npy

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
```

Using Python `@dataclass` is a clean, lightweight way to define these result containers. They behave like simple named tuples with dot-access syntax (`artifact.trained_file_path`), making the data handoff between pipeline stages readable and self-documenting.

---

### `networksecurity/components/data_ingestion.py` — Stage 1: Data Ingestion

This component is responsible for pulling raw data out of MongoDB and saving it locally in a structured folder.

```python
def export_collection_as_dataframe(self):
    database_name = self.data_ingestion_config.database_name
    collection_name = self.data_ingestion_config.collection_name
    self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
    collection = self.mongo_client[database_name][collection_name]
    df = pd.DataFrame(list(collection.find()))
    if "_id" in df.columns.to_list():
        df = df.drop(columns=["_id"], axis=1)
    df.replace({"na": np.nan}, inplace=True)
    return df
```

`collection.find()` with no arguments returns a cursor over every document in the MongoDB collection. Wrapping it in `list()` materialises all documents into memory, and `pd.DataFrame()` converts the list of dicts into a tabular structure.

`df.drop(columns=["_id"])` removes the MongoDB-generated ObjectId column. MongoDB automatically adds `_id` to every inserted document, but it has no predictive value for the ML model and would confuse sklearn transformers if left in.

`df.replace({"na": np.nan})` standardises missing value representation. The CSV may have stored missing values as the string `"na"` (a common issue in network security datasets), which pandas doesn't recognise as a null. Replacing with `np.nan` makes them detectable by `df.isnull()`, `df.dropna()`, and sklearn imputers.

```python
def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
    feature_store_file_path = self.data_ingestion_config.feature_store_file_path
    dir_path = os.path.dirname(feature_store_file_path)
    os.makedirs(dir_path, exist_ok=True)
    dataframe.to_csv(feature_store_file_path, index=False, header=True)
    return dataframe
```

`os.makedirs(dir_path, exist_ok=True)` creates the full directory path including any intermediate folders that don't exist yet. `exist_ok=True` prevents an error if the directory already exists — without this flag, re-running the pipeline would crash here.

The raw data is saved as a CSV at the `feature_store_file_path`. This "feature store" acts as a permanent local cache of the raw MongoDB data — if the database connection goes down, you can reprocess from here without re-querying MongoDB.

```python
def split_data_as_train_test(self, dataframe: pd.DataFrame):
    train_set, test_set = train_test_split(
        dataframe,
        test_size=self.data_ingestion_config.train_test_split_ratio
    )
    dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
    os.makedirs(dir_path, exist_ok=True)
    train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
    test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
```

`train_test_split()` from sklearn randomly shuffles and divides the dataset. With `test_size=0.2`, **80% of rows go to training** and **20% go to testing**. The split is random but reproducible if you pass a `random_state` parameter.

Why split here and not later? Splitting early ensures that **data validation, transformation, and model evaluation all operate on truly unseen test data**. If you applied transformations to the full dataset before splitting, statistical properties (like mean and variance used for normalisation) would leak from the test set into the training process — a form of data leakage that inflates evaluation scores.

---

### `networksecurity/components/data_validation.py` — Stage 2: Data Validation

This component checks two things: that the data has the expected structure, and that the data distribution hasn't shifted significantly.

```python
def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
    number_of_columns = len(self._schema_config)
    if len(dataframe.columns) == number_of_columns:
        return True
    return False
```

`self._schema_config` is loaded from `data_schema/schema.yaml`, which lists all expected column names. If the ingested data has a different number of columns than the schema specifies — perhaps due to a corrupt CSV export or a schema migration in MongoDB — this check fails immediately before wasting compute time on the rest of the pipeline.

```python
def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
    status = True
    report = {}
    for column in base_df.columns:
        d1 = base_df[column]
        d2 = current_df[column]
        is_same_dist = ks_2samp(d1, d2)
        if threshold > is_same_dist.pvalue:
            is_found = True
            status = False
        else:
            is_found = False
        report.update({column: {
            "p_value": float(is_same_dist.pvalue),
            "drift_status": is_found
        }})
    drift_report_file_path = self.data_validation_config.drift_report_file_path
    os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
    write_yaml_file(file_path=drift_report_file_path, content=report)
    return status
```

**The Kolmogorov-Smirnov (KS) Two-Sample Test** is a non-parametric statistical test that measures whether two distributions are drawn from the same underlying probability distribution. It works on any numerical distribution — no assumption of normality required.

`ks_2samp(d1, d2)` returns a `KstestResult` with two values: the `statistic` (the maximum absolute difference between the two cumulative distribution functions) and the `pvalue`. 

The **p-value** represents the probability of observing differences this extreme if the two distributions were actually the same. A low p-value (below the `threshold` of 0.05) means the distributions are **statistically significantly different** — i.e., drift is detected.

**Why does drift matter?** A model trained on data from January may perform poorly on data from September if, for example, attackers changed their URL patterns, or if network traffic characteristics shifted. The drift report flags which specific columns drifted, so you can decide whether to retrain or investigate.

The report is saved as a YAML file, recording the p-value for every column. This creates an auditable, human-readable drift log for each pipeline run.

---

### `networksecurity/components/data_transformation.py` — Stage 3: Data Transformation

This component prepares the validated data for the ML algorithm by handling missing values and restructuring the data into arrays.

```python
@staticmethod
def get_data_transformer_object() -> Pipeline:
    logging.info("Initializing KNNImputer transformer pipeline")
    imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
    processor = Pipeline(steps=[("imputer", imputer)])
    return processor
```

**KNN Imputer — How it Works Mathematically:**

Real-world network security data frequently has missing values — a sensor might fail to record a URL feature, or a field might be optional. Simply dropping rows with missing values wastes data; filling with the column mean/median ignores relationships between features.

`KNNImputer` uses the K-Nearest Neighbours algorithm to estimate missing values. For each row with a missing value in feature `X`, it finds the `k` most similar rows (based on Euclidean distance across all *non-missing* features), then fills the missing value with the average of those `k` rows' values for feature `X`.

With `n_neighbors=3`, each missing value is estimated from the 3 most similar rows. With `weights="uniform"`, all 3 neighbours contribute equally. This is a powerful technique because it respects the correlation structure of the dataset — a phishing URL that is similar to known phishing URLs in 30 other features will have its missing 31st feature imputed based on those similar phishing URLs.

```python
def initiate_data_transformation(self):
    train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
    test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

    # Feature and Target Separation
    input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
    target_feature_train_df = train_df[TARGET_COLUMN]
    input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
    target_feature_test_df = test_df[TARGET_COLUMN]
```

`TARGET_COLUMN = "Result"` is the label column. Separating features (`X`) from labels (`y`) before applying transformations is mandatory: you must never transform the target column with the same pipeline you use for features. The imputer should only learn patterns from input features.

```python
    # Target Label Cleaning
    target_feature_train_df = target_feature_train_df.replace(-1, 0)
    target_feature_test_df = target_feature_test_df.replace(-1, 0)
```

The phishing dataset originally uses `-1` for "legitimate" and `1` for "phishing". Binary classification algorithms in sklearn typically expect labels `{0, 1}`. Converting `-1 → 0` standardises the target space, preventing issues with certain loss functions and metrics that assume non-negative labels.

```python
    # Fit and Transform
    preprocessor = self.get_data_transformer_object()
    preprocessor_object = preprocessor.fit(input_feature_train_df)
    transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
    transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
```

`preprocessor.fit(input_feature_train_df)` **learns** the KNN structure from the training data — it builds the internal KD-tree or ball-tree used to find neighbours efficiently.

`preprocessor_object.transform(input_feature_train_df)` applies the learned imputation to the training features.

`preprocessor_object.transform(input_feature_test_df)` applies the **same** learned imputation to the test features. This is critical: the imputer must use the training data's neighbourhood structure to impute the test data. Fitting a separate imputer on test data would be data leakage.

```python
    # Data Recombination
    train_arr = np.c_[
        transformed_input_train_feature,
        np.array(target_feature_train_df)
    ]
    test_arr = np.c_[
        transformed_input_test_feature,
        np.array(target_feature_test_df)
    ]
```

`np.c_[...]` performs **column-wise concatenation** (the `c_` stands for "column stack"). It stacks the 2D transformed feature matrix and the 1D target array side-by-side, producing a single matrix where the last column is the label. This format is what `save_numpy_array_data()` stores as `.npy` files.

```python
    # Save transformed arrays and preprocessor
    save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
    save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
    save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
```

Saving the `preprocessor_object` as a `.pkl` file is essential. At prediction time, incoming data must be transformed in **exactly the same way** as the training data — same imputation strategy, same fitted parameters. By saving and loading this object at inference time, we guarantee consistency between training and serving.

---

### `networksecurity/components/model_trainer.py` — Stage 4: Model Training with MLflow

This is the core ML stage. It evaluates multiple classification algorithms, tunes hyperparameters, selects the best model, and logs everything to MLflow/DagHub.

```python
def train_model(self, x_train, y_train):
    models = {
        "Random Forest": RandomForestClassifier(verbose=1),
        "Decision Tree": DecisionTreeClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        "Logistic Regression": LogisticRegression(verbose=1),
        "AdaBoost": AdaBoostClassifier(),
    }

    params = {
        "Decision Tree": {
            'criterion': ['gini', 'entropy', 'log_loss'],
        },
        "Random Forest": {
            'n_estimators': [8, 16, 32, 128, 256]
        },
        "Gradient Boosting": {
            'learning_rate': [.1, .01, .05, .001],
            'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
            'n_estimators': [8, 16, 32, 64, 128, 256]
        },
        "Logistic Regression": {},
        "AdaBoost": {
            'learning_rate': [.1, .01, 0.5, 0.001],
            'n_estimators': [8, 16, 32, 64, 128, 256]
        }
    }

    model_report: dict = evaluate_models(
        X_train=x_train, y_train=y_train,
        X_test=x_test, y_test=y_test,
        models=models, param=params
    )
```

**What each algorithm does and why it is included:**

**Decision Tree** — Builds a tree of if-else rules on features (e.g., "if URL length > 75 AND contains '@' symbol → phishing"). Simple to interpret, prone to overfitting on its own, but useful as a baseline and for feature importance analysis. The `criterion` hyperparameter controls how the tree chooses splits: `gini` (Gini Impurity) and `entropy` (Information Gain) are mathematically different impurity measures but often produce similar trees; `log_loss` is newer and treats splits as probability estimates.

**Random Forest** — An ensemble of many Decision Trees, each trained on a random subset of training rows (bagging) and a random subset of features at each split. Final prediction is the majority vote across all trees. Random subsets reduce variance compared to a single tree. `n_estimators` controls how many trees to grow (more trees = more stable predictions, more compute time).

**Gradient Boosting** — Builds trees sequentially where each new tree specifically targets the residual errors of the previous ensemble. The `learning_rate` controls how much each new tree's contribution is shrunk — lower rates require more trees (`n_estimators`) but generalise better. `subsample < 1.0` means each tree is trained on a random fraction of the data (Stochastic Gradient Boosting), which further reduces overfitting. Gradient Boosting is frequently the top performer on tabular classification tasks.

**Logistic Regression** — A linear model that models the log-odds of the probability of phishing as a linear combination of features. Fast to train, highly interpretable, works well when the decision boundary is approximately linear. Included as a strong linear baseline.

**AdaBoost (Adaptive Boosting)** — An earlier boosting method that reweights training samples — misclassified samples get higher weights in the next iteration, forcing subsequent classifiers to focus on hard examples. `learning_rate` shrinks the contribution of each classifier.

```python
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    report = {}
    for i in range(len(list(models))):
        model = list(models.values())[i]
        para = param[list(models.keys())[i]]

        gs = GridSearchCV(model, para, cv=3)
        gs.fit(X_train, y_train)
        model.set_params(**gs.best_params_)
        model.fit(X_train, y_train)

        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_model_score = r2_score(y_train, y_train_pred)
        test_model_score = r2_score(y_test, y_test_pred)
        report[list(models.keys())[i]] = test_model_score
    return report
```

**GridSearchCV — Hyperparameter Tuning Explained:**

`GridSearchCV(model, param_grid, cv=3)` performs an exhaustive search over every combination of hyperparameter values in `param_grid`. For example, for Gradient Boosting with 4 `learning_rate` values × 5 `subsample` values × 6 `n_estimators` values = **120 combinations**. For each combination, it runs **3-fold cross-validation**: splits the training data into 3 equal parts, trains on 2 and validates on 1, repeats 3 times (rotating which part is the validation set), then averages the 3 scores. So Gradient Boosting alone runs 120 × 3 = **360 model fits** just during hyperparameter search. This exhaustive approach finds the best parameter combination at the cost of significant compute time.

`gs.best_params_` is a dict of the winning hyperparameter values. `model.set_params(**gs.best_params_)` applies those values to the model, and `model.fit(X_train, y_train)` trains the final version on the complete training set (not just 2/3 of it as in CV).

```python
    # Find the best model
    best_model_score = max(sorted(model_report.values()))
    best_model_name = list(model_report.keys())[
        list(model_report.values()).index(best_model_score)
    ]
    best_model = models[best_model_name]

    if best_model_score < MODEL_TRAINER_EXPECTED_SCORE:
        raise NetworkSecurityException("No best model found")
```

`MODEL_TRAINER_EXPECTED_SCORE = 0.6` is a quality gate. If even the best model scores below 0.6, the pipeline raises an exception rather than deploying a poor model. This protects production from silent model degradation.

```python
    # Overfitting / Underfitting check
    if abs(train_metric.f1_score - test_metric.f1_score) > MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:
        raise NetworkSecurityException("Model is overfitting or underfitting")
```

`MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD = 0.05` means if the F1 score on training data is more than 5 percentage points higher than on test data, the model is considered overfitted (memorised training data rather than learned generalisable patterns). Conversely, if both scores are low, the model is underfitting. Either condition triggers an exception.

```python
def track_mlflow(self, best_model, classificationmetric):
    with mlflow.start_run():
        f1_score = classificationmetric.f1_score
        precision_score = classificationmetric.precision_score
        recall_score = classificationmetric.recall_score

        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("precision", precision_score)
        mlflow.log_metric("recall", recall_score)
        mlflow.sklearn.log_model(best_model, "model")
```

**MLflow Experiment Tracking:**

`mlflow.start_run()` begins a new tracked experiment run. Every metric logged inside this context manager (`mlflow.log_metric()`) is stored in the `mlflow.db` SQLite database locally, and optionally pushed to DagHub's remote tracking server.

**Why track these specific metrics?**

**F1 Score** = `2 × (Precision × Recall) / (Precision + Recall)`. The harmonic mean of precision and recall. In phishing detection, both false positives (blocking legitimate sites) and false negatives (allowing phishing) are costly, so F1 provides a balanced single-number summary.

**Precision** = `True Positives / (True Positives + False Positives)`. Of all URLs the model flagged as phishing, what fraction actually were phishing? Low precision means too many legitimate sites are incorrectly blocked.

**Recall** = `True Positives / (True Positives + False Negatives)`. Of all actual phishing URLs, what fraction did the model catch? Low recall means dangerous phishing URLs are slipping through.

```python
import dagshub
dagshub.init(repo_owner='BikashBIOS', repo_name='Network-Security', mlflow=True)
```

DagHub is a platform for ML experiment tracking that integrates with MLflow. By initialising DagHub here, every `mlflow.log_metric()` call is mirrored to your DagHub repository's Experiments tab. You can then compare runs from different hyperparameter configurations side-by-side with interactive charts, filter by metric value, and visually identify the best model.

**To view experiments:**
```bash
mlflow ui   # opens http://localhost:5000 for local tracking
```
Or navigate to your DagHub repository → Experiments tab.

---

### `networksecurity/utils/ml_utils/metric/classification_metric.py` — Metrics

```python
def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    model_f1_score = f1_score(y_true, y_pred)
    model_recall_score = recall_score(y_true, y_pred)
    model_precision_score = precision_score(y_true, y_pred)
    classification_metric = ClassificationMetricArtifact(
        f1_score=model_f1_score,
        precision_score=model_precision_score,
        recall_score=model_recall_score
    )
    return classification_metric
```

All three sklearn metric functions (`f1_score`, `recall_score`, `precision_score`) default to binary classification mode, which is correct for this project since `Result` is `0` or `1`. The results are packaged into the `ClassificationMetricArtifact` dataclass for structured downstream usage.

---

### `networksecurity/utils/ml_utils/model/estimator.py` — NetworkModel Wrapper

```python
class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)
```

`NetworkModel` bundles the **fitted preprocessor** and the **trained model** into a single object. This is the object that gets serialised to `final_model/model.pkl` and loaded at inference time.

`self.preprocessor.transform(x)` applies the same KNN imputation that was fitted on training data to the incoming prediction data. This guarantees that missing values in new data are handled identically to how they were handled during training.

`self.model.predict(x_transform)` passes the transformed features through the best ML model to produce predictions. The `y_hat` notation is the ML convention for "predicted y values" (as opposed to `y` for true labels).

---

### `networksecurity/pipeline/training_pipeline.py` — Full Orchestrator

```python
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        return data_ingestion_artifact

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        data_validation_config = DataValidationConfig(self.training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        return data_validation_artifact

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        return data_transformation_artifact

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        return model_trainer_artifact

    def sync_artifact_dir_to_s3(self):
        aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
        self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)

    def sync_saved_model_dir_to_s3(self):
        aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
        self.s3_sync.sync_folder_to_s3(folder=MODEL_TRAINER_TRAINED_MODEL_DIR, aws_bucket_url=aws_bucket_url)

    def run_pipeline(self) -> ModelTrainerArtifact:
        data_ingestion_artifact = self.start_data_ingestion()
        data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
        data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
        model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        self.sync_artifact_dir_to_s3()
        self.sync_saved_model_dir_to_s3()
        return model_trainer_artifact
```

`run_pipeline()` is the master orchestration function. Each stage's output artifact is automatically passed as the input to the next stage. This **artifact chaining** is the design pattern that makes the pipeline robust: each stage only knows about its own config and the upstream artifact, not the details of any other stage.

After training completes, `sync_artifact_dir_to_s3()` uploads the entire `Artifacts/` folder (with all intermediate data, drift reports, and transformed arrays) to S3 under a timestamped key. `sync_saved_model_dir_to_s3()` uploads just the final model files. This ensures artifacts are preserved in the cloud even if the local EC2 instance is terminated.

---

### `main.py` — Manual Pipeline Runner

```python
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    trainingpipelineconfig = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
    data_ingestion = DataIngestion(dataingestionconfig)
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    # ... continues through all 4 stages manually
```

`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` explicitly sets the console output encoding to UTF-8. This prevents `UnicodeEncodeError` crashes on Windows systems when the pipeline logs contain non-ASCII characters (common with progress bars or special symbols in dependency libraries).

`main.py` runs the same four pipeline stages as `training_pipeline.py`'s `run_pipeline()`, but calls each one individually. This is useful for **debugging** — you can comment out stages below the one you're testing and inspect the artifact output at each step without re-running the full pipeline.

**To run:**
```bash
python main.py
```

---

### `app.py` — FastAPI Web Server

```python
import certifi
ca = certifi.where()
mongo_db_url = os.getenv("MONGO_URL_KEY")
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]
```

Establishes a persistent MongoDB connection at server startup. `tlsCAFile=ca` enables TLS certificate verification for the encrypted MongoDB Atlas connection. The `database` and `collection` objects are kept as module-level globals — connection pooling means this single `MongoClient` is reused across all requests without creating a new connection per request.

```python
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

`CORSMiddleware` (Cross-Origin Resource Sharing) is required when a frontend hosted at one domain (e.g., `http://yourfrontend.com`) makes API calls to a backend at a different domain or port (e.g., `http://your-ec2-ip:8000`). `origins = ["*"]` permits any origin — appropriate for development; in production you would restrict this to your specific frontend domain.

```python
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
```

The root route redirects to `/docs`, FastAPI's auto-generated **Swagger UI** — an interactive browser-based API testing page built from your route definitions. No manual documentation writing required.

```python
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
```

Clicking "Execute" on the `/train` endpoint in the Swagger UI triggers the complete 4-stage ML pipeline — data ingestion from MongoDB, validation, KNN transformation, multi-model training with GridSearchCV, MLflow logging, and S3 sync — all from a single HTTP GET request.

```python
templates = Jinja2Templates(directory="./templates")

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    preprocesor = load_object("final_model/preprocessor.pkl")
    final_model = load_object("final_model/model.pkl")
    network_model = NetworkModel(preprocessor=preprocesor, model=final_model)
    y_pred = network_model.predict(df)
    df['predicted_column'] = y_pred
    os.makedirs('prediction_output', exist_ok=True)
    df.to_csv('prediction_output/output.csv', index=False)
    table_html = df.to_html(classes='table table-striped')
    return templates.TemplateResponse("tables.html", {"request": request, "table": table_html})
```

`UploadFile = File(...)` tells FastAPI to accept a multipart file upload. The `...` (Ellipsis) marks the field as required.

`load_object("final_model/preprocessor.pkl")` deserialises the `KNNImputer` pipeline that was fitted and saved during training. `load_object("final_model/model.pkl")` deserialises the best sklearn classifier. Critically, these are the same fitted objects from training — the imputer's learned neighbour structure and the model's learned weights are preserved exactly.

`df.to_html(classes='table table-striped')` converts the entire prediction DataFrame into an HTML `<table>` string, applying Bootstrap CSS classes for styled alternating-row colouring. `Jinja2Templates.TemplateResponse` injects this HTML string into `tables.html`'s `{{ table }}` placeholder and returns the fully rendered HTML page.

**To run locally:**
```bash
uvicorn app:app --reload
# Opens at http://127.0.0.1:8000
# Go to http://127.0.0.1:8000/docs for Swagger UI
```

---

### `Dockerfile` — Container Definition

```dockerfile
FROM python:3.10-slim-bullseye
WORKDIR /app
COPY . /app
RUN apt update -y && apt install awscli -y
RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]
```

`FROM python:3.10-slim-bullseye` starts from an official Python 3.10 image based on Debian Bullseye ("slim" removes unnecessary packages, reducing the image size from ~1GB to ~150MB).

`WORKDIR /app` sets the working directory inside the container. All subsequent `COPY`, `RUN`, and `CMD` instructions execute relative to `/app`.

`COPY . /app` copies the entire project directory (everything not in `.dockerignore`) into the container at `/app`.

`RUN apt install awscli -y` installs the AWS CLI inside the container, enabling the S3 sync functions in `training_pipeline.py` to work when the container runs on EC2.

`CMD ["python3", "app.py"]` is the default command that runs when the container starts. It launches the FastAPI server via `app.py`'s `if __name__ == "__main__": app_run(app, host="0.0.0.0", port=8000)`. Using `host="0.0.0.0"` makes the server bind to all network interfaces, which is required for the EC2 instance's public IP to reach the container.

---

## 🚀 Running the Project Locally

```bash
# Step 1 — Activate environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Step 2 — Push phishing data to MongoDB (only needed once)
python push_data.py

# Step 3 — Start the FastAPI server
uvicorn app:app --reload

# Step 4 — Open in browser
# http://127.0.0.1:8000/docs
```

**Training:**
1. Go to `/train` in Swagger UI → Click **Try it out** → Click **Execute**
2. Watch the terminal — the full pipeline runs: MongoDB pull → validation → KNN transformation → GridSearchCV across 5 models → MLflow logging
3. After completion: `final_model/model.pkl` and `final_model/preprocessor.pkl` are saved
4. A success response appears in the browser

**Prediction:**
1. Go to `/predict` in Swagger UI → Click **Try it out**
2. Upload `valid_data/test.csv`
3. Click **Execute**
4. The response renders an HTML table with a new `predicted_column` added
5. `prediction_output/output.csv` is also saved locally

---

## ☁️ AWS Setup — S3, ECR & EC2 Deployment

### Step 1 — Configure AWS CLI

```bash
# Install AWS CLI (download from aws.amazon.com/cli)
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g. ap-south-1), Output format (json)
```

**Create an IAM User with Admin Access:**

1. AWS Console → IAM → Users → Create User (`testsecurity`)
2. Attach Policy: `AdministratorAccess`
3. Security Credentials → Create Access Key → Select CLI → Copy Key ID and Secret

### Step 2 — Create S3 Bucket

1. AWS Console → S3 → Create Bucket
2. Bucket name must exactly match `TRAINING_BUCKET_NAME` in `constants/training_pipeline/__init__.py`
3. Uncheck "Block all public access" if needed for EC2 access

After training, artifacts and final models are automatically pushed to:
```
s3://<TRAINING_BUCKET_NAME>/artifact/<timestamp>/
s3://<TRAINING_BUCKET_NAME>/final_model/<timestamp>/
```

### Step 3 — Create ECR Repository (Docker Image Registry)

1. AWS Console → ECR → Create Repository → Name it (e.g., `networksecurity`)
2. Copy the repository URI (format: `<account_id>.dkr.ecr.<region>.amazonaws.com/networksecurity`)

### Step 4 — Add GitHub Secrets

Go to your GitHub repo → Settings → Secrets and Variables → Actions → Add:

| Secret Name | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your IAM access key |
| `AWS_SECRET_ACCESS_KEY` | Your IAM secret key |
| `AWS_REGION` | e.g. `ap-south-1` |
| `AWS_ECR_LOGIN_URI` | ECR URI without the repo name |
| `ECR_REPOSITORY_NAME` | e.g. `networksecurity` |

### Step 5 — GitHub Actions CI/CD Pipeline (`.github/workflows/main.yaml`)

The workflow has three jobs that run automatically on every push to `main`:

**Job 1 — Continuous Integration:**
Checks out code, lints, runs tests. Ensures the code is valid before building anything.

**Job 2 — Continuous Delivery (Build & Push to ECR):**
```yaml
- name: Build, tag, and push image to Amazon ECR
  run: |
    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
```
Builds the Docker image from the `Dockerfile`, tags it as `latest`, and pushes to AWS ECR. After this job, the Docker image is available in your ECR repository.

**Job 3 — Continuous Deployment (Pull & Run on EC2):**
```yaml
- name: Pull image from ECR and run
  run: |
    docker pull $ECR_REGISTRY/$ECR_REPOSITORY:latest
    docker run -d -p 8080:8000 $ECR_REGISTRY/$ECR_REPOSITORY:latest
```
Runs on the **self-hosted runner** (your EC2 instance), pulls the latest Docker image from ECR, and starts the container, mapping EC2 port 8080 to the container's port 8000.

### Step 6 — Set Up EC2 Instance

1. AWS Console → EC2 → Launch Instance
2. Name: `NetworkSecurityInstance`, AMI: Ubuntu 22.04, Instance type: `t3.micro` (free tier)
3. Create/select a key pair, launch

**Connect and install Docker on EC2:**
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

**Register EC2 as a GitHub Self-Hosted Runner:**
1. GitHub Repo → Settings → Actions → Runners → New self-hosted runner → Linux
2. Execute the 4 download/extract commands on EC2
3. Run the config command, enter runner name as `self-hosted`
4. Run `./run.sh` — the runner status shows as Idle in GitHub

**Open EC2 Security Group Port:**
1. EC2 → Security Groups → Edit Inbound Rules → Add Custom TCP port `8080`, source `0.0.0.0/0`

**Access your deployed app:**
```
http://<EC2-Public-IPv4>:8080/docs
```

---

## 📊 MLflow + DagHub Experiment Tracking

After running `/train` (either locally or via the API), visit your DagHub repository:

1. Go to [dagshub.com](https://dagshub.com) → Login with GitHub → Create repository from existing GitHub repo
2. Navigate to the **Experiments** tab
3. You will see each training run logged with F1, Precision, and Recall metrics for both training and test data
4. Use the **Compare** feature to view side-by-side bar charts and scatter plots across runs
5. The best model's parameters and metrics are logged alongside the serialised `model.pkl` artifact

**To view MLflow UI locally:**
```bash
mlflow ui
# Opens http://127.0.0.1:5000
```

---

## 📊 Results

### Model Comparison — F1 Score

Five classifiers were benchmarked with hyperparameter tuning (GridSearchCV) during training. Each model's F1 score was logged as a separate MLflow/Dagshub experiment run for full comparison and auditability.

| Rank | Model | F1 Score |
|:---:|---|:---:|
| 🥇 | **Random Forest** | **0.9711** |
| 🥈 | Decision Tree | 0.9649 |
| 🥉 | Gradient Boosting | 0.9635 |
| 4 | Logistic Regression | 0.9352 |
| 5 | AdaBoost | 0.9320 |

**Winning Model: Random Forest** (F1 Score: **0.9711**) — selected automatically based on the highest F1 score across all candidates.

---

### Experiment Tracking (MLflow + Dagshub)

All 5 candidate models, plus the winning model's performance on both the training and testing splits, are tracked as separate experiment runs:

- **5 comparison runs** — one per candidate model (`Random Forest_comparison`, `Decision Tree_comparison`, `Gradient Boosting_comparison`, `Logistic Regression_comparison`, `AdaBoost_comparison`), each logging `model_name` and `score`.
- **2 train/test runs** — the winning model (Random Forest) evaluated separately on training data and testing data, logging `f1_score`, `precision`, and `recall_score`.

**Random Forest — Train vs. Test Performance:**

| Metric | Training Set | Testing Set |
|---|:---:|:---:|
| F1 Score | 0.971 | 0.992 |
| Precision | 0.961 | 0.990 |
| Recall | 0.982 | 0.994 |

Consistently high scores across both splits (with no signs of overfitting — testing performance matches or exceeds training performance) confirm the model generalizes well to unseen data.

View live experiment comparisons on [Dagshub Experiments](https://dagshub.com/BikashBIOS/Network-Security/experiments) or via the MLflow UI (`mlflow ui`).

---

### Captured Logs

```
[ 2026-07-08 18:40:46,119 ] 94 root - INFO - Model Report: {'Random Forest': 0.9710661910424099, 'Decision Tree': 0.9649402390438248, 'Gradient Boosting': 0.9634630659253376, 'Logistic Regression': 0.9352290679304898, 'AdaBoost': 0.9319701140385371}

[ 2026-07-08 18:40:46,119 ] 103 root - INFO - Best Model: Random Forest with score 0.9710661910424099
```

---

### Results

Please see the Results screenshots in Results.pdf file.


---


## 🧱 Key ML Concepts Explained

**KNN Imputer** estimates missing values by finding the K most similar rows in the dataset (based on non-missing features) and averaging their value for the missing feature. This respects feature correlations better than mean/median imputation.

**KS Test (Kolmogorov-Smirnov)** is a statistical test to detect whether two samples come from the same distribution. Used here to catch data drift — when live incoming data starts looking statistically different from training data, model performance degrades.

**GridSearchCV** exhaustively tries every combination of specified hyperparameter values using K-fold cross-validation to find the optimal configuration for each algorithm.

**Artifact Chaining** is the design pattern where each pipeline stage produces a typed output (an "artifact") that is passed directly as input to the next stage. This makes stages loosely coupled, independently testable, and easy to restart mid-pipeline.

**Data Leakage Prevention** is enforced by (1) splitting train/test before any transformations, (2) fitting the imputer only on training data, and (3) applying the fitted imputer to test data — never fitting on test data.

**The `preprocessor.pkl` at Serving Time** ensures that raw incoming prediction data goes through the same imputation process the model was trained on, preventing distribution mismatch between training and inference.

---

## 📦 Requirements

| Package | Purpose |
|---|---|
| `scikit-learn` | KNNImputer, RandomForest, GradientBoosting, GridSearchCV, all ML algorithms |
| `pandas` | DataFrame operations, CSV I/O |
| `numpy` | Array operations, `.npy` file storage |
| `pymongo[srv]` | MongoDB Atlas connection via SRV connection string |
| `certifi` | SSL/TLS root certificates for secure MongoDB connection |
| `python-dotenv` | Loads `.env` file into OS environment variables |
| `mlflow` | Experiment tracking — logs metrics, parameters, model artifacts |
| `dagshub` | Remote MLflow tracking server integrated with GitHub |
| `dill` | Extended pickle serialisation (handles lambda functions, closures) |
| `pyaml` | YAML file reading/writing (drift reports, schema config) |
| `fastapi` | Asynchronous Python web framework for `/train` and `/predict` APIs |
| `uvicorn` | ASGI server that runs FastAPI |
| `python-multipart` | Required by FastAPI to handle `UploadFile` file uploads |
| `setuptools` | `find_packages()` and `setup()` for packaging |

---

## 🗝️ Environment Variables Required

| Variable | Purpose |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string (used by `push_data.py`) |
| `MONGO_URL_KEY` | MongoDB Atlas connection string (used by `app.py`) |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key for S3 sync |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret for S3 sync |
| `AWS_REGION` | AWS region for ECR and S3 |

---

*Made with ❤️ by [BikashBIOS](https://github.com/BikashBIOS)*
