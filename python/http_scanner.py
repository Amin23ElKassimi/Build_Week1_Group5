#   PER MIGLIORARE IL CODICE/ HTTP_Scanner V2.0
# - Possibilità di assegnare il tipo di richiesta (Verbo) tramite una variabile input; stessa cosa con la directory. (A RIGA 13) / FATTO MA DA VERIFICARE
# - Migliorare la struttura dello script usando le funzioni e "Main():". / FATTO
# - Rendiamo il programma continuo (ciclo while) in modo da evitare che alla fine di ogni verifica HTTP il programma si spegne, dobbiamo poterlo spegnere noi digitando "exit" per esempio. / DA DISCUTERE

import http.client #Importiamo l'estenzione necessaria per parlare con i server web.


def main():
    print_team_banner()
    print_tool_banner()
    host, port, verb, path, body, headers= initialize()
    httprequest(host, port, verb, path, body, headers)

def initialize():
    # --- CONTROLLO HOST ---
    while True:
        input_host = input('Inserire indirizzo IP: ').strip() # strip() Rimuove eventuali spazi accidentali.
        if input_host == '':
            print("Errore: L'IP non può essere vuoto")
        else:
            break


    # --- CONTROLLO PORTA ---
    input_port = input('Inserire la porta (default: 80): ') #Input in cui inserire la porta che utilizzeremo per collegarci.
    if input_port == '': #SE immettiamo un input vuoto allora utilizza in automatico la porta 80
        input_port = 80
    else:
        while True: #creo un ciclo in modo da costringere l'utente ad immettere un valore corretto per la porta (se immette un valore sbagliato lo faccio riprovare all'infinito)
            if input_port == '': #rifaccio il controllo del comando vuoto altrimenti se a questo punto l'utente preme direttamente invio darebbe un errore
                input_port = 80
            try:
                input_port = int(input_port) #prova a convertire il valore port in un intero, se non ci riesci passi ad "except"
                break
            except:
                print("Inserisci un numero!") #Lancio un errore.
                input_port = input('Inserire la porta (default: 80): ')   #Faccio immettere nuovamente l'input port e ricomincio il ciclo


    # --- CONTROLLO VERB ---
    valid_verbs = ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH"] # Lista di comandi esistenti
    while True:
        input_verb = input('Inserire la tua richiesta (GET, POST, ): ').strip().upper() # strip() Rimuove eventuali spazi accidentali, upper() mette tutto in maiuscolo.

        if input_verb in valid_verbs: #Se il comando inserito appartiene alla lista valid_verbs[] allora...
            break# ...esci dal ciclo
        else:#Altrimenti...
            print('Il comando che hai inserito non è valido, riprova.')#...printo l'errore e ripeto il ciclo


    # --- CONTROLLO PATH ---
    input_path = input('Inserire la directory che vuoi analizzare (default "/"): ').strip()
    if input_path == '': #se non scrivo nulla e premo invio...
        input_path = '/'#...il path scelto è la Home
    elif not input_path.startswith("/"): #altrimenti se il path non inizia con una "/"
        input_path = "/" + input_path # Esempio: se l'utente scrive "file/images" allora diventa in automatico "/file/images"

# --- NUOVO: CONTROLLO BODY E HEADERS (Per POST/PUT) ---
    input_body = None
    input_headers = {}

    # Se il metodo prevede invio di dati, chiediamo il body
    if input_verb in ["POST", "PUT", "PATCH"]:
        print(f"\n[INFO] Hai selezionato {input_verb}. È necessario inviare dei dati.")
        input_body = input('Inserire il BODY della richiesta: ')

        # Di default impostiamo un content-type generico se c'è un body.
        # In un tool avanzato potresti chiedere anche il Content-Type (json, html, ecc.)
        input_headers = {"Content-type": "application/x-www-form-urlencoded"} #"Content-type": application/x-www-form-urlencoded è il formato standard dei moduli.


    return input_host , input_port , input_verb , input_path, input_body, input_headers

def httprequest(host, port, verb, path, body, headers):

    try:
        connection = http.client.HTTPConnection(host, port) #APRE il canale di comunicazione con il server.
        connection.request(verb, path, body=body, headers=headers) #Invia la richiesta vera e propria. Il primo valore di request indica il verbo, la seconda indica il path (In questo caso "/" indica la radice ovvero la cartella iniziale, la Home).

        response = connection.getresponse() #Il server risponde e noi salviamo quella risposta nella variabile response.


        print(f"\n--- RISPOSTA SERVER ---")
        print(f"Status: {response.status} {response.reason}")

        # --- LOGICA DI CONTROLLO LOGIN ---
        # Cerchiamo l'header "Location"
        location_header = None
        for k, v in response.getheaders():
            print(f"  {k}: {v}") # Stampiamo tutto per debug
            if k == 'Location':
                location_header = v

        print("-----------------------")

        # LOGICA DI SUCCESSO/FALLIMENTO SPECIFICA PER DVWA
        if response.status == 302 and location_header:
            if "login.php" in location_header:
                print("\n[!] RISULTATO: LOGIN FALLITO (Reindirizzato al login)")
            elif "index.php" in location_header:
                print("\n[***] RISULTATO: LOGIN RIUSCITO! (Reindirizzato alla home)")
            else:
                print(f"\n[?] RISULTATO: Redirect sconosciuto verso {location_header}")


        connection.close()

    except ConnectionRefusedError:
        print("Connessione fallita")

def print_team_banner():
    print(r"""
      ____                        _   ___    ____  _                                 _ _
     / ___| _ __   ___  __ _ _ __(_) ( _ )  |  _ \(_) __ _  ___ ___ ___ _ __   __| (_)
     \___ \| '_ \ / _ \/ _` | '_ \ | / _ \/\| |_) | |/ _` |/ __/ __/ _ \ '_ \ / _` | |
      ___) | |_) |  __/ (_| | | | | | (_>  <|  _ <| | (_| | (_| (__  __/ | | | (_| | |
     |____/| .__/ \___|\__, |_| |_|_|\___/\/|_| \_\_|\__,_|\___\___\___|_| |_|\__,_|_|
           |_|         |___/
    """)

def print_tool_banner():
    print(r"""
     _   _ _____ _____ ____  ____
    | | | |_   _|_   _|  _ \/ ___|
    | |_| | | |   | | | |_) \___ \  ___ __ _ _ __  _ __   ___ _ __
    |  _  | | |   | | |  __/ ___) |/ __/ _` | '_ \| '_ \ / _ \ '__|
    |_| |_| |_|   |_| |_|   |____/ \___\__,_|_| |_|_| |_|\___|_|
    """)

if __name__ == "__main__":
    main()
