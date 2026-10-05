from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from supabase import Client, create_client

# --- HIDE STREAMLIT HEADER & GITHUB ICONS ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ====================== CONFIG & SUPABASE ======================
st.set_page_config(page_title="MAT 2247 Chapter Notes", page_icon="📚", layout="wide")

# ====================== CUSTOM DARK MODE CSS ======================
st.markdown("""
    <style>
        /* Force Dark Theme on Streamlit UI Elements */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        [data-testid="stSidebar"] {
            background-color: #161b22;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0);
        }
        /* Style form inputs, text boxes, and buttons for dark mode */
        .stTextInput input, .stPasswordInput input {
            background-color: #21262d;
            color: #ffffff;
            border-color: #30363d;
        }
        .stButton>button {
            background-color: #238636;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #2ea043;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

SA_TZ = ZoneInfo("Africa/Johannesburg")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

# ====================== AUTHENTICATION STATE ======================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Enter PIN to Access Notes")
    with st.form("pin_form"):
        entered_pin = st.text_input("PIN", type="password", max_chars=6)
        submit_button = st.form_submit_button("Unlock")

        if submit_button:
            if entered_pin == st.secrets["APP_PIN"]:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect PIN.")
else:
    if st.sidebar.button("🔒 Lock App"):
        st.session_state["authenticated"] = False
        st.rerun()

    def load_logs():
        try:
            response = supabase.table("logs").select("id, timestamp, subject, focus_state, notes").order("id", desc=True).execute()
            if not response.data:
                return pd.DataFrame(columns=["ID", "Timestamp", "Subject", "Focus_State", "Notes"])
            df = pd.DataFrame(response.data)
            return df.rename(columns={
                "id": "ID",
                "timestamp": "Timestamp",
                "subject": "Subject",
                "focus_state": "Focus_State",
                "notes": "Notes"
            })
        except Exception:
            return pd.DataFrame(columns=["ID", "Timestamp", "Subject", "Focus_State", "Notes"])

    st.title("📚 MAT 2247 — Latest Chapter Notes")

    history = load_logs()

    if not history.empty:
        # Filter strictly for MAT 2247 and "Chapter Notes" category/focus_state
        mat_notes = history[
            (history["Subject"].str.contains("MAT 2247", case=False, na=False)) & 
            (history["Focus_State"].str.lower() == "chapter notes")
        ]

        if not mat_notes.empty:
            # Get the latest entry (your uploaded test2.md content)
            latest_entry = mat_notes.iloc[0]

            st.subheader(f"🗓️ {latest_entry.get('Timestamp', 'Recent Entry')}")
            notes_content = latest_entry.get("Notes", "No content provided.")

            stripped = notes_content.strip().lower()
            if stripped.startswith("<!doctype") or stripped.startswith("<html") or stripped.startswith("<div"):
                components.html(notes_content, height=600, scrolling=True)
            else:
                # Render Markdown content from test2.md with HTML allowed for custom styling
                st.markdown(notes_content, unsafe_allow_html=True)
        else:
            st.warning("No entries found under 'Chapter Notes' for MAT 2247 in Supabase.")
    else:
        st.warning("No logs found in Supabase database.")
