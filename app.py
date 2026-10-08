import pandas as pd
import streamlit as st

# Page setup for mobile responsiveness
st.set_page_config(
    page_title="Operator Data Portal", page_icon="📊", layout="centered"
)

st.title("📊 Operator Lookup Portal")

# Sidebar for admin file upload
st.sidebar.header("Admin Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload Today's Excel File", type=["xlsx", "xls"]
)

st.markdown("---")

if uploaded_file is not None:
    try:
        # Load Excel file
        df = pd.read_excel(uploaded_file)

        # Clean up column names (strip whitespace)
        df.columns = df.columns.astype(str).str.strip()

        st.info("💡 Enter your Operator ID below to check your payment & defect rate.")

        # Search bar for operators
        search_id = st.text_input("Enter Operator ID:", placeholder="e.g. OP-101")

        if st.button("Search", use_container_width=True):
            if search_id.strip():
                # Perform search matching string representation
                matched_data = df[
                    df["Operator ID"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == search_id.strip().upper()
                ]

                if not matched_data.empty:
                    st.success("Record Found!")

                    payment = matched_data.iloc[0].get(
                        "Total Payment", "N/A"
                    )
                    defect = matched_data.iloc[0].get("Defect Rate %", "N/A")

                    # Display clean metrics on mobile screens
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            label="💰 Total Payment", value=f"{payment}"
                        )
                    with col2:
                        st.metric(
                            label="⚠️ Defect Rate", value=f"{defect}"
                        )
                else:
                    st.error("Operator ID not found in today's file.")
            else:
                st.warning("Please enter a valid Operator ID.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.warning("⚠️ No file uploaded yet. Admin must upload today's Excel file.")