# Stroke Prediction – EDA Summary

- **File:** `healthcare-dataset-stroke-data.csv`
- **Rows x Cols:** 5110 x 12
- **Overall stroke rate:** 4.87%

## Stroke rate by Gender
- Male: 5.11%
- Female: 4.71%
- Other: 0.00%

## Stroke rate by Age Group
- <30: 0.13%
- 30–45: 1.05%
- 45–60: 4.97%
- 60+: 13.57%

- **Avg glucose (mean±std):** 106.1 ± 45.3
- **BMI (mean±std):** 28.9 ± 7.7

## Top numeric correlations (by |r|)
- age ↔ bmi: 0.32
- age ↔ hypertension: 0.28
- heart_disease ↔ age: 0.26
- stroke ↔ age: 0.25
- age ↔ avg_glucose_level: 0.24

---
## Notes you can use in your report
- The overall stroke rate is **4.9%**. We examine how risk varies by gender and age.
- Gender distribution and stroke rates show which group appears more at risk in this dataset.
- Stroke risk generally increases with age; the age-group chart makes this visible.
- Higher average glucose appears associated with stroke in the density plot.
- BMI distribution suggests whether obesity relates to stroke in this sample.