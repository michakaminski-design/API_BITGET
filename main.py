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

        tickers_to_fetch = [
            # === TOP LIQUIDITY ===
            'AAVE/USDT', 'ADA/USDT', 'ALGO/USDT', 'APE/USDT', 'ATOM/USDT', 'BCH/USDT', 'BNB/USDT', 
            'BTC/USDT', 'CHZ/USDT', 'CRV/USDT', 'DOGE/USDT', 'DOT/USDT', 'ETC/USDT', 'ETH/USDT', 
            'FIL/USDT', 'FLOW/USDT', 'GRT/USDT', 'ICP/USDT', 'INJ/USDT', 'LINK/USDT', 'LTC/USDT', 
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
