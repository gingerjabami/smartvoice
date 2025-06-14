import speech_recognition as sr
import pyttsx3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from spacy.matcher import Matcher
import time
import nltk

# Ensure VADER lexicon is downloaded
nltk.download('vader_lexicon')


class SmartVoice:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
        except OSError:
            print("Microphone not found. Please check your audio input device.")
            exit()

        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Load spaCy NLP model
        self.nlp = spacy.load("en_core_web_sm")

        # Initialize intent matcher
        self.matcher = Matcher(self.nlp.vocab)
        self._setup_intent_patterns()

        # User context
        self.user_context = {
            'previous_commands': [],
            'preferences': {}
        }

    def _setup_intent_patterns(self):
        # Define patterns with LEMMA
        alarm_pattern = [{"LEMMA": "set"}, {"LEMMA": "alarm"}]
        reminder_pattern = [{"LEMMA": "remind"}, {"LEMMA": "me"}]
        music_pattern = [{"LEMMA": "play"}, {"LEMMA": {"IN": ["music", "song"]}}]

        frustration_patterns = [
            [{"LOWER": "why"}, {"LOWER": "can't"}, {"LOWER": "you"}],
            [{"LOWER": "you"}, {"LOWER": "never"}, {"LOWER": "understand"}]
        ]

        self.matcher.add("SET_ALARM", [alarm_pattern])
        self.matcher.add("SET_REMINDER", [reminder_pattern])
        self.matcher.add("PLAY_MUSIC", [music_pattern])
        self.matcher.add("FRUSTRATION", frustration_patterns)

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                print(f"User said: {text}")
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def analyze_sentiment(self, text):
        return self.sentiment_analyzer.polarity_scores(text)

    def recognize_intent(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        if matches:
            # Return first matching intent
            match_id, _, _ = matches[0]
            return self.nlp.vocab.strings[match_id]
        return None

    def generate_response(self, text):
        sentiment = self.analyze_sentiment(text)
        is_negative = sentiment['compound'] < -0.2
        intent = self.recognize_intent(text)

        self.user_context['previous_commands'].append({
            'text': text,
            'intent': intent,
            'sentiment': sentiment,
            'timestamp': time.time()
        })

        if is_negative:
            return self._handle_negative_sentiment(intent)
        elif intent == "SET_ALARM":
            return "I'll set an alarm for you. For what time should I set it?"
        elif intent == "SET_REMINDER":
            return "I can remind you. What should I remind you about and when?"
        elif intent == "PLAY_MUSIC":
            return "Playing some relaxing music for you."
        elif intent == "FRUSTRATION":
            return "I'm sorry you're having trouble. Could you rephrase your request?"
        else:
            return "I'm not sure I understand. Could you please repeat that?"

    def _handle_negative_sentiment(self, intent):
        if intent:
            return f"I sense some frustration with {intent.replace('_', ' ').lower()}. Let’s work on that together."
        return "I'm sorry you're having trouble. Tell me more so I can assist you better."

    def run(self):
        self.speak("Hello! I'm SmartVoice. How can I help you today?")

        while True:
            text = self.listen()
            if text:
                if text.lower() in ["quit", "exit", "stop", "goodbye"]:
                    self.speak("Goodbye! Have a nice day.")
                    break

                response = self.generate_response(text)
                self.speak(response)
            else:
                self.speak("I didn't catch that. Could you repeat, please?")


if __name__ == "__main__":
    assistant = SmartVoice()
    assistant.run()
