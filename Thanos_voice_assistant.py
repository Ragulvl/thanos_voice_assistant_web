import openai
import speech_recognition as sr
import pyttsx3
import os
from deep_translator import GoogleTranslator  # Replacing googletrans

recognizer = sr.Recognizer()
engine = pyttsx3.init()

language_codes = {
    'english': 'en',
    'french': 'fr',
    'spanish': 'es',
    'german': 'de',
    'italian': 'it',
    'japanese': 'ja',
    'chinese': 'zh-cn',
    'russian': 'ru',
    'hindi': 'hi',
    'arabic': 'ar'
}

language_names = {v: k.capitalize() for k, v in language_codes.items()}

# Text-to-Speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to interact with OpenAI API
def chat_with_gpt(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Using GPT-3
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Translation Function using deep_translator
def translate_text(text, dest_language_code):
    try:
        language_name = language_names.get(dest_language_code, dest_language_code.capitalize())
        translation = GoogleTranslator(source='auto', target=dest_language_code).translate(text)
        speak(f"The translation in {language_name} is: {translation}")
        return f"Original text: {text}, Translated text: {translation}"
    except Exception as e:
        return f"Error during translation: {e}"

# App opening function
def open_app(app_name):
    apps = {
        'microsoft word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        'microsoft excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        'notepad': r"C:\Windows\system32\notepad.exe",
        'calculator': r"C:\Windows\System32\calc.exe",
        'paint': r"C:\Windows\System32\mspaint.exe",
        'file explorer': r"C:\Windows\explorer.exe",
        'vlc': r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        'spotify': r"C:\Users\<YourUsername>\AppData\Roaming\Spotify\Spotify.exe",
        'edge browser': r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    }

    if app_name in apps:
        os.startfile(apps[app_name])
        return f"Opening {app_name}."
    else:
        return f"Sorry, I can't open {app_name}."

# Respond to voice commands
def respond_to_command(command, api_key):
    command = command.lower()

    if 'translate' in command:
        try:
            to_translate = command.split('translate')[-1].split('to')[0].strip()
            dest_language_name = command.split('to')[-1].strip().lower()

            if dest_language_name in language_codes:
                dest_language_code = language_codes[dest_language_name]
                return translate_text(to_translate, dest_language_code)
            else:
                return f"Sorry, I don't know how to translate to {dest_language_name}. Please try another language."
        except IndexError:
            return "Please specify the text and the language for translation."
        except Exception as e:
            return f"Error in translation processing: {e}"

    elif 'open' in command:
        app_name = command.split('open')[-1].strip().lower()
        return open_app(app_name)

    else:
        # Default behavior is to pass the command to ChatGPT for processing
        return chat_with_gpt(command, api_key)

# Main voice listening loop
def listen_for_commands(api_key):
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language='en-IN')
                print(f"You said: {command}")
                response = respond_to_command(command, api_key)
                print(f"Response: {response}")
                speak(response)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                speak("Network error. Please check your connection.")

# Main function
def main():
    api_key = "your_openai_api_key"  # Replace with your OpenAI API key
    speak("Hello! How can I assist you today?")
    listen_for_commands(api_key)

if __name__ == "__main__":
    main()
