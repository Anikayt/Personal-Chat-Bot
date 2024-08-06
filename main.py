import asyncio
import base64
import streamlit as st
from streamlit_chat import message
import json
import requests
from openai import OpenAI

with open('creds.json', 'r') as f:
    file = json.load(f)
    token = file["output"]


def generate_response(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    completion = client.chat.completions.create(
        extra_headers={
        },
        model="google/gemma-2-9b-it",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


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
