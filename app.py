import streamlit as st
from graph import chatbot 
from langchain_core.messages import HumanMessage
import uuid
from styles import custom_css

st.set_page_config(
    page_title="The Clothing Store - Customer Support Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(custom_css,unsafe_allow_html=True)

if 'CHAT_NO' not in st.session_state:
    st.session_state['CHAT_NO'] = 0

## Utility Functions
def CONFIG(thread_id : str) -> dict:
    """
    Returns a configuration dictionary for the chatbot, containing the thread ID.
    
    :param thread_id: The unique identifier for the chat thread.
    :type thread_id: str
    """
    return {'configurable': {'thread_id': thread_id}}

def generate_thread_id() -> tuple[str, str]:
    """
    Generates a new unique thread ID and increments the chat counter in the session state.
    """
    st.session_state['CHAT_NO'] += 1
    thread_id = str(uuid.uuid4())
    thread_name = f"Chat - {st.session_state['CHAT_NO']}"
    return (thread_name, thread_id)

def add_thread(thread : tuple[str, str]):
    """
    Adds a new chat thread to the session state if it doesn't already exist.
    
    :param thread: Tuple of thread name and thread ID to be added to the chat threads.
    :type thread: tuple[str, str]
    """
    if thread not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread)

def reset_chat():
    """
    Resets the chat by generating a new thread ID, adding it to the session state, and clearing the message history.
    """
    thread = generate_thread_id()
    st.session_state['thread'] = thread
    add_thread(thread)
    st.session_state['message_history'] = []

def load_conversation(thread_id : str):
    """
    Loads the conversation history for a given thread ID from the chatbot's state.
    
    :param thread_id: The unique identifier for the chat thread whose conversation history is to be loaded.
    :type thread_id: str
    """
    state = chatbot.get_state(CONFIG(thread_id))
    
    messages = state.values.get('messages', [])

    if messages:
        temp_messages = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages
    
    else :
        st.session_state['message_history'] = []


## Session Setup
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []  ## Initialize message history if none exists

if 'thread' not in st.session_state:
    st.session_state['thread'] = generate_thread_id()  ## Initialize a new chat thread if none exists

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = [st.session_state['thread']]  ## Initialize the chat threads list with the current thread if none exists

## Title and Description
st.title("The Clothing Store - Customer Support Chatbot",width="content")
st.write("Ask me anything about our orders, shipping, and returns policies. I'm here to help!")

## Sidebar UI
st.sidebar.header("🛍️ The Clothing Store")

st.divider()

if st.sidebar.button("New Chat", width="stretch"):
    reset_chat()

st.sidebar.header("My Conversations")

if st.session_state['chat_threads']: # Check if there are any threads 
    for thread_name, thread_id in st.session_state['chat_threads'][::-1]:  ## Display threads in reverse order (most recent first)
        if st.sidebar.button(thread_name, width="stretch"):
            st.session_state['thread'] = (thread_name, thread_id)
            load_conversation(thread_id)


## Main UI
current_thread_id = st.session_state['thread'][1]

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        spinner = st.spinner("Searching FAQ of The Clothing Store...")
        spinner.__enter__()

        def response_stream():
            spinner_hidden = False
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG(current_thread_id),
                stream_mode='messages'
            ):
                if message_chunk.content and not isinstance(message_chunk.content, str):
                    if not spinner_hidden:
                        spinner.__exit__(None, None, None)
                        spinner_hidden = True
                    yield message_chunk.content[0]["text"]
            if not spinner_hidden:
                spinner.__exit__(None, None, None)

        ai_message = st.write_stream(response_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
