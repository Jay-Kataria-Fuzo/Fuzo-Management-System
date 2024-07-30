import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd

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

df_brands = pd.DataFrame(execute_query(conn.table("brands").select("*", count="None"), ttl="0").data)
df_brands["identifier"] = df_brands["id"].astype(str)+" - "+df_brands["brand_name"]
sel_brand = tab2.selectbox("Select Brand", options=list(df_brands["identifier"]), index=None)

if sel_brand:
    with tab2.form("Edit Brand"):
        placeholder_form_top = st.empty()
        new_brand_name = st.text_input("Brand Name*", value=df_brands.loc[df_brands["identifier"] == sel_brand, "brand_name"].values[0])
        new_brand_image = st.text_input("Brand Image", value=df_brands.loc[df_brands["identifier"] == sel_brand, "brand_image"].values[0])
        col_submit, col_refresh = st.columns(2)
        submit_edit = col_submit.form_submit_button("Save", use_container_width=True)
        reset_edit = col_refresh.form_submit_button("Refresh", type="primary", use_container_width=True )
        placeholder_form_bottom = st.empty()

    if submit_edit:
        if new_brand_name.strip() != "":
            placeholder_form_top.success("Brand updated Successfully!")
            placeholder_form_bottom.success("Brand updated Successfully!")
            execute_query(conn.table("brands").update([{"brand_name":new_brand_name,"brand_image":new_brand_image}], count="None").eq("id",df_brands.loc[df_brands["identifier"] == sel_brand, "id"].values[0] ), ttl='0')
        else:
            placeholder_form_top.error("Fill all required Fields!")
            placeholder_form_bottom.error("Fill all required Fields!")
