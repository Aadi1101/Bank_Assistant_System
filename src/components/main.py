import streamlit as st
from src.components.authentication import authenticate
from src.components.chat_interface import BankAssistant
from src.utils import get_user_id
st.set_page_config(page_title="Bank Assistant")

try:
    authenticator = authenticate()
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["username"]}*')
    if st.session_state["roles"][0] == 'viewer':
        user_id = get_user_id(username=st.session_state["username"])
        st.write(f'UserId of *{st.session_state["name"]}* is {user_id}')
        app = BankAssistant()
        app.run(user_id=user_id)
    else:
        app = BankAssistant()
        app.run()
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
