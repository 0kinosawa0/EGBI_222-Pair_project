# 🩺 Stroke Prediction Dataset - Exploratory Data Analysis (EDA)

## 📘 Overview
This project performs **Exploratory Data Analysis (EDA)** on the **Stroke Prediction Dataset** from Kaggle.  
The goal is to identify factors that may influence the likelihood of stroke, such as age, gender, BMI, smoking habits, and health conditions like hypertension or heart disease.

📊 Dataset Source:  
[Kaggle - Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)

---

## 🎯 Objectives
1. Understand the structure and key statistics of the dataset  
2. Identify relationships between features (e.g., age, BMI, glucose level) and stroke occurrence  
3. Visualize health and demographic patterns clearly and effectively  
4. Create insights that could help in preventive healthcare analytics  

---

## 🧠 Dataset Description
The dataset contains 5,110 records of patients with several attributes related to lifestyle and medical history.

| Column | Description |
|--------|--------------|
| gender | Male / Female |
| age | Age of the patient |
| hypertension | 0 = No, 1 = Yes |
| heart_disease | 0 = No, 1 = Yes |
| ever_married | Yes / No |
| work_type | Type of work (e.g. Private, Self-employed) |
| Residence_type | Urban / Rural |
| avg_glucose_level | Average glucose level in blood |
| bmi | Body Mass Index |
| smoking_status | Smokes / Formerly Smoked / Never Smoked |
| stroke | 1 = Had a stroke, 0 = Did not have a stroke |

---

## ⚙️ How to Run
Make sure you have Python installed (3.9+ recommended).  
Install the required libraries using:

```bash
pip install pandas matplotlib seaborn
