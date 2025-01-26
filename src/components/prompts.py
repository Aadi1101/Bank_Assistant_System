from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.utils import query_database
import os
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
        self.llm = ChatGroq(model=LLM_MODEL)

    def handle_user_query(self,user_query,user_id=None):
        if user_id is None:
            base_query = ADMIN_BASE_QUERY
        else:
            base_query = USER_BASE_QUERY
            base_query = base_query.format(user_id=user_id)
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
        response = self.choose_action(user_query=user_query,bool_response=result,user_id=user_id)
        return response
    
    def general_query(self,user_query):
        base_query = GENERAL_QUERY
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
        return result
    
    def choose_action(self,user_query,bool_response:str,user_id=None):
        if user_id is None:
            if bool_response.__contains__('TRUE') or bool_response.__contains__('true'):
                sql_result = self.query_to_sql(user_query)
                result = self.sql_query_validator(sql_query=sql_result)
            elif bool_response.__contains__('FALSE') or bool_response.__contains__('false'):
                result = self.general_query(user_query)
        else:
            if bool_response.__contains__('TRUE') or bool_response.__contains__('true'):
                sql_result = self.query_to_sql(user_query,user_id)
                result = self.sql_query_validator(sql_query=sql_result)
            elif bool_response.__contains__('FALSE') or bool_response.__contains__('false'):
                result = self.general_query(user_query)
        return result
    
    def query_to_sql(self,user_query,user_id=None):
        if user_id is None:
            base_query = ADMIN_QUERY_TO_SQL
        else:
            base_query = USER_QUERY_TO_SQL
            base_query = base_query.format(user_id=user_id)
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
        return result
    
    def sql_query_validator(self,sql_query):
        base_query = SQL_QUERY_VALIDATOR
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",sql_query)]}).content
        response = self.sql_action(sql_query=sql_query,bool_response=result)
        return response
    
    def sql_action(self,sql_query:str,bool_response:str):
        if bool_response.__contains__('VALID') or bool_response.__contains__('valid'):
            if sql_query.__contains__('`'):
                sql_query = sql_query.replace('`','')
            sql_result = query_database(sql_query=sql_query)
            result = self.result_formatter(sql_result=sql_result)
        elif bool_response.__contains__('INVALID') or bool_response.__contains__('invalid'):
            result = 'Rewrite the query please'
        return result
    
    def result_formatter(self,sql_result):
        base_query = SQL_QUERY_FORMATTER
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",sql_result)]}).content
        return result