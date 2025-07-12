import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="CBTC Log Analyzer", layout="wide")

st.title("🚆 CBTC Log Analyzer with Fault Classification")

# ---------- DATABASE FUNCTIONS ----------

DB_NAME = "cbtc_logs.db"

def insert_faults_to_db(df):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO logs (timestamp, log_level, log_message, fault_type)
            VALUES (?, ?, ?, ?)
        """, (row["Timestamp"], row["LogLevel"], row["LogMessage"], row["FaultType"]))
    conn.commit()
    conn.close()

def load_logs_from_db():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df


# ---------- CLASSIFICATION FUNCTION ----------

def classify_message(msg):
    msg_lower = msg.lower()
    if "track" in msg_lower:
        return "Track Circuit Failure"
    elif "signal" in msg_lower:
        return "Signal Conflict"
    elif "balise" in msg_lower:
        return "Balise Error"
    elif "comm" in msg_lower or "communication" in msg_lower:
        return "Communication Fault"
    else:
        return "Unknown"

# ---------- FILE UPLOAD SECTION ----------

st.sidebar.header("📤 Upload CBTC Log File")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'LogMessage' not in df.columns:
        st.error("❌ 'LogMessage' column not found.")
    else:
        st.success("✅ File uploaded!")

        df["FaultType"] = df["LogMessage"].apply(classify_message)

        # Add default fields if missing
        if "Timestamp" not in df.columns:
            df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "LogLevel" not in df.columns:
            df["LogLevel"] = "INFO"

        insert_faults_to_db(df)

        st.subheader("✅ Uploaded Data (Classified)")
        st.dataframe(df.head())


# ---------- SEARCH & FILTER SECTION ----------

st.markdown("---")
st.header("🔍 Search & Filter Saved Logs")

log_df = load_logs_from_db()

if not log_df.empty:
    # Filters
    fault_types = log_df["fault_type"].unique().tolist()
    selected_faults = st.multiselect("Select Fault Types:", options=fault_types, default=fault_types)
    search_term = st.text_input("Search in Log Message:")

    filtered_df = log_df[
        (log_df["fault_type"].isin(selected_faults)) &
        (log_df["log_message"].str.contains(search_term, case=False))
    ]

    st.write(f"### Showing {len(filtered_df)} results")
    st.dataframe(filtered_df)
    st.write("### 📊 Fault Type Distribution (Filtered Logs)")
    from collections import Counter
    import matplotlib.pyplot as plt

    fault_counts = Counter(filtered_df["fault_type"])
    fig, ax = plt.subplots()
    ax.bar(fault_counts.keys(), fault_counts.values(), color='skyblue')
    ax.set_ylabel("Count")
    ax.set_xlabel("Fault Type")
    ax.set_title("Fault Distribution")
    st.pyplot(fig)

    # 📁 Export CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📁 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_fault_logs.csv',
        mime='text/csv',
    )
    
else:
    st.info("📭 No logs in database yet.")