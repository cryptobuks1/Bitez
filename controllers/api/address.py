# TODO: add a label to each address
from flask_restful import Resource, abort
from flask import request, jsonify
from mongoengine import connect
from config import DB_HOST, DB_PORT, DB_CLIENT
from services.dbconfig import Database
from resources.btc.network import btc_network
from resources.btc.generate import GenerateBtcKey
from resources.btc.prkey import encrypt
from models.wallet import Wallet, BtcWallet
from services.api_calls import use_api_key

# init db
client = Database()
db = client.light()

# init mongoengine
connect(DB_CLIENT, host=DB_HOST, port=DB_PORT, retryWrites=False)

class GenerateAddr(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            btc_key = GenerateBtcKey()
            btc_std_addr = btc_key.generate_std_addr()
            btc_wit_addr = btc_key.generate_wit_addr()
            btc_prkey = btc_key.generate_prkey()
            # encrypt and save prkey
            btc_prkey = encrypt(btc_prkey)
            btc_wallet = BtcWallet(
                    std_address = btc_std_addr,
                    wit_address = btc_wit_addr,
                    prkey = btc_prkey
                    )
            wallet = Wallet.objects.get(username="merwane")
            wallet.btc_wallet.append(btc_wallet)
            wallet.save()
            # reponse
            response = {
                    "network": "BTC",
                    "address": btc_std_addr,
                    "wit_address": btc_wit_addr
                    }
        else:
            abort(404, message="currency not found")
        return jsonify(status="success", data=response)


class GetAllAddr(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'btc_wallet.prkey': False})
            user_addr = []
            for addr in wallet['btc_wallet']:
                user_addr.append(addr)
        else:
            abort(404, message="currency not found")
        return jsonify(addresses=user_addr)
