# Django Machine Learning Lab - Vehicle Analytics System

## Project Overview
This project implements a Vehicle Analytics System with Django and Machine Learning, providing:
- Price Prediction using Regression
- Income Level Classification 
- Client Segmentation using Clustering

## Technology Stack
- Django
- Python
- Pandas
- Scikit-learn
- HTML Templates with Bootstrap

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Machine Learning Models
```bash
# Train regression model
python model_generators/regression/train_regression.py

# Train classification model  
python model_generators/classification/train_classifier.py

# Train clustering model
python model_generators/clustering/train_cluster.py
```

### 3. Run Django Server
```bash
python manage.py runserver
```

### 4. Access the Application
Open your browser and navigate to: http://127.0.0.1:8000/data_exploration

## Features
- **Data Exploration**: View and analyze the vehicle dataset
- **Regression Analysis**: Predict vehicle selling prices
- **Classification Analysis**: Predict customer income levels
- **Clustering Analysis**: Segment customers into client categories

## Project Structure
```
vehicle/
├── config/                 # Django project configuration
├── predictor/             # Django app
│   ├── templates/         # HTML templates
│   ├── views.py          # View functions
│   └── urls.py           # URL patterns
├── model_generators/     # ML model training scripts
│   ├── regression/
│   ├── classification/
│   └── clustering/
├── dummy-data/           # Sample dataset
└── requirements.txt      # Python dependencies
```

## Dataset
The sample dataset includes vehicle information such as:
- Client name
- Vehicle year
- Kilometers driven
- Seating capacity
- Estimated income
- Selling price
- Income level

## Machine Learning Models
1. **Random Forest Regression**: Predicts selling prices
2. **Random Forest Classification**: Categorizes income levels
3. **K-Means Clustering**: Segments customers into Economy, Standard, and Premium categories
