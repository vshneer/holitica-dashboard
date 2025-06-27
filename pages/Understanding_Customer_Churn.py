import pandas as pd
import streamlit as st
import shap
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from shared.form import show_sidebar_form

# -------------------------
# Column descriptions
# -------------------------


insight_map = {
    "tenure": "Tenure is a strong predictor of churn. The longer a customer has been on board, the lower their churn risk. This suggests that retention improves significantly once customers have used the product for some time. However, many new users leave early.",
    "OnlineBackup": "Having an online backup service (for customers with internet access) is linked to a lower risk of churn.",
    "PhoneService": "Customers who have phone service are generally less likely to churn.",
    "Dependents": "Customers with dependents (e.g. children) are slightly more likely to churn.",
    "gender": "Gender does not significantly affect churn risk.",
    "InternetService": "Customers using fiber optic internet are more likely to churn than those using DSL or no service.",
    "OnlineSecurity": "Lack of security services increases churn. Customers without online protection tend to leave more.",
    "TechSupport": "Lack of tech support is associated with higher churn rates.",
    "Contract":"Monthly contract increases churn, two years contract - decreases churn.",
}


column_descriptions = {
    "gender": "Customer's gender",
    "SeniorCitizen": "Is the customer a senior",
    "Partner": "Has a partner",
    "Dependents": "Has dependents (e.g. children)",
    "tenure": "How long the customer has stayed",
    "PhoneService": "Has phone service",
    "MultipleLines": "Has multiple phone lines",
    "InternetService": "Type of internet service",
    "OnlineSecurity": "Has online security",
    "OnlineBackup": "Has online backup",
    "DeviceProtection": "Has device protection",
    "TechSupport": "Has tech support",
    "StreamingTV": "Uses streaming TV service",
    "StreamingMovies": "Uses streaming movies service",
    "Contract": "Type of contract",
    "PaperlessBilling": "Uses paperless billing",
    "PaymentMethod": "Payment method used",
    "MonthlyCharges": "Monthly charge amount",
    "TotalCharges": "Total amount charged",
}

# Reverse map: description → column name
description_to_column = {v: k for k, v in column_descriptions.items()}

# Friendly renaming for plot readability
rename_map = {
    "InternetService_Fiber optic": "Fiber optic",
    "TechSupport_No": "Customer lacks tech support",
    "InternetService_DSL":"Internet service: DSL",
    "MultipleLines_No":"No multiple phone lines",
    "gender_Female":"Female",
    "StreamingTV_No":"No streaming TV",
    "StreamingMovies_No":"No streaming Movies",
    "DeviceProtection_No":"No device protection",
    "InternetService_No":"No internet service",
    "MultipleLines_Yes":"Multiple phone lines",
    "MultipleLines_No phone service":"Phone service",
    "StreamingMovies_Yes":"Streaming Movies",
    "DeviceProtection_Yes":"Device protection",
    "TechSupport_Yes":"Got tech support",
    "TechSupport_No internet service": "Tech Support Internet service",
    "DeviceProtection_No internet service":"Device Protection Internet service",
    "OnlineSecurity_Yes":"Use online security",
    "OnlineSecurity_No": "Customer lacks online security",
    "Contract_Month-to-month": "Monthly contract",
    "SeniorCitizen_1": "Customer is a senior",
    "SeniorCitizen_0": "Customer is not a senior",
    "PaperlessBilling_Yes": "Uses paperless billing",
    "Dependents_No": "No dependents (e.g. children)",
    "Partner_No": "No partner",
    "OnlineBackup_No": "No online backup",
    "PhoneService_No": "No phone service",
    "OnlineBackup_Yes": "Has online backup",
    "PhoneService_Yes": "Has phone service",
    "Dependents_Yes": "Has dependents (e.g. children)",
    "Partner_Yes": "Has partner",
    "tenure": "Tenure",
    "OnlineBackup_No internet service": "No internet service",
    "Contract_Two years":"Two years contract",
    "PaymentMethod_Electronic check":"Electronic check",
    "StreamingTV_Yes":"Streaming TV",
    "Contract_One year":"One year contract",
    "Contract_Two year": "Two year contract",
    "PaperlessBilling_No":"No paperless billing",
    "PaymentMethod_Mailed check":"Mailed check",
    "PaymentMethod_Bank transfer (automatic)":"Automatic bank transfer",
}


# -------------------------
# Load and preprocess data
# -------------------------
df = pd.read_csv('data/churn.csv')

# Drop index column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Treat 'SeniorCitizen' as categorical
df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)



# -------------------------
# Streamlit UI
# -------------------------
show_sidebar_form()
st.title("📉 Understanding Customer Churn")
st.markdown("""
Welcome! This tool helps you explore **why customers leave** by analyzing their behaviors, services, and account features.  
Instead of simply predicting churn, our goal is to **understand the key drivers behind it** — and help you make better business decisions.
""")
st.markdown("""
### 📦 Dataset Overview

This dataset contains customer records from a telecom company, including demographics, subscribed services, and billing information.  
""")


st.subheader("📊 Dataset Preview")
df_display = df.reset_index(drop=True)
df_display.index = [''] * len(df_display)
st.dataframe(df_display.head(3))
st.markdown('''
The goal is to predict whether a customer is likely to churn (leave the service) and how can we prevent it.
''')
st.markdown('''
To train the model, make predictions and explain feature importance please chose what features to use.
''')
st.subheader("🧠 Select Features to Explore Churn Drivers")

# Multiselect with only descriptions
selected_options = st.multiselect(
    "Select the features you'd like to include. Five at least.",
    options=list(description_to_column.keys()),
    default=None
)

# Only run if user selected at least 5 features
if len(selected_options) > 4 and st.button("Explore Churn Risk Factors"):
    st.toast("🚀 Running churn prediction...")

    # Immediately show the help text
    st.markdown("""
    ### ℹ️ How to Read the SHAP Summary Plot

    - **Each dot** = one customer  
    - **Each row** = one feature used in the model  
    - **X-axis (left ↔ right)** = how much the feature influenced the model's churn prediction
        - **Wide spread** = this feature has a **strong impact** (important)
        - **Tight cluster near 0** = this feature has **little impact** (unimportant)
        - **Right** = increases predicted churn  
        - **Left** = decreases predicted churn  
    - **Color** shows the actual value of the feature:
        - 🔴 Red = high value  
        - 🔵 Blue = low value  

    ---
    **Example**: If blue dots (short tenure) appear on the right for "tenure", it means short-tenure customers are more likely to churn.
    """)

    selected_columns = [description_to_column[desc] for desc in selected_options]

    # Show insights for selected features (if any are in the map)
    st.markdown("### 🔍 Feature Insights")

    for col in selected_columns:
        if col in insight_map:
            st.markdown(f"- **{column_descriptions[col]}**: {insight_map[col]}")

    with st.spinner("⏳ Training model and explaining predictions..."):
        import time

        time.sleep(0.5)  # Give spinner time to show before heavy lifting
        # Feature matrix and target
        X = df[selected_columns]
        y = df["Churn"]

        # Identify column types
        cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
        num_cols = X.select_dtypes(exclude=["object", "category"]).columns.tolist()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Preprocessor and pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", drop=None), cat_cols)
            ],
            remainder="passthrough"
        )
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42))
        ])
        clf.fit(X_train, y_train)

        # Get encoded feature names
        ohe = preprocessor.named_transformers_['cat']
        encoded_cat_cols = ohe.get_feature_names_out(cat_cols)
        feature_names = list(encoded_cat_cols) + num_cols
        feature_names = [rename_map.get(name, name) for name in feature_names]


        # Create DataFrame with named columns
        X_encoded = preprocessor.transform(X_train)
        X_encoded_df = pd.DataFrame(X_encoded, columns=feature_names)

        # SHAP explainer
        explainer = shap.Explainer(clf.named_steps["classifier"], X_encoded_df)
        shap_values = explainer(X_encoded_df)

    # Optional toast after spinner
    st.toast("✅ Model is ready. Scroll down to view insights!")
    # Display plot
    st.subheader("🔍 What Influences Churn the Most?")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values.values, X_encoded_df, feature_names=feature_names, show=False)
    st.pyplot(plt.gcf())
