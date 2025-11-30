import streamlit as st
import uuid
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


def generate_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id

#session state for message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []


# config thread for langgraph
CONFIG = {'configurable': {'thread_id': st.session_state["thread_id"]}}

def reset_chat():
    st.session_state['message_history'] = []
    st.session_state["thread_id"] = generate_thread_id()
    add_thread(st.session_state["thread_id"])

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversations_from_thread(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values.get('messages', [])


add_thread(st.session_state["thread_id"])



# -----------------------------Sidebar UI --------------------------------

with st.sidebar:
    st.title("LangGraph Chatbot")
    st.header("Conversations")
    if st.button("New chat"):
        reset_chat()
    for thread_id in st.session_state["chat_threads"]:
        if st.button(thread_id):
            st.session_state["thread_id"] = thread_id
            messages=load_conversations_from_thread(thread_id)
            temp_message_history=[]
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role='user'
                else:
                    role='assistant'
                temp_message_history.append({'role': role, 'content': msg.content})
            st.session_state['message_history'] = temp_message_history



# ------------------------------Main UI--------------------------------



# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


# If user input is given
user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})