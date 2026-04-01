from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated,Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

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

checkpointer=InMemorySaver()

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

thread_id='1'
while True:
    user_message=input('Type here:')
    print(f'User: {user_message}')
    if user_message.strip().lower() in ['exit','quit','bye']:
        break
    config={'configurable':{'thread_id': thread_id}}
    response=chatbot.invoke({'message':[HumanMessage(content=user_message)]},config=config)
    print(f'Assistant: {response["message"][-1].content}')
