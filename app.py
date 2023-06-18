import os 
import langchain
import streamlit as st 

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain


apikey = os.getenv('OPENAI_API_KEY')

#App framework
st.title ('🔥Roast Machine 🔥')
st.markdown("""
Welcome to the Roast Machine, where we turn your friends' quirks into comedy gold! 
Enter their details below to churn out a roast hotter than a summer barbecue. 
Remember, the more "well-done" your inputs, the more sizzling the output roast will be. 
So, get creative and let's start roasting! 🍖
""")
name = st.text_input(' **Enter the name of the person to roast** ')
traits = st.text_input(' **Enter some strange habits, quirks or personality traits about the person to roast.** Do they snore really loudly? Do they take freebies from hotels? Do they always leave the toilet seat up?')
funny_story = st.text_input(' **Enter some funny and notable memories about this person.** Was there ever a time where the person did something really stupid, like drop their phone down a  portable toilet at a festival or get lost in Ikea?')
appearance = st.text_input(' **Enter some funny aspects about their appearance.** Just state the obvious about the person, especially things that everyone watching can easily recognize about your target. Can they not grow a beard? Do they have a squeaky voice? Do they never stop using their phone?')
tone = st.selectbox(
    'Select the tone of the roast:',
    ('Friendly', 'Harsh', 'Sarcastic', 'Witty', 'Absurd', 'Vulgar' )
)

#Chatmodel

chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo")

#Prompt template

system_message_prompt = SystemMessagePromptTemplate.from_template("You are a comedian, specialized in writing roasts. You are inspired by Dave Chapelle and Ricky Gervais. You are very creative, funny and do not shy away from dark humor or satire. For this roast make sure the tone is {tone}")
human_message_prompt = HumanMessagePromptTemplate.from_template("Roast {name} who has these interesting traits: {traits}. Do you recall the time when {funny_story}? And let's not forget about their unique appearance: {appearance}. Give us a good laugh!")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


 #LLM CHain

roast_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

# Show stuff on the screen when there is a prompt 
if st.button('Generate'):
    try:
        if name and traits and funny_story:
            response = roast_chain.run({"name": name, "traits": traits, "funny_story": funny_story, "appearance": appearance , "tone": tone})
            st.write(response)
    except Exception as e:
        st.error(f"an error occurred:{e}")
