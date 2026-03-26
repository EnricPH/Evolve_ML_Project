# Online Retail II — Customer Purchase Prediction

## Overview

This project analyzes transactional data from an online retail business to understand customer behavior and predict the likelihood of repeat purchases. The goal is to support business decision-making by identifying customers who are likely to return and those at risk of not purchasing again.

The analysis combines data cleaning, exploratory data analysis (EDA), feature engineering, and machine learning models to generate actionable insights for marketing and retention strategies.

---

## Objective

The main objective is to build a predictive model that estimates whether a customer will make a future purchase.

This enables two key business actions:
- **Loyalty actions** for customers likely to return
- **Retention actions** for customers at risk of churn

---

## Dataset

The dataset contains transactional records, including:
- Invoice information
- Product details
- Quantities and prices
- Customer identifiers
- Country
- Transaction timestamps

It includes both purchases and cancellations, which are explicitly modeled as part of customer behavior.

---

## Project Structure

### 1. Data Preparation

#### Data Loading
- Load multiple sheets from the dataset
- Combine into a unified dataframe

#### Cleaning
- Data type corrections
- Handling missing values
- Duplicate detection and removal
- Identification of invalid or inconsistent values

---

### 2. Exploratory Data Analysis (EDA)

#### Descriptive Statistics
- Summary statistics of numerical variables
- Distribution analysis
- Outlier detection

#### Visualizations
- Customer behavior analysis
- Sales trends over time
- Country-level insights
- Product-level performance

---

### 3. Feature Engineering

Customer-level features are created to capture behavioral patterns.

#### RFM Features
- **Recency**: Time since last purchase  
- **Frequency**: Number of purchases  
- **Monetary**: Total spending  

#### Cancellation Features
- Number of cancellations  
- Cancellation value  
- Cancellation rate  

#### Additional Features
- Customer lifetime  
- Average order value  
- Average quantity per order  
- Purchase frequency rate  
- Country (categorical)  

#### Target Variable
- Defined using a time-based split  
- Indicates whether a customer makes a future purchase  

---

### 4. Preprocessing

- Train-test split with stratification  
- Feature scaling for distance-based and linear models  
- Handling categorical variables (CatBoost-ready approach for country)  

---

### 5. Modeling

Several models are trained and optimized using Optuna with cross-validation:

- Logistic Regression  
- Support Vector Machine (SVM)  
- K-Nearest Neighbors (KNN)  
- Naive Bayes  
- Random Forest  
- XGBoost  

Each model is tuned for optimal performance and evaluated consistently.

---

### 6. Evaluation

Models are compared using:

- Accuracy  
- Precision  
- Recall  
- F1-score  
- ROC AUC (primary metric)  

Additional analysis includes:
- Confusion matrix  
- Feature importance comparison  
- Model interpretability  

---

### 7. Business Insights

#### Loyalty Actions (High Probability Customers)
- Target frequent and recent buyers  
- Apply personalized promotions and loyalty programs  
- Focus on maximizing customer lifetime value  

#### Retention Actions (Low Probability Customers)
- Identify inactive or declining customers  
- Launch re-engagement campaigns  
- Offer incentives to encourage return purchases  

---

## Key Findings

- RFM features are the strongest predictors of customer behavior  
- All models perform similarly, indicating strong signal in the data  
- Tree-based models (Random Forest, XGBoost) slightly outperform others in ranking ability  
- Recency is the most influential feature across all models  

---

## Conclusion

The project demonstrates that customer purchase behavior can be effectively modeled using transactional data. The results provide a reliable framework for:

- Customer segmentation  
- Targeted marketing  
- Retention strategy optimization  
