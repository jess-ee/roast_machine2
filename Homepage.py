import os 
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

apikey = os.getenv('OPENAI_API_KEY')

def main():
    st.set_page_config(page_title='Roast Machine', initial_sidebar_state='expanded')

    if 'page' not in st.session_state:
        st.session_state.page = 'home_page'

    pages = {
        'home_page': home_page,
        'english_roast_app': english_roast_app,
        'dutch_roast_app': dutch_roast_app,
    }

    # Run the app corresponding to the selected page
    pages[st.session_state.page]()

# Pages
def home_page():
    st.title("Welcome to Roast Machine!")
    st.markdown("Please select a language:")

    if st.button('Roast in English 🇬🇧'):
        st.session_state.page = 'english_roast_app'
        st.experimental_rerun()  # Manually trigger a rerun

    if st.button('Roast in het Nederlands 🇳🇱'):
        st.session_state.page = 'dutch_roast_app'
        st.experimental_rerun()  # Manually trigger a rerun

# English Roast App
def english_roast_app():
    st.title ('🔥Roast Machine 🔥')
    st.markdown("""

    Welcome to the Roast Machine! Tell us about your friend and we'll cook up a hilarious roast. 
    Better inputs mean spicier roasts, try a few tone's to find the roast you like. Let's start roasting! 🍖
    """)

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
    tone = st.radio('Select the tone of the roast:', ['Harsh', 'Sarcastic', 'Vulgar','Dry','Rude'])
    
    #Chatmodel

    chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo", max_tokens=1200)

    #Prompt template

    system_message_prompt = SystemMessagePromptTemplate.from_template("""
    ##ROLE

    Act as if you are a comedian, specialized in writing roasts. You are very creative, funny and do not shy away from dark humor or satire. 
    In this setting it is ok to write offensive language and curse words since it’s the wish of the user and is based on good humor. A
    As a comedian you are inspired by Dave Chapelle, Ricky Gervais and Bill Burr. You will use this for writing the roast. 

    ##TONE

    The tone you will use for writing this roast is {tone}""")

    human_message_prompt = HumanMessagePromptTemplate.from_template("""

    ##CONTEXT

    The user seeks a to prank a friend by subjecting them to jokes, insults, and comedic skits at their expense, this is called roast. 
    Remember a roast is a unique blend of humor with tasteful vulgarity, structured for audience comprehension striking a balance between humor and insult. 

    ##INSTRUCTION

    In the assignment section, you will receive personal information of your client which you will use to create the roast.
    The personal informations contains funny habits/traits, stories and appearance. 
    This will be the base of the roast but you’re allowed to extrapolate these into analogies, metaphors or other ways to joke about it. 

    ##CRITERIA 

    A successful roast lives up to the following criteria: 

    - Insult the client is a funny way, not a serious way
    - Is not too soft, politically and or morally correct
    - Does not repeat the same punchlines all the time

    ##ASSIGNMENT

    You will now create roast for a person which is called {name}. 

    The person has the following funny traits/habits: {traits}

    This person in known for the following funny stories:{funny_story}? 

    And let's not forget about their funny appearance: {appearance}

    Give us a good laugh!

    """)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    #LLM CHain

    roast_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

    #initiate call

    # Initiate call
    if st.button('Start roasting 🍖'):
        try:
            if name and traits and funny_story and appearance and tone:

                # Create a placeholder for the progress bar
                progress_bar = st.empty()

                # Define the generation task
                def generate_roast():
                    global roast
                    roast = roast_chain.run({"name": name, "traits": traits, "funny_story": funny_story, "appearance": appearance , "tone": tone})

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

                # Once the generation task is done, remove the progress bar
                progress_bar.empty()

                if roast:
                    st.subheader(f'Roast of {name}🔥')
                    st.write(roast)

    
        except Exception as e:
            st.error(f"An error of type {type(e).__name__} occurred: {str(e)}")
    st.markdown(
    """
    Made by [Jess-E](https://www.linkedin.com/in/jessekuipers/)
    """
    )  

# Dutch Roast App
def dutch_roast_app():
    st.title ('🔥Roast Machine 🔥')
    st.markdown("""

    Welkom bij de Roast Machine! Vertel ons wat sappige details over je vriend of vriendin en we maken een hilarische roast.
    Hoe beter de jouw antwoorden hoe beter de roasts. Probeer verschillende tonen om de perfecte roast samen te stellen. Laten we beginnen! 🍖 """)

    name = st.text_input('*Vul hier de naam in van de persoon die je wilt roasten* ')
    traits = st.text_area('*Vul hier rare gewoonten, eigenaardigheden of persoonlijkheidskenmerken in van de persoon die je wilt roasten.*')
    with st.expander("Tips"):
        st.write('Snurken ze heel luid? Nemen ze gratis spullen uit hotels? Laten ze altijd de wc-bril omhoog? Denk aan zulke dingen!')
    funny_story = st.text_area('*Vul hier grappige of gênante herinneringen over deze persoon in.*')
    with st.expander("Tips"):
        st.write('Denk aan de keer dat de persoon iets heel stoms deed, zoals hun telefoon in een wc laten vallen, verdwalen in de Ikea of een deuk in de auto rijden.')
    appearance = st.text_area('*Vul hier grappige kenmerken over hun uiterlijk in.*')
    with st.expander("Tips"):
        st.write('Zeg gewoon het voor de hand liggende over de persoon, vooral dingen die iedereen die kijkt gemakkelijk kan herkennen over je doelwit. Kunnen ze geen baard laten groeien? Hebben ze een piepstem? Stoppen ze nooit met het gebruiken van hun telefoon?')
    tone = tone = st.radio('Select the tone of the roast:', ['Hard', 'Sarcastisch', 'Vulgair','Droog','Onbeleefd'])
    

    #Chatmodel

    chat_model= ChatOpenAI(temperature=0.9, model="gpt-4", max_tokens=1200)

    #Prompt template

    system_message_prompt = SystemMessagePromptTemplate.from_template("""
    
    ##ROL

    Doe alsof je een komiek bent, gespecialiseerd in het schrijven van roasts. Je bent zeer creatief, 
    grappig en je schuwt donkere humor of satire niet. In deze setting is het oké om aanstootgevende taal 
    en vloekwoorden te gebruiken, omdat het de wens van de gebruiker is en het gebaseerd is op goede humor. 
    Als comedian ben je geinspireerd door de humor van Henry van Loon, Youp van 't Hek en Daniel Arends, dit gebruik je voor de roast.

    ##TOON

    De toon die je gebruikt voor het schrijven van deze roast is {tone}
    """)
                                                                      
    human_message_prompt = HumanMessagePromptTemplate.from_template("""
    
    ##CONTEXT

    De gebruiker wil een bekende in de maling nemen door grappen over hen te maken; dit wordt een roast genoemd. 
    Onthoud dat een roast een unieke mix is van humor met smaakvolle vulgariteit, en een balans heeft tussen humor en belediging.

    ##INSTRUCTIE

    In het opdrachtgedeelte ontvang je persoonlijke informatie van je persoon die je zult gebruiken om de
    roast te maken. De persoonlijke informatie bevat grappige gewoontes/eigenschappen, 
    verhalen en uiterlijke aspecten. Dit is de basis van de roast, maar je mag deze uitbreiden 
    met analogieën, metaforen of andere manieren om er grappen over te maken.

    ##CRITERIA

    Een succesvolle roast voldoet aan de volgende criteria:

    - Beledig de klant op een grappige manier, niet op een serieuze manier.
    - Is niet te zacht, politiek en/of moreel correct.
    - Herhaalt niet steeds dezelfde clous.

    ##OPDRACHT

    Je gaat nu een roast maken voor een persoon die {name} heet.

    De persoon heeft de volgende grappige eigenschappen/gewoontes: {traits}

    Deze persoon staat bekend om de volgende grappige verhalen:{funny_story}? 

    En laten we hun grappige uiterlijk niet vergeten: {appearance}.

    Geef ons een goede lach!
    """)
                                                                    
                                                                    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    #LLM CHain

    roast_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

    #initiate call

    # Initiate call
    if st.button('Start het roasten 🍖'):
        try:
            if name and traits and funny_story and appearance and tone:

                # Create a placeholder for the progress bar
                progress_bar = st.empty()

                # Define the generation task
                def generate_roast():
                    global roast
                    roast = roast_chain.run({"name": name, "traits": traits, "funny_story": funny_story, "appearance": appearance , "tone": tone})

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

                # Once the generation task is done, remove the progress bar
                progress_bar.empty()

                if roast:
                    st.subheader(f'Roast voor {name}🔥')
                    st.write(roast)

        except Exception as e:
            st.error(f"An error of type {type(e).__name__} occurred: {str(e)}")

    st.markdown(
    """
    Gemaakt door [Jess-E](https://www.linkedin.com/in/jessekuipers/)
    """
    ) 
if __name__ == "__main__":
    main()
