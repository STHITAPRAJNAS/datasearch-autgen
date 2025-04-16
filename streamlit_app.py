import streamlit as st
import requests
import json

# Streamlit App
st.title("Intelligent Chatbot")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store LLM generated responses
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
if prompt := st.chat_input("Enter your message here"):  # Input box
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to FastAPI endpoint
    url = "http://localhost:8000/chat"
    headers = {"Content-Type": "application/json"}
    params = {"user_id": "test_user", "conversation_id": "test_conversation"}

    try:
        response = requests.post(url, params=params, json={"message": prompt})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Display response
        response_content = response.json()
        bot_message = f"{response_content}"
        st.session_state.messages.append({"role": "assistant", "content": bot_message})
        with st.chat_message("assistant"):
            st.markdown(bot_message)

    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Request Error: {err}")
    except json.JSONDecodeError as json_err:
        st.error(f"JSON Decode Error: {json_err}")
    except Exception as e:
      st.error(f"Error: {e}")