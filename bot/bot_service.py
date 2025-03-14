import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class BotService :
    def __init__(self) :
        self.default_responses = {
            "greeting" : ["Hello! How can I help you?", "Hi there! What can I do for you?",
                          "Welcome! How may I assist you today?"],
            "farewell" : ["Goodbye! Have a great day!", "See you later!",
                          "Until next time! Take care!"],
            "fallback" : ["I'm not sure I understand. Could you rephrase that?",
                          "I didn't catch that. Can you say it differently?",
                          "I'm still learning. Could you try asking in a different way?"]
        }

    def process_message(self, message) :
        """Process incoming message and return appropriate response"""
        try :
            logger.info(f"Processing message: {message}")

            # Simple keyword-based response (replace with more sophisticated NLP)
            message = message.lower()

            if any(word in message for word in ["hello", "hi", "hey", "greetings"]) :
                return random.choice(self.default_responses["greeting"])

            elif any(word in message for word in ["bye", "goodbye", "see you", "later"]) :
                return random.choice(self.default_responses["farewell"])

            elif any(word in message for word in ["time", "what time", "current time"]) :
                return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

            elif any(word in message for word in ["date", "what date", "today", "day"]) :
                return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"

            elif any(word in message for word in ["who are you", "your name", "about you"]) :
                return "I am TESH, a voice assistant designed to help you with various tasks."

            elif any(word in message for word in ["thank", "thanks", "appreciate"]) :
                return "You're welcome! Is there anything else I can help you with?"

            elif any(word in message for word in ["weather", "forecast", "temperature"]) :
                return "I'm sorry, I don't have access to weather information yet. This feature will be available soon."

            # Add more custom responses here

            # Fallback response
            return random.choice(self.default_responses["fallback"])

        except Exception as e :
            logger.error(f"Error processing message: {str(e)}")
            return "I'm having trouble processing your request right now."