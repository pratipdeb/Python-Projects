import datetime
import subprocess
import webbrowser
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return ""


def main():
    speak("Hello! Jarvis is online.")

    while True:
        query = listen_command()

        if not query:
            continue

        # Basic greetings
        if "hello" in query or "hey" in query:
            speak("Hello! How can I help you?")

        # Time check
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Web utilities
        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "search" in query:
            search_term = query.replace("search", "").strip()
            if search_term:
                speak(f"Searching Google for {search_term}")
                webbrowser.open(
                    f"https://www.google.com/search?q={search_term}"
                )
            else:
                speak("What would you like me to search for?")

        # System actions
        elif "open notepad" in query:
            speak("Opening Notepad")
            subprocess.Popen(["notepad"]) 

        elif "open calculator" in query:
            speak("Opening Calculator")
            subprocess.Popen(["calc"])

        # Exit
        elif "exit" in query or "stop" in query or "quit" in query:
            speak("Shutting down. Have a good day!")
            break


if __name__ == "__main__":
    main()