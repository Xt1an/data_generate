import streamlit as st
import xml.etree.ElementTree as ET
import random
import hashlib
from datetime import datetime
import json
import pandas as pd

def load_computer_names_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []

def load_discovery_names_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []


def load_publisher_groups_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []
    
def load_group_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []
    
def load_license_server_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []
    
def load_license_type_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []


# Usage:
COMPUTER_NAMES = load_computer_names_from_csv("user.csv")
PUBLISHER_GROUPS = load_publisher_groups_from_csv("products.csv")
DISCOVERY_MODELS = load_discovery_names_from_csv("discovery.csv")
GROUP_NAMES = load_discovery_names_from_csv("group.csv")
LICENSE_SERVER_VALUES = load_discovery_names_from_csv("license_server.csv")
LICENSE_TYPE_VALUES= load_discovery_names_from_csv("license_type.csv")



if not PUBLISHER_GROUPS:
    st.error("No Autodesk groups found. Ensure the 'publisher_group.json' file exists and contains valid data.")
if not COMPUTER_NAMES:
    st.error("No computer names found. Ensure the 'data.json' file exists and contains valid data.")

# Other Fixed Values

DENIAL_ID_TEMPLATE = "Denial {}"

def generate_unique_hash():
    """Generates a unique hash value to ensure each XML field requiring a hash is unique and randomized."""
    return hashlib.md5(str(random.random()).encode()).hexdigest()

def generate_xml_record(denial_num):
    # Randomly select from AUTODESK_GROUPS
    group = random.choice(PUBLISHER_GROUPS)
    
    # Select a computer name and append "-PC"
    users = random.choice(COMPUTER_NAMES)
    discovery = random.choice(DISCOVERY_MODELS)
    group = random.choice(GROUP_NAMES)
    license_server = random.choice(LICENSE_SERVER_VALUES)
    license_type = random.choice(LICENSE_TYPE_VALUES)

    # Create the <samp_eng_app_denial> element with "INSERT_OR_UPDATE" action
    denial = ET.Element("samp_eng_app_denial", action="INSERT_OR_UPDATE")
    ET.SubElement(denial, "additional_key")
    ET.SubElement(denial, "computer", display_value=users["computer_name"]).text = users["computer_sys_id"]
    ET.SubElement(denial, "denial_date").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(denial, "denial_id").text = DENIAL_ID_TEMPLATE.format(denial_num + 100)  # Offset by 29 to start at 30
    ET.SubElement(denial, "discovery_model", display_value=discovery["discovery_model"]).text = discovery["discovery_sys_id"]
    ET.SubElement(denial, "group", display_value=group["group"]).text = group["group_sys_id"]
    ET.SubElement(denial, "is_product_normalized").text = "true"
    ET.SubElement(denial, "last_denial_time").text = datetime.now().strftime("%Y-%m-%d %H:%M")
    ET.SubElement(denial, "license_server", display_value=license_server["license_server"]).text = license_server["license_server_sys_id"]
    ET.SubElement(denial, "license_type", display_value=license_type["license_type"]).text = license_type["license_type_sys_id"]
    ET.SubElement(denial, "norm_product", display_value=discovery["norm_product"]).text = discovery["norm_product_sys_id"]
    ET.SubElement(denial, "norm_publisher", display_value=discovery["norm_publisher"]).text = discovery["norm_publisher_sys_id"]
    ET.SubElement(denial, "product").text = discovery["product"]
    ET.SubElement(denial, "publisher").text = discovery["publisher"]
    ET.SubElement(denial, "source").text = "OpeniT"
    ET.SubElement(denial, "sys_created_by").text = "admin"
    ET.SubElement(denial, "sys_created_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(denial, "sys_domain").text = generate_unique_hash()
    ET.SubElement(denial, "sys_domain_path").text = "/"
    ET.SubElement(denial, "sys_id").text = generate_unique_hash()
    ET.SubElement(denial, "sys_mod_count").text = str(random.randint(1, 100))
    ET.SubElement(denial, "sys_updated_by").text = "admin"
    ET.SubElement(denial, "sys_updated_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(denial, "total_denial_count").text = str(random.randint(1, 10))
    ET.SubElement(denial, "user", display_value=users["user"]).text = users["user_sys_id"]
    ET.SubElement(denial, "version").text = "2020"
    ET.SubElement(denial, "workstation", display_value=users["workstation"]).text = users["workstation_sys_id"]
    return denial

st.title("XML Record Generator for samp_eng_app_denial.xml")

num_records_input = st.text_input("Enter the number of records to generate", value="")

if num_records_input.isdigit():
    num_records = int(num_records_input)
else:
    num_records = 0

if st.button("Generate XML"):
    if num_records <= 0:
        st.error("Please enter a valid number greater than 0.")
    else:
        root = ET.Element("unload")
        root.set("unload_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for i in range(1, num_records + 1):
            record = generate_xml_record(i)
            root.append(record)
        xml_data = ET.tostring(root, encoding="utf-8").decode("utf-8")
        st.code(xml_data, language="xml")
        st.download_button(
            label="Download XML",
            data=xml_data,
            file_name="samp_eng_app_denial.xml",
            mime="application/xml"
        )
