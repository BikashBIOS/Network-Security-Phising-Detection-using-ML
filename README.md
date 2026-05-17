# Network Security Project for Phising Data

## Requirements & GitHub
1. Create new env -- python -m venv venv
2. Create files - requirements.txt, .gitignore, setup.py, .github/workflows/main.yaml, Dockerfile, .env
3. Create folders as per the project requirement :
- Network_Data - for your data (added phisingdata.csv)
- networksecurity - for your main codes(src)
- notebooks - for your jupyter notebooks
4. Specify your libraries in the requirements.txt and then run pip install -r requirements.txt
5. Write venv and .env files in the .gitignore for the git to ignore all these files while pushing the code to our github repo.
6. Create a new github repo - Network Security and then push the code : 
- git init
- git add .
- git commit -m "First commit"
- git branch -M main
- git remote add origin https://github.com/BikashBIOS/Network-Security.git
- git push -u origin main
7. Remember to add __init__.py in all the folders. Push again.


## Setup.py 
1. Specify the code in setup.py to get the libraries from requirements.txt
2. Specify the version, package info and retrieve from get_requirements()
3. After executing pip install -r requirments.txt, you can see your package folder getting created with all the info and requirements. 


## Logging and Exception
1. Create the logging and Exception file as per the generic code of logging and exception.
2. __main__ file in exception can be used to test if exception is working fine or not. 


## ETL Pipeline (Extract, Transform, Load)
1. We have our Source and Destination between that 'Transformation' happens.
2. Source here is our local database from which we EXTRACT the csv dataset, we apply TRANSFORMATION to this dataset to change it to json, then we LOAD the data in the destination i.e our MongoDB.


## MongoDB Connection
1. Create a new Free account in MongoDB Atlas. 
2. Create a default Cluster0 cluster.
3. Let the default username and password remain. 
4. Click Next -> Choose a connection Method -> Click on Drivers
5. Select Driver as Python and version.
6. Add the pymongo libraray version in requirements.txt file.
7. Then click on Done and the Cluster0 will be created.
8. Then click on Connect on the cluster. Check the full code sample. Copy that code. 
9. Create a new file - push_data.py in root folder and paste that code. 
10. In the code, we have to change the dbpassword (in uri object) to our password. (If you have forgotten, go to Quickstart and then you can update the password for your username).
11. The uri object shouldn't be hardcoded, so to ensure that, we add the same uri string in our .env file. 
12. Now run python push_data.py and if all is good, it will show You successfully connected to MongoDB.
13. Cut the push_data.py code into a new file - test_mongodb.py as we will use it later. 
14. In push_data.py, load that env variable. Get the MONGO_DB_URL from env file and print. 



## ETL Pipeline Setup with Python/Inserting Record into MongoDB
1. Import certifi in push_data.py
2. Certifi - Python package that provides a set of root certificates - commonly used to make a secure HTTP connection.
3. Now we will write the function for converting our csv data to json. 
4. Json data is basically One row's data in key:value pairs while key being column and value being row value. And one row's data would be in a dict with key values pairs.
5. cv_to_json_converter() - converts the csv data into json and stores the json records in records.
6. insert_data_mongodb() - create the database, collection and records. Connect to your mongodb client and then create the database and collection. Then insert and return the records.
7. __main__() - To run this, pass in the FILE_PATH for your dataset (i.e phisingData.csv), give some random name to your dataset and collection, Call the NetworkDataExtract() to convert the data to json, and then insert_data_mongodb() - to insert your data into MongoDB cluster.
8. After you run python push_data.py - the data gets inserted into MongoDB cluster database. Open that Cluster0 in browser, and open the database, and you can find your json data inserted into it. 


## Data Ingestion Summary
1. Data Ingestion Config - It is the basic info to where our data will be stored, train test split, their paths and other things. 
2. Read the data from MongoDB and converting this data to a Data Ingestion Artifact based on Data Ingestion Config features. 
3. Artifact would contain our raw data - train and test split also. 
4. Then we will do feature engineering on the train and test data and then proceed for Data Transformation.


## Data Ingestion Configuration
1. Create training_pipeline folder in constants -> in that create __init__.py where you store the common data that we insert into our Data Ingestion Config. Also define the common constant variable in training pipeline i.e raw data, train and test data. 
2. Go to MongoDB -> Network Access -> IP Access List -> Create New IP Address -> Add 0.0.0.0/0 
3. Create config_entity.py in entity folder. Edit it acc. to the below points:
- Goal : To create Folder Artifact -> Date and Time folder -> Data Ingestion -> feature store -> data.csv
- TrainingPipelineConfig() - sets the timestamp and main folder. (self.artifact_dir: It joins the main "Artifact" folder name with the "Timestamp".)
- DataIngestionConfig() - defines exactly where the data goes during the Data Ingestion phase (pulling data from a source)
- self.data_ingestion_dir: Creates a sub-folder inside your timestamped artifact folder specifically for ingestion.
- self.feature_store_file_path: This is where the raw data is saved.
- self.training_file_path & self.testing_file_path: Once the code splits the training and test data, it saves those two specific files in the ingested folder.
- self.train_test_split_ratio: A number (like 0.2) that tells the code how much data to keep aside for testing.
- self.collection_name & database_name: Since you'll likely pull data from your MongoDB's database and collection. 


## Data Ingestion Component/Initiate
### Read the Data from MongoDB -> Create Feature Store -> Split Test and Train Data -> Save in Ingested folder.
#### Read Data from MongoDB:
1. Create data_ingestion.py in components folder. Edit code as per below:
- export_collection_as_dataframe() - Connects to MongoDB database and converts into a dataframe. 
- collection.find(): It grabs every single record in that database table.
- pd.DataFrame() - converts to dataframe.
- Drop the _id column (_id column is always present if you retrieve data from MongoDB).
- Replace NA values with NAN (null value).
- initiate_data_ingestion() - collect the data frame using the above function. 
#### Create Feature Store
- export_data_into_feature_store() - gets the df data -> Stores in the feature store by converting into csv in feature_store_file_path
#### Split Training and Testing Data
- split_data_as_train_test() - divides the above csv data into train and test csv. 
- os.makedirs(dir_path) - It looks at the path you defined (Artifacts/timestamp/data_ingestion/ingested)
- It saves the Training data to your training_file_path and Testing data to testing_file_path.
- Call split_data_as_train_test() function in initiate_data_ingestion() with the dataframe.
2. Create artifact_entity.py in entity folder and initialize DataIngestionArtifact dataclass to store your Trained and Test data in Artifacts folder.
- Now call this dataclass in initiate_data_ingestion() - with the trained data and test data file path.
3. Create main.py in your root folder and call TrainingPipelineConfig and DataIngestionConfig
- From that, create DataIngestion() obj and then use initiate_data_ingestion() to start the Full Process of Data Ingestion. 
- Execute python main.py - if it will create artifacts folder with train and test.csv in ingested folder and raw data in feature store, then our code is a success.
4. If your code is success, delete the Artifacts folder and logs folder, then commit the code.


## Data Validation Configuration
Validate data based upon:
- Our dataset should have same no. of features(columns). 
- Data Drift - it happens when the data you see today is significantly different from the data you used to train the model.
- Validate no. of columns, numerical columns exist or not. 
1. In training_pipeline.py, you store the common data - Data validation, invalid, valid data, Drift report, preprocessing.pkl - that we insert into our Data Validation Config.
2. Then in config_entity.py, we use DataValidation() to get the paths for valid data, invalid data, train invalid and valid, test valid and invalid data, data drift report. 
3. Add the no. 2 values in DataValidationArtifact dataclass also in artifact_entity.py
4. Create data_schema folder in root. Then create schema.yaml file and paste the code in that. Also specify the path for this in training_pipeline > __init__.py file.
5. Create main_utils folder in utils > Add __init__.py and utils.py in it. Now add the code in utils.py for reading yaml file. 
6. Create data_validation.py, then write code below:
- initialize dataingestionartifact and datavalidationartifact and then read the schema file. 


## Data Validation Initiation
1. Load the training and test data with their filepath. 
2. status checks the no. of columns defined in our schema on the training and testing data. 
3. Then we need to check the data drift - compares the distribution of the test data against the training data to see if the statistical properties have shifted significantly. Result would be stored as True or False. 
4. Store the validated data in the new folder path. 
5. Save the trained and test data frames as CSV in the path. 
6. Create Data Validation Artifact which checks the Status based on the Training and Test data. If the data drift is detected and then store the data in the specific path. 
7. To run this data validation, go to main.py -> Initialize the data validation config and data validation (pass the data validation config and data ingestion artifact).
8. At last, then initialize the data validation artifact by calling the initiate_data_validation(). 


## Data Transformation
1. Add the class DataTransformationConfig in the config_entity.py.
2. Add the dataclass Data Transformation Artifact in artifact_entity.py
3. Add the Data Transformation related costants in constants>training_pipeline>__py_cache__>__init__.py
4. Add the new functions - save_numpy_array_data(), save_object(), load_object() and load_numpy_array_data() in utils>utils.py
5. Now create a new data_transformation.py file and write the code there. 
6. Load the Validated Data: Load the training and test DataFrames using the file paths provided by the DataValidationArtifact.
7. Feature and Target Separation: Separate the features from the target column for both training and testing datasets by dropping the TARGET_COLUMN.
8. Target Label Cleaning: Replace the target labels (specifically converting -1 to 0) to ensure the target feature is in a standard format for the model.
9. Initialize Preprocessing Object: Create a get_data_transformer_object which initializes a KNNImputer using parameters defined in your constants. This pipeline handles missing values by estimating them based on the "nearest neighbors" in the data.
10. Fit and Transform:
Fit the preprocessor on the training features to learn the imputation patterns.
Apply the transformation to both the training and testing feature sets.
11. Data Recombination: Combine the transformed features back with their respective target columns using np.c_ to create final training and testing arrays.
12. Artifact Storage:
Save the transformed training and testing data as NumPy arrays (.npy) in the designated folder.
Save the preprocessor object as a pickle file (.pkl) so it can be reused during model prediction/deployment.
13. Create Data Transformation Artifact: Generate an artifact containing the paths to the transformed data and the saved preprocessor object.
14. Execution via main.py: To run this component, initialize the DataTransformationConfig and DataTransformation class (passing the config and the DataValidationArtifact), then call the initiate_data_transformation() method.


## Model Trainer (along with MLFlow and Dagshub)
1. Define ModelTrainerConfig class in config_entity.py
2. Create Model Trainer constants DIR NAME in constants>training pipeline> __init__.py
3. Add 2 data class - Classification Metrics and Model Trainer Artifacts in artifact_entity.py
4. Create load_object and load_numpy_array_data functions in utils.py
5. Create 2 folders - metric and model in utils folder.
6. Create classification_metric in metric folder and write the function to get the classification score like recall, f1 score, precision score.
7. Create estimator.py in model folder of utils > Then write the code for prediction. (Ensure you use SAVED_MODEL and MODEL FILE NAME in __init__.py > constants)
8. Create model_trainer.py in components and write the following code:
9. Create Model Trainer class with model trainer config and data transformation artifact.
10. Create the inititate_model_training() and pass the train and test data. Then divide into X and y.
11. Then create train_model() to load the models, apply hyperparameter tuning. 
12. Then pass these values in the evaluate_model() > We can configure this function in the utils.py.
13. Find the best model with the code.
14. Then get the classification score for both test and train. 
15. Load the object and model in the designed path using load_object() and load numpy array().
16. Then make your Network Model using your best model and preprocessor and then save your object in the pickle .pkl file. 
16. Then make the ModelTrainerArtifact and return it. 
17. Create the track_mlflow() -> to execute the classification score, f1 score, precision score and recall score.
18. Then apply this function to your best model to calculate the scores in the MLFlow. 
19. In terminal, run "mlflow ui" -> to generate a link - where you can access MLFlow website to view your data.
20. Then we can mention Dagshub -> Go to Dagshub -> Login by Github -> Create the repository from your exisiting Github repo and then go to Experiments tab -> Copy the import dagshub and your repository line in your model_trainer.py file. (import dagshub)
21. Then run python main.py -> To execute the training process for the model training and then it will be saved into your dagshub. 
22. In the 'Experiments' tab -> we can see the 2 models created -> Then we can compare the 2 models and see the classification scores and graphs. 
23. Based on your best model, the model.pkl will be saved in final_model folder and the preprocessing.pkl file will also be based from data_transformation.py


## PIPELINE of Model Training
1. Create 2 py files - batch_prediction and training_pipeline in 'pipeline' folder.
2. Start writing code in training_pipeline.py : 
3. Initialization (__init__)
Sets up the base TrainingPipelineConfig, which holds the global configurations needed across the entire pipeline.
4. Stage 1: Data Ingestion (start_data_ingestion)
Action: Fetches or loads the raw data.
Process: Initializes DataIngestion using its specific config.
Output: Returns a DataIngestionArtifact (contains paths to the train and test files).
5. Stage 2: Data Validation (start_data_validation)
Input: Requires the DataIngestionArtifact from Stage 1.
Action: Checks the ingested data for structural integrity and data drift.
Output: Returns a DataValidationArtifact (contains paths to validated, clean data).
4. Stage 3: Data Transformation (start_data_transformation)
Input: Requires the DataValidationArtifact from Stage 2.
Action: Applies feature engineering, scaling, or encoding to prepare the data for the algorithm.
Output: Returns a DataTransformationArtifact (contains paths to the transformed data and preprocessing objects).
5. Stage 4: Model Training (start_model_trainer)
Input: Requires the DataTransformationArtifact from Stage 3.
Action: Trains the actual machine learning model using the prepared data.
Output: Returns a ModelTrainerArtifact (contains paths to the final trained model and performance metrics).
6. Master Orchestration (run_pipeline)
This is the main trigger function. It executes Stages 1 through 4 in sequential order.
It automatically handles passing the artifact from one step directly into the next step.
Ultimately returns the final model_trainer_artifact.


## APP.PY - To execute all the above functions in our Frontend by creating APIs.
1. Create app.py in your main/root folder.
2. Install fastapi and uvicorn libraries.
3. Start writing code in app.py : 
4. Database Connection & Setup :
-> Initializes a MongoDB client connection (pymongo.MongoClient) using a secure database URL and a TLS certificate (tlsCAFile=ca) to encrypt the connection.
-> Targets a specific database and collection dynamically using predefined constants (DATA_INGESTION_DATABASE_NAME and DATA_INGESTION_COLLECTION_NAME).
5. FastAPI App Initialization
-> Instantiates the web application object with app = FastAPI().
6. CORS Middleware Configuration
-> Registers CORSMiddleware with origins = ["*"] (wildcard). This permits frontend applications hosted on any domain or port to securely communicate with this backend API, allowing all HTTP methods and headers.
7. Root Route Redirect (/)
-> Defines a basic GET endpoint for the root URL (/).
-> Automatically redirects users to /docs, which is FastAPI's built-in interactive Swagger UI documentation page where all available APIs can be tested.
8. Model Training Route (/train)
-> Exposes an asynchronous GET endpoint at /train to kick off the ML pipeline.
-> Logic: Instantiates the TrainingPipeline object and calls its run_pipeline() method to execute data ingestion, validation, transformation, and training.
-> Success Response: Returns "Training is successful" if the pipeline finishes without crashing.
9. Now initialize the main function to execute the app.py
10. Run "uvicorn app:app --reload" in terminal to execute the app.py in your localhost.
11. Open Localhost link -> Go to default/train and execute it. 
12. After you execute, the full project will start training and new train and test experiments models will be created to compare in Dagshub. 


## Batch Prediction PIPELINE
1. Create templates folder > tables.html > Write the prewritten html code.
2. Create valid_data folder > paste the test.csv (data in which you want to predict via your model)
3. Now add the following code for /predict in app.py:
4. Template Engine Initialization
-> Sets up Jinja2Templates to look into the ./templates folder, allowing FastAPI to serve and render dynamic HTML files.
5. File Upload and Data Loading
-> Exposes a POST route at /predict that accepts a user-uploaded file via UploadFile.
-> Reads the incoming raw uploaded file straight into a Pandas DataFrame using pd.read_csv(file.file).
6. Model Loading and Wrapper Initialization
-> Deserializes and loads two critical components from the local disk (final_model/ directory) using a helper function load_object():
-> The feature preprocessing object (preprocessor.pkl).
-> The trained machine learning classification/regression algorithm (model.pkl).
-> Binds both items together inside a custom wrapper class named NetworkModel.
7. Prediction Logic
-> Passes the entire DataFrame into the network_model.predict(df) method to generate model inferences (y_pred).
-> Appends these results back into the original data by creating a brand-new column named predicted_column.
8. Output Persistence (File Saving)
-> Ensures the target folder prediction_output exists via os.makedirs(..., exist_ok=True).
-> Saves the newly updated DataFrame containing the predictions as a CSV file locally (prediction_output/output.csv) without keeping the DataFrame row index.
9. HTML Presentation and Rendering
-> Converts the entire Pandas DataFrame into a raw HTML table string via df.to_html(), applying Bootstrap styling classes (table table-striped) for a polished frontend appearance.
-> Returns a TemplateResponse targeting "tables.html" (Note: ensure your file is named tables.html with an 's' to match this line). It safely injects both the HTTP request context and the generated table_html string into the webpage template.
10. Now run uvicorn app:app --reload to run it in your local machine. 
11. Now you can see the /predict section in your page. 
12. Click on try it out > Upload your test.csv > Then click on execute > If successfully executed, then you can see the full data in the table format there > And you can verify there will be a predicted_output folder with the output.csv in your project with an additional predicted_column in the file. 




