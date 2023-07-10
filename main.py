import asyncio
import base64
import streamlit as st
from streamlit_chat import message
from bardapi import Bard
import json

with open('creds.json', 'r') as f:
    file = json.load(f)
    token = file["output"]
def generate_response(prompt):
    bard = Bard(token=token)
    response = bard.get_answer(prompt)
    return response['content']

async def main():
    st.title('🧛Personal Bot')

    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
            unsafe_allow_html=True
        )

    add_bg_from_local('Bg.jpg')

    changes = '''
    <style>
    [data-testid="stAppViewContainer"]
    {
    background-size:cover;
    }
    .st-bx {{
    background-color: rgba(255, 255, 255, 0.05);
    }}
    
    /* .css-1hynsf2 .esravye2 */
    
    html {
    background: transparent;
    }
    div.esravye2 > iframe {{
        background-color: transparent;
    }}
    </style>
    '''
    st.markdown(changes, unsafe_allow_html=True)
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def get_input():
        input_text = st.text_input("Vivy: ", "Hey there!!", key='input')
        return input_text

    user_input = get_input()

    if user_input:
        output = await asyncio.to_thread(generate_response, user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))



asyncio.run(main())
