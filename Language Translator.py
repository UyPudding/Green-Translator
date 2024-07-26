import streamlit as st  # pip install streamlit
import clipboard        # pip install clipboard
import pyglet           # pip install pyglet
from gtts import gTTS   # pip install gTTS
from deep_translator import GoogleTranslator      # pip install -U deep-translator
from streamlit_star_rating import st_star_rating  # pip install st-star-rating
import gtts.lang  # Get gTTS Language Codes
from io import BytesIO
from time import sleep 


st.set_page_config(
    page_title='Green Translator - Free Online Translator',
    page_icon='📗'
)


st.markdown(f"<style>{open('language style.css').read()}</style>",unsafe_allow_html=True)   # CSS Style

## Session States ##
if 'star' not in st.session_state:
    st.session_state.star=None     # For st_star_rating

if 'translate' not in st.session_state:
    st.session_state.translate=[]  # For Translation

if 'get_value' not in st.session_state:
    st.session_state.get_value=''  # For Uploaded File

if 'widget' not in st.session_state:
    st.session_state.widget=''     # For clearing text area


## Sidebar ##
with st.sidebar:
    st.markdown('<div style="color:#3EDC07;text-align:center;font-size:32px;"><b>Background Color</b></div>',unsafe_allow_html=True)

    background_color=st.color_picker(label='🎨**Pick a Color for Background**',help='Change Background Color',value='#FFFFFF')
    
    # CSS Changing background color
    st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
                background-color: {background_color}
}}
</style>""",unsafe_allow_html=True)
    
    # Default and Current Color
    st.markdown(f'''<p>•  Default Color: <b>#FFFFFF</b><br>
             •  Current Color: <b>{background_color.upper()}</b></p>''',unsafe_allow_html=True)
    st.divider()

    # Rating
    st.markdown('<div style="color:#3EDC07;text-align:center;font-size:32px;"><b>Rating</b></div>',unsafe_allow_html=True)

    rating=st_star_rating(label='Rate this Web App',maxValue=5,defaultValue=0,size=25,resetButton=True,key='star')

    if st.session_state.star is not None:
        st.write(f'You have rated <span style="color:#ffc043"><b>{st.session_state.star} Stars!</b></span>',unsafe_allow_html=True)
        st.success('**Thanks For Rating!**')



### Functions ###
def translator():  # Translate input text area
    try:
       translation=GoogleTranslator(source=st.session_state.input.lower(),
                                    target=st.session_state.output.lower()).translate(text_area)
       if not st.session_state.translate:   # Add translation if list st.session_state.translate is empty, else clear and add new one
           st.session_state.translate.append(translation)
       else:
           st.session_state.translate.clear()
           st.session_state.translate.append(translation)
    except:  # Handling LanguageNotSupportEdexception error
        st.toast(body=f'The text \"{text_area}\" is not in {st.session_state.input}!',icon='❌')

def replace_file_text():  # Replace text area value with Uploaded File value
    st.session_state.get_value=text_area.replace(text_area,file_uploader.read().decode('utf-8'))
    st.toast(body='Press \"X\" to confirm!',icon='⚙️')

def clear_text():
    st.session_state.pop('get_value')  # Clear content from uploaded file
    st.session_state.widget=''         # Clear content from keyboard

def swap_textarea():
    st.session_state.input=keep_output  # Change Input language to Output language
    st.session_state.output=keep_input  # Change Output language to Input language



## Languages ##
languages=[
    "Afrikaans","Akan","Albanian","Amharic","Arabic","Armenian","Assamese","Aymara","Azerbaijani",
    "Bambara","Bangla","Basque","Belarusian","Bhojpuri","Bosnian","Bulgarian","Burmese",
    "Catalan","Cebuano","Central Kurdish","Chinese (Simplified)","Chinese (Traditional)","Corsican","Croatian","Czech",
    "Danish","Divehi","Dogri","Dutch","English","Esperanto","Estonian","Ewe","Filipino","Finnish","French",
    "Galician","Ganda","Georgian","German","Goan Konkani","Greek","Guarani","Gujarati",
    "Haitian Creole","Hausa","Hawaiian","Hebrew","Hindi","Hmong","Hungarian",
    "Icelandic","Igbo","Iloko","Indonesian","Irish","Italian","Japanese","Javanese",
    "Kannada","Kazakh","Khmer","Kinyarwanda","Korean","Krio","Kurdish","Kyrgyz",
    "Lao","Latin","Latvian","Lingala","Lithuanian","Luxembourgish",
    "Macedonian","Maithili","Malagasy","Malay","Malayalam","Maltese","Manipuri (Meitei Mayek)","Māori","Marathi","Mizo","Mongolian",
    "Nepali","Northern Sotho","Norwegian","Nyanja",
    "Odia","Oromo",
    "Pashto","Persian","Polish","Portuguese","Punjabi",
    "Quechua",
    "Romanian","Russian",
    "Samoan","Sanskrit","Scottish Gaelic","Serbian","Shona","Sindhi","Sinhala","Slovak","Slovenian","Somali","Southern Sotho","Spanish","Sundanese","Swahili","Swedish",
    "Tajik","Tamil","Tatar","Telugu","Thai","Tigrinya","Tsonga","Turkish","Turkmen",
    "Ukrainian","Urdu","Uyghur","Uzbek","Vietnamese",
    "Welsh","Western Frisian","Xhosa","Yiddish","Yoruba","Zulu"
]



st.markdown('''<h1 style="color:#3EDC07;text-align:center;font-family:Segoe UI;
            font-size:50px;">📑Green Translator</h1>''',
            unsafe_allow_html=True)
sleep(1)

st.success('This is :green[**Green Translator**]. Can translate every languages in the world!'
           ,icon='📃')

# Select input language
target_input=st.selectbox(label='**Input Language**',
                    options=languages,
                    index=languages.index('English'),
                    help='Select an input language',
                    key='input'
                    )


# Input text area
text_area=st.text_area(label='Input',value=st.session_state.get_value,
                          height=260,
                          placeholder='Enter text',
                        help='Enter the text need to be translated!',key='widget',label_visibility='collapsed')

# File uploader Button
file_uploader=st.file_uploader(label='**Upload a TXT File**',type=['txt'])

if file_uploader is not None:
    replace_file_text()

col1,col2,col3,col4=st.columns([1,1,1,1]) # Four st.button on same line
with col1:   # Voice speaker input Button
   voice_speaker_button_input=st.button(label='🔊',type='primary')
with col2:   # Clear input text area Button
   clear_button=st.button(label='Clear',type='secondary',on_click=clear_text)
with col3:   # Translate input text area Button
   translate_button=st.button(label='Translate',type='secondary')
with col4:   # Swap input & output Value
    swap_value=st.button(label='🔁',on_click=swap_textarea,type='primary')

# Select output language
target_output=st.selectbox(label='**Output Language**',
                           options=languages,
                           index=languages.index('Vietnamese'),
                           help='Select an output language',
                           key='output')

keep_input=st.session_state.input    # Keep st.session_state.input Value
keep_output=st.session_state.output  # Keep st.session_state.output Value

if voice_speaker_button_input:  # Voice speaker input system
    mp3_fp_input=BytesIO()  # Keep input Voice
    try:
       input_voice=gTTS(text=text_area,
                        lang=list(gtts.lang.tts_langs().keys())[list(gtts.lang.tts_langs().values()).index(st.session_state.input)],
                        slow=False)
       input_voice.write_to_fp(mp3_fp_input)
       mp3_fp_input.seek(0)
       play_sound=pyglet.media.load(None,file=mp3_fp_input,streaming=False)
       play_sound.play()
       pyglet.app.run()
    except RuntimeError:  # Handling RuntimeError
        pass

if translate_button:  # Translate Button system
    translator()  # Call function to translate input text area

# Translation text area
st.html(f"""
        <textarea class='disable_textarea' name='Translation' placeholder='Translation'>{"".join(st.session_state.translate)}</textarea>""")

col5,col6=st.columns([1,1])  # Two st.button on same line
with col5:  # Voice speaker output Button
   voice_speaker_button_output=st.button(label='🔊',type='primary',key='count') # Key='count' to avoid WidgetID Error
with col6:  # Copy Button
   clipboard_button=st.button(label='📋',type='primary')

if clipboard_button:  # Copy system
    clipboard.copy("".join(st.session_state.translate))
    st.toast(body='Copied!',icon='✅')

if voice_speaker_button_output:  # Voice speaker output system
    mp3_fp_output=BytesIO()  # Keep output Voice
    try:
       input_voice=gTTS(text=f'{"".join(st.session_state.translate)}',
                        lang=list(gtts.lang.tts_langs().keys())[list(gtts.lang.tts_langs().values()).index(st.session_state.output)],
                        slow=False)
       input_voice.write_to_fp(mp3_fp_output)
       mp3_fp_output.seek(0)
       play_sound=pyglet.media.load(None,file=mp3_fp_output,streaming=False)
       play_sound.play()
       pyglet.app.run()
    except RuntimeError:  # Handling RuntimeError
        pass