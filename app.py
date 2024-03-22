import datetime
import os
import streamlit as st
from pymongo import MongoClient
from streamlit_webrtc import webrtc_streamer
import av
from PIL import Image
from moviepy.editor import ImageSequenceClip
from validator_deploy import DataValidator
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Create a temporary directory to store uploaded files
temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = temp_dir.name

MONGO_URL = os.getenv("MONGO_URL")

def save_uploaded_files(uploaded_files):
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        # if file_extension == "mp4":
        #     continue

        with open(os.path.join(temp_dir_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())




if 'validator' not in st.session_state:
    st.session_state.validator = DataValidator()

# MongoDB Atlas connection details (replace with your actual credentials)
client = MongoClient(f"mongodb+srv://shieldinnovsense:{MONGO_URL}")
db = client["CampusGuard"]  # Replace with your database name
collection = db["UserReports3"]  # Replace with your collection name

# Incident type options
incident_types = ["Mobile Phone", "No Helmet", "Sleeping", "Triples", "Violence"]
places = ["Kalaiarangam", "ECE Department", "Chemical Engineering Department", "Department of Biomedical Engineering",
          "Imperial Hall Entrance", "ATM", "1st Year Block Entrance", "Mario Juicy", "UCC and Mathampatty Pakashala",
          "Gym Entrance", "Hostel Entrance", "Ganesh Cafe", "Just Print", "Pond", "Admin Block Entrance 1",
          "Admin Block Entrance 2", "OAT Entrance", "Royal Kitchen", "Bosch Lab", "CSE Department Entrance",
          "Sangamam Club House", "Civil Block Entrance", "Car Parking", "Dining Hall", "Bike Parking",
          "Ground Turning 1", "Library", "Coffee House", "1st Year Mario", "E-Gate", "Staff Car Parking",
          "Water Purifier", "2nd Year AD Classroom", "HOD Office", "3rd AD Year Class", "Steps", "Round Table",
          "4th AD Year Class", "AI Lab", "Staff Room", "Admin Block", "Principal Office", "S&H Block Entrance"]

st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>Campus <span style='color: green;'>Guard</span></h1>",
            unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 20px;">
             <h2 style="font-weight: bold; color: #008000;"> <span style="color: white;">Introducing Campus</span> Guard:</h2>
            <p style="font-weight: bold;">Your go-to web app for reporting campus incidents.</p>
            <p style="font-weight: bold;">Developed by students at <span style="color: #008000;">KPR Institute of Engineering and Technology</span>,</p>
            <p style="font-weight: bold;">CampusGuard allows users to quickly report concerns like violence, ragging, and unauthorized activities.</p>
            <p style="font-weight: bold;">Join us in fostering a safer campus environment today.</p>
             <p style="font-weight: bold;">In CampusGuard, the identity of individuals reporting incidents will remain confidential to protect their privacy.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Choose between file upload and camera
# upload_option = st.radio("Choose option:", ("Upload from Local Device", "Capture from Camera"))

uploaded_files = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4"],
                                      accept_multiple_files=True)


# Location input section
location = st.selectbox("Incident Location", places)

# Incident type selection section
selected_type = st.selectbox("Incident Type", incident_types)

# Submit button
submit_button = st.button("Submit Report")

if submit_button:
        if uploaded_files is not None:
            save_uploaded_files(uploaded_files)
            incident_data = []  # Initialize incident_data list
            try:
                for uploaded_file in uploaded_files:

                    path = os.path.join(temp_dir_path, uploaded_file.name)

                    res = st.session_state.validator.validate(path, selected_type)
                    if not res:
                        continue

                    with open(path, "rb") as f:
                        file_bytes = f.read()

                    # Create a dictionary for each file
                    incident_data.append({
                        "file_content": file_bytes,
                        "file_type": uploaded_file.type
                    })
                    # print(incident_data)

                if incident_data:
                    # Insert data into MongoDB collection with incident_data containing all images
                    collection.insert_one({
                        "incident_data": incident_data,
                        "location": location,
                        "incident_type": selected_type,
                        "timestamp": datetime.datetime.now()
                    })

                    st.success("Incident reports submitted successfully!")
                else:
                    st.warning("No Data to Upload")

                temp_dir.cleanup()

            except Exception as e:
                st.warning(f"Error occurred while uploading files. {e}")
        else:
            st.error("Please upload at least one image or video.")
