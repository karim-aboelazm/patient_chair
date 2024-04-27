import speech_recognition as sr
import pyttsx3
import json
def voice_output(text):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.8)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(str(text))
    print("Ok")
    engine.runAndWait()

def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0,4)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en')
        # print(f'You said : {query}')
    except:
        return 
    query = str(query)
    return query.lower()

def eye_direction():
    return "Eye Tracking Mode"

class PatientChair(object):
    def __init__(self,deaf:bool,speech:bool):
        self.deaf = deaf
        self.speech = speech
        self.display_mode = None
        self.controll_mode = None
        
    def set_display_mode(self):
        if (self.deaf and self.speech) or (self.deaf and not self.speech):
            self.display_mode = "s" # screen only
        elif (not self.deaf and self.speech) or (not self.deaf and not self.speech):
            self.display_mode = "vs" # screen and voice
        else:
            self.display_mode = None
        
    def get_display_mode(self):
        return self.display_mode
    
    def set_controll_mode(self):
        if (self.deaf and self.speech) or (self.deaf and not self.speech):
            self.controll_mode = "e" # eye only
        elif (not self.deaf and self.speech) or (not self.deaf and not self.speech):
            self.controll_mode = "le" # listen and eye
        else:
            self.controll_mode = None
        
    def get_controll_mode(self):
        return self.controll_mode
    
    def display_message(self,msg):
        if self.get_display_mode() == 's':
            print(msg)
        elif self.get_display_mode() == 'vs':
            print(msg)
            voice_output(msg)
        else:
            return

    def response_message(self):
        if self.get_controll_mode() == 'e':
            msg = eye_direction()
            print(msg)
        elif self.get_controll_mode() == 'le':
            msg = voice_input()
            # msg = eye_direction()
            print(msg)
        else:
            return

with open('conf.json', 'r') as f:
    conf_data = json.load(f)    

deaf = bool(conf_data['configurations']['deaf'])
speech = bool(conf_data['configurations']['speech'])
print(deaf,speech)
pc = PatientChair(deaf=deaf,speech=speech)
pc.set_display_mode()
display_mode = pc.get_display_mode()
pc.set_controll_mode()
controll_mode = pc.get_controll_mode()
pc.display_message("Hello")
pc.response_message()
