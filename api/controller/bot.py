import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

# Initialize your LLM and other necessary components
llm = Ollama(model="gemma:2b")

# General purpose prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])


@csrf_exempt  # Disable CSRF (Cross-Site Request Forgery) protection for this view
def process(request) :
    if request.method == 'POST' :
        try :
            # Assuming you're sending data as JSON in the request body
            data = json.loads(request.body)
            user_input = data.get('text', '')  # Adjust according to your JSON structure

            # Assuming prompt_template and llm are defined elsewhere in your code
            prompt_template = "User input: {input}"
            # Example llm function call
            response = llm(prompt_template.format(input=user_input))

            # Assuming StrOutputParser is a class or function to parse the response
            parsed_output = StrOutputParser().parse(response)

            return JsonResponse({'response' : parsed_output})

        except json.JSONDecodeError :
            return JsonResponse({'error' : 'Invalid JSON format in request body'}, status=400)

        except Exception as e :
            return JsonResponse({'error' : str(e)}, status=500)

    return JsonResponse({'error' : 'Method not allowed'}, status=405)

