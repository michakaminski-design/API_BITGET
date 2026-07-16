import ccxt
import time
from datetime import datetime

# Inicjalizacja giełdy
exchange = ccxt.bitget({'enableRateLimit': True})

# Lista symboli (Twoja lista ok. 200 par)
# Upewnij się, że masz tu wszystkie interesujące Cię pary
SYMBOLS = [
    'EDU/USDT', 'PTB/USDT', 'JCT/USDT', 'GTC/USDT', 'CC/USDT', 'ESPORTS/USDT', 
    'BTR/USDT', 'PHB/USDT', 'HIGH/USDT', 'CETUS/USDT', 'SUPER/USDT', 'COMP/USDT', 
    'ARKM/USDT', 'GUN/USDT', 'PIPPIN/USDT', 'ZBT/USDT', 'B3/USDT', 'HANA/USDT', 
    'MUBARAK/USDT', 'SAGA/USDT', 'DYM/USDT', 'ARC/USDT', 'ZRO/USDT', 'HEMI/USDT', 
    'BICO/USDT', 'PNUT/USDT', 'STO/USDT', 'H/USDT', 'RESOLV/USDT', 'LUMIA/USDT', 
    'ENJ/USDT', 'BAT/USDT', 'MERL/USDT', 'VANRY/USDT', 'ZBCN/USDT', 'ACT/USDT', 
    'YGG/USDT', 'GRT/USDT', 'MAGIC/USDT', 'TWT/USDT', 'APE/USDT', 'ORDI/USDT', 
    'FLOW/USDT', 'BAND/USDT', 'SCR/USDT', 'TIA/USDT', 'JTO/USDT', 'FLUID/USDT', 
    'SIGN/USDT', 'METIS/USDT', 'CELO/USDT', 'USUAL/USDT', 'OP/USDT', 'BARD/USDT', 
    'RED/USDT', 'MINA/USDT', 'CKB/USDT', 'NOT/USDT', 'LINEA/USDT', 'F/USDT', 
    'XPIN/USDT', 'PAXG/USDT', 'GALA/USDT', 'XAUT/USDT', 'AIA/USDT', 'RPL/USDT', 
    'POLYX/USDT', 'GAS/USDT', 'LPT/USDT', 'MASK/USDT', 'ZIL/USDT', 'ARB/USDT', 
    'AGLD/USDT', 'CFX/USDT', 'MYX/USDT', 'QTUM/USDT', 'BROCCOLI/USDT', 'XPL/USDT', 
    'MMT/USDT', 'AXS/USDT', 'NEO/USDT', 'ZRX/USDT', 'DOT/USDT', 'ORBS/USDT', 
    'ATOM/USDT', 'WLD/USDT', 'ZENT/USDT', 'ALGO/USDT', 'MANA/USDT', 'AUCTION/USDT', 
    'APT/USDT', 'DUSK/USDT', 'KAVA/USDT', 'BIGTIME/USDT', 'ACX/USDT', '1INCH/USDT', 
    'POL/USDT', 'TURBO/USDT', 'STG/USDT', 'STEEM/USDT', 'DOOD/USDT', 'WAXP/USDT', 
    'TRX/USDT', 'CHZ/USDT', 'RVN/USDT', 'CVC/USDT', 'PEOPLE/USDT', 'ONG/USDT', 
    'M/USDT', 'ASTR/USDT', 'DOGE/USDT', 'BCH/USDT', 'CRO/USDT', 'ASTER/USDT', 
    'WIF/USDT', 'FIL/USDT', 'ORCA/USDT', 'THE/USDT', 'ICP/USDT', 'GMX/USDT', 
    'JASMY/USDT', 'ZKC/USDT', 'SEI/USDT', 'PYTH/USDT', 'SNX/USDT', 'OGN/USDT', 
    'HYPE/USDT', 'USTC/USDT', 'ENA/USDT', 'RSR/USDT', 'OG/USDT', 'HEI/USDT', 
    'XVG/USDT', 'ETH/USDT', 'FLOKI/USDT', 'AERGO/USDT', 'SOL/USDT', 'C98/USDT', 
    'VIRTUAL/USDT', 'DYDX/USDT', 'MTL/USDT', 'CARV/USDT', 'JUP/USDT', 'LUNA/USDT', 
    'STX/USDT', 'LTC/USDT', 'LUNA2/USDT', 'AT/USDT', 'ENS/USDT', 'ANIME/USDT', 
    'INJ/USDT', 'CLANKER/USDT', 'BLUAI/USDT', 'STRK/USDT', 'KAS/USDT', 'AVAX/USDT', 
    'ADA/USDT', 'BTC/USDT', 'VVV/USDT', 'WLFI/USDT', 'SOMI/USDT', 'NEAR/USDT', 
    'JELLYJELLY/USDT', 'ICNT/USDT', 'QNT/USDT', 'CAKE/USDT', 'ETC/USDT', 'SYN/USDT', 
    'HBAR/USDT', 'UNI/USDT', '1000LUNC/USDT', 'LINK/USDT', 'SHIB/USDT', 'BNB/USDT', 
    'COW/USDT', 'ONDO/USDT', 'DOLO/USDT', 'TAO/USDT', 'USELESS/USDT', 'ENSO/USDT', 
    'MEW/USDT', 'WOO/USDT', 'XRP/USDT', 'SUI/USDT', 'CTK/USDT', 'PHA/USDT', 
    'GRASS/USDT', 'TAU/USDT', 'I/USDT', 'PUMP/USDT', 'BAN/USDT', 'ZEC/USDT', 
    'RAD/USDT', 'PIXEL/USDT', 'CRV/USDT', 'RDNT/USDT', 'Q/USDT', 'PARTI/USDT', 
    '4/USDT', 'LIGHT/USDT', 'GIGGLE/USDT', 'FIO/USDT', 'PIEVERSE/USDT', 'IP/USDT', 
    'XMR/USDT', 'PENGU/USDT', 'LRC/USDT', 'AAVE/USDT', 'DAM/USDT', 'NOM/USDT', 
    'TON/USDT', 'ALCH/USDT', 'PENDLE/USDT', 'API3/USDT', 'TRUTH/USDT', 'ONT/USDT', 
    'NIL/USDT', 'IMX/USDT', 'FLOCK/USDT', 'AKE/USDT', 'BR/USDT', 'LDO/USDT', 
    'VANA/USDT', 'SAROS/USDT', 'NAORIS/USDT', 'XLM/USDT', 'AXL/USDT', 'RIVER/USDT', 
    'NEWT/USDT', 'VELVET/USDT', 'ZEREBRO/USDT', 'UMA/USDT', 'APR/USDT', 'XNY/USDT', 
    'JST/USDT', 'SKYAI/USDT', 'BLESS/USDT', 'LYN/USDT', 'ARIA/USDT', 'UAI/USDT', 
    'ROAM/USDT', 'TRU/USDT', 'DENT/USDT'
]

def fetch_data():
    results = []
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    for symbol in SYMBOLS:
        try:
            ticker = exchange.fetch_ticker(f"{symbol}/USDT")
            price = ticker['last']
            results.append(f"{symbol} | {price:.4f} | Bitget")
        except Exception:
            continue
    return timestamp, results

if __name__ == "__main__":
    print("Skaner uruchomiony...")
    while True:
        timestamp, data = fetch_data()
        
        # Zapis do pliku
        with open("ceny.txt", "w", encoding="utf-8") as f:
            f.write(f"OSTATNIA AKTUALIZACJA: {timestamp}\n")
            f.write("Asset | Cena LIVE | Źródło\n")
            f.write("-" * 40 + "\n")
            for line in data:
                f.write(line + "\n")
        
        print(f"Zapisano dane o {timestamp}")
        time.sleep(60)
