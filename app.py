import os 
from apikey import apikey
import langchain
import streamlit as st 
import time
import threading
import urllib.parse

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain
event = threading.Event() 

os.environ ['OPENAI_API_KEY'] = apikey

#App framework
st.title ('🔥Roast Machine 🔥')
st.markdown("""

Welcome to the Roast Machine! Tell us about your friend and we'll cook up a hilarious roast. Better inputs mean spicier roasts. Let's start roasting! 🍖
""")
language = st.selectbox(
    'Select the language for your roast (**Provide the input in the languange you select**):',
    ('English','Dutch')
)
name = st.text_input('*Enter the name of the person to roast* ')
traits = st.text_input('*Enter some strange habits, quirks or personality traits about the person to roast.*')
with st.expander("Tips"):
    st.write('Do they snore really loudly? Do they take freebies from hotels? Do they always leave the toilet seat up? Think about stuff like that!')
funny_story = st.text_input('*Enter some funny or embarrassing memories about this person.*')
with st.expander("Tips"):
    st.write('Think about the time when the person did something really stupid, like drop their phone down a portable toilet at a festival or get lost in Ikea?')
appearance = st.text_input('*Enter some funny aspects about their appearance.* ')
with st.expander("Tips"):
    st.write('Just state the obvious about the person, especially things that everyone watching can easily recognize about your target. Can they not grow a beard? Do they have a squeaky voice? Do they never stop using their phone?')
tone = st.selectbox(
    'Select the tone of the roast:',
    ('Harsh', 'Sarcastic', 'Witty', 'Absurd', 'Vulgar','Dry','Rude')
)


#Translation
english_to_dutch_tones = {
    'Harsh': 'Harde',
    'Sarcastic': 'Sarcastische',
    'Witty': 'Geestige',
    'Absurd': 'Absurde',
    'Vulgar': 'Vulgaire',
    'Dry': 'Droge',
    'Rude': 'Grove'
}

selected_tone = st.selectbox('Tone', list(english_to_dutch_tones.keys()))
translated_tone = english_to_dutch_tones[selected_tone]


#Chatmodel

chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo", max_tokens=1200)

#Prompt template

if language == 'English':
    system_message_prompt = SystemMessagePromptTemplate.from_template("Act as if you are a comedian, specialized in writing roasts. Remember a roast is a unique blend of humor with tasteful vulgarity, structured for audience comprehension striking a balance between humor and insult. Your humor is inspired by Dave Chapelle and Ricky Gervais. You are very creative, funny and do not shy away from dark humor or satire. For this roast make sure the tone is {tone}")
    human_message_prompt = HumanMessagePromptTemplate.from_template("Roast {name} and make sure to respond in {language}. This person has these interesting traits: {traits}. Do you recall the time when {funny_story}? And let's not forget about their unique appearance: {appearance}. Give us a good laugh!")
elif language == 'Dutch':
    system_message_prompt = SystemMessagePromptTemplate.from_template("Doe alsof je een comedian bent, gespecialiseerd in het schrijven van roast speeches. Onthoud dat een roast een unieke mix is van humor met smaakvolle vulgariteit, gestructureerd voor begrip van het publiek die een balans vindt tussen humor en belediging. Je humor is geïnspireerd door Dave Chapelle en Ricky Gervais. Je bent erg creatief, grappig en schuwt donkere humor of satire niet. Zorg er voor dat deze roast in een {tone} toon wordt geschreven".format(tone=translated_tone))
    human_message_prompt = HumanMessagePromptTemplate.from_template("Roast {name} en zorg ervoor dat je reageert in het {language}. Die persoon heeft deze interessante eigenschappen heeft: {traits}. Herinner je je de keer dat {funny_story}? En laten we hun unieke uiterlijk niet vergeten: {appearance}. Maak ons aan het lachen!")

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


 #LLM CHain

roast_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

# Show stuff on the screen when there is a prompt 
if st.button('Start roasting 🍖'):
    try:
        if name and traits and funny_story and appearance and tone:

            # Create a placeholder for the progress bar
            progress_bar = st.empty()

            # Define the generation task
            def generate_roast():
                global response
                response = roast_chain.run({"name": name,"language":language, "traits": traits, "funny_story": funny_story, "appearance": appearance , "tone": tone})

            # Start the generation task in a separate thread
            thread = threading.Thread(target=generate_roast)
            thread.start()

            # Display a loading message
            progress_bar.text('Generating roast...')

            # Wait for the generation task to complete
            while thread.is_alive():
                # Display an animation to indicate that the task is still running
                for i in range(100):
                    time.sleep(0.01)  # Small delay to slow down the animation
                    progress_bar.progress((i + 1) % 100)

            # Once the generation task is done, display the result
            progress_bar.empty()
            st.write(response)

            share_text = f"Check out this roast: {response}"
            share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}"
            st.markdown(f'[Share on Twitter]({share_url})')


    except Exception as e:
        st.error(f"An error of type {type(e)._name_} occurred: {str(e)}")