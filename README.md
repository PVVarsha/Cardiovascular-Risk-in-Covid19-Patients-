# Heart Disease Classification and Analysis Project

This project contains code for analyzing, preprocessing, visualizing, and training machine learning and deep learning models (including LeNet and custom CNN architectures) to predict/classify heart disease. It also includes a Django-based web application for deploying and interacting with the models.

## Project Structure

```
├── heart disease/
│   ├── DATASET/                  # Raw image datasets (Train/Test) - [Gitignored]
│   ├── Deploy/
│   │   └── Project/             # Django Web Application
│   │       ├── App/             # Django Application logic
│   │       ├── Project/         # Django Project configuration
│   │       ├── manage.py        # Django CLI tool
│   │       └── db.sqlite3       # Local SQLite Database - [Gitignored]
│   ├── M1-DATA PREPROCESSING.ipynb
│   ├── M2- DATA VISUALIZATION.ipynb
│   ├── M3-HYBRID.ipynb
│   ├── M4 - VOTING.ipynb
│   ├── M5 -MANUAL NET.ipynb
│   ├── M6- LENET.ipynb
│   ├── LENET.h5                  # Trained LeNet model weights - [Gitignored]
│   ├── MANUAL.h5                 # Trained custom model weights - [Gitignored]
│   ├── heart.pkl                 # Heart risk model/scaler
│   └── heart_risk.csv            # Structured tabular dataset
├── .gitignore                    # Git ignore file configurations
└── README.md                     # Project documentation (this file)
```

## Getting Started

### 1. Prerequisites
Make sure you have Python installed. You can install the required dependencies using pip:
```bash
pip install tensorflow django pandas numpy matplotlib scikit-learn seaborn jupyter
```

### 2. Running Jupyter Notebooks
To run the notebooks for data preprocessing, visualization, and training:
1. Open your terminal in the `heart disease/` folder.
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Run the notebooks in sequential order:
   - **`M1-DATA PREPROCESSING.ipynb`**: Preprocessing the heart disease dataset.
   - **`M2- DATA VISUALIZATION.ipynb`**: Exploratory data analysis and visualization.
   - **`M3-HYBRID.ipynb`**: Hybrid classifier training.
   - **`M4 - VOTING.ipynb`**: Voting classifier training.
   - **`M5 -MANUAL NET.ipynb`**: Training a custom CNN model (`MANUAL.h5`).
   - **`M6- LENET.ipynb`**: Training the LeNet CNN model (`LENET.h5`).

### 3. Running the Django Web Application
To start the Django web server for local deployment:
1. Navigate to the Django project directory:
   ```bash
   cd "heart disease/Deploy/Project"
   ```
2. Apply database migrations to set up the database structure:
   ```bash
   python manage.py migrate
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```
4. Access the web interface at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

> [!NOTE]
> **Large Files Notice:**
> The trained model weight files (`MANUAL.h5`, `LENET.h5`) and the `DATASET/` folder are excluded from this Git repository to avoid exceeding GitHub's file size limits (100MB max per file) and repository size recommendations. 
> 
> To run the notebooks or web application, please ensure you place the `DATASET` folder and the `.h5` model files in their respective folders locally.
