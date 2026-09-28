import streamlit as st

st.set_page_config(
    page_title="MAT2247 Study Document", page_icon="⌚", layout="centered"
)

# Force Streamlit's background to true black to match your HTML
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #f0f6fc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MAT2247Viewer")


def load_local_html(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    return None


html_content = load_local_html("Test_1.html")

if html_content:
  # Renders full height for easy scrolling on a smartwatch browser
  st.components.v1.html(html_content, height=800, scrolling=True)
else:
  st.error("Test_1.html not found in the repository folder.")
