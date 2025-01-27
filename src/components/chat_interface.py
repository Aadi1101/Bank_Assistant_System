import sys
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from src.components.prompts import BankAssistantPrompts
from src.logger import logging
from src.exception import CustomException

class BankAssistant:
    def __init__(self):
        try:
            logging.info("Successfully initialized the session and all the prompts")
            self.initialize_session()
            self.bank_assistant = BankAssistantPrompts()
        except Exception as e:
            raise CustomException(e,sys)

    def initialize_session(self):
        try:
            logging.info("Initializing Chat History for the session")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    AIMessage(
                        content="""
                            Welcome to your personalized Bank Assistant!\n
                            I'm here to provide you with seamless, secure, and tailored support for all your financial needs. Whether it's checking balances, managing transactions, exploring loan options, or receiving smart investment recommendations, I've got you covered.
                            How can I assist you today?"
                        """
                    )
                ]
            return st.session_state.chat_history
        except Exception as e:
            raise CustomException(e,sys)
    
    def handle_user_message(self,user_query,user_id=None):
        try:
            logging.info("Handling the user query passed by the user")
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
        except Exception as e:
            raise CustomException(e,sys)
    
    def display_chat_history(self):
        try:
            logging.info("Displaying the Messages...")
            for message in st.session_state.chat_history:
                if isinstance(message,AIMessage):
                    with st.chat_message("AI"):
                        st.write(message.content)
                elif isinstance(message,HumanMessage):
                    with st.chat_message("Human"):
                        st.write(message.content)
        except Exception as e:
            raise CustomException(e,sys)
    
    def run(self,user_id=None):
        try:
            logging.info("Running the Chat Interface")
            self.display_chat_history()
            user_query = st.chat_input("Type your message here...")
            if user_query:
                st.session_state.chat_history.append(HumanMessage(content=user_query))
                if user_id == None:
                    self.handle_user_message(user_query=user_query)
                else:
                    self.handle_user_message(user_query=user_query,user_id=user_id)
        except Exception as e:
            raise CustomException(e,sys)