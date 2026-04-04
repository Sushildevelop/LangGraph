from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated,Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

load_dotenv()
llm=ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]
    
def chat_node(state:ChatState):
    # Initialize the LLM
 
    # Create messages for the LLM
    messages = state['message']
    
    #send to llm
    response=llm.invoke(messages)
    
    #response store state
    return {'message':[response]}

conn=sqlite3.connect(database='chatbot.db', check_same_thread=False) # Create the database file if it doesn't exist

checkpointer=SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
        
    return list(all_threads)  

