# --- 3. Główna pętla programu ---
if __name__ == "__main__":
    # Tutaj definiujesz listę par, które chcesz monitorować
    SYMBOLS_TO_MONITOR = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT']
    TIMEFRAME = '1h'
    
    print(f"Rozpoczynam analizę dla {len(SYMBOLS_TO_MONITOR)} par...")
    
    all_results = []
    
    # Pętla po wszystkich parach
    for symbol in SYMBOLS_TO_MONITOR:
        print(f"Analizuję: {symbol}")
        results = fetch_and_analyze(symbol, TIMEFRAME)
        if results:
            all_results.extend(results) # Dodajemy wyniki do wspólnej listy
    
    # Wysyłamy wszystkie zebrane dane do arkusza za jednym razem
    if all_results:
        print(f"Znaleziono łącznie {len(all_results)} FVG. Wysyłam do arkusza...")
        update_spreadsheet(all_results)
    else:
        print("Nie znaleziono żadnych FVG dla żadnej z par.")
