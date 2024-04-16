# module contains class required for gemini model
import os
import google.generativeai as genai
import openai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

genai.configure(api_key=os.getenv("GGEMINI_API_KEY"))

class GeminiLLM:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = ChatGoogleGenerativeAI(model="gemini-pro",
                                            google_api_key=self.api_key,
                                            convert_system_message_to_human=True,
                                            temperature=0.0)
    
    def get_response(self, question):
        """used to generate response from Gemini model

        Args:
            question (string): question we want to ask gemini

        Returns:
            string: response from gemini
        """
        return self.model.invoke(question)