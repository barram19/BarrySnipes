import streamlit as st
import requests

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

# Create a text input box for the user to type their inquiry
user_input = st.text_input("Type your question here:")

# Add a button to send the user's input to the backend
if st.button("Send"):
    if user_input:
        # Send the input to the backend API
        try:
            response = requests.post(f'{backend_url}/interact', json={'input': user_input})
            
            # Check if the request was successful
            if response.status_code == 200:
                # Display the AI's response from the backend
                ai_response = response.json().get("response", "No response received from the AI")
                st.write("AI Response: ", ai_response)
            else:
                # Handle backend error responses
                st.write(f"Error: Backend returned status code {response.status_code}")
        except Exception as e:
            # Handle exceptions like network issues
            st.write(f"Error connecting to backend: {e}")
    else:
        # If the user hasn't entered any input
        st.write("Please type a question to get a response.")
