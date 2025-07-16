from fastapi import APIRouter, Depends
from typing import List

from app.api.deps import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat import ChatMessage, ChatResponse, ChatHistoryItem

router = APIRouter()

@router.post("", response_model=ChatResponse, tags=["Chat"])
def process_chat_message(message: ChatMessage, current_user: dict = Depends(get_current_user)):
    """
    Handles an incoming chat message, invokes the RAG service,
    and saves the interaction to the database.
    """
    final_response = ChatService.process_message(
        message.message, 
        message.document_ids, 
        message.session_id, 
        current_user['username']
    )
    
    return ChatResponse(response=final_response)

@router.get("/history/{session_id}", response_model=List[ChatHistoryItem], tags=["Chat"])
def get_chat_session_history(session_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves the chat history for a specific session ID belonging to the current user.
    """
    return ChatService.get_session_history(session_id, current_user['username'])
