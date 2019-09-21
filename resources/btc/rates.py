from bit.network import satoshi_to_currency_cached, currency_to_satoshi_cached

def btc_to_fiat(amount, currency):
    amount = amount * (10**8)
    conversion = satoshi_to_currency_cached(amount, currency)
    return conversion

def fiat_to_btc(amount, currency):
    conversion = currency_to_satoshi_cached(amount, currency)
    conversion = conversion / (10**8)
    return conversion
