import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize Aurora
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Initialize Text-to-Speech
alex = pyttsx3.init()
voices = alex.getProperty('voices')
alex.setProperty('voice', voices[1].id)

def speak(answer):
    print('Aurora : ', answer)
    alex.say(answer)
    alex.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Aurora listening...")
            voice = listener.listen(source)
            query = listener.recognize_google(voice)
            return query
    except:
        return "Sound can't be captured . Please adjust your microphone"

def chatWithAurora():
    query = listen()
    print('Me : ', query)

    # Preprocess query
    input_ids = tokenizer.encode(query, return_tensors='pt').to(device)

    # Generate response
    output = model.generate(input_ids, max_length=50)

    # Postprocess response
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    speak(response)

    # Handle specific intents like play,time, jokes ,etc
    if 'play' in query:
        song = query.replace('play ', '')
        speak("Playing" + song)
        pywhatkit.playonyt(song)
    elif 'time' in query:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak("It's " + time + " now")
    elif 'joke' in query:
        speak(pyjokes.get_joke())
    elif 'bye' in query:
        speak("Okay bye! Have a nice day ahead!")
        exit()

while True:
    chatWithAurora()
