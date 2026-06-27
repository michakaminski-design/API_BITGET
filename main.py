import os
import ccxt

def fetch_live_prices():
    BG_KEY = os.getenv('BG_KEY')
    BG_SECRET = os.getenv('BG_SECRET')
    BG_PASS = os.getenv('BG_PASS')

    if not all([BG_KEY, BG_SECRET, BG_PASS]):
        print("BŁĄD: Brak kluczy API w zmiennych środowiskowych Rendera!")
        return

    try:
        exchange = ccxt.bitget({
            'apiKey': BG_KEY,
            'secret': BG_SECRET,
            'password': BG_PASS,
            'enableRateLimit': True,
        })

        tickers_to_fetch = ['SOL/USDT', 'GALA/USDT', 'LTC/USDT', 'ARB/USDT', 'PEOPLE/USDT']
        markets = exchange.fetch_tickers(tickers_to_fetch)
        
        print("\n=== RAPORT CENOWY OMNI-FLOW V6.0 ===")
        print(f"{'Asset':<10} | {'Cena LIVE (Bitget)':<20}")
        print("-" * 35)
        
        for ticker in tickers_to_fetch:
            if ticker in markets:
                price = markets[ticker]['last']
                asset_name = ticker.split('/')[0]
                print(f"{asset_name:<10} | {price:<20}")
                
        print("====================================")
        
    except Exception as e:
        print(f"Błąd API Bitget: {e}")

if __name__ == "__main__":
    fetch_live_prices()
