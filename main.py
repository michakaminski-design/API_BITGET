import os
import ccxt
import base64
import requests
from datetime import datetime, timezone

def format_price(price):
    if price is None:
        return "[BRAK CENY]"
    if price < 0.0001:
        return f"{price:.8f}".rstrip('0').rstrip('.') if f"{price:.8f}".rstrip('0').rstrip('.') else "0.0"
    elif price < 1:
        return f"{price:.6f}"
    else:
        return f"{price:.4f}"

def fetch_live_prices():
    BG_KEY = os.getenv('BG_KEY')
    BG_SECRET = os.getenv('BG_SECRET')
    BG_PASS = os.getenv('BG_PASS')
    GH_TOKEN = os.getenv('GH_TOKEN')

    if not all([BG_KEY, BG_SECRET, BG_PASS, GH_TOKEN]):
        print("BŁĄD: Brak skonfigurowanych zmiennych środowiskowych na Renderze!")
        return

    try:
        # Inicjalizacja Bitget z wymuszeniem typu SPOT dla fetch_tickers
        bitget = ccxt.bitget({
            'apiKey': BG_KEY,
            'secret': BG_SECRET,
            'password': BG_PASS,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })

        # Inicjalizacja Binance z wymuszeniem typu SPOT
        binance = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })

        tickers_to_fetch = [
            # === TOP LIQUIDITY ===
            'AAVE/USDT', 'ADA/USDT', 'ALGO/USDT', 'APE/USDT', 'ATOM/USDT', 'BCH/USDT', 'BNB/USDT', 
            'BTC/USDT', 'CHZ/USDT', 'CRV/USDT', 'DOGE/USDT', 'DOT/USDT', 'ETC/USDT', 'ETH/USDT', 
            'FIL/USDT', 'GRT/USDT', 'ICP/USDT', 'INJ/USDT', 'LINK/USDT', 'LTC/USDT', 
            'MANA/USDT', 'NEAR/USDT', 'NEO/USDT', 'OP/USDT', 'POL/USDT', 'QNT/USDT', 'QTUM/USDT', 
            'RUNE/USDT', 'SHIB/USDT', 'SOL/USDT', 'SNX/USDT', 'TRX/USDT', 'TWT/USDT', 'UNI/USDT', 
            'XLM/USDT', 'XMR/USDT', 'XRP/USDT', 'XTZ/USDT', 'YFI/USDT', 'ZEC/USDT',

            # === MID-CAPS & ALGO DRIVEN ===
            '1INCH/USDT', 'ACX/USDT', 'AGLD/USDT', 'AGX/USDT', 'ALCH/USDT', 'API3/USDT', 'APT/USDT', 
            'ARB/USDT', 'ARKM/USDT', 'ASTR/USDT', 'AUCTION/USDT', 'AXS/USDT', 'BICO/USDT', 'BIGTIME/USDT', 
            'BLUR/USDT', 'CAKE/USDT', 'CELO/USDT', 'CFX/USDT', 'COMP/USDT', 'DYDX/USDT', 'DYM/USDT', 
            'ENA/USDT', 'ENJ/USDT', 'ENS/USDT', 'GALA/USDT', 'GAS/USDT', 'GMX/USDT', 'HIGH/USDT', 
            'HBAR/USDT', 'IMX/USDT', 'IO/USDT', 'JASMY/USDT', 'JTO/USDT', 'JUP/USDT', 'KAVA/USDT', 
            'KNC/USDT', 'LDO/USDT', 'LRC/USDT', 'LPT/USDT', 'METIS/USDT', 'MINA/USDT', 'MOVR/USDT', 
            'MASK/USDT', 'MTL/USDT', 'NFP/USDT', 'NOT/USDT', 'ONDO/USDT', 'ORDI/USDT', 'PENDLE/USDT', 
            'PHB/USDT', 'POLYX/USDT', 'PYTH/USDT', 'REZ/USDT', 'RPL/USDT', 'RSR/USDT', 'RVN/USDT', 
            'SCR/USDT', 'SEI/USDT', 'STRK/USDT', 'STX/USDT', 'SUI/USDT', 'SUPER/USDT', 'TAO/USDT', 
            'THE/USDT', 'TIA/USDT', 'TON/USDT', 'TSTBSC/USDT', 'TURBO/USDT', 'UMA/USDT', 'VANRY/USDT', 
            'VIC/USDT', 'WLD/USDT', 'WOO/USDT', 'WIF/USDT', 'YGG/USDT', 'ZIL/USDT', 'ZRO/USDT',

            # === LOW-CAPS, MEMES & NEW BORN ===
            '1000LUNC/USDT', 'ACT/USDT', 'AIXBT/USDT', 'AIX/USDT', 'AKE/USDT', 'ANIME/USDT', 'ANKR/USDT', 
            'APR/USDT', 'ARC/USDT', 'ARIA/USDT', 'ASTER/USDT', 'AT/USDT', 'B3/USDT', 'BAN/USDT', 
            'BARD/USDT', 'BLESS/USDT', 'BLUAI/USDT', 'BR/USDT', 'BROCCOLI/USDT', 'BTR/USDT', 'CARV/USDT', 
            'CC/USDT', 'CETUS/USDT', 'CKB/USDT', 'CLANKER/USDT', 'COW/USDT', 'CVC/USDT', 'DASH/USDT', 
            'DOOD/USDT', 'DOLO/USDT', 'DUSK/USDT', 'EDU/USDT', 'ENSO/USDT', 'ESPORTS/USDT', 'FLOCK/USDT', 
            'FLOKI/USDT', 'FLUID/USDT', 'GIGGLE/USDT', 'GRASS/USDT', 'GTC/USDT', 'GUN/USDT', 'HANA/USDT', 
            'HEI/USDT', 'HEMI/USDT', 'HYPER/USDT', 'HYPE/USDT', 'ICNT/USDT', 'IP/USDT', 'JCT/USDT', 
            'JELLYJELLY/USDT', 'JST/USDT', 'KAS/USDT', 'LAB/USDT', 'LIGHT/USDT', 'LINEA/USDT', 'LUMIA/USDT', 
            'LYN/USDT', 'MAGIC/USDT', 'MERL/USDT', 'MEW/USDT', 'MMT/USDT', 'MUBARAK/USDT', 'MYX/USDT', 
            'NAORIS/USDT', 'NEWT/USDT', 'NOM/USDT', 'OG/USDT', 'OGN/USDT', 'ONG/USDT', 'ONT/USDT', 
            'OPEN/USDT', 'ORBS/USDT', 'ORCA/USDT', 'PARTI/USDT', 'PAXG/USDT', 'PENGU/USDT', 'PEOPLE/USDT', 
            'PIPIN/USDT', 'PIEVERSE/USDT', 'PIXEL/USDT', 'PNUT/USDT', 'PTB/USDT', 'PUMP/USDT', 'RAD/USDT', 
            'RARE/USDT', 'RED/USDT', 'RESOLV/USDT', 'RIVER/USDT', 'ROAM/USDT', 'SAGA/USDT', 'SAROS/USDT', 
            'SIGN/USDT', 'SKYAI/USDT', 'SOMI/USDT', 'STG/USDT', 'STO/USDT', 'SXT/USDT', 'TNSR/USDT', 
            'TRUST/USDT', 'TRUTH/USDT', 'USELESS/USDT', 'USUAL/USDT', 'USTC/USDT', 'VANA/USDT', 'VELVET/USDT', 
            'VINE/USDT', 'VIRTUAL/USDT', 'VVV/USDT', 'WAXP/USDT', 'WLFI/USDT', 'XNY/USDT', 'XPIN/USDT', 
            'XPLUS/USDT', 'XRO/USDT', 'ZBCN/USDT', 'ZBT/USDT', 'ZENT/USDT', 'ZEREBRO/USDT', 'ZKC/USDT', 
            'ZRX/USDT'
        ]

        print("Inicjalizacja rynków...")
        try:
            bitget.load_markets()
        except Exception as e:
            print(f"Błąd load_markets Bitget: {e}")

        try:
            binance.load_markets()
        except Exception as e:
            print(f"Błąd load_markets Binance: {e}")

        print("Pobieranie cen z Bitget...")
        bg_markets = {}
        try:
            bg_markets = bitget.fetch_tickers()
            print(f"Pobrano {len(bg_markets)} tickerów z Bitget.")
        except Exception as e:
            print(f"Błąd pobierania z Bitget: {e}")
        
        print("Pobieranie cen z Binance...")
        bn_markets = {}
        try:
            bn_markets = binance.fetch_tickers()
            print(f"Pobrano {len(bn_markets)} tickerów z Binance.")
        except Exception as e:
            print(f"Błąd pobierania z Binance: {e}")
        
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        content = f"OSTATNIA AKTUALIZACJA: {current_time}\n"
        content += f"{'Asset':<15} | {'Cena LIVE':<20} | {'Źródło':<15}\n"
        content += "-" * 56 + "\n"
        
        for ticker in tickers_to_fetch:
            asset_name = ticker.split('/')[0]
            
            # 1. Próba z Bitget
            if ticker in bg_markets and bg_markets[ticker].get('last') is not None:
                raw_price = bg_markets[ticker]['last']
                content += f"{asset_name:<15} | {format_price(raw_price):<20} | Bitget\n"
            
            # 2. Próba z Binance
            elif ticker in bn_markets and bn_markets[ticker].get('last') is not None:
                raw_price = bn_markets[ticker]['last']
                content += f"{asset_name:<15} | {format_price(raw_price):<20} | Binance (Zapas)\n"
            
            # 3. Próba mapowania specyficznych nazw dla Binance (np. 1000LUNC -> LUNC)
            elif asset_name.startswith("1000") and f"{asset_name[4:]}/USDT" in bn_markets:
                binance_ticker = f"{asset_name[4:]}/USDT"
                if bn_markets[binance_ticker].get('last') is not None:
                    raw_price = bn_markets[binance_ticker]['last'] * 1000
                    content += f"{asset_name:<15} | {format_price(raw_price):<20} | Binance (Zapas-Przeliczony)\n"
                else:
                    content += f"{asset_name:<15} | {'[BRAK PARY]':<20} | -\n"
                
            # 4. Brak pary całkowity
            else:
                content += f"{asset_name:<15} | {'[BRAK PARY]':<20} | -\n"

        # Zapis pliku na GitHubie
        repo_owner = "michakaminski-design"
        repo_name = "API_BITGET"
        file_path = "ceny.txt"
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {GH_TOKEN}"}
        
        response = requests.get(url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        message = f"Aktualizacja cen {current_time}"
        content_bytes = content.encode("utf-8")
        base64_content = base64.b64encode(content_bytes).decode("utf-8")
        
        payload = {
            "message": message,
            "content": base64_content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha
            
        put_response = requests.put(url, json=payload, headers=headers)
        if put_response.status_code in [200, 201]:
            print(f"Sukces: Plik ceny.txt zaktualizowany!")
        else:
            print(f"Błąd zapisu na GitHub: {put_response.json()}")

    except Exception as e:
        print(f"Błąd krytyczny skryptu: {e}")

if __name__ == "__main__":
    fetch_live_prices()
