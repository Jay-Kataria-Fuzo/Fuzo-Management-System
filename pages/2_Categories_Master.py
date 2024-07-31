import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd

st.set_page_config("Management Dashboard", "https://joinfuzo.com/images/favicon/favicon-32x32.png", layout="wide")

conn = st.connection("supabase",type=SupabaseConnection)

st.markdown('''
            <style>
            header {visibility: hidden;}
            .st-emotion-cache-1jicfl2 {padding-top: 1rem}
            </style>
            ''', unsafe_allow_html=True)

logo_url = "https://joinfuzo.com/images/logo-fuzo.png"  

st.image(logo_url)

st.header("Category Master")

def build_paths(df):
    paths = []
    ids = []

    def find_path(row, current_path):
        if pd.isna(row['parent_id']):
            paths.append(current_path)
            return
        parent_row = df[df['id'] == row['parent_id']].iloc[0]
        find_path(parent_row, f"{parent_row['title']} > {current_path}")

    for _, row in df.iterrows():
        find_path(row, row['title'])
        ids.append(row["id"])

    return paths, ids

df = pd.DataFrame(execute_query(conn.table("categories").select("*", count="None"), ttl='0').data)

paths, ids = build_paths(df)

with st.form("Add Category", clear_on_submit=True):

    st.header("Add Category")

    placeholder_form_top = st.empty()

    selected_path = st.selectbox("Find in category", options=paths, index=None) or ""

    new_category = st.text_input("Add category*")

    col_submit, col_delete, col_refresh = st.columns(3)
    submit = col_submit.form_submit_button("Save", use_container_width=True)
    delete = col_delete.form_submit_button("Delete", type="primary", use_container_width=True)
    reset = col_refresh.form_submit_button("Refresh", type="primary", use_container_width=True )

    placeholder_form_bottom = st.empty()

if submit:
    if new_category.strip() != "":
        parent_id = None
        if selected_path != "":
            parent_id = ids[paths.index(selected_path)]
        execute_query(conn.table("categories").insert([{"title":new_category,"parent_id":parent_id}], count="None"), ttl='0')
        placeholder_form_top.success("Category added Successfully!")
        placeholder_form_bottom.success("Category added Successfully!")

    else:
        placeholder_form_top.error("Fill all required Fields!")
        placeholder_form_bottom.error("Fill all required Fields!")

if delete:
    if selected_path != "":
        parent_id = ids[paths.index(selected_path)]
        execute_query(conn.table("categories").delete(count="None").eq("id",parent_id), ttl='0')
        placeholder_form_top.success("Category deleted Successfully!")
        placeholder_form_bottom.success("Category deleted Successfully!")
    else:
        placeholder_form_top.error("Select a Category!")
        placeholder_form_bottom.error("Select a Category!")




