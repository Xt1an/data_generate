import streamlit as st
import xml.etree.ElementTree as ET
import random
import hashlib
from datetime import datetime
import pandas as pd

def load_data_from_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading CSV file: {e}")
        return []


# Usage:
USER_NAMES = load_data_from_csv("user.csv")
DISCOVERY_MODELS = load_data_from_csv("discovery.csv")
GROUP_NAMES = load_data_from_csv("group.csv")




if not USER_NAMES:
    st.error("No user names found. Ensure the 'user.csv' file exists and contains valid data.")
if not DISCOVERY_MODELS:
    st.error("No discovery models found. Ensure the 'discovery.csv' file exists and contains valid data.")
if not GROUP_NAMES:
    st.error("No group names found. Ensure the 'group.csv' file exists and contains valid data.")

# Other Fixed Values

CON_USAGE_ID_TEMPLATE = "Con Usage {}"

def generate_unique_hash():
    """Generates a unique hash value to ensure each XML field requiring a hash is unique and randomized."""
    return hashlib.md5(str(random.random()).encode()).hexdigest()

def generate_xml_record(denial_num):
    
    #randomly select from csv files
    discovery = random.choice(DISCOVERY_MODELS)


 # Create the <samp_eng_app_concurrent_usage> element with "INSERT_OR_UPDATE" action
    concurrent_usage = ET.Element("samp_eng_app_concurrent_usage", action="INSERT_OR_UPDATE")
    ET.SubElement(concurrent_usage, "conc_usage_id").text = CON_USAGE_ID_TEMPLATE.format(denial_num + 100)
    ET.SubElement(concurrent_usage, "concurrent_usage").text = str(random.randint(1, 100))
    ET.SubElement(concurrent_usage, "license", display_value=discovery["norm_product"]).text = discovery["license_sys_id"]
    ET.SubElement(concurrent_usage, "source").text = "OpeniT"
    ET.SubElement(concurrent_usage, "sys_created_by").text = "admin"
    ET.SubElement(concurrent_usage, "sys_created_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(concurrent_usage, "sys_domain").text = generate_unique_hash()
    ET.SubElement(concurrent_usage, "sys_domain_path").text = "/"
    ET.SubElement(concurrent_usage, "sys_id").text = generate_unique_hash()
    ET.SubElement(concurrent_usage, "sys_mod_count").text = str(random.randint(1, 100))
    ET.SubElement(concurrent_usage, "sys_updated_by").text = "admin"
    ET.SubElement(concurrent_usage, "sys_updated_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(concurrent_usage, "usage_date").text = datetime.now().strftime("%Y-%m-%d")
    return concurrent_usage

st.title("XML Record Generator for samp_eng_app_concurrent_usage.xml")

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
            file_name="samp_eng_app_concurrent_usage.xml",
            mime="application/xml"
        )
