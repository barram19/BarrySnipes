import streamlit as st
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
        message(chat["user"], is_user=True, avatar_style=" ", seed="user_message")  # Display user message with user=True
        message(chat["bot"], avatar_style=" ", seed="bot_message")  # Display bot response

# Create a placeholder for the chat history (to ensure it's above the input box)
chat_placeholder = st.container()

# Input box at the bottom of the page
user_input = st.text_input("Type your question here:", key="input_box")

# Add a button to send the user's input to the backend
send_button = st.button("Send")

# Processing the user input when the send button is clicked
if send_button and user_input:
    # Disable the send button while processing the request
    with st.spinner("Processing..."):
        # Send the input to the backend API
        try:
            response = requests.post(f'{backend_url}/interact', json={'input': user_input})
            
            # Check if the request was successful
            if response.status_code == 200:
                # Get the AI's response from the backend
                ai_response = response.json().get("response", "No response received from the AI")
                
                # Add the user input and bot response to the chat history
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
