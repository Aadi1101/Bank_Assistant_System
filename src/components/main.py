import os
import sys
import streamlit as st
from src.components.authentication import authenticate
from src.components.chat_interface import BankAssistant
from src.utils import get_user_id
from dotenv import load_dotenv
from src.logger import logging
from src.exception import CustomException
load_dotenv()
USER_ROLE = os.getenv('USER_ROLE')
st.set_page_config(page_title="Bank Assistant")
st.title("Bank Assistant")

try:
    authenticator = authenticate()
    authenticator.login()
except Exception as e:
    st.error(e)

try:
    if st.session_state['authentication_status']:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["username"]}*')
        if st.session_state["roles"][0] == USER_ROLE:
            user_id = get_user_id(username=st.session_state["username"])
            logging.info(f"User {user_id} is attempting to log in.")
            app = BankAssistant()
            app.run(user_id=user_id)
        else:
            app = BankAssistant()
            app.run()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
except Exception as e:
    raise CustomException(e,sys)
