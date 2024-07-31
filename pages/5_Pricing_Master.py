import pandas as pd
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
from itertools import product

st.set_page_config(
    "Management Dashboard",
    "https://joinfuzo.com/images/favicon/favicon-32x32.png",
    layout="wide",
)

st.markdown('''
            <style>
            header {visibility: hidden;}
            .st-emotion-cache-1jicfl2 {padding-top: 1rem}
            </style>
            ''', unsafe_allow_html=True)

logo_url = "https://joinfuzo.com/images/logo-fuzo.png"  

st.image(logo_url)

st.header("Pricing Master")



conn = st.connection("supabase", type=SupabaseConnection)

df_vendors = pd.DataFrame(execute_query(conn.table("vendors").select("id, display_name", count="None"), ttl="0").data)
df_products = pd.DataFrame(execute_query(conn.table("products").select("id, product_name", count="None"), ttl="0").data)
df_pricing = pd.DataFrame(execute_query(conn.table("pricing").select("*", count="None"), ttl="0").data)


if len(df_vendors) >= 0 and len(df_products) >= 0:


    vendor_id_to_name = dict(zip(df_vendors['id'], df_vendors['display_name']))
    product_id_to_name = dict(zip(df_products['id'], df_products['product_name']))

    vendor_name_to_id = dict(zip(df_vendors['display_name'], df_vendors['id']))
    product_name_to_id = dict(zip(df_products['product_name'], df_products['id']))


    selected_vendors = st.multiselect("Vendors", options=df_vendors["display_name"].to_list(), default=None)
    selected_products = st.multiselect("Products", options=df_products["product_name"].to_list(), default=None)

    if len(selected_vendors) == 0:
        selected_vendors = df_vendors["display_name"].to_list()

    if len(selected_products) == 0:
        selected_products = df_products["product_name"].to_list()

    selected_vendor_ids = [vendor_name_to_id[vendor] for vendor in selected_vendors]
    selected_product_ids = [product_name_to_id[product] for product in selected_products]

    combinations = list(product(selected_vendor_ids, selected_product_ids))
    if combinations:
        data = {
            'id': [0] * len(combinations),
            'vendor_id': [combo[0] for combo in combinations],
            'product_id': [combo[1] for combo in combinations],
            'selling_price': [0] * len(combinations),
            'commission': [0] * len(combinations),
            'inventory': [0] * len(combinations),
            'specification': [""] * len(combinations)
        }
    df_pricing = pd.concat([pd.DataFrame(data), df_pricing], ignore_index=True)

    df_pricing['vendor_name'] = df_pricing['vendor_id'].map(vendor_id_to_name)
    df_pricing['product_name'] = df_pricing['product_id'].map(product_id_to_name)

    display_df = df_pricing.drop(columns=['vendor_id', 'product_id'])
    display_df = display_df[display_df["vendor_name"].isin(selected_vendors)]
    display_df = display_df[display_df["product_name"].isin(selected_products)]
    display_df = display_df.reset_index(drop=True)

    column_config = {
        'id': {'header':'ID', 'editable': False},
        'vendor_name': {'header': 'Vendor', 'editable': False},
        'product_name': {'header': 'Product', 'editable': False},
        'selling_price': {'header': 'Selling Price (₹)', 'type': 'number', 'step': 0.01},
        'commission': {'header': 'Commission (₹)', 'type': 'number', 'step': 0.01},
        'inventory': {'header': 'Inventory', 'type': 'number', 'step': 1},
        'specification': {'header': 'Specification'}
    }

    edited_df = st.data_editor(
        data=display_df[["id", "vendor_name", "product_name", "selling_price", "commission", "inventory", "specification"]],
        column_config=column_config,
        height=400,  
        width=800,   
        use_container_width=True
    )

    col_save, col_reset = st.columns(2)
    if col_save.button("Save Changes", use_container_width=True):
        st.write(edited_df)
    if col_reset.button("Resest", type="primary", use_container_width=True):
        st.rerun()


