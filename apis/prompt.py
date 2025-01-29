
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

def get_Query(text : str):

    llm = OllamaLLM(model="gemma:2b")


    prompt_template = """
    You are an expert in SQL query generation. Below are the schemas of two tables:

    ### Table 1 : "Users" ###
    - user_id: Integer (Primary Key, Auto Increment) - it is user id
    - username: String (255, Not Null) - it is username
    - email: String (255, Unique, Not Null) - it is user email
    - password: String (255, Not Null) - it is user password

    ### Table 2 : "Tasks" ###
    - task_id: Integer (Primary Key, Auto Increment) - it is task id
    - todo: String (255, Not Null) - it is task
    - createdAt: DateTime (Default: Current Timestamp) - it is time when task is created
    - status: String (255, Not Null) - it is status of the task
    - isExist: Boolean (Default: True, Not Null) - it says whether task is there or not
    - user_id: Integer (Foreign Key -> users.user_id, Cascade on Delete, Not Null) - it is the foreign key of user id in user table

    Using the above table schemas, **generate an optimized SQL query** for the following natural language request:

    ### DON'T GIVE THE EXPLANATION. GIVE ONLY SQL STATEMENT. GIVE STATEMENT IN ONE LINE ###

    Query: {query}

    SQL:
    """

    prompt = PromptTemplate(input_variables=["query"], template=prompt_template)


    llm_chain = prompt | llm


    user_prompt = text

    sql_query = llm_chain.invoke({"query": user_prompt})

    return sql_query[6:-3]
