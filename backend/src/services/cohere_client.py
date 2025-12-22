import cohere
from backend.src.config.settings import settings
from typing import List, Dict, Any
import random


class CohereClient:
    """
    Cohere API client wrapper for embeddings and generation
    """

    def __init__(self):
        # Check if API key is provided
        if not settings.cohere_api_key or settings.cohere_api_key == "your_cohere_api_key_here":
            print("Cohere API key not provided, using mock implementation for development")
            self.client = None
            self.use_mock = True
        else:
            self.client = cohere.Client(settings.cohere_api_key)
            self.use_mock = False
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of documents
        """
        if self.use_mock:
            # Return mock embeddings (1024 dimensions as specified in the requirements)
            return [[random.random() for _ in range(1024)] for _ in texts]
        else:
            response = self.client.embed(
                texts=texts,
                model='embed-english-v3.0',  # Using the embed-english-v3.0 model as specified
                input_type="search_document"  # Proper input_type for documents
            )
            return response.embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Create embeddings for a query
        """
        if self.use_mock:
            # Return mock embedding (1024 dimensions as specified in the requirements)
            return [random.random() for _ in range(1024)]
        else:
            response = self.client.embed(
                texts=[query],
                model='embed-english-v3.0',  # Using the embed-english-v3.0 model as specified
                input_type="search_query"  # Proper input_type for queries
            )
            return response.embeddings[0]

    def generate_response(self, prompt: str, max_tokens: int = 300) -> str:
        """
        Generate a response using Cohere's Command R+ model
        """
        if self.use_mock:
            # Return mock response
            return f"Mock response to: {prompt[:50]}..."
        else:
            response = self.client.generate(
                model='command-r-plus',  # Using Command R+ model as specified
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.3,  # Lower temperature for more factual responses
            )

            if response.generations:
                return response.generations[0].text
            else:
                raise Exception("No response generated from Cohere")

    def chat(self, message: str, chat_history: List[Dict[str, str]] = None) -> str:
        """
        Conduct a chat conversation using Cohere's chat model
        """
        if self.use_mock:
            # Return mock chat response
            return f"Mock chat response to: {message[:50]}..."
        else:
            response = self.client.chat(
                message=message,
                chat_history=chat_history or [],
                model='command-r-plus',  # Using Command R+ model as specified
                temperature=0.3,  # Lower temperature for more factual responses
            )

            return response.text


# Create a singleton instance
cohere_client = CohereClient()