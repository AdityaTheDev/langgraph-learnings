from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer
conn=sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# #test
# CONFIG={'configurable': {'thread_id': 'thread-1'}}
# response=chatbot.invoke({'messages': [HumanMessage(content="What is my name?")]}, 
#                config=CONFIG)

# print(response)

def list_all_thread_ids():
    checkpoints=checkpointer.list(None)
    unique_thread_ids=set()

    for checkpoint in checkpoints:
        unique_thread_ids.add(checkpoint.config["configurable"]['thread_id'])

    return list(unique_thread_ids)