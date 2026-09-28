import streamlit as st

st.set_page_config(
    page_title="MAT2141 Study Document", page_icon="📚", layout="wide"
)

st.title("MAT2141 - Study Document Viewer")
st.write("Rendering `Test_1.html` directly from the repository.")


# Read the HTML file directly from the local directory
def load_local_html(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    return None


html_content = load_local_html("Test_1.html")

if html_content:
  # Render the HTML content inside Streamlit with a scrollable frame
  st.components.v1.html(html_content, height=900, scrolling=True)
else:
  st.error(
      "`Test_1.html` was not found in the same folder. Please make sure both"
      " files are in the same directory."
  )
