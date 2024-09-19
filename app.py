import streamlit as st
import requests
from streamlit_chat import message

# Title for the application
st.title("Chat w/Barry Snipes")

# Backend API URL
backend_url = 'https://backend-api-dot-barrysnipes.uc.r.appspot.com'

# Test backend connectivity
try:
    response = requests.get(backend_url)
    if response.status_code == 200:
        st.write("Backend API is reachable!")
    else:
        st.write(f"Backend API error: {response.status_code}")
except Exception as e:
    st.write(f"Error reaching backend: {e}")

# Chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input function
def get_input():
    return st.text_input("Type your question here:", disabled=st.session_state.get('is_locked', False))

# Display chat history
def display_chat():
    for i, chat in enumerate(st.session_state['chat_history']):
        message(chat['user'], is_user=True, key=f'user_{i}', avatar_style=None, background_color="#ADD8E6")
        message(chat['bot'], is_user=False, key=f'bot_{i}', avatar_style=None, background_color="#D3D3D3")

# Send message to backend and display response
def send_message(user_input):
    if user_input:
        st.session_state.is_locked = True
        try:
            with st.spinner("Processing..."):
                response = requests.post(f'{backend_url}/interact', json={'input': user_input})
                if response.status_code == 200:
                    ai_response = response.json().get("response", "No response received from the AI")
                    st.session_state.chat_history.append({'user': user_input, 'bot': ai_response})
                    st.session_state.is_locked = False
                else:
                    st.write(f"Error: Backend returned status code {response.status_code}")
                    st.session_state.is_locked = False
        except Exception as e:
            st.write(f"Error connecting to backend: {e}")
            st.session_state.is_locked = False

# Display chat messages
display_chat()

# User input box at the bottom
user_input = get_input()

# Send button
if st.button("Send") and not st.session_state.get('is_locked', False):
    send_message(user_input)
    st.session_state['user_input'] = ""  # Clear input box
