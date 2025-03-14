import logging
import speech_recognition as sr
import json
import time
from django.http import JsonResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VoiceController :
    def __init__(self, voice_service) :
        self.voice_service = voice_service

    def process_voice(self, request) :
        try :
            # Add timeout handling for long-running requests
            start_time = time.time()
            timeout = 15  # seconds

            audio_data = request.FILES.get('audio')
            if not audio_data :
                return JsonResponse({"success" : False, "error" : "No audio file provided"}, status=400)

            # Check file size to prevent large file uploads
            if audio_data.size > 10 * 1024 * 1024 :  # 10MB limit
                return JsonResponse({"success" : False, "error" : "Audio file too large"}, status=413)

            # Process the audio
            result = self.voice_service.recognize_speech(audio_data)

            # Check for timeout
            if time.time() - start_time > timeout :
                return JsonResponse({"success" : False, "error" : "Request timed out"}, status=408)

            if result["success"] :
                response = self.voice_service.generate_response(result["text"])
                return JsonResponse({
                    "success" : True,
                    "text" : result["text"],
                    "response" : response
                })
            else :
                return JsonResponse(result, status=400)

        except Exception as e :
            logger.error(f"Error processing voice request: {str(e)}")
            return JsonResponse({"success" : False, "error" : "Failed to process voice request"}, status=500)

    def process_text(self, request) :
        """Process text input instead of voice"""
        try :
            if request.method != 'POST' :
                return JsonResponse({"success" : False, "error" : "Method not allowed"}, status=405)

            data = json.loads(request.body)
            text = data.get('text')

            if not text :
                return JsonResponse({"success" : False, "error" : "No text provided"}, status=400)

            # Process through the bot service
            response = self.voice_service.generate_response(text)
            return JsonResponse({
                "success" : True,
                "response" : response
            })

        except json.JSONDecodeError :
            return JsonResponse({"success" : False, "error" : "Invalid JSON"}, status=400)
        except Exception as e :
            logger.error(f"Error processing text request: {str(e)}")
            return JsonResponse({"success" : False, "error" : "Failed to process text request"}, status=500)