import streamlit as st
import xml.etree.ElementTree as ET
import random
import hashlib
from datetime import datetime, timedelta
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


if not USER_NAMES:
    st.error("No user names found. Ensure the 'user.csv' file exists and contains valid data.")
if not DISCOVERY_MODELS:
    st.error("No discovery models found. Ensure the 'discovery.csv' file exists and contains valid data.")


def generate_unique_hash():
    """Generates a unique hash value to ensure each XML field requiring a hash is unique and randomized."""
    return hashlib.md5(str(random.random()).encode()).hexdigest()


def generate_durations_small_range():
    """
    Generate random durations for idle and session within specified small ranges.

    Returns:
        tuple: Idle and session durations as strings in 'HH:MM:SS' format.
    """
    idle_duration = timedelta(seconds=random.randint(30, 60))  # 30 seconds to 1 minute
    session_duration = timedelta(minutes=random.randint(1, 15))  # 1 to 15 minutes
    return idle_duration, session_duration


def generate_xml_record(usage_summary_num, base_date):
    # Randomly select from csv files
    users = random.choice(USER_NAMES)
    discovery = random.choice(DISCOVERY_MODELS)

    # Generate durations
    idle_duration, session_duration = generate_durations_small_range()

    # Offset the base date with the idle and session durations
    total_idle_duration = (base_date + idle_duration).strftime("%Y-%m-%d %H:%M:%S")
    total_sess_duration = (base_date + session_duration).strftime("%Y-%m-%d %H:%M:%S")

    # Create the <samp_eng_app_usage_summary> element with "INSERT_OR_UPDATE" action
    usage_summary = ET.Element("samp_eng_app_usage_summary", action="INSERT_OR_UPDATE")
    ET.SubElement(usage_summary, "norm_product", display_value=discovery["norm_product"]).text = discovery["norm_product_sys_id"]
    ET.SubElement(usage_summary, "norm_publisher", display_value=discovery["norm_publisher"]).text = discovery["norm_publisher_sys_id"]
    ET.SubElement(usage_summary, "reporting_version").text = "v1"
    ET.SubElement(usage_summary, "source").text = "OpeniT"
    ET.SubElement(usage_summary, "sys_created_by").text = "admin"
    ET.SubElement(usage_summary, "sys_created_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(usage_summary, "sys_domain").text = generate_unique_hash()
    ET.SubElement(usage_summary, "sys_domain_path").text = "/"
    ET.SubElement(usage_summary, "sys_id").text = generate_unique_hash()
    ET.SubElement(usage_summary, "sys_mod_count").text = str(random.randint(1, 100))
    ET.SubElement(usage_summary, "sys_updated_by").text = "admin"
    ET.SubElement(usage_summary, "sys_updated_on").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(usage_summary, "total_idle_duration").text = total_idle_duration
    ET.SubElement(usage_summary, "total_sess_duration").text = total_sess_duration
    ET.SubElement(usage_summary, "usage_date").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(usage_summary, "user", display_value=users["user"]).text = users["user_sys_id"]
    return usage_summary


st.title("XML Record Generator for samp_eng_app_usage_summary.xml")

num_records_input = st.text_input("Enter the number of records to generate", value="")

if num_records_input.isdigit():
    num_records = int(num_records_input)
else:
    num_records = 0

# Base date for the records
base_date = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

if st.button("Generate XML"):
    if num_records <= 0:
        st.error("Please enter a valid number greater than 0.")
    else:
        root = ET.Element("unload")
        root.set("unload_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for i in range(1, num_records + 1):
            record = generate_xml_record(i, base_date)
            root.append(record)
        xml_data = ET.tostring(root, encoding="utf-8").decode("utf-8")
        st.code(xml_data, language="xml")
        st.download_button(
            label="Download XML",
            data=xml_data,
            file_name="samp_eng_app_usage_summary.xml",
            mime="application/xml"
        )
