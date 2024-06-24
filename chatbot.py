import streamlit as st
import google.generativeai as genai
import time

# Page setup
st.set_page_config(layout='wide', page_title='Chatbot', page_icon=':robot_face:')
st.title('💬 Chatbot using Google Gemini Model')

with st.sidebar:
    # API key setup
    GOOGLE_API_KEY = st.text_input('Gemini API Key', type='password')
    st.markdown('''[Get an API key](https://aistudio.google.com/app/apikey)''')
        
model = genai.GenerativeModel('gemini-1.5-pro')
    

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun 
for message in st.session_state.messages:
    avatar = '👩🏻‍💻' if message['role'] == 'user' else '🤖'
    with st.chat_message(message['role'], avatar=avatar):
        st.markdown(message['content'])

def response_generator(response):
    for word in response.split(' '):
        yield word + ' '
        time.sleep(0.02)

if prompt := st.chat_input('Hi! How can I help you?'):
    
    if not GOOGLE_API_KEY:
        st.info('Please add your gemini API key to continue')
        st.stop()
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Display user message in chat message container
    with st.chat_message('user', avatar='👩🏻‍💻'):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message('assistant', avatar='🤖'):
        stream = model.generate_content(prompt).text
        response = st.write_stream(response_generator(stream))
    st.session_state.messages.append({'role': 'assistant', 'content': response})

# Button - clear chat history
if st.sidebar.button('Clear chat history', type='primary'):
    st.session_state.messages = []
    st.rerun()
