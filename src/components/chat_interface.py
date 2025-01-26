import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from src.components.prompts import BankAssistantPrompts

class BankAssistant:
    def __init__(self):
        self.initialize_session()
        self.bank_assistant = BankAssistantPrompts()

    def initialize_session(self):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(
                    content="""
                        Hello! I am a Bank Assistant. How may I help you?
                    """
                )
            ]
        return st.session_state.chat_history
    
    def handle_user_message(self,user_query,user_id=None):
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            with st.spinner("Generating response..."):
                try:
                    response = None
                    if user_id is None:
                        response = self.bank_assistant.handle_user_query(user_query=user_query)
                    else:
                        response = self.bank_assistant.handle_user_query(user_query=user_query,user_id=user_id)
                    st.write(response)
                    st.session_state.chat_history.append(AIMessage(content=response))
                except Exception as e:
                    st.error(f"Error generating response: {e}")
    
    def display_chat_history(self):
        for message in st.session_state.chat_history:
            if isinstance(message,AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message,HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)
    
    def run(self,user_id=None):
        self.display_chat_history()
        user_query = st.chat_input("Type your message here...")
        if user_query:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            if user_id == None:
                self.handle_user_message(user_query=user_query)
            else:
                self.handle_user_message(user_query=user_query,user_id=user_id)