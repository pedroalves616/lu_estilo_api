from fastapi import HTTPException
import httpx
from app.core.config import settings

async def send_whatsapp_message(to_number: str, message: str) -> dict:
    """
    Sends a WhatsApp message to a given number.
    This is a placeholder for actual WhatsApp API integration.
    You'd typically use a provider like Twilio, MessageBird, etc.
    """
    api_url = settings.WHATSAPP_API_URL
    api_token = settings.WHATSAPP_API_TOKEN

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": to_number,
        "message": message
       
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{api_url}/messages", json=payload, headers=headers)
            response.raise_for_status() 
            return response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to WhatsApp API")
    except httpx.HTTPStatusError as e:
        print(f"Error response {e.response.status_code} while requesting {e.request.url!r}: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"WhatsApp API error: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred with WhatsApp API")