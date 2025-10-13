import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
from fuzzywuzzy import fuzz

fake = Faker('en_IN')  # use Indian context
np.random.seed(42)

st.title("🧠 Domain-Based Synthetic Data Generator")
st.markdown("Generate realistic synthetic datasets for different domains — with built-in plagiarism checks.")

# === Step 1: Select or enter a domain ===
domain = st.selectbox(
    "Select a domain/use case",
    ["Employee Salary Data (India)", "Student Academic Performance", "Retail Transactions", "Healthcare Patients", "Custom Domain"]
)

if domain == "Custom Domain":
    custom = st.text_input("Enter your custom use case (e.g., Insurance Claims, Loan Applications)")
    if custom:
        domain = custom

rows = st.slider("Number of synthetic records", 50, 5000, 100)

generate = st.button("🚀 Generate Synthetic Data")

if generate:
    st.subheader(f"🧩 Synthetic Data for {domain}")
    df = pd.DataFrame()

    # === Domain-specific generation logic ===
    if "Employee" in domain:
        df["employee_id"] = [f"E{1000+i}" for i in range(rows)]
        df["employee_name"] = [fake.name() for _ in range(rows)]
        df["department"] = np.random.choice(["IT", "HR", "Finance", "Sales", "Marketing"], rows)
        df["city"] = [fake.city() for _ in range(rows)]
        df["experience_years"] = np.random.randint(0, 25, rows)
        df["salary_inr"] = np.random.normal(800000, 250000, rows).round(0).astype(int)

    elif "Student" in domain:
        df["student_id"] = [f"S{1000+i}" for i in range(rows)]
        df["student_name"] = [fake.name() for _ in range(rows)]
        df["school"] = np.random.choice(["Delhi Public School", "DAV", "Kendriya Vidyalaya", "Ryan International"], rows)
        df["city"] = [fake.city() for _ in range(rows)]
        df["math_score"] = np.random.randint(35, 100, rows)
        df["science_score"] = np.random.randint(35, 100, rows)
        df["english_score"] = np.random.randint(35, 100, rows)
        df["overall_percentage"] = ((df["math_score"] + df["science_score"] + df["english_score"]) / 3).round(2)

    elif "Retail" in domain:
        df["transaction_id"] = [fake.uuid4() for _ in range(rows)]
        df["customer_name"] = [fake.name() for _ in range(rows)]
        df["city"] = [fake.city() for _ in range(rows)]
        df["product"] = np.random.choice(["Laptop", "Mobile", "TV", "Fridge", "Headphones"], rows)
        df["quantity"] = np.random.randint(1, 5, rows)
        df["unit_price"] = np.random.randint(1000, 50000, rows)
        df["total_amount"] = df["quantity"] * df["unit_price"]

    elif "Healthcare" in domain:
        df["patient_id"] = [f"P{1000+i}" for i in range(rows)]
        df["patient_name"] = [fake.name() for _ in range(rows)]
        df["age"] = np.random.randint(10, 90, rows)
        df["gender"] = np.random.choice(["Male", "Female"], rows)
        df["city"] = [fake.city() for _ in range(rows)]
        df["disease"] = np.random.choice(["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Arthritis"], rows)
        df["bill_amount"] = np.random.randint(500, 20000, rows)

    else:
        st.warning("⚠️ Please define a valid domain or custom schema.")
        st.stop()

    st.dataframe(df.head())

    # === Step 2: Plagiarism / Repetition Check ===
    st.subheader("🧪 Plagiarism / Repetition Check")

    # (a) Duplicate check
    duplicate_rows = df[df.duplicated()]
    st.write(f"🔍 Exact duplicates found: {len(duplicate_rows)}")

    # (b) Fuzzy similarity (within generated data)
    sample_names = df.select_dtypes(include='object').columns.tolist()
    fuzzy_matches = []
    threshold = 95

    if len(sample_names) > 0:
        col_to_check = sample_names[0]
        sample_vals = df[col_to_check].sample(min(10, len(df)))
        for i, val1 in enumerate(sample_vals):
            for j, val2 in enumerate(sample_vals):
                if i < j and fuzz.ratio(str(val1), str(val2)) > threshold:
                    fuzzy_matches.append((val1, val2))
        st.write(f"🧠 Fuzzy-similar text pairs (>95% similarity): {len(fuzzy_matches)}")
        if len(fuzzy_matches) > 0:
            st.write(fuzzy_matches[:5])

    # === Step 3: Download option ===
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download Synthetic Data", csv, f"synthetic_{domain.lower().replace(' ', '_')}.csv", "text/csv")