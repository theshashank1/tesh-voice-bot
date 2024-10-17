import json
import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()


class ModelHandler :
    def __init__(self) :
        """Initialize model configurations"""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

        # Initialize models using LangChain's chat models
        self.models = {
            "ollama": ChatOllama(model="gemma:2b"),
            "gemini": ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=self.google_api_key,
                temperature=0.7,
                convert_system_message_to_human=True
            )
        }

        # Create separate prompt templates for each model
        self.prompts = {
            "ollama": ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant, your name is TESH"),
                ("user", "{input}")
            ]),
            "gemini": ChatPromptTemplate.from_messages([
                ("human", "You are a helpful assistant, your name is TESH. Remember this role."),
                ("user", "{input}")
            ])
        }

        # Initialize output parser
        self.parser = StrOutputParser()

    def remove_chars(self, text: str) -> str :
        """Removes * and # characters from the given text."""
        return text.replace('*', '').replace('#', '')

    def create_chain(self, model_name: str) :
        """Create a LangChain chain for the specified model."""
        if model_name not in self.models :
            raise ValueError(f"Model {model_name} not supported")

        return (
                self.prompts[model_name] |
                self.models[model_name] |
                self.parser |
                self.remove_chars
        )

    def process_input(self, data: str, model_name: str) -> str :
        """Process input using the specified model.

        Args:
            data: Input text to process
            model_name: Name of the model to use ('ollama' or 'gemini')

        Returns:
            Processed response from the model
        """
        try :
            chain = self.create_chain(model_name)
            return chain.invoke({"input": data})
        except Exception as e :
            return f"{model_name.capitalize()} Error: {str(e)}"


def process_with_ollama(data: str) -> str :
    """Process input using Ollama model."""
    handler = ModelHandler()
    return handler.process_input(data, "ollama")


def process_with_gemini(data: str) -> str:
    """Process input using Gemini model."""
    handler = ModelHandler()
    return handler.process_input(data, "gemini")


if __name__ == "__main__" :
    test_input = "What is your name?"

    # Test Ollama
    print("Ollama response:")
    print(process_with_ollama(test_input))

    # Test Gemini
    print("\nGemini response:")
    print(process_with_gemini(test_input))