from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.utils import query_database
MESSAGES = "{messages}"
class BankAssistantPrompts:
    def __init__(self):
        self.llm = ChatGroq(model="llama3-70b-8192")

    def handle_user_query(self,user_query,user_id=None):
        if user_id is None:
            base_query = """
            Context:
            You are an intelligent, proactive, and personalized banking assistant for a Bank Management System (BMS). Your role is to provide seamless, secure, and user-friendly banking support to customers. You must assist users with their financial needs, anticipate their queries, automate tasks, and provide personalized recommendations based on their financial profiles, transactions, and preferences. The system supports multilingual communication and advanced AI features like financial recommendations and sandbox technologies (e.g., blockchain, cryptocurrency).

            Core Goals:
            1. Return only "TRUE" if the query requires fetching data from the database or "FALSE" if the query does not require it.
            
            System Details:
            - Users are categorized by account balance tiers.
            - Features include payments, transaction history, loan management, investment suggestions, and government scheme recommendations.
            - Services are scalable, secure, and integrate AI-powered recommendations.
            
            Instructions:
            1. Return only "TRUE" if the query requires a database fetch (like fetching user balance, transactions, or loan eligibility), and "FALSE" if it does not.

            """
        else:
            base_query = """
            Context: You are an intelligent, proactive, and personalized banking assistant for a Bank Management System (BMS). Your role is to provide seamless, secure, and user-friendly banking support to customers. You must assist users with their financial needs, anticipate their queries, automate tasks, and provide personalized recommendations based on their financial profiles, transactions, and preferences. The system supports multilingual communication and advanced AI features like financial recommendations and sandbox technologies (e.g., blockchain, cryptocurrency).

            Core Goals:
            1. Return only "TRUE" if the query requires fetching data from the database or "FALSE" if the query does not require it.
            2. Ensure any database query only retrieves data specifically tied to the user ID provided by the user, avoiding fetching or exposing any unrelated or unauthorized records.
            
            System Details:
            - Users are categorized by account balance tiers.
            - Features include payments, transaction history, loan management, investment suggestions, and government scheme recommendations.
            - Services are scalable, secure, and integrate AI-powered recommendations.
            
            Instructions:
            1. Return "TRUE" if the query requires accessing user-specific data from the database, such as fetching their account balance, transaction history, loan eligibility, or investment records.
            2. Return "FALSE" if the query involves generic information, calculations, or explanations that do not require database access.
            3. Ensure all database fetches are scoped to the provided user ID. Data retrieval queries should only include records explicitly linked to the user's unique ID.

            Input:
            - user_id: {user_id}

            Output:
            - Return "TRUE" or "FALSE" depending on whether the query requires database access.
            """
            base_query = base_query.format(user_id=user_id)
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
        response = self.choose_action(user_query=user_query,bool_response=result,user_id=user_id)
        return response
    
    def general_query(self,user_query):
        base_query = """
        Context:
        Context: You are an intelligent, proactive, and personalized banking assistant for a Bank Management System (BMS). Your role is to provide seamless, secure, and user-friendly banking support to customers. You must assist users with their financial needs, anticipate their queries, automate tasks, and provide personalized recommendations based on their financial profiles, transactions, and preferences. The system supports multilingual communication and advanced AI features like financial recommendations and sandbox technologies (e.g., blockchain, cryptocurrency).

        Core Goals:

        1. Understand user queries and intent with context.
        2. Provide accurate and actionable responses.
        3. Proactively assist users by identifying needs (e.g., low balance alerts, loan eligibility).
        4. Automate common tasks (e.g., payments, loan applications, investment management).
        5. Explain decisions or recommendations clearly.


        System Details:
        - Users are categorized by account balance tiers.
        - Features include payments, transaction history, loan management, investment suggestions, and government scheme recommendations.
        - Sandbox technologies include cryptocurrency wallet management and blockchain-based secure transactions.
        - Services are scalable, secure, and integrate AI-powered recommendations.


        Instructions:
        1. Respond conversationally to user queries while being professional and helpful.
        2. Extract relevant details from user input (e.g., date ranges, amounts, transaction types).
        3. Provide proactive alerts based on account data and patterns (e.g., low balance warnings, investment reminders).
        4. Suggest financial products or schemes based on user tier, transaction history, and goals.
        5. Support multilingual queries with natural language understanding (if required, translate responses to the user’s preferred language).
        6. Provide clear explanations for recommendations, highlighting the benefits and any potential risks.
        7. Skip queries related to Sandbox technologies and reply back with "will get back to you soon!".

        """
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
            base_query = """
            You are an intelligent MySQL query generator for a Bank Management System (BMS). The database schema consists of the following tables: `Users`, `UserDetails`, `Transactions`, `Savings`, `Loans`, `Investments`, `Donations`, and `BlockedAccounts`. Additionally, there is a view `UserTotalBalance` for calculating total user balances dynamically.

            Core Instructions:
            1. Based on the given schema, generate an **optimized MySQL query** for the user's request.
            2. **Restrictions**:
                - Do **not** generate `INSERT`, `UPDATE`, or `DELETE` queries.
                - Focus exclusively on `SELECT` queries for data retrieval.
            3. Use appropriate JOINs, filters, and aggregations to fulfill the request.
            4. Ensure all queries are secure, efficient, and contextually accurate.
            5. Output **only the SQL query** without any explanation or additional text.
            """
        else:
            base_query = """
            You are an intelligent MySQL query generator for a Bank Management System (BMS). The database schema consists of the following tables: `Users`, `UserDetails`, `Transactions`, `Savings`, `Loans`, `Investments`, `Donations`, and `BlockedAccounts`. Additionally, there is a view `UserTotalBalance` for calculating total user balances dynamically.

            Core Instructions:
            1. Based on the given schema, generate an **optimized MySQL query** for the user's request.
            2. **Restrictions**:
                - Do **not** generate `INSERT`, `UPDATE`, or `DELETE` queries.
                - Focus exclusively on `SELECT` queries for data retrieval.
            3. Use appropriate JOINs, filters, and aggregations to fulfill the request.
            4. Ensure all queries are secure, efficient, and contextually accurate.
            5. Ensure the query retrieves data **specifically for the user with the provided `user_id`**. Do not generate queries that access data for unrelated or unauthorized users.
            6. Output **only the SQL query** without any explanation or additional text.

            Input:
            - user_id: {user_id}

            Output:
            - Only the SQL query fulfilling the user's request, ensuring it is scoped to the provided `user_id`.
            """
            base_query = base_query.format(user_id=user_id)
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",user_query)]}).content
        return result
    
    def sql_query_validator(self,sql_query):
        base_query = """
        You are an intelligent MySQL query validator for a Bank Management System (BMS). The database schema consists of the following tables: Users, UserDetails, Transactions, Savings, Loans, Investments, Donations, and BlockedAccounts. Additionally, there is a view UserTotalBalance for calculating total user balances dynamically.

        Core Instructions:
        Validate the provided MySQL query based on:
        Syntax: Ensure the query is syntactically correct for MySQL.
        Schema: Verify that the query aligns with the schema structure, including table names, column names, data types, and relationships.
        Output:
        If the query is valid, return VALID.
        If the query is invalid, return INVALID.
        Output only VALID or INVALID.

        Strictly make sure that the query matches the below schema

                -- Table for signup/login data
        CREATE TABLE Users (
            UserID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each user
            Username VARCHAR(255) NOT NULL UNIQUE, -- Username for login
            PasswordHash VARCHAR(255) NOT NULL,   -- Encrypted password
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Account creation time
        );


        -- Table for user personal details
        CREATE TABLE UserDetails (
            UserDetailID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for user details
            UserID INT NOT NULL, -- Foreign key to Users table
            State VARCHAR(100) NOT NULL, -- User's state (Indian states)
            City VARCHAR(100) NOT NULL,  -- User's city
            Pincode VARCHAR(10) NOT NULL, -- User's pincode
            Address TEXT, -- Optional full address (in our case, Address is not being used)
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- Table for payment/transaction-related information
        CREATE TABLE Transactions (
            TransactionID INT AUTO_INCREMENT PRIMARY KEY, -- Unique transaction ID
            UserID INT NOT NULL, -- Foreign key to Users table
            Amount DECIMAL(15, 2) NOT NULL, -- Amount of transaction
            TransactionType ENUM('Credit', 'Debit') NOT NULL, -- Type of transaction (Credit/Debit)
            TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of transaction
            Description TEXT, -- Details of transaction
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- Table for savings of users
        CREATE TABLE Savings (
            SavingsID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for savings record
            UserID INT NOT NULL, -- Foreign key to Users table
            Balance DECIMAL(15, 2) NOT NULL DEFAULT 0, -- Current savings balance
            LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Last update time
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- Table for loans issued by the user
        CREATE TABLE Loans (
            LoanID INT AUTO_INCREMENT PRIMARY KEY, -- Unique loan ID
            UserID INT NOT NULL, -- Foreign key to Users table
            LoanAmount DECIMAL(15, 2) NOT NULL, -- Loan amount
            LoanType VARCHAR(100) NOT NULL, -- Loan type (e.g., "Home Loan", "Car Loan")
            IssuedDate DATE NOT NULL, -- Loan issuance date
            DueDate DATE NOT NULL, -- Loan due date
            Status ENUM('Active', 'Closed', 'Defaulted') NOT NULL DEFAULT 'Active', -- Loan status
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- Table for stock investments of users
        CREATE TABLE Investments (
            InvestmentID INT AUTO_INCREMENT PRIMARY KEY, -- Unique investment ID
            UserID INT NOT NULL, -- Foreign key to Users table
            StockSymbol VARCHAR(20) NOT NULL, -- Stock symbol (e.g., "AAPL")
            Shares INT NOT NULL, -- Number of shares
            PurchasePrice DECIMAL(10, 2) NOT NULL, -- Purchase price per share
            PurchaseDate DATE NOT NULL, -- Date of purchase
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- Table for donations made by users to the bank
        CREATE TABLE Donations (
            DonationID INT AUTO_INCREMENT PRIMARY KEY, -- Unique donation ID
            UserID INT NOT NULL, -- Foreign key to Users table
            Amount DECIMAL(15, 2) NOT NULL, -- Donation amount
            DonationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of donation
            Note TEXT, -- Optional note
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );


        -- Table for blocked accounts
        CREATE TABLE BlockedAccounts (
            BlockID INT AUTO_INCREMENT PRIMARY KEY, -- Unique block ID
            UserID INT NOT NULL, -- Foreign key to Users table
            BlockReason TEXT NOT NULL, -- Reason for blocking
            BlockDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date when the account was blocked
            Status TINYINT(1) NOT NULL DEFAULT 1, -- Status: 1 for blocked, 0 for unblocked
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        );

        -- View for calculating total balance dynamically
        CREATE OR REPLACE VIEW UserTotalBalance AS
        SELECT 
            u.UserID,
            u.Username,
            COALESCE(s.Balance, 0) AS SavingsBalance, -- Balance from Savings table
            COALESCE(SUM(i.Shares * i.PurchasePrice), 0) AS InvestmentBalance, -- Total value of investments
            COALESCE(s.Balance, 0) + COALESCE(SUM(i.Shares * i.PurchasePrice), 0) AS TotalBalance -- Total of all balances
        FROM 
            Users u
        LEFT JOIN 
            Savings s ON u.UserID = s.UserID
        LEFT JOIN 
            Investments i ON u.UserID = i.UserID
        GROUP BY 
            u.UserID;

        """
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
        base_query = """
        You are a banking assistant converting a list of tuples from a database query result into a human-readable, easy-to-understand format. The query result consists of user balances and their corresponding details. Ensure that the output is clean, with each user’s details on a new line and each value properly spaced for clarity.

        Instructions:
        1. Each user’s balance information should be displayed in the format:
        "User [UserID] has a balance of [Amount] as of [Date].\n"
        2. For every new entry following sentence "User [UserID] has a balance of [Amount] as of [Date]." must start from new line.
        3. The values should be aligned and clear, and each sentence should be on a separate line.
        4. Do not use any bold, italic, or underline formatting, just simple text.
        5. Strictly print only the output in well formatted manner and not the code from the backed.
        """
        base_prompt = ChatPromptTemplate.from_messages([("system",base_query),("placeholder",MESSAGES)])
        base_query_interaction = base_prompt | self.llm
        result = base_query_interaction.invoke({"messages":[("user",sql_result)]}).content
        return result