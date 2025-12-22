from typing import Dict, Any
from backend.src.services.retrieval_service import retrieval_service
from backend.src.services.generation_service import generation_service
from backend.src.utils.error_handler import QueryProcessingError


class RAGService:
    """
    Main RAG service that orchestrates retrieval and generation
    """

    def __init__(self):
        pass

    def process_query(
        self,
        query_text: str,
        query_mode: str = "full-book",
        session_id: str = None,
        selected_text: str = None,
        top_k: int = 4,
        max_tokens: int = 300
    ) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline
        """
        try:
            # Retrieve relevant context based on the query
            context = retrieval_service.retrieve_relevant_context(
                query=query_text,
                top_k=top_k,
                query_mode=query_mode,
                selected_text=selected_text
            )

            # Generate a response based on the context
            generation_result = generation_service.generate_response(
                query=query_text,
                context=context,
                max_tokens=max_tokens
            )

            # Return the complete response with citations
            return {
                "response_id": f"resp_{session_id}_{len(query_text)}" if session_id else "resp_temp",
                "response_text": generation_result["response_text"],
                "citations": generation_result["citations"],
                "query_mode": query_mode,
                "context_used": len(context)
            }

        except Exception as e:
            raise QueryProcessingError(f"Error processing query: {str(e)}")


# Create a singleton instance
rag_service = RAGService()