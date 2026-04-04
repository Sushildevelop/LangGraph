import streamlit as st
from chatbot_langgraph_backend import chatbot
from langchain_core.messages import SystemMessage, HumanMessage

#st.session_state -> dict ->

if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

message_history = st.session_state['message_history']

for message in message_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.text(message["content"])
    else:
        with st.chat_message("assistant"):
            st.text(message["content"])

user_input = st.chat_input("Enter your message:")

if user_input:
    #First add the user message to the history
    message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    # response = chatbot.invoke({'message':[HumanMessage(content=user_input)]}, config={'configurable':{'thread_id': '1'}})
    
    # #First add the user message to the history
    # responses=response["message"][-1].content
    # message_history.append({"role": "assistant", "content": responses})
    # with st.chat_message("assistant"):
    #     st.markdown(responses)
    
    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk ,metadata in chatbot.stream(
                {'message':[HumanMessage(content=user_input)]},
                config={'configurable':{'thread_id': '1'}},
                stream_mode='messages'
            )
        )
        
    message_history.append({"role": "assistant", "content": ai_message})
        

    
    