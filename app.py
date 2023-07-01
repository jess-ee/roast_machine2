import os 
from apikey import apikey
import langchain
import streamlit as st 
import time

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain


os.environ ['OPENAI_API_KEY'] = apikey

#App framework
st.title ('🔥Roast Machine 🔥')
st.markdown("""

Welcome to the Roast Machine! Provide your friends' quirks and we'll cook up a hilarious roast. Better inputs mean spicier roasts. Let's start roasting! 🍖
""")
language = st.selectbox(
    'Select the language for your roast (Please provide the input in the languange you select):',
    ('English','Dutch')
)
name = st.text_input('**Enter the name of the person to roast** ')
traits = st.text_input('**Enter some strange habits, quirks or personality traits about the person to roast.**')
with st.expander("Examples"):
    st.write('Do they snore really loudly? Do they take freebies from hotels? Do they always leave the toilet seat up?')
funny_story = st.text_input('**Enter some funny or embarrassing memories about this person.**')
with st.expander("Examples"):
    st.write('Was there ever a time where the person did something really stupid, like drop their phone down a portable toilet at a festival or get lost in Ikea?')
appearance = st.text_input('**Enter some funny aspects about their appearance.** ')
with st.expander("Examples"):
    st.write('Just state the obvious about the person, especially things that everyone watching can easily recognize about your target. Can they not grow a beard? Do they have a squeaky voice? Do they never stop using their phone?')
tone = st.selectbox(
    'Select the tone of the roast:',
    ('Harsh', 'Sarcastic', 'Witty', 'Absurd', 'Vulgar','Friendly' )
)

#Chatmodel

chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo", max_tokens=500)

#Prompt template

if language == 'English':
    system_message_prompt = SystemMessagePromptTemplate.from_template("Act as if you are a comedian, specialized in writing roasts. Remember a roast is a unique blend of humor with tasteful vulgarity, structured for audience comprehension striking a balance between humor and insult. Your humor is inspired by Dave Chapelle and Ricky Gervais. You are very creative, funny and do not shy away from dark humor or satire. For this roast make sure the tone is {tone}")
    human_message_prompt = HumanMessagePromptTemplate.from_template("Roast {name} in the {language} language who has these interesting traits: {traits}. Do you recall the time when {funny_story}? And let's not forget about their unique appearance: {appearance}. Give us a good laugh!")
elif language == 'Dutch':
    system_message_prompt = SystemMessagePromptTemplate.from_template("Doe alsof je een comedian bent, gespecialiseerd in het schrijven van roast speeches. Onthoud dat een roast een unieke mix is van humor met smaakvolle vulgariteit, gestructureerd voor begrip van het publiek die een balans vindt tussen humor en belediging. Je humor is geïnspireerd door Dave Chapelle en Ricky Gervais. Je bent erg creatief, grappig en schuwt donkere humor of satire niet. Zorg er voor dat deze roast en een {tone} toon wordt geschreven")
    human_message_prompt = HumanMessagePromptTemplate.from_template("Roast {name} in de {language} taal die deze interessante eigenschappen heeft: {traits}. Herinner je je de tijd dat {funny_story}? En laten we hun unieke uiterlijk niet vergeten: {appearance}. Maak ons aan het lachen!")

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


 #LLM CHain

roast_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

# Show stuff on the screen when there is a prompt 
if st.button('Start roasting'):
    try:
        if name and traits and funny_story:
            progress_bar = st.progress(0)
            for perc_completed in range(100):
                time.sleep(0.05)
                progress_bar.progress(perc_completed+1)
            response = roast_chain.run({"name": name,"language":language, "traits": traits, "funny_story": funny_story, "appearance": appearance , "tone": tone})
            st.write(response)
    except Exception as e:
        st.error(f"An error of type {type(e).__name__} occurred: {str(e)}")


