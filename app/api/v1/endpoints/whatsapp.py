from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.core.security import has_role
from app.services import whatsapp as whatsapp_service

router = APIRouter()

class WhatsAppMessage(BaseModel):
    to_number: str = Field(..., example="+5511987654321", description="Recipient's WhatsApp number with country code")
    message: str = Field(..., example="Your order #123 has been shipped!", description="Message to send")

@router.post("/send", status_code=status.HTTP_200_OK)
async def send_whatsapp_message_endpoint(
    message_data: WhatsAppMessage,
    current_user: Any = Depends(has_role(["admin", "regular"])) # Only authorized users can send messages
) -> Any:
    """
    Implement additional functionality in the API that allows sending WhatsApp messages to clients using WhatsApp API[cite: 5].
    This can be triggered by commercial events like new orders, quote submissions, or promotions[cite: 4].
    """
    try:
        response = await whatsapp_service.send_whatsapp_message(
            to_number=message_data.to_number,
            message=message_data.message
        )
        return {"status": "success", "message": "WhatsApp message sent", "details": response}
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WhatsApp message: {e}")