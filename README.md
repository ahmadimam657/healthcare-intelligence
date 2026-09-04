# Healthcare Intelligence

A healthcare analytics and machine learning project designed to transform raw patient records into structured, analysis-ready data and build the foundation for future clinical intelligence workflows. The project currently focuses on dataset acquisition, preprocessing, feature encoding, and data pipeline automation, with a strong roadmap toward explainable ML, patient analytics, and AI-assisted healthcare exploration.

## Overview

Healthcare data is often noisy, inconsistent, and difficult to interpret without a well-structured pipeline. This project provides a practical foundation for working with healthcare records by:

- downloading a public healthcare dataset from Kaggle,
- cleaning and standardizing raw values,
- deriving clinically meaningful fields such as length of stay,
- encoding categorical variables for downstream modeling,
- logging data processing steps for reproducibility,
- preparing the dataset for exploratory analysis and machine learning experiments.

The repository is intentionally built to be extensible, so it can evolve from a preprocessing-focused project into a full healthcare intelligence platform.

## Current Project Scope

At the present stage, this project includes the following capabilities:

- Kaggle dataset download and project-local storage
- Structured healthcare data loading and preprocessing
- Removal of irrelevant or redundant columns
- Standardization of categorical values
- Date conversion and length-of-stay computation
- Duplicate detection and data-quality checks
- Label encoding with saved mapping files
- Logging and project utilities for maintainable workflows
- Exploratory analysis notebook for dataset understanding

## Project Goals

This project aims to support:

- data preparation for healthcare analytics,
- reproducible research workflows,
- feature engineering for clinical modeling,
- explainable AI for healthcare decision support,
- future patient similarity, anomaly detection, and AI assistant features.

## Tech Stack

- Python 3.11+
- pandas
- scikit-learn
- NumPy / SciPy
- matplotlib
- seaborn
- Jupyter Notebook
- KaggleHub for dataset acquisition
- JSON-based encoding metadata

## Repository Structure

```text
healthcare-intelligence/
├── data/
│   ├── healthcare_dataset.csv
│   ├── preprocessed_healthcare_dataset.csv
│   └── encodings/
│       ├── Admission Type_mapping.json
│       ├── Blood Type_mapping.json
│       ├── Doctor_mapping.json
│       ├── Gender_mapping.json
│       ├── Hospital_mapping.json
│       ├── Medical Condition_mapping.json
│       ├── Medication_mapping.json
│       └── Test Results_mapping.json
├── logs/
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── generate_data.py
│   └── preprocessing.py
├── utils/
│   └── logging.py
├── main.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .env.example (if used in your local setup)
```

## Data Pipeline

The project currently follows a clean and modular healthcare data workflow:

1. Download the dataset from Kaggle.
2. Store it inside the local `data/` folder.
3. Load and inspect the raw records.
4. Clean and standardize values.
5. Convert date fields and compute `Length of Stay`.
6. Validate data quality and remove duplicates.
7. Encode categorical variables for machine learning readiness.
8. Save the processed output for downstream analysis.

## Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python 3.11 or newer
- pip or a virtual environment manager
- access to a Kaggle API token if downloading the dataset from Kaggle

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/healthcare-intelligence.git
cd healthcare-intelligence
```
If you want to sync the project dependencies from the lockfile or configuration, you can use

```bash
uv sync
```

### Configuration

If you want to download the dataset from Kaggle, set your Kaggle API token in a `.env` file:

```bash
KAGGLE_API_TOKEN=your_kaggle_api_token_here
```

You can also use the project environment if your setup already includes the required token.

### Running the Data Generation Pipeline

```bash
python src/generate_data.py
```

This script loads the environment variables, downloads the healthcare dataset from Kaggle, copies it into the local `data/` directory, and verifies the results.

### Running the Preprocessing Pipeline

```bash
python src/preprocessing.py
```

This script performs the preprocessing workflow and writes the final processed dataset to `data/preprocessed_healthcare_dataset.csv`.

## Example Workflow

```python
from src.preprocessing import preprocess_healthcare_data

preprocess_healthcare_data(
    input_file="healthcare_dataset.csv",
    output_file="preprocessed_healthcare_dataset.csv"
)
```

## Current Data Characteristics

The dataset contains patient-level variables such as:

- age and gender
- blood type and medical condition
- admission and discharge dates
- doctor and hospital identity
- billing amount
- admission type
- medication and test results

This makes it suitable for a range of analyses, including feature engineering, patient risk estimation, and billing and operational analytics.

## Notebook and Analysis

The repository includes an exploratory notebook in `notebooks/eda.ipynb`, which can be used to:

- profile the dataset,
- inspect distributions,
- understand missing or invalid values,
- review feature relationships,
- prepare for modeling experiments.

## Future Work

This project is intentionally designed to grow into a full healthcare intelligence platform. The roadmap below outlines the next major directions for development.

### 1. Machine Learning & Explainable AI Extensions

- Enforce inference-time guardrails for classification models to avoid post-treatment data leakage, such as preventing variables like `Length of Stay` from being used as admission-time predictors.
- Track per-class precision, recall, macro and weighted F1, and confusion matrices for model evaluation.
- Add global and local SHAP explanations for interpretability, especially for tree-based models such as XGBoost and CatBoost.
- Benchmark administrative vs. clinical feature sets to evaluate the predictive gain of billing and operational variables compared with clinical indicators.

### 2. Patient Analytics & Unsupervised Learning

- Build a patient similarity finder using KNN-based historical matching to retrieve similar patient cohorts with confidence scores and average outcomes.
- Execute clustering pipelines using K-Means and DBSCAN on scaled clinical and demographic data.
- Reduce dimensions with PCA or UMAP for 2D visualization of patient groups and patterns.
- Apply anomaly detection methods such as Isolation Forest and Local Outlier Factor to identify unusual billing behaviors without labeling them as explicit fraud.
- Perform survival and temporal analysis using Kaplan-Meier estimation for time-to-event metrics such as length of stay and hospital utilization change over time.

### 3. Hybrid RAG & SQL Copilot

- Develop a dual-retrieval architecture combining a text-to-SQL engine (DuckDB or PostgreSQL) for structured healthcare data queries and a vector database (Chroma or FAISS) for unstructured medical policy documents.
- Implement hybrid query routing across SQL, RAG, and combined retrieval systems.
- Benchmark answer quality using retrieval precision/recall, faithfulness, and latency metrics.
- Create an AI assistant that can query patient data and medical guidance in a controlled, explainable way.

### 4. Engineering, UI & Deployment

- Build a Streamlit application with tabs for dashboarding, patient exploration, ML predictions, similar patient insights, anomaly review, and AI assistance.
- Refactor the codebase into modular packages under `src/`, `rag/`, and `app/` for maintainability.
- Add containerization using Docker for deployment on cloud platforms.
- Prepare the project for scalable production-style deployment and operational monitoring.

## Contributing

Contributions are welcome. This project is meant to be a collaborative healthcare analytics and AI platform, and improvements in data quality, model evaluation, analytics, and application design are all valuable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Notes

This repository is currently in a strong foundational stage: it provides a reproducible healthcare data pipeline and a clear roadmap toward applied clinical analytics, explainable ML, and AI-powered healthcare support systems.
