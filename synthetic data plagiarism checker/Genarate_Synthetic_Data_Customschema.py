import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
from fuzzywuzzy import fuzz

fake = Faker('en_IN')
np.random.seed(42)

st.set_page_config(page_title="AI Synthetic Data Generator", layout="wide")
st.title("🧠 AI Synthetic Data Generator + Custom Schema Builder")

st.markdown("""
Build **custom synthetic datasets** for any use case (Employee, Student, Finance, Healthcare, etc.)  
✅ No real data required  
✅ Domain-driven generation  
✅ Built-in plagiarism & duplication checks  
""")

# ------------------------------------------
# Step 1: Choose Generation Mode
# ------------------------------------------
mode = st.radio("Select Mode", ["Predefined Domain", "Custom Schema Builder"])

# ==========================================
# PREDEFINED DOMAINS
# ==========================================
if mode == "Predefined Domain":
    domain = st.selectbox(
        "Choose Domain",
        ["Employee Salary Data (India)", "Student Academic Performance", "Retail Transactions", "Healthcare Patients"]
    )
    rows = st.slider("Number of Records", 50, 5000, 200)

    generate = st.button("🚀 Generate Synthetic Data")

    if generate:
        df = pd.DataFrame()
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
            df["school"] = np.random.choice(["DPS", "DAV", "Kendriya Vidyalaya", "Ryan International"], rows)
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

        st.dataframe(df.head())

        # --- Plagiarism / Repetition Check ---
        st.subheader("🧪 Plagiarism / Repetition Check")

        duplicate_rows = df[df.duplicated()]
        st.write(f"🔍 Exact duplicates found: {len(duplicate_rows)}")

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

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Synthetic Data", csv, f"synthetic_{domain.lower().replace(' ', '_')}.csv", "text/csv")

# ==========================================
# CUSTOM SCHEMA BUILDER
# ==========================================
else:
    st.subheader("🧩 Define Your Custom Schema")

    with st.expander("➕ Add Columns"):
        num_cols = st.number_input("How many columns?", 1, 20, 3)
        schema = []
        for i in range(num_cols):
            st.markdown(f"**Column {i+1}**")
            col_name = st.text_input(f"Name of column {i+1}", key=f"name_{i}")
            dtype = st.selectbox(
                f"Data Type of column {i+1}",
                ["Text (Name, City, Email)", "Integer", "Float", "Boolean", "Date", "Category (Custom List)"],
                key=f"type_{i}"
            )

            extra = {}
            if dtype == "Integer":
                min_val = st.number_input(f"Min value (Column {i+1})", 0)
                max_val = st.number_input(f"Max value (Column {i+1})", 100)
                extra = {"min": min_val, "max": max_val}
            elif dtype == "Float":
                min_val = st.number_input(f"Min value (Column {i+1})", 0.0)
                max_val = st.number_input(f"Max value (Column {i+1})", 100.0)
                extra = {"min": min_val, "max": max_val}
            elif dtype == "Category (Custom List)":
                cat_list = st.text_area(f"Enter comma-separated values for Column {i+1}")
                extra = {"values": [v.strip() for v in cat_list.split(",") if v.strip()]}

            schema.append({"name": col_name, "type": dtype, "extra": extra})

    rows = st.slider("Number of Synthetic Records", 10, 5000, 100)
    generate_custom = st.button("🚀 Generate Custom Synthetic Data")

    if generate_custom:
        df = pd.DataFrame()
        for col in schema:
            if not col["name"]:
                continue
            dtype = col["type"]
            if dtype == "Text (Name, City, Email)":
                df[col["name"]] = np.random.choice(
                    [fake.name(), fake.city(), fake.email()], rows)
            elif dtype == "Integer":
                df[col["name"]] = np.random.randint(col["extra"]["min"], col["extra"]["max"] + 1, rows)
            elif dtype == "Float":
                df[col["name"]] = np.random.uniform(col["extra"]["min"], col["extra"]["max"], rows).round(2)
            elif dtype == "Boolean":
                df[col["name"]] = np.random.choice([True, False], rows)
            elif dtype == "Date":
                df[col["name"]] = [fake.date_this_decade() for _ in range(rows)]
            elif dtype == "Category (Custom List)" and col["extra"]["values"]:
                df[col["name"]] = np.random.choice(col["extra"]["values"], rows)

        st.dataframe(df.head())

        # --- Non-Plagiarism Check ---
        st.subheader("🧪 Duplication / Similarity Check")
        duplicate_rows = df[df.duplicated()]
        st.write(f"🔍 Exact duplicates found: {len(duplicate_rows)}")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Custom Synthetic Data", csv, "custom_synthetic_data.csv", "text/csv")