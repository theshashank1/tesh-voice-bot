import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
import langsmith

# Initialize your LLM and other necessary components
llm = Ollama(model="gemma:2b")  # Replace with the correct Gemini model

# General purpose prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant, your name is TESH"),
    ("user", "{input}")
])

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage




def remove_chars(text):
  """Removes * and # characters from the given text.

  Args:
    text: The input text.

  Returns:
    The cleaned text.
  """

  cleaned_text = text.replace('*', '').replace('#', '')
  return cleaned_text


@langsmith.traceable
def process_handler(data):
    prompt_template.invoke(input = data)
    parser = StrOutputParser()
    chain = prompt_template | llm | parser | remove_chars

    return chain.invoke(data)

if __name__ == "__main__":
    print(process_handler("What is your name?"))
