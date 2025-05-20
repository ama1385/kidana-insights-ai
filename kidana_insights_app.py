import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import os
from tabulate import tabulate

# إعداد مفتاح OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY"))

# --------- تسجيل الدخول ---------
def show_login():
    st.title("🔐 نظام الدخول - Kidana Insights AI")
    st.markdown("يرجى تسجيل الدخول للمتابعة")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("تم تسجيل الدخول بنجاح ✅")
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة ❌")

# --------- كود النظام الأساسي ---------
def main():
    st.set_page_config(page_title="Kidana Insights AI", layout="wide")
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        show_login()
        st.stop()

    st.title("📊 Kidana Insights AI")
    st.markdown("نظام التحليل الذكي للبلاغات التشغيلية وملفات الأداء - تم تطويره بواسطة خالد السهلي")

    with st.expander("ℹ️ حول نظام Kidana Insights AI"):
        st.markdown("""
        ### 🎯 ما هو هذا النظام؟
        نظام تحليلي داخلي لتحويل البيانات التشغيلية أو ملفات الأداء إلى رسوم بيانية فورية.

        ### 🧠 ما الهدف؟
        - تسريع اتخاذ القرار
        - توفير تقارير فورية
        - دعم العمليات التشغيلية والإدارية بالتحليل الذكي

        ### ⚙️ كيف تستخدمه؟
        1. اضغط على زر "رفع ملف"
        2. اختر ملف Excel أو CSV فيه البيانات
        3. يتعرف النظام تلقائيًا على نوع الملف ويعرض التحليل المناسب

        ### 📌 تنبيهات:
        - يدعم حاليًا نوعين من الملفات: بلاغات تشغيلية وملفات KPIs
        """)

    uploaded_file = st.file_uploader("📤 ارفع ملف بيانات (Excel/CSV)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")

            st.success("✅ تم تحميل البيانات بنجاح!")
            st.subheader("📋 نظرة عامة على البيانات")
            st.dataframe(df)

            if "نوع_الخدمة" in df.columns:
                st.markdown("### 🔎 تم التعرف على ملف بلاغات تشغيلية")
                if "نوع_الخدمة" in df.columns:
                    fig_service = px.histogram(df, x="نوع_الخدمة", color="نوع_الخدمة", title="عدد البلاغات حسب نوع الخدمة")
                    st.plotly_chart(fig_service, use_container_width=True)
                if "الموقع" in df.columns:
                    fig_location = px.histogram(df, x="الموقع", color="الموقع", title="عدد البلاغات حسب الموقع")
                    st.plotly_chart(fig_location, use_container_width=True)
                if "مستوى_الخطورة" in df.columns:
                    fig_severity = px.histogram(df, x="مستوى_الخطورة", color="مستوى_الخطورة", title="عدد البلاغات حسب مستوى الخطورة")
                    st.plotly_chart(fig_severity, use_container_width=True)
                if "الحالة" in df.columns and "مدة_الحل_ساعة" in df.columns:
                    closed_df = df[df["الحالة"] == "مغلق"]
                    avg_response = closed_df.groupby("نوع_الخدمة")["مدة_الحل_ساعة"].mean().reset_index()
                    fig_response = px.bar(avg_response, x="نوع_الخدمة", y="مدة_الحل_ساعة", color="نوع_الخدمة", title="متوسط مدة الحل حسب نوع الخدمة")
                    st.plotly_chart(fig_response, use_container_width=True)

            elif "KPI Name" in df.columns and "Department" in df.columns:
                st.markdown("### 📈 تم التعرف على ملف KPIs")
                kpi_by_dept = df["Department"].value_counts().reset_index()
                kpi_by_dept.columns = ["Department", "Count"]
                fig_kpi_dept = px.bar(kpi_by_dept, x="Department", y="Count", color="Department", title="عدد KPIs حسب القسم")
                st.plotly_chart(fig_kpi_dept, use_container_width=True)
                if "Perspective" in df.columns:
                    kpi_perspective = df["Perspective"].value_counts().reset_index()
                    kpi_perspective.columns = ["Perspective", "Count"]
                    fig_kpi_persp = px.pie(kpi_perspective, names="Perspective", values="Count", title="توزيع KPIs حسب Perspective")
                    st.plotly_chart(fig_kpi_persp, use_container_width=True)
                if "Frequency" in df.columns:
                    freq_counts = df["Frequency"].value_counts().reset_index()
                    freq_counts.columns = ["Frequency", "Count"]
                    fig_freq = px.bar(freq_counts, x="Frequency", y="Count", color="Frequency", title="تكرار KPIs حسب Frequency")
                    st.plotly_chart(fig_freq, use_container_width=True)

            # 🧠 مساعد الذكاء الاصطناعي:
            with st.expander("🧠 مساعد ذكي (GPT)"):
                st.markdown("""**📌 اسأل عن البيانات بأي صيغة وسأجيب باستخدام الذكاء الاصطناعي 👇**""")
                user_question = st.text_area("✍️ اكتب سؤالك هنا:")

                if st.button("🔍 تحليل بالسؤال") and user_question:
                    try:
                        sample_limit = 200 if len(df) > 200 else len(df)
                        sampled_df = df.sample(n=sample_limit, random_state=42)
                        context = tabulate(sampled_df, headers='keys', tablefmt='grid', showindex=False)

                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "أنت مساعد ذكي متخصص في تحليل ملفات Excel والإجابة بدقة"},
                                {"role": "user", "content": f"البيانات:
{context}\n\nالسؤال:
{user_question}"}
                            ]
                        )
                        st.success("📌 الإجابة:")
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"❌ حدث خطأ في المساعد الذكي:\n\n{e}")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء معالجة البيانات: {str(e)}")
    else:
        st.warning("📌 الرجاء رفع ملف البيانات لبدء التحليل.")

if __name__ == "__main__":
    main()
