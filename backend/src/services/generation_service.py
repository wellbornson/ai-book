from typing import List, Dict, Any
from backend.src.services.cohere_client import cohere_client


class GenerationService:
    """
    Service for generating responses using Cohere's Command R/R+ model
    """
    
    def __init__(self):
        pass
    
    def generate_response(
        self, 
        query: str, 
        context: List[Dict[str, Any]], 
        max_tokens: int = 300
    ) -> Dict[str, Any]:
        """
        Generate a response based on the query and context
        """
        # Format the context for the LLM
        context_str = "\n\n".join([item["content"] for item in context])
        
        # Create the prompt for the model
        prompt = f"""
        You are a helpful assistant that answers questions based on provided book content.
        Only use the information provided in the context below to answer the question.
        Do not make up information that is not in the context.
        If the answer is not available in the context, clearly state that.
        
        Context:
        {context_str}
        
        Question: {query}
        
        Answer (with citations to specific book sections):
        """
        
        # Generate the response
        response_text = cohere_client.generate_response(prompt, max_tokens=max_tokens)
        
        # Extract citations from the context
        citations = []
        for item in context:
            citations.append({
                "source_location": item.get("source_location", ""),
                "content": item.get("content", "")[:200] + "..."  # Truncate for brevity
            })
        
        return {
            "response_text": response_text,
            "citations": citations
        }


# Create a singleton instance
generation_service = GenerationService()