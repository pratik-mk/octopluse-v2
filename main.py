from zerodha.login import ZerodhaSession

# Create a session object
session = ZerodhaSession()

# Access token
token = session.get_access_token()

# KiteConnect instance
kite = session.get_kite_session()
print(kite.holdings())
