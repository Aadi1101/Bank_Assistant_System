# Bank Assistant System

This project is a banking assistant system built using Streamlit, Langchain, and MySQL. It provides a personalized, intelligent assistant for users of a Bank Management System (BMS). The assistant helps with user-specific queries such as transaction history, account balance, loan eligibility, and more. The assistant communicates in natural language and can handle a variety of banking-related requests.

## Features

- **User Authentication**: Streamlit user authentication for secure access.
- **Database Integration**: Fetches user-specific data from a MySQL database.
- **AI-Powered Chat**: Langchain integration for AI-driven responses.
- **Multilingual Support**: Supports multilingual queries.
- **Financial Assistance**: Provides help with transactions, loans, investments, and other banking-related activities.

## Project Structure

```plaintext
.
├── data
│   └── config.yaml           # Contains configuration for authentication and cookies
├── src
│   ├── components
│   │   ├── authentication.py # Authentication logic
│   │   ├── chat_interface.py # Chat interface and message handling
│   │   ├── prompts.py        # Contains AI prompt logic and query generation
│   ├── utils.py              # Utility functions (e.g., fetching user ID)
│   └── main.py               # Main entry point to run the app
├── .env                      # Environment variables (database credentials, secret keys)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── app.py                    # Entry script for the Streamlit app
```

## Setup

1. **Install dependencies**:

    You can install the required libraries by running:

    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**:

    Set up your `.env` file to include the following variables:

    ```env
    DB_HOST=your_database_host
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_NAME=your_database_name
    PROMPTS= prompts
    ```

3. **Database**:

    Ensure that your MySQL database schema is set up according to the required tables (`Users`, `UserDetails`, `Transactions`, `Savings`, `Loans`, `Investments`, `Donations`, `BlockedAccounts`, `UserTotalBalance`).

4. **Running the App**:

    To run the app, use the following command:

    ```bash
    streamlit run src/components/main.py
    ```

    The application will launch locally, and you can interact with the banking assistant.

## Components

### 1. `main.py`

This is the main entry point for the Streamlit application. It sets up the page configuration, handles user authentication, and initiates the chatbot interface.

### 2. `authentication.py`

This file handles the authentication logic using `streamlit_authenticator`. It reads configuration from a YAML file and performs user login/logout operations.

### 3. `chat_interface.py`

This file contains the core chat interface logic. It initializes the session, handles user queries, and displays AI responses using Langchain.

### 4. `prompts.py`

Contains the prompts used by the AI model. The prompts are designed to handle user queries related to bank transactions, loans, investments, etc., by generating the appropriate SQL queries and validating them.

### 5. `utils.py`

Utility functions like `get_user_id` and others that help in various tasks like fetching user-specific data.

## Environment Variables

- `DB_HOST`: The host address of the MySQL database.
- `DB_USER`: The username for accessing the database.
- `DB_PASSWORD`: The password for the database.
- `DB_NAME`: The name of the database.
- `PROMPTS`: All kinds of different prompts used in the application
