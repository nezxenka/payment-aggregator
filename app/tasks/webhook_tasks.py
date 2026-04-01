import httpx
import json
import hmac
import hashlib
from datetime import datetime

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.webhook import WebhookLog, WebhookEndpoint


@celery_app.task(bind=True, max_retries=3)
def send_webhook(self, endpoint_id: int, event_type: str, payload: dict):
    """Отправка вебхука с retry логикой"""
    
    db = SessionLocal()
    try:
        endpoint = db.query(WebhookEndpoint).filter(WebhookEndpoint.id == endpoint_id).first()
        if not endpoint or not endpoint.is_active:
            return
        
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            endpoint.secret.encode(),
            payload_json.encode(),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Event-Type": event_type
        }
        
        with httpx.Client(timeout=10.0) as client:
            response = client.post(endpoint.url, json=payload, headers=headers)
        
        log = WebhookLog(
            endpoint_id=endpoint_id,
            event_type=event_type,
            payload=payload_json,
            response_status=response.status_code,
            response_body=response.text[:1000],
            success=response.status_code < 300,
            attempts=self.request.retries + 1
        )
        db.add(log)
        db.commit()
        
        if response.status_code >= 300:
            raise Exception(f"Webhook failed with status {response.status_code}")
            
    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
    finally:
        db.close()
