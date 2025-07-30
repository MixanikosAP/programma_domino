import streamlit as st
import pandas as pd

st.set_page_config(page_title="Domino Effect Καθυστερήσεων", page_icon="🛠")

st.title("⏳ Domino Effect Καθυστερήσεων Εργασιών")

# 📂 File uploader αντί για σταθερό αρχείο
uploaded_file = st.file_uploader("📂 Ανέβασε το αρχείο Excel με τις εργασίες", type=["xlsx"])

if uploaded_file:
    try:
        # 📊 Διαβάζουμε το αρχείο που ανέβασε ο χρήστης
        df = pd.read_excel(uploaded_file)
        df["Ημερομηνία Έναρξης"] = pd.to_datetime(df["Ημερομηνία Έναρξης"])
        df["Ημερομηνία Λήξης"] = pd.to_datetime(df["Ημερομηνία Λήξης"])

        εργασία_καθυστέρηση = st.selectbox("Επίλεξε εργασία που καθυστερεί", df["Εργασία"].tolist())
        καθυστέρηση_ημέρες = st.number_input("Καθυστέρηση (ημέρες)", min_value=1, step=1)

        def βρες_επηρεαζόμενες(εργασία, εξαρτήσεις):
            επηρεαζόμενες = []
            for _, row in εξαρτήσεις.iterrows():
                if row["Εξαρτάται από"] == εργασία:
                    επηρεαζόμενες.append(row["Εργασία"])
                    επηρεαζόμενες.extend(βρες_επηρεαζόμενες(row["Εργασία"], εξαρτήσεις))
            return επηρεαζόμενες

        if st.button("Υπολόγισε Νέες Ημερομηνίες"):
            επηρεαζόμενες_εργασίες = βρες_επηρεαζόμενες(εργασία_καθυστέρηση, df)
            επηρεαζόμενες_εργασίες.append(εργασία_καθυστέρηση)

            for εργασία in επηρεαζόμενες_εργασίες:
                df.loc[df["Εργασία"] == εργασία, "Ημερομηνία Έναρξης"] += pd.Timedelta(days=καθυστέρηση_ημέρες)
                df.loc[df["Εργασία"] == εργασία, "Ημερομηνία Λήξης"] += pd.Timedelta(days=καθυστέρηση_ημέρες)

            st.success("✅ Νέες ημερομηνίες υπολογίστηκαν!")
            st.dataframe(df)

            # 📥 Export αρχείο
            output_excel = "updated_schedule.xlsx"
            df.to_excel(output_excel, index=False)
            with open(output_excel, "rb") as f:
                st.download_button("📥 Κατέβασε το ενημερωμένο Excel", f, file_name="updated_schedule.xlsx")

    except Exception as e:
        st.error(f"⚠️ Σφάλμα: {e}")
else:
    st.info("➕ Ανέβασε Excel για να ξεκινήσεις...")
