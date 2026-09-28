import streamlit as st

st.set_page_config(
    page_title="MAT2247 Study Document", page_icon="⌚", layout="wide"
)

# Force Streamlit's background to true black and expand container width
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #f0f6fc;
    }
    /* Expand the main container to use 100% of the screen width */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MAT Viewer")

def load_local_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

html_content = load_local_html("Test_1.html")

if html_content:
    # Use 100% width or a responsive layout height for the watch
    st.components.v1.html(html_content, height=600, scrolling=True)
else:
    st.error("Test_1.html not found in the repository folder.")
