import ccxt
import time
import os
import threading
from datetime import datetime, timezone
from flask import Flask, Response

# --- Konfiguracja Giełdy ---
exchange = ccxt.bitget({'enableRateLimit': True})

ASSET_GROUPS = {
    'TOP_LIQUIDITY': ['AAVE', 'ADA', 'ALGO', 'APE', 'ATOM', 'BCH', 'BNB', 'BTC', 'CHZ', 'CRV', 'DOGE', 'DOT', 'ETC', 'ETH', 'FIL', 'FLOW', 'GRT', 'ICP', 'INJ', 'LINK', 'LTC', 'MANA', 'NEAR', 'NEO', 'OP', 'POL', 'QNT', 'QTUM', 'RUNE', 'SHIB', 'SOL', 'SNX', 'TRX', 'TWT', 'UNI', 'XLM', 'XMR', 'XRP', 'XTZ', 'YFI', 'ZEC'],
    'MID_CAPS': ['1INCH', 'ACX', 'AGLD', 'AGX', 'ALCH', 'API3', 'APT', 'ARB', 'ARKM', 'ASTR', 'AUCTION', 'AXS', 'BICO', 'BIGTIME', 'BLUR', 'CAKE', 'CELO', 'CFX', 'COMP', 'DYDX', 'DYM', 'ENA', 'ENJ', 'ENS', 'GALA', 'GAS', 'GMX', 'HIGH', 'HBAR', 'IMX', 'IO', 'JASMY', 'JTO', 'JUP', 'KAVA', 'KNC', 'LDO', 'LRC', 'LPT', 'METIS', 'MINA', 'MOVR', 'MASK', 'MTL', 'NFP', 'NOT', 'ONDO', 'ORDI', 'PENDLE', 'PHB', 'POLYX', 'PYTH', 'REZ', 'RPL', 'RSR', 'RVN', 'SCR', 'SEI', 'STRK', 'STX', 'SUI', 'SUPER', 'TAO', 'THE', 'TIA', 'TON', 'TSTBSC', 'TURBO', 'UMA', 'VANRY', 'VIC', 'WLD', 'WOO', 'WIF', 'YGG', 'ZIL', 'ZRO'],
    'LOW_CAPS': ['1000LUNC', '4', 'ACT', 'AIXBT', 'AIX', 'ANIME', 'ANKR', 'APR', 'ARC', 'ARIA', 'ASTER', 'AT', 'B', 'B3', 'BAN', 'BARD', 'BLESS', 'BLUAI', 'BR', 'BROCCOLI', 'BTR', 'CARV', 'CC', 'CETUS', 'CKB', 'CLANKER', 'COW', 'CVC', 'DASH', 'DOOD', 'DOLO', 'DUSK', 'EDU', 'ENSO', 'ESPORTS', 'F', 'FLOCK', 'FLOKI', 'FLUID', 'GIGGLE', 'GRASS', 'GTC', 'GUN', 'H', 'HANA', 'HEI', 'HEMI', 'HIGH', 'HYPER', 'HYPE', 'ICNT', 'IP', 'INUSDT', 'JASMY', 'JCT', 'JELLYJELLY', 'JST', 'KAS', 'LAB', 'LIGHT', 'LINEA', 'LUMIA', 'LYN', 'M', 'MAGIC', 'MERL', 'MEW', 'MMT', 'MUBARAK', 'MYX', 'NAORIS', 'NEWT', 'NOM', 'OG', 'OGN', 'ONG', 'ONT', 'OPEN', 'ORBS', 'ORCA', 'PARTI', 'PAXG', 'PENGU', 'PEOPLE', 'PIPIN', 'PIEVERSE', 'PIXEL', 'PNUT', 'PTB', 'PUMP', 'Q', 'RAD', 'RARE', 'RED', 'RESOLV', 'RIVER', 'ROAM', 'SAGA', 'SAROS', 'SIGN', 'SKYAI', 'SOMI', 'STG', 'STO', 'SXT', 'TA', 'TNSR', 'TRUST', 'TRUTH', 'UA', 'USELESS', 'USUAL', 'USTC', 'VANA', 'VELVET', 'VINE', 'VIRTUAL', 'VVV', 'WAXP', 'WLFI', 'XNY', 'XPIN', 'XPLUS', 'XRO', 'ZBCN', 'ZBT', 'ZENT', 'ZEREBRO', 'ZKC', 'ZRX']
}

SYMBOLS = ASSET_GROUPS['TOP_LIQUIDITY'] + ASSET_GROUPS['MID_CAPS'] + ASSET_GROUPS['LOW_CAPS']
FILENAME = 'ceny.txt'
TEMP_FILENAME = 'ceny_temp.txt'

# --- Inicjalizacja Serwera ---
app = Flask(__name__)

def fetch_data():
    results = []
    errors = 0
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    for symbol in SYMBOLS:
        try:
            ticker = exchange.fetch_ticker(f"{symbol}/USDT")
            price = ticker['last']
            if price is not None:
                results.append(f"{symbol:<10} | {price:.8f}")
        except Exception:
            errors += 1
            continue
        time.sleep(0.05) 
        
    return timestamp, results, errors

def background_scanner():
    while True:
        timestamp, data, error_count = fetch_data()
        
        # Zapis atomowy zapobiegający ucięciu pliku
        with open(TEMP_FILENAME, "w", encoding="utf-8") as f:
            f.write(f"OSTATNIA AKTUALIZACJA: {timestamp}\n")
            f.write(f"{'Asset':<10} | Cena\n")
            f.write("-" * 30 + "\n")
            for line in data:
                f.write(line + "\n")
        
        os.replace(TEMP_FILENAME, FILENAME)
        print(f"Zapisano o {timestamp}. Pobrane: {len(data)}, Błędy API: {error_count}")
        time.sleep(30)

# --- Konfiguracja endpointu (widoku w przeglądarce) ---
@app.route('/')
def show_prices():
    if not os.path.exists(FILENAME):
        return Response("Skaner inicjalizuje dane. Odśwież stronę za 30 sekund.", mimetype='text/plain')
        
    with open(FILENAME, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype='text/plain')

if __name__ == "__main__":
    # Odpalenie skanera w oddzielnym wątku
    scanner_thread = threading.Thread(target=background_scanner, daemon=True)
    scanner_thread.start()
    
    # Render używa zmiennej środowiskowej PORT, domyślnie nasłuchujemy na porcie
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
