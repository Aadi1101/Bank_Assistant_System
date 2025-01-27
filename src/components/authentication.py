import sys
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from src.logger import logging
from src.exception import CustomException

def authenticate():
    try:
        logging.info("Accessing Configuration file")
        with open('data\config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Pre-hashing all plain text passwords once
        # stauth.Hasher.hash_passwords(config['credentials'])

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        logging.info("Successfully authenticated the user.")
        return authenticator
    except Exception as e:
        raise CustomException(e,sys)