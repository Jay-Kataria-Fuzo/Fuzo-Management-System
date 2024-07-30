import pandas as pd
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

st.set_page_config(
    "Management Dashboard",
    "https://joinfuzo.com/images/favicon/favicon-32x32.png",
    layout="wide",
)

st.header("Product Master")

conn = st.connection("supabase", type=SupabaseConnection)

tab1, tab2 = st.tabs(["Add Product", "Edit Product"])

df_categories = pd.DataFrame(
    execute_query(conn.table("categories").select("*", count="None"), ttl="0").data
)
df_brands = execute_query(conn.table("brands").select("*", count="None"), ttl="0").data

brand_dict = {item["brand_name"]: item["id"] for item in df_brands}


def build_paths(df):
    paths = []
    ids = []

    def find_path(row, current_path):
        if pd.isna(row["parent_id"]):
            paths.append(current_path)
            return
        parent_row = df[df["id"] == row["parent_id"]].iloc[0]
        find_path(parent_row, f"{parent_row['title']} > {current_path}")

    for _, row in df.iterrows():
        find_path(row, row["title"])
        ids.append(row["id"])

    return paths, ids


categories, category_ids = build_paths(df_categories)


with tab1.form("Add Product", clear_on_submit=True):
    st.header("Add Product")

    placeholder_form_top = st.empty()

    product_display_name = st.text_input(
        "Product Display Name*",
    )
    product_category = st.selectbox("Category*", options=categories, index=None)
    product_brand = st.selectbox("Brand*", options=list(brand_dict.keys()), index=None)
    product_description = st.text_area("Product Description")
    product_images = st.text_area("Image URLs (one per line)", height=100)
    product_dimensions = st.text_input("Product Dimensions")
    product_weight = st.number_input("Product Weight* (in grams)")
    col_measurement, col_unit = st.columns([1, 0.5])
    product_unit_measurement = col_measurement.number_input("Unit Measurement*")
    product_unit = col_unit.selectbox("Measurement Units*", options=["ml", "gm"])
    product_mrp = st.number_input("MRP* (in Rupee's)")

    col_submit, col_reset = st.columns(2)
    submit_add = col_submit.form_submit_button("Save", use_container_width=True)
    reset = col_reset.form_submit_button(
        "Reset", type="primary", use_container_width=True
    )

    placeholder_form_bottom = st.empty()

if submit_add:
    if (
        product_display_name != ""
        and product_category != ""
        and product_brand != ""
        and product_weight != ""
        and product_unit_measurement != ""
        and product_unit != ""
        and product_mrp != ""
    ):
        placeholder_form_top.success("Product added Successfully!")
        placeholder_form_bottom.success("Product added Successfully!")
        execute_query(
            conn.table("products").insert(
                [
                    {
                        "product_name": product_display_name,
                        "category_id": category_ids[categories.index(product_category)],
                        "brand_id": brand_dict[product_brand],
                        "product_description": product_description,
                        "product_images": [
                            url.strip()
                            for url in product_images.split("\n")
                            if url.strip()
                        ],
                        "product_dimensions": product_dimensions,
                        "product_weight": product_weight,
                        "unit_measurement": product_unit_measurement,
                        "units": product_unit == "ml",
                        "product_mrp": product_mrp,
                    }
                ],
                count="None",
            ),
            ttl="0",
        )
    else:
        placeholder_form_top.error("Fill all required Fields!")
        placeholder_form_bottom.error("Fill all required Fields!")
