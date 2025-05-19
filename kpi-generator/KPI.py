import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import datetime
import pickle
import random

# ✅ إعداد الصفحة (يجب أن يكون أول أمر)
st.set_page_config(page_title="منشئ مؤشرات الأداء الذكي", layout="centered")

# ✅ تنسيق CSS مخصص
st.markdown("""
    <style>
    body {
        background-color: #f9f9fb;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 2px solid #a77af4;
        padding: 6px;
        color: black;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        border: 2px solid #a77af4;
        color: black;
    }
    .stButton>button {
        background-color: #4a148c;
        color: white;
        padding: 0.5em 1em;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- تحميل ملفات النموذج والمتجهات والبيانات ---
with open("kpi_model_updated.pkl", "rb") as f:
    model = pickle.load(f)

with open("kpi_vectorizer_updated.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("kpi_data.pkl", "rb") as f:
    df_kpi = pickle.load(f)

# --- واجهة المستخدم ---
st.title("📊 منشئ مؤشرات الأداء الذكي")
description = st.text_area("✏️ اكتب وصف المؤشرات المطلوبة (سطر لكل مؤشر):", height=250)

if st.button("🚀 توليد ملف مؤشرات الأداء"):
    if description.strip():
        inputs = description.strip().split("\n")
        generated = []

        for desc in inputs:
            vec = vectorizer.transform([desc])
            idx = model.predict(vec)[0]
            base = df_kpi.iloc[idx]

            weight = random.choice([5, 10, 15])

            row = {
                "Department": base.get("Department", "General"),
                "Dept. Lvl": base.get("Dept. Lvl", "N-1"),
                "Perspective": base.get("Perspective", "Internal"),
                "Strategic Objective": base.get("Strategic Objective", "N/A"),
                "KPI Code": base.get("KPI Code", f"GEN.{random.randint(100,999)}"),
                "KPI Name": base.get("KPI Name", desc),
                "KPI Formula": base.get("KPI Formula", "(Actual / Target) * 100"),
                "UOM": base.get("UOM", "Percentage"),
                "Frequency": base.get("Frequency", "Quarterly"),
                "Polarity": base.get("Polarity", "Positive"),
                "Weight": f"{weight}%",
                "Target": "",
                "Actual": "",
                "Score": "",
                "Weighted Score": "",
                "status": "=IF(N2>L2, \"Achieved\", \"Not Achieved\")",
                "Achievement": "",
                "Challenges ": "",
                "Resolve the Challenge ": base.get("Resolve the Challenge ", ""),
                "Support": base.get("Support", "")
            }
            generated.append(row)

        df_out = pd.DataFrame(generated)
        output_file = "KPI_Generated_Modified.xlsx"
        df_out.to_excel(output_file, index=False)

        with open(output_file, "rb") as file:
            st.download_button("📥 تحميل ملف مؤشرات الأداء", file, file_name=output_file)
    else:
        st.warning("🛑 يرجى إدخال وصف واحد على الأقل.")
