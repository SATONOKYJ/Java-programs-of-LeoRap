import random
# Dodajemy url_for do importów
from flask import Flask, Response, url_for
import socket # Importujemy socket, aby znaleźć lokalny adres IP

# --- Konfiguracja ---
# Losowanie liczby TYLKO raz, przy starcie aplikacji
try:
    TARGET_NUMBER = random.randint(0, 2255)
    print(f"--- Serwer uruchomiony. Wylosowana liczba (do celów testowych): {TARGET_NUMBER} ---")
except Exception as e:
    print(f"Błąd podczas losowania liczby: {e}")
    exit(1)

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# --- Funkcja pomocnicza do znalezienia lokalnego IP ---
def get_local_ip():
    """Próbuje znaleźć lokalny adres IP maszyny."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Nie musi być osiągalny, po prostu inicjuje połączenie
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '192.168.1.147' # Fallback na localhost
    finally:
        s.close()
    return IP

# --- Definicja tras (routes) ---

# NOWA TRASA: Obsługa strony głównej "/"
@app.route('/')
def index():
    """Wyświetla stronę główną z przyciskiem do sprawdzenia liczby 0."""
    # Używamy url_for, aby dynamicznie wygenerować link do trasy 'check_guess'
    # z parametrem guess_str ustawionym na '0'. To dobra praktyka.
    link_do_zero = url_for('check_guess', guess_str=0)

    # Prosty kod HTML strony
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Zgadnij Liczbę</title>
    </head>
    <body>
        <h1>Zgadnij Liczbę (0-2255)</h1>
        <p>Wylosowana liczba pozostaje taka sama do restartu serwera.</p>
        <p>Kliknij przycisk, aby sprawdzić, czy wylosowaną liczbą jest 0:</p>

        <!-- Przycisk jako link kierujący do /0 -->
        <a href="/0">
            <button>Sprawdź 0</button>
        </a>

        <hr>
        <p>Aby sprawdzić inną liczbę, wpisz ją w pasku adresu po ukośniku</p>
        <p>Adres IP serwera (do użycia w przeglądarce skonfigurowanej z proxy): <code>{get_local_ip()}</code></p>
    </body>
    </html>
    """
    return html_content

# ISTNIEJĄCA TRASA: Obsługa zgadywania liczby "/<liczba>"
@app.route('/<guess_str>')
def check_guess(guess_str):
    """
    Sprawdza, czy podana w URL liczba jest równa wylosowanej.
    Zwraca status 200 dla poprawnej liczby, 400 dla błędnej lub niepoprawnego formatu.
    """
    print(f"Otrzymano próbę: /{guess_str}") # Logowanie próby

    # 1. Sprawdź, czy podany ciąg jest liczbą całkowitą
    if not guess_str.isdigit():
        print(f"Błąd: '{guess_str}' nie jest poprawną liczbą całkowitą.")
        return Response("Błąd: Podana wartość nie jest liczbą całkowitą.", status=400)

    # 2. Konwertuj na liczbę całkowitą
    try:
        guess_int = int(guess_str)
    except ValueError:
        # Ten kod jest technicznie zbędny przez wcześniejsze .isdigit(), ale zostawiamy dla pewności
        print(f"Błąd konwersji: '{guess_str}' nie może być przekonwertowane na int.")
        return Response("Błąd wewnętrzny podczas konwersji.", status=400)

    # 3. Porównaj z wylosowaną liczbą
    if guess_int == TARGET_NUMBER:
        print(f"SUKCES: {guess_int} == {TARGET_NUMBER}")
        # Zwracamy bardziej opisową wiadomość, która będzie widoczna w Burp
        return Response(f"OK - Zgadles! Liczba to {TARGET_NUMBER}", status=200)
    else:
        print(f"BŁĄD: {guess_int} != {TARGET_NUMBER}")
        # Zwracamy bardziej opisową wiadomość
        return Response(f"Bledna liczba. Probujesz {guess_int}, ale sie nie poddawaj", status=400)

# --- Uruchomienie serwera ---
if __name__ == '__main__':
    # ZMIANA KLUCZOWA: Ustaw host na '0.0.0.0'
    # To sprawia, że serwer nasłuchuje na wszystkich interfejsach sieciowych,
    # a nie tylko na localhost (127.0.0.1). Dzięki temu możesz
    # uzyskać dostęp do serwera przez lokalny adres IP Twojej maszyny
    # (np. 192.168.1.100), co jest łatwiejsze do przechwycenia przez proxy
    # niż ruch do 127.0.0.1.
    HOST_IP = '0.0.0.0'
    PORT = 5000

    local_ip_address = get_local_ip()
    print(f"\n--- Serwer Flask startuje ---")
    print(f"Aby przechwycić ruch w Burp Suite:")
    print(f"1. Upewnij się, że Burp Proxy Listener jest aktywny (zwykle na 127.0.0.1:8080).")
    print(f"2. Skonfiguruj przeglądarkę, aby używała proxy Burp (http://127.0.0.1:8080).")
    print(f"3. W przeglądarce przejdź pod adres: http://{local_ip_address}:{PORT}")
    print(f"   (Jeśli {local_ip_address} to 127.0.0.1, spróbuj znaleźć swój rzeczywisty adres IP np. komendą 'ipconfig' lub 'ifconfig' i użyj go zamiast 127.0.0.1)")
    print(f"Serwer nasłuchuje na: {HOST_IP}:{PORT}\n")

    # Uruchomienie serwera na wszystkich interfejsach
    app.run(host=HOST_IP, port=PORT, debug=False)

    # Ten komunikat pojawi się po zatrzymaniu serwera (np. przez Ctrl+C)
    print("\n--- Serwer zatrzymany. ---")