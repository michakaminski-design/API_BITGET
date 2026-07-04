import ccxt
import time
from datetime import datetime

# --- Konfiguracja ---
exchange = ccxt.bitget({'enableRateLimit': True})

ASSET_GROUPS = {
    'TOP_LIQUIDITY': ['AAVE', 'ADA', 'ALGO', 'APE', 'ATOM', 'BCH', 'BNB', 'BTC', 'CHZ', 'CRV', 'DOGE', 'DOT', 'ETC', 'ETH', 'FIL', 'FLOW', 'GRT', 'ICP', 'INJ', 'LINK', 'LTC', 'MANA', 'NEAR', 'NEO', 'OP', 'POL', 'QNT', 'QTUM', 'RUNE', 'SHIB', 'SOL', 'SNX', 'TRX', 'TWT', 'UNI', 'XLM', 'XMR', 'XRP', 'XTZ', 'YFI', 'ZEC'],
    'MID_CAPS': ['1INCH', 'ACX', 'AGLD', 'AGX', 'ALCH', 'API3', 'APT', 'ARB', 'ARKM', 'ASTR', 'AUCTION', 'AXS', 'BICO', 'BIGTIME', 'BLUR', 'CAKE', 'CELO', 'CFX', 'COMP', 'DYDX', 'DYM', 'ENA', 'ENJ', 'ENS', 'GALA', 'GAS', 'GMX', 'HIGH', 'HBAR', 'IMX', 'IO', 'JASMY', 'JTO', 'JUP', 'KAVA', 'KNC', 'LDO', 'LRC', 'LPT', 'METIS', 'MINA', 'MOVR', 'MASK', 'MTL', 'NFP', 'NOT', 'ONDO', 'ORDI', 'PENDLE', 'PHB', 'POLYX', 'PYTH', 'REZ', 'RPL', 'RSR', 'RVN', 'SCR', 'SEI', 'STRK', 'STX', 'SUI', 'SUPER', 'TAO', 'THE', 'TIA', 'TON', 'TSTBSC', 'TURBO', 'UMA', 'VANRY', 'VIC', 'WLD', 'WOO', 'WIF', 'YGG', 'ZIL', 'ZRO'],
    'LOW_CAPS': ['1000LUNC', '4', 'ACT', 'AIXBT', 'AIX', 'AKE', 'ANIME', 'ANKR', 'APR', 'ARC', 'ARIA', 'ASTER', 'AT', 'B', 'B3', 'BAN', 'BARD', 'BLESS', 'BLUAI', 'BR', 'BROCCOLI', 'BTR', 'CARV', 'CC', 'CETUS', 'CKB', 'CLANKER', 'COW', 'CVC', 'DASH', 'DOOD', 'DOLO', 'DUSK', 'EDU', 'ENSO', 'ESPORTS', 'F', 'FLOCK', 'FLOKI', 'FLUID', 'GIGGLE', 'GRASS', 'GTC', 'GUN', 'H', 'HANA', 'HEI', 'HEMI', 'HIGH', 'HYPER', 'HYPE', 'ICNT', 'IP', 'INUSDT', 'JASMY', 'JCT', 'JELLYJELLY', 'JST', 'KAS', 'LAB', 'LIGHT', 'LINEA', 'LUMIA', 'LYN', 'M', 'MAGIC', 'MERL', 'MEW', 'MMT', 'MUBARAK', 'MYX', 'NAORIS', 'NEWT', 'NOM', 'OG', 'OGN', 'ONG', 'ONT', 'OPEN', 'ORBS', 'ORCA', 'PARTI', 'PAXG', 'PENGU', 'PEOPLE', 'PIPIN', 'PIEVERSE', 'PIXEL', 'PNUT', 'PTB', 'PUMP', 'Q', 'RAD', 'RARE', 'RED', 'RESOLV', 'RIVER', 'ROAM', 'SAGA', 'SAROS', 'SIGN', 'SKYAI', 'SOMI', 'STG', 'STO', 'SXT', 'TA', 'TNSR', 'TRUST', 'TRUTH', 'UA', 'USELESS', 'USUAL', 'USTC', 'VANA', 'VELVET', 'VINE', 'VIRTUAL', 'VVV', 'WAXP', 'WLFI', 'XNY', 'XPIN', 'XPLUS', 'XRO', 'ZBCN', 'ZBT', 'ZENT', 'ZEREBRO', 'ZKC', 'ZRX']
}

# Łączymy wszystkie grupy w jedną listę
SYMBOLS = ASSET_GROUPS['TOP_LIQUIDITY'] + ASSET_GROUPS['MID_CAPS'] + ASSET_GROUPS['LOW_CAPS']
FILENAME = 'ceny.csv'

def get_price(symbol):
    try:
        ticker = exchange.fetch_ticker(f"{symbol}/USDT")
        return ticker['last']
    except Exception as e:
        # Pomijamy printowanie błędu przy tak dużej liście, 
        # żeby nie zaśmiecać logów
        return None

if __name__ == "__main__":
    try:
        with open(FILENAME, 'x') as f:
            f.write("Timestamp,Symbol,Price\n")
    except FileExistsError:
        pass

    print(f"Mini-bot cenowy działa. Monitoruję {len(SYMBOLS)} par.")
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for symbol in SYMBOLS:
            price = get_price(symbol)
            if price:
                with open(FILENAME, "a") as f:
                    f.write(f"{timestamp},{symbol},{price}\n")
            time.sleep(0.05) # Szybsze odświeżanie przy większej ilości par
        
        # Pętla po wszystkich parach zajmie chwilę, 
        # czekamy dodatkowo przed kolejnym cyklem
        time.sleep(30)
