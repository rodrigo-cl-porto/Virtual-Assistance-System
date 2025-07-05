from datetime import datetime
from gtts import gTTS
from deep_translator import GoogleTranslator
from IPython.display import Audio
from pygame import mixer
import speech_recognition as sr
import os
import wikipedia
import webbrowser
import winshell

class VirtualAssistanceSystem:

    __my_voice_path = '.content/assistant_voice.mp3'
    __music_dir = "C:/Users/UserName/Downloads/Music/" #add your music directory here..

    def __init__(self, lang='en'):
        self.said = ''
        self.lang = lang

    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            self.said = ''
            try:
                self.said  = r.recognize_google(audio)
                print(self.said)
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't get that.")
            except sr.RequestError:
                self.speak("Sorry, the service is not available")
        return self.said.lower()

    def speak(self, text:str):
        text_to_speech = gTTS(text=text, lang=self.lang)
        filename = VirtualAssistanceSystem.__my_voice_path
        try:
            os.remove()
        except OSError:
            pass
        text_to_speech.save(filename)
        Audio(filename)

    def __search_video(self):
        self.speak("What do you want to search for?")
        keyword = self.get_audio()
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            self.speak(f"Here is what I have found for {keyword} on youtube")

    def __search_wikipedia(self):
        self.speak("What do you want to search for?")
        query = self.get_audio()
        if query != '':
            result = wikipedia.summary(query, sentences=3)
            self.speak("According to wikipedia...")
            print(result)
            self.speak(result)

    def __empty_recycle_bin(self):
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        self.speak("Recycle bin emptied")

    def __say_time(self):
        str_time = datetime.today().strftime("%H:%M %p")
        print(str_time)
        self.speak(str_time)

    def __play_music(self):
        self.speak("Now playing...")
        music_dir = VirtualAssistanceSystem.__music_dir
        songs = os.listdir(music_dir)
        print(songs)

        if len(songs) > 0:
            song = music_dir + "/" + songs[0]
            mixer.init()
            mixer.music.load(song)
            mixer.music.play()
        else:
            raise FileNotFoundError("You don't have any music to play!")

    def __stop_music(self):
        self.speak("Stopping playback.")
        mixer.music.stop()

    def __translate(self):
        self.speak("Say what you want to translate.")
        text = self.get_audio()
        translator = GoogleTranslator(source='auto', target=self.lang)
        translation = translator.translate(text=text)
        print(translation)
        self.speak(translation)

    def __exit(self):
        self.speak("Goodbye, till next time")
        exit()

    #function to respond to commands
    def respond(self, text:str):
        print(f'Text from the audio: "{text}"')
        if 'youtube' in text:
            self.__search_video()
        elif 'search' in text:
            self.__search_wikipedia()
        elif 'empty recycle bin' in text:
            self.__empty_recycle_bin()
        elif 'what time' in text:
            self.__say_time()
        elif 'play music' in text or 'play song' in text:
            self.__play_music()
        elif 'stop music' in text:
            self.__stop_music()
        elif 'translate' in text:
            self.__translate()
        elif 'exit' in text:
            self.__exit()

if __name__ == "__main__":
    while True:
        vas = VirtualAssistanceSystem()
        text = vas.get_audio()
        vas.respond(text)