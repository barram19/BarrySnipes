import streamlit as st
import requests
from streamlit_chat import message  # Using streamlit-chat for chat UI

# Title for the application
st.title("Chat w/Barry Snipes")

# Instructions or description for the user
st.write("Send your sports betting questions to Barry below. The more specific you are regarding sport or player, the better.")

# Backend API URL (no change)
backend_url = 'https://backend-api-dot-barrysnipes.uc.r.appspot.com'

# Test backend connectivity on initial page load
try:
    response = requests.get(backend_url)
    if response.status_code == 200:
        st.write("Backend API is reachable!")
    else:
        st.write(f"Backend API error: {response.status_code}")
except Exception as e:
    st.write(f"Error reaching backend: {e}")

# Chat message history stored in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input
def get_input():
    return st.text_input("Type your question here:", disabled=st.session_state.get('is_locked', False))

# Add new messages to chat history
def add_to_history(user_message, bot_response):
    st.session_state.chat_history.append({'user': user_message, 'bot': bot_response})

# Display chat conversation
def display_chat():
    for i, chat in enumerate(st.session_state['chat_history']):
        message(chat['user'], is_user=True, key=f'user_{i}', avatar_style=None, background_color="#ADD8E6")
        message(chat['bot'], is_user=False, key=f'bot_{i}', avatar_style=None, background_color="#D3D3D3")

# Main function to handle user input and send to backend
def send_message(user_input):
    if user_input:
        # Lock the input box while processing
        st.session_state.is_locked = True
        
        # Send the input to the backend API
        try:
            with st.spinner("Processing..."):
                response = requests.post(f'{backend_url}/interact', json={'input': user_input})
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Display the AI's response from the backend
                    ai_response = response.json().get("response", "No response received from the AI")
                    
                    # Add user and bot responses to the chat history
                    add_to_history(user_input, ai_response)
                    
                    # Unlock the input box after receiving a response
                    st.session_state.is_locked = False
                else:
                    # Handle backend error responses
                    st.write(f"Error: Backend returned status code {response.status_code}")
                    st.session_state.is_locked = False

        except Exception as e:
            # Handle exceptions like network issues
            st.write(f"Error connecting to backend: {e}")
            st.session_state.is_locked = False

# Display the chat messages
display_chat()

# User input box at the bottom
user_input = get_input()

# Send button to send the message
if st.button("Send") and not st.session_state.get('is_locked', False):
    send_message(user_input)

    # Clear the input box after submission
    st.session_state['user_input'] = ""
