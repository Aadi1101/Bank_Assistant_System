from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.utils import query_database
import os
import sys
from src.exception import CustomException
from src.logger import logging


MESSAGES = os.getenv('MESSAGES')
LLM_MODEL = os.getenv('LLM_MODEL')
SQL_QUERY_FORMATTER = os.getenv('SQL_QUERY_FORMATTER')
SQL_QUERY_VALIDATOR = os.getenv('SQL_QUERY_VALIDATOR')
GENERAL_QUERY = os.getenv('GENERAL_QUERY')
USER_QUERY_TO_SQL=os.getenv('USER_QUERY_TO_SQL')
USER_BASE_QUERY = os.getenv('USER_BASE_QUERY')
ADMIN_QUERY_TO_SQL = os.getenv('ADMIN_QUERY_TO_SQL')
ADMIN_BASE_QUERY = os.getenv('ADMIN_BASE_QUERY')

class BankAssistantPrompts:
    def __init__(self):
        try:
            logging.info("Initializing the LLM")
            self.llm = ChatGroq(model=LLM_MODEL)
        except Exception as e:
            raise CustomException(e,sys)

    def handle_user_query(self,user_query,user_id=None):
        try:
            logging.info("Check whether the query is for local search or global search")
            if user_id is None:
                logging.info("Base Query for Admin")
                base_query = ADMIN_BASE_QUERY
            else:
                logging.info("Base Query for Customers")
                base_query = USER_BASE_QUERY
                base_query = base_query.format(user_id=user_id)
            base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
            base_query_interaction = base_prompt | self.llm
            result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
            response = self.choose_action(user_query=user_query,bool_response=result,user_id=user_id)
            return response
        except Exception as e:
            raise CustomException(e,sys)
    
    def general_query(self,user_query):
        try:
            logging.info("Global Search Started...")
            base_query = GENERAL_QUERY
            base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
            base_query_interaction = base_prompt | self.llm
            result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
            return result
        except Exception as e:
            raise CustomException(e,sys)
    
    def choose_action(self,user_query,bool_response:str,user_id=None):
        try:
            if user_id is None:
                logging.info("Action set for Admins - Whether to go for Global search or Local search")
                if bool_response.__contains__('TRUE') or bool_response.__contains__('true'):
                    sql_result = self.query_to_sql(user_query)
                    result = self.sql_query_validator(sql_query=sql_result)
                elif bool_response.__contains__('FALSE') or bool_response.__contains__('false'):
                    result = self.general_query(user_query)
            else:
                logging.info("Action set for Users - Whether to go for Global search or Local search")
                if bool_response.__contains__('TRUE') or bool_response.__contains__('true'):
                    sql_result = self.query_to_sql(user_query,user_id)
                    result = self.sql_query_validator(sql_query=sql_result)
                elif bool_response.__contains__('FALSE') or bool_response.__contains__('false'):
                    result = self.general_query(user_query)
            return result
        except Exception as e:
            raise CustomException(e,sys)
    
    def query_to_sql(self,user_query,user_id=None):
        try:
            if user_id is None:
                logging.info("Admin querying to database")
                base_query = ADMIN_QUERY_TO_SQL
            else:
                logging.info("Users querying to database")
                base_query = USER_QUERY_TO_SQL
                base_query = base_query.format(user_id=user_id)
            base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
            base_query_interaction = base_prompt | self.llm
            result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
            return result
        except Exception as e:
            raise CustomException(e,sys)
    
    def sql_query_validator(self,sql_query):
        try:
            logging.info("Validating the database query...")
            base_query = SQL_QUERY_VALIDATOR
            base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
            base_query_interaction = base_prompt | self.llm
            result = base_query_interaction.invoke({"messages":[("user",sql_query)]}).content
            response = self.sql_action(sql_query=sql_query,bool_response=result)
            return response
        except Exception as e:
            raise CustomException(e,sys)
    
    def sql_action(self,sql_query:str,bool_response:str):
        try:
            logging.info("Based on Query Validation choosing the database action")
            if bool_response.__contains__('VALID') or bool_response.__contains__('valid'):
                if sql_query.__contains__('`'):
                    sql_query = sql_query.replace('`','')
                sql_result = query_database(sql_query=sql_query)
                result = self.result_formatter(sql_result=sql_result)
            elif bool_response.__contains__('INVALID') or bool_response.__contains__('invalid'):
                result = 'Rewrite the query please'
            return result
        except Exception as e:
            raise CustomException(e,sys)
    
    def result_formatter(self,sql_result):
        try:
            logging.info("Formatting the result received from the database.")
            base_query = SQL_QUERY_FORMATTER
            base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
            base_query_interaction = base_prompt | self.llm
            result = base_query_interaction.invoke({"messages":[("user",sql_result)]}).content
            return result
        except Exception as e:
            raise CustomException(e,sys)