import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, Header, Request, HTTPException, status
from fastapi.concurrency import run_in_threadpool
import stripe

router = APIRouter(prefix="/api/v1/billing", tags=["Commercial Monetization"])

# System environmental parameters
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_keys_here")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock_webhook")
PLATFORM_DOMAIN = os.getenv("PLATFORM_DOMAIN", "https://fly.dev")

# Notification Configuration
NOTIFICATION_RECIPIENT = "david@odynexaxis.biz"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.sendgrid.net")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

def send_transaction_email(subject: str, html_body: str):
    """Synchronous worker thread to handle secure outbound system notices via SMTP."""
    if not SMTP_USER or not SMTP_PASS:
        print(f"📧 Notification Skipped (SMTP Credentials Missing) -> Subject: {subject}")
        return
        
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"PokePlap Matrix Gateway <sys-alerts@{PLATFORM_DOMAIN.replace('https://', '')}>"
        msg["To"] = NOTIFICATION_RECIPIENT
        
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(msg["From"], NOTIFICATION_RECIPIENT, msg.as_string())
        print(f"📧 System alert sent successfully to {NOTIFICATION_RECIPIENT}")
    except Exception as e:
        print(f"❌ Failed to dispatch system email: {e}")

@router.post("/webhook")
async def stripe_webhook_handler(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Webhook signature verification rejected.")

    event_type = event['type']
    data_object = event['data']['object']

    if event_type == "checkout.session.completed":
        customer_id = data_object.get("customer")
        sub_id = data_object.get("subscription")
        email = data_object.get("customer_details", {}).get("email", "unknown@domain.com")
        amount = data_object.get("amount_total", 0) / 100
        
        subject = "🎉 Commercial Node Activated: New PokePlap Subscriber"
        body = f"""
        <h2>PokePlap System Provisioning Notice</h2>
        <p>A new institutional node has successfully cleared the payment gateway.</p>
        <ul>
            <li><strong>Customer Email:</strong> {email}</li>
            <li><strong>Customer ID:</strong> {customer_id}</li>
            <li><strong>Subscription ID:</strong> {sub_id}</li>
            <li><strong>Initial Invoice Total:</strong> ${amount:.2f} USD</li>
        </ul>
        <p>Telemetry ledger allocation and isolated container context initialized.</p>
        """
        await run_in_threadpool(send_transaction_email, subject, body)

    elif event_type == "customer.subscription.deleted":
        customer_id = data_object.get("customer")
        sub_id = data_object.get("id")
        
        subject = "🛑 Production Node Deallocated: Subscription Terminated"
        body = f"""
        <h2>PokePlap Lifecycle Termination Alert</h2>
        <p>An active subscription has lapsed or been manually terminated by the customer.</p>
        <ul>
            <li><strong>Customer ID:</strong> {customer_id}</li>
            <li><strong>Subscription ID:</strong> {sub_id}</li>
        </ul>
        <p>Premium time-scrubbing parameters and time-series logging targets are being restricted.</p>
        """
        await run_in_threadpool(send_transaction_email, subject, body)

    return {"status": "event_processed"}
