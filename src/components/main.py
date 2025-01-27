import os
import streamlit as st
from src.components.authentication import authenticate
from src.components.chat_interface import BankAssistant
from src.utils import get_user_id
from dotenv import load_dotenv
load_dotenv()
USER_ROLE = os.getenv('USER_ROLE')
st.set_page_config(page_title="Bank Assistant")
st.title("Bank Assistant")

try:
    authenticator = authenticate()
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["username"]}*')
    if st.session_state["roles"][0] == USER_ROLE:
        user_id = get_user_id(username=st.session_state["username"])
        app = BankAssistant()
        app.run(user_id=user_id)
    else:
        app = BankAssistant()
        app.run()
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
