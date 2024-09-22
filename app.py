import streamlit as st
import time
import requests
from streamlit_chat import message  # Import to create chat-style interface

# Title for the application
st.title("Chat w/Barry Snipes")

# Instructions or description for the user
st.write("Send your sports betting questions to Barry below. The more specific you are regarding sport or player, the better.")

# Backend API URL
backend_url = 'https://backend-api-dot-barrysnipes.uc.r.appspot.com'

# Initialize chat history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to add user input and bot response to the chat history
def add_to_history(user_input, ai_response):
    st.session_state['history'].append({"user": user_input, "bot": ai_response})

# Function to display the chat history
def display_chat_history():
    for chat in st.session_state['history']:
        message(chat["user"], is_user=True)  # Display user message with user=True
        message(chat["bot"],  seed="bot_message")  # Display bot response

# Create a placeholder for the chat history (to ensure it's above the input box)
chat_placeholder = st.container()

# Input box at the bottom of the page
user_input = st.text_input("Type your question here:", key="input_box")

# Add a button to send the user's input to the backend
send_button = st.button("Send")

# Create a placeholder for dynamic status messages
status_placeholder = st.empty()

# Processing the user input when the send button is clicked
if send_button and user_input:
    # Disable the send button while processing the request
    try:
        # Start with the initial status message
        status_placeholder.text("Crunching the latest numbers... results are coming!")
        
        # Start the request and time tracking
        start_time = time.time()

        # Send the input to the backend API
        response = requests.post(f'{backend_url}/interact', json={'input': user_input})
        
        # If the processing takes longer than 10 seconds, change the message
        while response.status_code == None and (time.time() - start_time) < 10:
            time.sleep(1)  # Wait for 1 second and then check if it took more than 10 seconds
        
        if (time.time() - start_time) > 10:
            status_placeholder.text("Analyzing every angle... nearly there!")

        # Check if the request was successful
        if response.status_code == 200:
            # Get the AI's response from the backend
            ai_response = response.json().get("response", "No response received from the AI")
            
            # Add the user input and bot response to the chat history
            add_to_history(user_input, ai_response)
        else:
            # Handle backend error responses
            status_placeholder.write(f"Error: Backend returned status code {response.status_code}")
    except Exception as e:
        # Handle exceptions like network issues
        status_placeholder.write(f"Error connecting to backend: {e}")
    
    # Clear the status message after completion
    status_placeholder.empty()

# Display chat history with auto-scrolling behavior
with chat_placeholder:
    display_chat_history()
