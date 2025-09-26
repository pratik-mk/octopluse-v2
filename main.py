# from zerodha.login import ZerodhaSession

# # Create a session object
# session = ZerodhaSession()

# # Access token
# token = session.get_access_token()

# # KiteConnect instance
# kite = session.get_kite_session()
# print(kite.holdings())


# from services.holdings_service import fetch_and_store_filtered_holdings
# from db.base import SessionLocal
# from db.models import Holding

# # Fetch and store only filtered holdings
# fetch_and_store_filtered_holdings()

# # Check database contents
# session = SessionLocal()
# holdings = session.query(Holding).all()
# for h in holdings:
#     print(h.trading_symbol, h.quantity, h.avg_price, h.pnl, h.pnl_percentage)
# session.close()



# angel login.py
from angel.login import AngelSession

session = AngelSession()
print("🎉 Angel SmartConnect session ready!")

# Tokens
print("JWT:", session.get_access_token())
print("Feed:", session.get_feed_token())
print("Refresh:", session.get_refresh_token())

# SmartConnect object
smart_api = session.get_smart_api()

# ✅ Correct way — use jwtToken
print("Profile (via session):", session.get_profile())
print("Profile (direct):", smart_api.getProfile(session.get_access_token()))
