import streamlit as st
import requests
from streamlit_chat import message  # Import to create chat-style interface

# Title for the application
st.title("Chat w/Barry Snipes")

# Instructions or description for the user
st.write("Send your sports betting questions to Barry below. The more specific you are regarding sport or player, the better.")

# Backend API URL (no change)
backend_url = 'https://backend-api-dot-barrysnipes.uc.r.appspot.com'

# Initialize chat history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to add user input and bot response to the chat history
def add_to_history(user_input, ai_response):
    st.session_state['history'].append({"user": user_input, "bot": ai_response})

# Function to display the chat history with auto-scrolling behavior
def display_chat_history():
    for chat in st.session_state['history']:
        message(chat["user"], is_user=True)  # Display user message
        message(chat["bot"])  # Display bot response

# Test backend connectivity on initial page load
try:
    response = requests.get(backend_url)
    if response.status_code == 200:
        st.write("Backend API is reachable!")
    else:
        st.write(f"Backend API error: {response.status_code}")
except Exception as e:
    st.write(f"Error reaching backend: {e}")

# Create a text input box for the user to type their inquiry
user_input = st.text_input("Type your question here:")

# Create an empty placeholder for showing the chat history
chat_placeholder = st.empty()

# Add a button to send the user's input to the backend
send_button = st.button("Send")

if send_button and user_input:
    # Disable the send button while processing the request
    with st.spinner("Processing..."):
        # Send the input to the backend API
        try:
            response = requests.post(f'{backend_url}/interact', json={'input': user_input})
            
            # Check if the request was successful
            if response.status_code == 200:
                # Display the AI's response from the backend
                ai_response = response.json().get("response", "No response received from the AI")
                add_to_history(user_input, ai_response)
            else:
                # Handle backend error responses
                st.write(f"Error: Backend returned status code {response.status_code}")
        except Exception as e:
            # Handle exceptions like network issues
            st.write(f"Error connecting to backend: {e}")

# Display chat history with auto-scrolling behavior
with chat_placeholder:
    display_chat_history()

# Clear the input box after sending
if send_button:
    st.session_state["input"] = ""

