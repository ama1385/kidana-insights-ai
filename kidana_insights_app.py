import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.markdown("نظام التحليل الذكي للبلاغات التشغيلية - تم تطويره بواسطة خالد السهلي")

    with st.expander("ℹ️ حول نظام Kidana Insights AI"):
        st.markdown("""
        ### 🎯 ما هو هذا النظام؟
        نظام تحليلي داخلي لتحويل البيانات التشغيلية (مثل البلاغات) إلى رسوم بيانية فورية

        ### 🧠 ما الهدف؟
        - تسريع اتخاذ القرار
        - توفير تقارير فورية
        - دعم العمليات التشغيلية بالتحليل الذكي

        ### ⚙️ كيف تستخدمه؟
        1. اضغط على زر "رفع ملف"
        2. اختر ملف Excel أو CSV فيه البيانات
        3. تشاهد التحليل مباشرة في الصفحة

        ### 📌 الأعمدة المطلوبة:
        - نوع_الخدمة، الموقع، تاريخ_البلاغ، مستوى_الخطورة، الحالة، مدة_الحل_ساعة
        """)

    uploaded_file = st.file_uploader("📤 ارفع ملف بيانات البلاغات (Excel/CSV)", type=["csv", "xlsx"])

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
                st.subheader("🔧 عدد البلاغات حسب نوع الخدمة")
                fig_service = px.histogram(df, x="نوع_الخدمة", color="نوع_الخدمة", title="عدد البلاغات حسب نوع الخدمة")
                st.plotly_chart(fig_service, use_container_width=True)

            if "الموقع" in df.columns:
                st.subheader("📍 عدد البلاغات حسب الموقع")
                fig_location = px.histogram(df, x="الموقع", color="الموقع", title="عدد البلاغات حسب الموقع")
                st.plotly_chart(fig_location, use_container_width=True)

            if "مستوى_الخطورة" in df.columns:
                st.subheader("🚨 عدد البلاغات حسب مستوى الخطورة")
                fig_severity = px.histogram(df, x="مستوى_الخطورة", color="مستوى_الخطورة", title="عدد البلاغات حسب مستوى الخطورة")
                st.plotly_chart(fig_severity, use_container_width=True)

            if "الحالة" in df.columns and "مدة_الحل_ساعة" in df.columns:
                closed_df = df[df["الحالة"] == "مغلق"]
                avg_response = closed_df.groupby("نوع_الخدمة")["مدة_الحل_ساعة"].mean().reset_index()
                st.subheader("🕒 متوسط مدة الحل حسب نوع الخدمة")
                fig_response = px.bar(avg_response, x="نوع_الخدمة", y="مدة_الحل_ساعة", color="نوع_الخدمة",
                                      title="متوسط مدة الحل حسب نوع الخدمة")
                st.plotly_chart(fig_response, use_container_width=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء معالجة البيانات: {str(e)}")

    else:
        st.warning("📌 الرجاء رفع ملف البيانات لبدء التحليل.")

if __name__ == "__main__":
    main()
