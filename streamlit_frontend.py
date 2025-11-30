import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# config thread for langgraph
CONFIG = {'configurable': {'thread_id': 'thread-1'}}



#session state for message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

message_history=st.session_state['message_history']





# loading the conversation history
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

# If user input is given
if user_input:

    # first add the message to message_history
    message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    ai_message = response['messages'][-1].content
    # first add the message to message_history
    message_history.append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)