import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

st.set_page_config("Management Dashboard", "https://joinfuzo.com/images/favicon/favicon-32x32.png", layout="wide")

conn = st.connection("supabase",type=SupabaseConnection)

st.header("Brand Master")


tab1, tab2 = st.tabs(["Add Brand", "Edit Brand"])

with tab1.form("Add Brand", clear_on_submit=True):
    st.header("Add Brand")

    placeholder_form_top = st.empty()

    brand_name = st.text_input("Brand Name*")
    brand_image = st.text_input("Brand Logo URL")

    col_submit, col_reset = st.columns(2)
    submit_add = col_submit.form_submit_button("Save", use_container_width=True)
    reset = col_reset.form_submit_button("Reset", type="primary", use_container_width=True )

    placeholder_form_bottom = st.empty()

if submit_add:
    if brand_name.strip() != "":
        placeholder_form_top.success("Brand added Successfully!")
        placeholder_form_bottom.success("Brand added Successfully!")
        execute_query(conn.table("brands").insert([{"brand_name":brand_name,"brand_image":brand_image or ""}], count="None"), ttl='0')

    else:
        placeholder_form_top.error("Fill all required Fields!")
        placeholder_form_bottom.error("Fill all required Fields!")


