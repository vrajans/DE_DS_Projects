import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from synthetic_data_plagiarims_checker_new import SyntheticDataPlagiarismChecker

st.title("Synthetic Data Plagiarism Detector")

# Upload real and synthetic datasets
real_file = st.file_uploader("Upload Real Dataset CSV", type="csv")
synthetic_file = st.file_uploader("Upload Synthetic Dataset CSV", type="csv")

if real_file and synthetic_file:
    real_df = pd.read_csv(real_file)
    synthetic_df = pd.read_csv(synthetic_file)
    
    st.write("**Real Dataset Sample:**")
    st.dataframe(real_df.head())
    
    st.write("**Synthetic Dataset Sample:**")
    st.dataframe(synthetic_df.head())
    
    # Initialize checker
    checker = SyntheticDataPlagiarismChecker(real_df, synthetic_df)
    
    # Exact duplicate check
    duplicates = checker.exact_duplicate_check()
    st.write(f"Number of exact duplicates: {len(duplicates)}")
    if len(duplicates) > 0:
        st.write("Duplicate rows:")
        st.dataframe(duplicates)
    
    # Numerical distance check
    min_distances = checker.numerical_distance_check()
    st.write(f"Minimum distance: {np.min(min_distances):.2f}")
    st.write(f"Average distance: {np.mean(min_distances):.2f}")
    
    # Plot distribution comparison for numerical columns
    num_cols = real_df.select_dtypes(include=np.number).columns
    for col in num_cols:
        plt.figure(figsize=(8,4))
        sns.histplot(real_df[col], color='blue', label='Real', kde=True, stat="density", alpha=0.5)
        sns.histplot(synthetic_df[col], color='orange', label='Synthetic', kde=True, stat="density", alpha=0.5)
        plt.title(f'Distribution Comparison: {col}')
        plt.legend()
        st.pyplot(plt)
    
    # Fuzzy matching for text columns
    text_cols = real_df.select_dtypes(include='object').columns
    for col in text_cols:
        high_sim = checker.fuzzy_text_check(col)
        if high_sim:
            st.write(f"High similarity detected in column '{col}':")
            st.write(high_sim[:10])  # show first 10
        else:
            st.write(f"Column '{col}' passed fuzzy similarity check.")
    
    # Risk score (simple example)
    risk_score = (len(duplicates) + np.sum(min_distances < 1)) / len(synthetic_df) * 100
    st.metric("Plagiarism Risk Score (%)", f"{risk_score:.2f}")
    
    st.success("Synthetic Data Check Complete!")