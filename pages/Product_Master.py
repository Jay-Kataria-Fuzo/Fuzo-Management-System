import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config("Management Dashboard", "https://joinfuzo.com/images/favicon/favicon-32x32.png", layout="wide")

st.header("Product Master")

tab1, tab2 = st.tabs(["Add Product", "Edit Product"])

with tab1.form("Add Product", clear_on_submit=True):
    st.header("Add Product")

    placeholder_form_top = st.empty()

    product_display_name = st.text_input("Product Display Name*", )
    product_category = st.selectbox("Category*", options=["Shampoo & Conditioner"], index=None)
    product_brand = st.text_input("Brand*")
    product_description = st.text_area("Product Description")
    product_dimensions = st.text_input("Product Dimensions")
    product_weight = st.number_input("Product Weight* (in grams)")
    col_measurement, col_unit = st.columns([1,0.5])
    product_unit_measurement = col_measurement.number_input("Unit Measurement*")
    product_unit = col_unit.selectbox("Measurement Units*", options=["ml", "gm"])
    product_mrp = st.number_input("MRP* (in Rupee's)")

    col_submit, col_reset = st.columns(2)
    submit_add = col_submit.form_submit_button("Save", use_container_width=True)
    reset = col_reset.form_submit_button("Reset", type="primary", use_container_width=True )

    placeholder_form_bottom = st.empty()

if submit_add:
    if product_display_name != "" and product_category !="" and product_brand != "" and product_weight != "" and product_unit_measurement !="" and product_unit != "" and product_mrp != "":
        placeholder_form_top.success("Product added Successfully!")
        placeholder_form_bottom.success("Product added Successfully!")
        st.write({
            "product_display_name":product_display_name,
            "product_category":product_category,
            "product_brand":product_brand,
            "product_description":product_description,
            "product_dimensions":product_dimensions,
            "product_weight":product_weight,
            "product_unit_measurement":product_unit_measurement,
            "product_unit":product_unit,
            "product_mrp":product_mrp
        })
    else:
        placeholder_form_top.error("Fill all required Fields!")
        placeholder_form_bottom.error("Fill all required Fields!")

