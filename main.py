# from zerodha.login import ZerodhaSession

# # Create a session object
# session = ZerodhaSession()

# # Access token
# token = session.get_access_token()

# # KiteConnect instance
# kite = session.get_kite_session()
# print(kite.holdings())


from services.holdings_service import fetch_and_store_filtered_holdings
from db.base import SessionLocal
from db.models import Holding

# Fetch and store only filtered holdings
fetch_and_store_filtered_holdings()

# Check database contents
session = SessionLocal()
holdings = session.query(Holding).all()
for h in holdings:
    print(h.trading_symbol, h.quantity, h.avg_price, h.pnl, h.pnl_percentage)
session.close()
