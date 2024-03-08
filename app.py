import datetime
import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("MONGODB_CLIENT")

client = MongoClient(url)
db = client["CampusGuard"]  # Replace with your database name
collection = db["UserReports"]  # Replace with your collection name



# Incident type options
incident_types = ["Mobile Phone", "No Helmet", "Sleeping", "Triples", "Violence"]
places = ["Kalaiarangam","ECE Department","Chemical Engineering Department","Department of Biomedical Engineering","Imperial Hall Entrance","ATM","1st Year Block Entrance","Mario Juicy","UCC and Mathampatty Pakashala","Gym Entrance","Hostel Entrance","Ganesh Cafe","Just Print","Pond","Admin Block Entrance 1","Admin Block Entrance 2","OAT Entrance","Royal Kitchen","Bosch Lab","CSE Department Entrance","Sangamam Club House","Civil Block Entrance","Car Parking","Dining Hall","Bike Parking","Ground Turning 1","Library","Coffee House","1st Year Mario","E-Gate","Staff Car Parking","Water Purifier","2nd Year AD Classroom","HOD Office","3rd AD Year Class","Steps","Round Table","4th AD Year Class","AI Lab","Staff Room","Admin Block","Principal Office","S&H Block Entrance"]
# st.title("Incident Reporting App")
# st.markdown("<h1 style='text-align: center; font-size: 2.9em;'>Your writing, Expertly Crafted</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>Campus <span style='color: green;'>Guard</span></h1>", unsafe_allow_html=True)

with st.sidebar:
   
    # st.image("image-removebg-preview.png",width=220)
    st.markdown("<h1 style='text-align: center; font-size: 2.3em;'><span style='color: green;'><span style='font-weight:bold;'>K</span>PR</span> <span style='font-weight:bold;color: green;'>I</span>nstitute of <span style='color: green;'>E</span>ngineering and <span style='font-weight:bold;color: green;'>T</span>echnology</h1>", unsafe_allow_html=True)
    # st.markdown("Introducing CampusGuard: Your go-to web app for reporting campus incidents. Developed by students at KPR Institute of Engineering and Technology, CampusGuard allows users to quickly report concerns like violence, ragging, and unauthorized activities. Join us in fostering a safer campus environment today.")
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
    

# File upload section
# uploaded_file = st.file_uploader("**Upload Image or Video**", type=["jpg", "jpeg", "png", "mp4","multiple"])
uploaded_files= st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4"], accept_multiple_files=True)



# Location input section
location = st.selectbox("**Incident Location**",places)

# Incident type selection section
selected_type = st.selectbox("**Incident Type**", incident_types)

# Submit button
submit_button = st.button("**Submit Report**")

if submit_button:
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # Read the uploaded file content
            file_bytes = uploaded_file.read()

            # Create a dictionary for each file
            incident_data = {
                "file_content": file_bytes,
                "file_type": uploaded_file.type,
                "location": location,
                "incident_type": selected_type,
                "timestamp": datetime.datetime.now()
            }

            # Insert data into MongoDB collection
            collection.insert_one(incident_data)

        st.success("Incident reports submitted successfully!")
    else:
        st.error("Please upload at least one image or video.")