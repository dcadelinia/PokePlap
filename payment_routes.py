import os
import json
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Header, Request, status
from fastapi.responses import RedirectResponse
from fastapi.concurrency import run_in_threadpool
import stripe

# Initialize router for explicit platform mounting
router = APIRouter(prefix="/api/v1/billing", tags=["Commercial Monetization"])

# Pull secrets from your Fly.io encrypted environment configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_keys_here")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock_webhook")
PLATFORM_DOMAIN = os.getenv("PLATFORM_DOMAIN", "https://fly.dev")

# Map your commercial product pricing IDs from your Stripe dashboard
SUBSCRIPTION_TIERS = {
    "professional": os.getenv("STRIPE_PRICE_PROFESSIONAL", "price_mock_prof_123"),
    "enterprise": os.getenv("STRIPE_PRICE_ENTERPRISE", "price_mock_ent_456")
}

@router.post("/checkout/session")
async def create_checkout_session(tier: str, request: Request):
    """
    Spins up an automated checkout session for prospective clinical accounts.
    Redirects buyers directly to Stripe's secure PCI-compliant gateway.
    """
    if tier not in SUBSCRIPTION_TIERS:
        raise HTTPException(status_code=400, detail="Invalid target subscription tier.")
        
    try:
        # Generate session routing matrices using thread pool
        session = await run_in_threadpool(
            stripe.checkout.Session.create,
            payment_method_types=['card'],
            line_items=[{
                'price': SUBSCRIPTION_TIERS[tier],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{PLATFORM_DOMAIN}/dashboard?session_id={{CHECKOUT_SESSION_ID}}&billing_status=success",
            cancel_url=f"{PLATFORM_DOMAIN}/pricing?billing_status=cancelled",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stripe Session Generation Error: {str(e)}")

@router.post("/portal")
async def create_billing_portal(customer_id: str):
    """
    Generates a secure self-service billing link.
    Allows hospital administrators to upgrade, downgrade, or cancel tiers.
    """
    try:
        portal_session = await run_in_threadpool(
            stripe.billing_portal.Session.create,
            customer=customer_id,
            return_url=f"{PLATFORM_DOMAIN}/dashboard"
        )
        return {"url": portal_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portal Generation Failure: {str(e)}")

@router.post("/webhook")
async def stripe_webhook_handler(request: Request, stripe_signature: str = Header(None)):
    """
    Asynchronous transaction listener endpoint.
    Intercepts raw webhooks from Stripe to activate/deactivate simulation features instantly.
    """
    payload = await request.body()
    
    try:
        # Securely verify payload origins using webhook signatures
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload signature metadata.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Signature verification rejected.")

    event_type = event['type']
    data_object = event['data']['object']

    # --- HANDLE COMMERCIAL ENTITY EVENTS ---
    if event_type == "checkout.session.completed":
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription")
        print(f"💰 Checkout Complete! Account Customer ID: {customer_id} | Sub: {subscription_id}")
        # TODO: Link your internal database to map account subscription state -> True

    elif event_type == "customer.subscription.deleted":
        customer_id = data_object.get("customer")
        print(f"🛑 Subscription terminated or lapsed for customer: {customer_id}")
        # TODO: Lock premium digital twin timeline features for this clinician group

    return {"status": "event_processed"}
