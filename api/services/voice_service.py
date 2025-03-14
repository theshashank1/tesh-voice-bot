import speech_recognition as sr
import logging
from pathlib import Path
import tempfile
import os

logger = logging.getLogger(__name__)


class VoiceService :
    def __init__(self, bot_service) :
        self.recognizer = sr.Recognizer()
        self.bot_service = bot_service

    def recognize_speech(self, audio_file) :
        """Convert speech to text with improved error handling"""
        temp_path = None
        try :
            # Save the audio file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio :
                for chunk in audio_file.chunks() :
                    temp_audio.write(chunk)
                temp_path = temp_audio.name

            # Use the speech recognition library
            with sr.AudioFile(temp_path) as source :
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)

            return {"success" : True, "text" : text}

        except sr.UnknownValueError :
            logger.warning("Speech recognition could not understand audio")
            return {"success" : False, "error" : "Could not understand audio"}

        except sr.RequestError as e :
            logger.error(f"Speech recognition service error: {e}")
            return {"success" : False, "error" : f"Speech service error: {e}"}

        except Exception as e :
            logger.error(f"Unexpected error in speech recognition: {e}")
            return {"success" : False, "error" : "Failed to process audio"}
        finally :
            # Clean up temp file
            if temp_path and os.path.exists(temp_path) :
                os.unlink(temp_path)

    def generate_response(self, text) :
        """Generate bot response from text input"""
        return self.bot_service.process_message(text)