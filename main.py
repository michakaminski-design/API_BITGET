import requests

def pobierz_i_parsuj_crt(url_do_surowego_pliku):
    """
    Pobiera plik ceny.txt i przekształca go w słownik Pythonowy.
    URL powinien prowadzić do wersji 'raw' pliku na GitHubie.
    """
    try:
        response = requests.get(url_do_surowego_pliku)
        if response.status_code != 200:
            print(f"Błąd pobierania pliku: Status {response.status_code}")
            return None

        linie = response.text.strip().split('\n')
        baza_danych_crt = {}

        # Przetwarzamy linie od trzeciej (indeks 2), pomijając nagłówki i linię przerywaną
        for linia in linie:
            if "|" not in linia or "Cena LIVE" in linia or "---" in linia:
                continue  # Pomija linie nagłówkowe i dekoracyjne
            
            # Podział linii na kolumny i usunięcie białych znaków
            kolumny = [kol.strip() for col in linia.split('|') for kol in [col.strip()]]
            
            if len(kolumny) >= 5:
                ticker = kolumny[0]
                str_live = kolumny[1]
                str_high = kolumny[2]
                str_low = kolumny[3]
                zrodlo = kolumny[4]

                # Filtrowanie braków danych
                if "[BRAK DANYCH]" in str_live or str_high == "-":
                    continue

                try:
                    baza_danych_crt[ticker] = {
                        "live": float(str_live),
                        "range_high": float(str_high),
                        "range_low": float(str_low),
                        "source": zrodlo
                    }
                except ValueError:
                    # Zabezpieczenie przed błędami konwersji tekst -> float
                    continue

        return baza_danych_crt

    except Exception as e:
        print(f"Błąd krytyczny parsera: {e}")
        return None

# =====================================================================
# PRZYKŁAD UŻYCIA W LOGICE TRADINGOWEJ
# =====================================================================
if __name__ == "__main__":
    # Link do wersji RAW Twojego pliku na GitHubie
    URL_RAW = "https://raw.githubusercontent.com/michakaminski-design/API_BITGET/main/ceny.txt"
    
    print("Pobieranie aktualnych poziomów CRT...")
    dane_rynkowe = pobierz_i_parsuj_crt(URL_RAW)

    if dane_rynkowe and "BTC" in dane_rynkowe:
        btc = dane_rynkowe["BTC"]
        print(f"\nPomyślnie załadowano dane dla {len(dane_rynkowe)} aktywów.")
        print(f"Przykładowe dane dla BTC:")
        print(f"  - Cena LIVE: {btc['live']}")
        print(f"  - CRT Range High: {btc['range_high']}")
        print(f"  - CRT Range Low: {btc['range_low']}")
        print(f"  - Źródło: {btc['source']}")

        # Przykład prostej weryfikacji warunku w locie:
        if btc['live'] > btc['range_high']:
            print("\n[ALERT] Cena BTC znajduje się powyżej struktury CRT Range High (Potencjalny Sweep / Szukanie Shorta).")
        elif btc['live'] < btc['range_low']:
            print("\n[ALERT] Cena BTC znajduje się poniżej struktury CRT Range Low (Potencjalny Sweep / Szukanie Longa).")
        else:
            print("\n[INFO] Cena BTC wewnątrz zakresu konsolidacji.")
