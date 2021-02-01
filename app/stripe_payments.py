import stripe
from os import environ

stripe.api_key = environ.get('STRIPE_API_KEY')

def account_setup(email):
    account = stripe.Account.create(
        type='express',
        email=email,
        )
    
    account_links = stripe.AccountLink.create(
    account=account['id'],
    refresh_url=environ.get('SITE_URL') + '/stripe/link',
    return_url=environ.get('SITE_URL') + '/stripe/link/validate',
    type='account_onboarding',
    )

    return [account['id'], account_links['url']]

def account_query(acc_id):
    return stripe.Account.retrieve(acc_id)

def create_checkout(acc_id, price, product, currency, user):
    create = stripe.checkout.Session.create(
        shipping_address_collection={
            'allowed_countries': ['US', 'CA', 'GB']
        },
        client_reference_id=user,
        payment_method_types=['card'],
        line_items=[{
            'name': product,
            'amount': price,
            'currency': currency,
            'quantity' : 1
        }],
        payment_intent_data={
            'transfer_data': {
            'destination': acc_id,
        },
        },
        success_url=environ.get('SITE_URL') + '/create/order',
        cancel_url=environ.get('SITE_URL') + f'/cancel/order/{user}',
    )
    return create['id']

def retrieve_order(sessionId):
    return stripe.checkout.Session.retrieve(sessionId)