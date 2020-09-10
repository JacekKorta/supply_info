import requests

client_id  = '392438'
client_secret = 'e37a8de6780a32f3d869286f56954619'

client_id_test  = '145227'
client_secret_test = '12f071174cb7eb79d4aac5bc2f07563f'

client_id_sandbox = '300746'
client_secret_sandbox = '2ee86a66e5d97e3fadc400c9f19b065d'

SITE = 'https://secure.payu.com/'
SANDBOX_SITE = 'https://secure.snd.payu.com/'

# http://developers.payu.com/pl/overview.html#endpoint_reference
RECEIVE_TOKEN_ENDPOINT_POST = 'pl/standard/user/oauth/authorize'  # POST
CREATE_ORDER_POST = '/api/v2_1/orders'



TEST_STRING = {"access_token":"2e23b444-669b-465d-a5ad-43378f394106","token_type":"bearer","expires_in":43199,"grant_type":"client_credentials"}