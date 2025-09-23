from zerodha.login import ZerodhaSession
from db.base import SessionLocal, engine
from db.models import Base, Holding
from datetime import datetime

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def fetch_and_store_filtered_holdings():
    """
    Fetch holdings from Zerodha, filter required fields, round numerical values, 
    and store/update in DB.
    """
    session = SessionLocal()
    try:
        zerodha_session = ZerodhaSession()
        kite = zerodha_session.get_kite_session()

        holdings_data = kite.holdings()  # list of holdings

        for h in holdings_data:
            trading_symbol = h.get("tradingsymbol")
            exchange = h.get("exchange")
            instrument_token = h.get("instrument_token")
            product = h.get("product")
            quantity = round(h.get("quantity", 0), 3)
            avg_price = round(h.get("average_price", 0), 3)
            pnl = round(h.get("pnl", 0), 3)
            pnl_percentage = round((pnl / (quantity * avg_price) * 100) if quantity and avg_price else 0, 3)
            created_at = datetime.utcnow()
            last_updated = datetime.utcnow()
            comments = None

            # Check if holding exists
            holding = session.query(Holding).filter_by(instrument_token=instrument_token).first()

            if holding:
                # Update existing record
                holding.trading_symbol = trading_symbol
                holding.exchange = exchange
                holding.product = product
                holding.quantity = quantity
                holding.avg_price = avg_price
                holding.pnl = pnl
                holding.pnl_percentage = pnl_percentage
                holding.last_updated = last_updated
            else:
                # Insert new record
                new_holding = Holding(
                    trading_symbol=trading_symbol,
                    exchange=exchange,
                    instrument_token=instrument_token,
                    product=product,
                    quantity=quantity,
                    avg_price=avg_price,
                    pnl=pnl,
                    pnl_percentage=pnl_percentage,
                    created_at=created_at,
                    last_updated=last_updated,
                    comments=comments
                )
                session.add(new_holding)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
