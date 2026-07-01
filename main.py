import requests

def pobierz_i_parsuj_crt(url_do_surowego_pliku):
    """
    Pobiera rozbudowany plik ceny.txt i przekształca go w słownik Pythonowy.
    Obsługuje zaawansowany kontekst rynkowy (FVG, Key Levels, Stany CRT).
    """
    try:
        response = requests.get(url_do_surowego_pliku)
        if response.status_code != 200:
            print(f"Błąd pobierania pliku: Status {response.status_code}")
            return None

        linie = response.text.strip().split('\n')
        baza_danych_crt = {}

        for linia in linie:
            if "|" not in linia or "Cena LIVE" in linia or "---" in linia or "OSTATNIA" in linia:
                continue  # Pomija nagłówki, linie dekoracyjne i metadane czasu
            
            # Podział linii na kolumny i oczyszczenie z białych znaków
            kolumny = [kol.strip() for col in linia.split('|') for kol in [col.strip()]]
            
            # Wymagamy rozszerzonej struktury (minimum 9 kolumn dla pełnego podglądu danych)
            if len(kolumny) >= 9:
                ticker = kolumny[0]
                str_live = kolumny[1]
                str_high = kolumny[2]
                str_low = kolumny[3]
                htf_context = kolumny[4]      # Np. "1D_FVG_SUPPORT" lub "1W_KEY_LEVEL_BOUNCE"
                str_sweep_max = kolumny[5]    # Maksimum manipulacji (do SL)
                str_sweep_min = kolumny[6]    # Minimum manipulacji (do SL)
                crt_state = kolumny[7]        # Stan: IDLE, SWEEP_HIGH, SWEEP_LOW, CONFIRMED_LONG, CONFIRMED_SHORT
                zrodlo = kolumny[8]

                # Filtrowanie braków danych
                if "[BRAK DANYCH]" in str_live or "[BRAK PARY]" in str_live or str_high == "-":
                    continue

                try:
                    baza_danych_crt[ticker] = {
                        "live": float(str_live),
                        "range_high": float(str_high),
                        "range_low": float(str_low),
                        "htf_context": htf_context,
                        "sweep_max": float(str_sweep_max) if str_sweep_max != "-" else None,
                        "sweep_min": float(str_sweep_min) if str_sweep_min != "-" else None,
                        "crt_state": crt_state.upper(),
                        "source": zrodlo,
                        "rsi_optional": None # Opcjonalne pole inicjalizacyjne, jeśli skrypt dopisze RSI
                    }
                except ValueError:
                    continue

        return baza_danych_crt

    except Exception as e:
        print(f"Błąd krytyczny parsera: {e}")
        return None

# =====================================================================
# ZAAWANSOWANA LOGIKA DECYZYJNA STRATEGII V6.1
# =====================================================================
def uruchom_logike_v61(ticker, dane):
    print(f"\n[ANALIZA: {ticker}] Stan: {dane['crt_state']} | Cena: {dane['live']}")
    print(f" -> Kontekst HTF: {dane['htf_context']}")
    print(f" -> Zakres CRT: {dane['range_low']} - {dane['range_high']}")

    # Definiowanie filtrów siły poziomów (Level Strength Filter)
    is_macro_level = "1D_KEY" in dane['htf_context'] or "1W_KEY" in dane['htf_context']
    is_fvg_zone = "4H_FVG" in dane['htf_context'] or "1D_FVG" in dane['htf_context']

    # --- SCENARIUSZ LONG (BULLISH CRT) ---
    if dane['crt_state'] == "CONFIRMED_LONG":
        # Sprawdzamy czy struktura zbiega się z wyższym interwałem rynkowym (POI)
        if is_macro_level or is_fvg_zone:
            print(f"🔥 [SYGNAŁ BUY] Wykryto setup Bullish CRT w strefie HTF!")
            
            # Punkt II (Arena) - Filtrowanie siły poziomu rynkowego
            if is_macro_level:
                print(" -> [FILTR] Reakcja na Kluczowy Poziom 1D/1W lub PDH/PDL.")
                print(" -> [EGZEKUCJA] Wejście AGRESYWNE (50% Market Order) ze względu na siłę poziomu.")
            else:
                print(" -> [EGZEKUCJA] Wejście standardowe po potwierdzeniu struktury (Limit/Stop).")
            
            # Kalkulacja poziomów obronnych i docelowych
            if dane['sweep_min']:
                sl = dane['sweep_min']
                tp = dane['range_high']
                print(f" -> Parametry zlecenia: SL: {sl} | TP: {tp}")
        else:
            print(" ❌ [ODRZUCONO] Sygnał CRT Long powstał w pustej przestrzeni (brak konfluencji z HTF/FVG).")

    # --- SCENARIUSZ SHORT (BEARISH CRT) ---
    elif dane['crt_state'] == "CONFIRMED_SHORT":
        if is_macro_level or is_fvg_zone:
            print(f"🔥 [SYGNAŁ SELL] Wykryto setup Bearish CRT w strefie HTF!")
            
            if is_macro_level:
                print(" -> [FILTR] Reakcja na Kluczowy Poziom 1D/1W lub PDH/PDL.")
                print(" -> [EGZEKUCJA] Wejście AGRESYWNE (50% Market Order) ze względu na siłę poziomu.")
            else:
                print(" -> [EGZEKUCJA] Wejście standardowe.")
                
            if dane['sweep_max']:
                sl = dane['sweep_max']
                tp = dane['range_low']
                print(f" -> Parametry zlecenia: SL: {sl} | TP: {tp}")
        else:
            print(" ❌ [ODRZUCONO] Sygnał CRT Short powstał w pustej przestrzeni (brak konfluencji z HTF/FVG).")

    # --- MONITOROWANIE FAZY MANIPULACJI (SWEEP) ---
    elif dane['crt_state'] == "SWEEP_LOW":
        print(" 👀 [MONITOROWANIE] Płynność z dołu wyczyszczona. Oczekiwanie na zamknięcie świecy LTF wewnątrz zakresu.")
    elif dane['crt_state'] == "SWEEP_HIGH":
        print(" 👀 [MONITOROWANIE] Płynność z góry wyczyszczona. Oczekiwanie na zamknięcie świecy LTF wewnątrz zakresu.")
    else:
        print(" 💤 [INFO] Brak aktywnych manipulacji na świecy referencyjnej.")


if __name__ == "__main__":
    # Testowy link RAW do bazy danych
    URL_RAW = "https://raw.githubusercontent.com/michakaminski-design/API_BITGET/main/ceny.txt"
    
    # Symulacja bazy danych po rozbudowaniu skryptu generującego plik tekstowy:
    # Format linii: Ticker | Live | High | Low | HTF_Context | Sweep_Max | Sweep_Min | CRT_State | Source
    print("Pobieranie rozszerzonych danych rynkowych i poziomów HTF...")
    
    # Dla celów testowych ręcznie symulujemy strukturę danych, którą Twój skrypt generujący powinien zapisać:
    testowa_baza = {
        "BTC": {
            "live": 58850.00,
            "range_high": 59000.00,
            "range_low": 58200.00,
            "htf_context": "1D_KEY_LEVEL_BOUNCE",
            "sweep_max": "-",
            "sweep_min": 58110.00,
            "crt_state": "CONFIRMED_LONG",
            "source": "Bitget"
        },
        "ETH": {
            "live": 1564.00,
            "range_high": 1580.00,
            "range_low": 1550.00,
            "htf_context": "BEARISH_4H_FVG_TEST",
            "sweep_max": 1585.00,
            "sweep_min": "-",
            "crt_state": "SWEEP_HIGH",
            "source": "Bitget"
        }
    }
    
    # Uruchomienie logiki handlowej dla danych testowych
    uruchom_logike_v61("BTC", testowa_baza["BTC"])
    uruchom_logike_v61("ETH", testowa_baza["ETH"])
