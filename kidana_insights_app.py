import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import os

# --------- إعداد مفتاح OpenAI ---------
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

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

            # التعرف التلقائي على نوع التحليل بناءً على الأعمدة:
            if "نوع_الخدمة" in df.columns:
                st.markdown("### 🔎 تم التعرف على ملف بلاغات تشغيلية")

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

            elif "KPI Name" in df.columns and "Department" in df.columns:
                st.markdown("### 📈 تم التعرف على ملف KPIs")

                st.subheader("📊 عدد KPIs حسب القسم")
                kpi_by_dept = df["Department"].value_counts().reset_index()
                kpi_by_dept.columns = ["Department", "Count"]
                fig_kpi_dept = px.bar(kpi_by_dept, x="Department", y="Count", color="Department",
                                      title="عدد KPIs حسب القسم")
                st.plotly_chart(fig_kpi_dept, use_container_width=True)

                if "Perspective" in df.columns:
                    st.subheader("📊 عدد KPIs حسب Perspective")
                    kpi_perspective = df["Perspective"].value_counts().reset_index()
                    kpi_perspective.columns = ["Perspective", "Count"]
                    fig_kpi_persp = px.pie(kpi_perspective, names="Perspective", values="Count",
                                           title="توزيع KPIs حسب Perspective")
                    st.plotly_chart(fig_kpi_persp, use_container_width=True)

                if "Frequency" in df.columns:
                    st.subheader("📊 توزيع KPIs حسب Frequency")
                    freq_counts = df["Frequency"].value_counts().reset_index()
                    freq_counts.columns = ["Frequency", "Count"]
                    fig_freq = px.bar(freq_counts, x="Frequency", y="Count", color="Frequency",
                                      title="تكرار KPIs حسب Frequency")
                    st.plotly_chart(fig_freq, use_container_width=True)

            # --------- المساعد الذكي ---------
            with st.expander("🧠 مساعد ذكي (GPT)"):
                st.markdown("**📌 اسأل عن البيانات بأي صيغة وسأجيب باستخدام الذكاء الاصطناعي 👇**")
                user_question = st.text_area("✍️ اكتب سؤالك هنا:")

                if st.button("تحليل بالسؤال") and user_question:
                    try:
                        sampled_df = df.sample(n=min(100, len(df)), random_state=42)
                        context = sampled_df.to_markdown(index=False)
                        prompt = f"""
                        جاوب على السؤال التالي بناءً على الجدول التالي:

                        {context}

                        السؤال: {user_question}
                        """

                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "أنت مساعد بيانات ذكي تحلل الجداول وتشرح النتائج بدقة"},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        answer = response.choices[0].message.content
                        st.markdown(f"**📌 الإجابة:**\n\n{answer}")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ في المساعد الذكي:\n\n{str(e)}")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء معالجة البيانات: {str(e)}")
    else:
        st.warning("📌 الرجاء رفع ملف البيانات لبدء التحليل.")

if __name__ == "__main__":
    main()
