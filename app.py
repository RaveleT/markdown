import requests
import streamlit as st

st.set_page_config(
    page_title="MAT2141 Study Document", page_icon="📚", layout="wide"
)

st.title("MAT2141 - Study Document Viewer")
st.write("Rendering `Test_1.html` directly from your GitHub repository.")

# TODO: Replace with your actual GitHub Raw URL
# Example: https://raw.githubusercontent.com/username/repo/main/Test_1.html
GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/Test_1.html"
)


@st.cache_data(ttl=600)  # Cache the HTML content for 10 minutes
def fetch_html_from_github(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses (404, 500, etc.)
    return response.text
  except Exception as e:
    return None


# Load the HTML content
html_content = fetch_html_from_github(GITHUB_RAW_URL)

if html_content:
  # Render the HTML content inside Streamlit with a scrollable frame
  st.components.v1.html(html_content, height=900, scrolling=True)
else:
  st.error(
      "Could not load the file from GitHub. Please check that the URL is"
      " correct and the repository is public."
  )