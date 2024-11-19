import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Load the processed company data
    company_data_path = "processed_innovius_data.xlsx"
    companies = pd.read_excel(company_data_path)

    # Load the similarity scores
    similarity_scores_path = "top_n_similarity_scores.xlsx"
    scores = pd.read_excel(similarity_scores_path)

    return companies, scores


st.title("Company Similarity Viewer")


companies, similarity_scores = load_data()


st.sidebar.header("Select a Company")
selected_name = st.sidebar.selectbox(
    "Choose a company by name:",
    companies['Name']
)

st.subheader("Selected Company Details")
selected_company = companies[companies['Name'] == selected_name].iloc[0]
selected_index = selected_company.name  # Get the index of the selected company
st.write(f"**Name:** {selected_company['Name']}")
st.write(f"**Description:** {selected_company['Cleaned_Description']}")


st.subheader("Top Similar Companies")
top_similar = similarity_scores.iloc[selected_index]
similar_companies = [
    (int(top_similar[f"Top_{i}_Company_ID"]), top_similar[f"Top_{i}_Similarity_Score"])
    for i in range(1, 11)
]


similarity_results = []
for company_id, score in similar_companies:
    similar_company = companies.iloc[company_id]
    similarity_results.append({
        "Company Name": similar_company['Name'],
        "Similarity Score": round(score, 4),
        "Description": similar_company['Cleaned_Description']
    })


similarity_df = pd.DataFrame(similarity_results)
st.write(similarity_df)

