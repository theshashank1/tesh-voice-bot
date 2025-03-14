import logging
import speech_recognition as sr
from django.http import JsonResponse
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VoiceController :
    def __init__(self, voice_service) :
        self.voice_service = voice_service

    def process_voice(self, request) :
        try :
            if request.method == 'POST' :
                audio_data = request.FILES.get('audio')
                if not audio_data :
                    return JsonResponse({"success" : False, "error" : "No audio file provided"}, status=400)

                # Process the audio using the service
                result = self.voice_service.recognize_speech(audio_data)

                if result["success"] :
                    # Process the recognized text through the bot
                    response = self.voice_service.generate_response(result["text"])
                    return JsonResponse({
                        "success" : True,
                        "text" : result["text"],
                        "response" : response
                    })
                else :
                    return JsonResponse(result, status=400)
            else :
                return JsonResponse({"success" : False, "error" : "Method not allowed"}, status=405)

        except Exception as e :
            logger.error(f"Error processing voice request: {str(e)}")
            return JsonResponse({"success" : False, "error" : "Failed to process voice request"}, status=500)

    def process_text(self, request) :
        try :
            if request.method == 'POST' :
                data = json.loads(request.body)
                text = data.get('text')

                if not text :
                    return JsonResponse({"success" : False, "error" : "No text provided"}, status=400)

                # Process text through the bot
                response = self.voice_service.generate_response(text)
                return JsonResponse({
                    "success" : True,
                    "response" : response
                })
            else :
                return JsonResponse({"success" : False, "error" : "Method not allowed"}, status=405)

        except Exception as e :
            logger.error(f"Error processing text request: {str(e)}")
            return JsonResponse({"success" : False, "error" : "Failed to process text request"}, status=500)