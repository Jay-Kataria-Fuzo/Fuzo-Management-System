import pandas as pd
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

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

st.header("Vendor Master")

conn = st.connection("supabase", type=SupabaseConnection)

tab_add, tab_edit = st.tabs(["Add Vendor", "Edit Vendor"])

with tab_add.form("Add Vendor", clear_on_submit=True):
    st.header("Add Vendor")

    placeholder_form_top = st.empty()

    display_name = st.text_input("Vendor Display Name*")
    vendor_name = st.text_input("Vendor Name*")

    billing_address = st.text_area("Billing Address*")
    billing_poc_name = st.text_input("Billing POC Name*")
    billing_poc_contact = st.text_input("Billing POC Contact*")

    fullfilment_address = st.text_area("Fullfilment Address*")
    fullfilment_poc_name = st.text_input("Fullfilment POC Name*")
    fullfilment_poc_contact = st.text_input("Fullfilment POC Contact*")

    contract_url = st.text_area("Contact/Agreement/BG URL* (Seperate by new lines)")

    col_submit, col_reset = st.columns(2)
    submit_add = col_submit.form_submit_button("Save", use_container_width=True)
    reset = col_reset.form_submit_button(
        "Reset", type="primary", use_container_width=True
    )

    placeholder_form_bottom = st.empty()

if submit_add:
    if (
        display_name.strip() != ""
        and vendor_name.strip() != ""
        and billing_address.strip() != ""
        and billing_poc_name.strip() != ""
        and billing_poc_contact.strip() != ""
        and fullfilment_address.strip() != ""
        and fullfilment_poc_name.strip() != ""
        and fullfilment_poc_contact.strip() != ""
        and contract_url.strip() != ""
    ):
        execute_query(
            conn.table("vendors").insert(
                [
                    {
                        "display_name":display_name,
                        "vendor_name":vendor_name,
                        "billing_address":billing_address,
                        "billing_poc_name":billing_poc_name,
                        "billing_poc_contact":billing_poc_contact,
                        "fullfilment_address":fullfilment_address,
                        "fullfilment_poc_name":fullfilment_poc_name,
                        "fullfilment_poc_contact":fullfilment_poc_contact,
                        "contract_url": [
                            url.strip()
                            for url in contract_url.split("\n")
                            if url.strip()
                        ]
                    }
                ],
                count="None",
            ),
            ttl="0",
        )
        placeholder_form_top.success("Vendor added Successfully!")
        placeholder_form_bottom.success("Vendor added Successfully!")
    else:
        placeholder_form_top.error("Fill all required Fields!")
        placeholder_form_bottom.error("Fill all required Fields!")


df = pd.DataFrame(execute_query(conn.table("vendors").select("*", count="None"), ttl="0").data)
if len(df)>0:
    df["identifiers"] = df["id"].astype(str) + " - " + df["display_name"]
    selected_vendor = tab_edit.selectbox("Select Vendor", options=list(df["identifiers"]), index=None)
    if selected_vendor:
        selected_data = df[df["identifiers"] == selected_vendor].to_dict('records')[0]
        with tab_edit.form("Edit Vendor", clear_on_submit=True):
            st.header("Edit Vendor")

            new_placeholder_form_top = st.empty()

            new_display_name = st.text_input("Vendor Display Name*", value=selected_data["display_name"])
            new_vendor_name = st.text_input("Vendor Name*", value=selected_data["vendor_name"])

            new_billing_address = st.text_area("Billing Address*", value=selected_data["billing_address"])
            new_billing_poc_name = st.text_input("Billing POC Name*", value=selected_data["billing_poc_name"])
            new_billing_poc_contact = st.text_input("Billing POC Contact*", value=selected_data["billing_poc_contact"])

            new_fullfilment_address = st.text_area("Fullfilment Address*", value=selected_data["fullfilment_address"])
            new_fullfilment_poc_name = st.text_input("Fullfilment POC Name*", value=selected_data["fullfilment_poc_name"])
            new_fullfilment_poc_contact = st.text_input("Fullfilment POC Contact*", value=selected_data["fullfilment_poc_contact"])

            new_contract_url = st.text_area("Contact/Agreement/BG URL* (Seperate by new lines)", value=",".join(selected_data["contract_url"]))

            new_col_submit, new_col_delete, new_col_reset = st.columns(3)
            new_submit_edit = new_col_submit.form_submit_button("Save", use_container_width=True)
            new_delete = new_col_delete.form_submit_button("Delete", type="primary", use_container_width=True)
            new_reset = new_col_reset.form_submit_button(
                "Reset", type="primary", use_container_width=True
            )

            new_placeholder_form_bottom = st.empty()

        if new_submit_edit:
            if (
                new_display_name.strip() != ""
                and new_vendor_name.strip() != ""
                and new_billing_address.strip() != ""
                and new_billing_poc_name.strip() != ""
                and new_billing_poc_contact.strip() != ""
                and new_fullfilment_address.strip() != ""
                and new_fullfilment_poc_name.strip() != ""
                and new_fullfilment_poc_contact.strip() != ""
                and new_contract_url.strip() != ""
            ):
                execute_query(
                    conn.table("vendors").insert(
                        [
                            {
                                "display_name":new_display_name,
                                "vendor_name":new_vendor_name,
                                "billing_address":new_billing_address,
                                "billing_poc_name":new_billing_poc_name,
                                "billing_poc_contact":new_billing_poc_contact,
                                "fullfilment_address":new_fullfilment_address,
                                "fullfilment_poc_name":new_fullfilment_poc_name,
                                "fullfilment_poc_contact":new_fullfilment_poc_contact,
                                "contract_url": [
                                    url.strip()
                                    for url in new_contract_url.split("\n")
                                    if url.strip()
                                ]
                            }
                        ],
                        count="None",
                    ),
                    ttl="0",
                )
                new_placeholder_form_top.success("Vendor updated Successfully!")
                new_placeholder_form_bottom.success("Vendor updated Successfully!")
            else:
                new_placeholder_form_top.error("Fill all required Fields!")
                new_placeholder_form_bottom.error("Fill all required Fields!")

        if new_delete:
            execute_query(conn.table("vendors").delete(count="None").eq("id",selected_data["id"]), ttl='0')
            new_placeholder_form_top.success("Vendor deleted Successfully!")
            new_placeholder_form_bottom.success("Vendor deleted Successfully!")
        
