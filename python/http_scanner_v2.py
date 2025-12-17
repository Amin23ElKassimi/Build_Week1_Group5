import http.client  # Importo il modulo necessario per far parlare il mio script con i server web.
import urllib.parse  # Importo gli strumenti per codificare i dati nel formato corretto per gli URL.

def test_phpmyadmin(host, port, path):  # Creo la mia funzione di test: decido io l'indirizzo IP.
    print(f"[*] Avvio test su: {host}:{port}{path}\n")  # Scrivo a video quale indirizzo sto per analizzare.

    body_data = {  # Preparo il pacchetto di dati per simulare un tentativo di accesso (login).
        "pma_username": "root",  
        "pma_password": "",  
        "server": "1",  
        "lang": "en", 
        "token": "e1ac3d57e592bebe00bdf33252fb9386"  
    }
    
    encoded_body = urllib.parse.urlencode(body_data)  # Trasformo i dati che ho preparato sopra in una stringa di testo che il server riesca a leggere.

    headers = {  # Qui preparo la mia "carta d'identità" digitale per ingannare il server e sembrare un browser vero.
        "Host": host,  # Gli dico chi sto cercando.
        "User-Agent": "Mozilla/5.0...",  
        "Accept": "text/html...", 
        "Accept-Language": "en-US...",  
        "Referer": f"http://{host}/phpMyAdmin/", 
        "Content-Type": "application/x-www-form-urlencoded",  
        "Origin": f"http://{host}",  
        "Connection": "close",  
        "Cookie": "phpMyAdmin=..." 
    }

    verbs = ["GET", "POST", "HEAD", "PUT", "DELETE"]  # Faccio la lista dei comandi che voglio provare uno alla volta.
    results = []  # Preparo un contenitore vuoto dove mi annoterò come è andata ogni prova.

    for verb in verbs:  # Inizio il giro: prendo un comando alla volta dalla lista e lo eseguo.
        connection = None  # Prima di iniziare, mi assicuro di non avere connessioni vecchie aperte.
        try:  # Provo a collegarmi.
            connection = http.client.HTTPConnection(host, port, timeout=5)  # Apro il canale con il server, ma aspetto al massimo 5 secondi.
            
            print(f"\n--- Testing {verb} {path} ---")  # Scrivo a video cosa sto testando adesso.
            
            if verb == "POST":  # Se il comando è "POST" (cioè devo inviare dati)...
                connection.request(verb, path, body=encoded_body, headers=headers)  # ...invio la richiesta allegando il pacchetto dati che ho preparato prima.
            else:  # Se invece è un altro comando (come GET, che serve solo a leggere)...
                connection.request(verb, path, headers=headers)  # ...invio la richiesta senza allegati.

            response = connection.getresponse()  # Aspetto la risposta del server e la salvo.
            
            data = response.read().decode("utf-8", errors="ignore")  # Leggo il contenuto della risposta e lo traduco in testo leggibile.
            
            print(f"Status: {response.status} {response.reason}")  # Stampo il risultato numerico (es. 200) e il messaggio (es. OK).
            print(f"Server: {response.getheader('Server')}")  # Stampo che tipo di software sta usando il server.
            
            if response.getheader('Set-Cookie'):  # Se il server prova a darmi un cookie...
                print(f"Set-Cookie: {response.getheader('Set-Cookie')}")  # ...lo mostro a video.
            if response.getheader('Location'):  # Se il server vuole spedirmi su un'altra pagina...
                print(f"Location: {response.getheader('Location')}")  # ...stampo dove vuole mandarmi.
            
            print(f"Body length: {len(data)} chars")  # Conto quanti caratteri mi ha risposto e lo scrivo.
            print("-" * 60)  # Tiro una riga per separare visivamente questo test dal prossimo.
            
            results.append((verb, response.status, response.reason))  # Mi segno il risultato finale di questo tentativo nella mia lista.

        except Exception as e:  # Se qualcosa va storto (il server è spento o non risponde)...
            print(f"Errore critico durante {verb}: {e}")  # ...scrivo l'errore a video.
            results.append((verb, "ERROR", str(e)))  # ...e registro che questo tentativo è fallito.
        
        finally:  # Alla fine di tutto, qualsiasi cosa sia successa...
            if connection:  # ...se la connessione è ancora attiva...
                connection.close()  # ...la chiudo per fare pulizia.

    print("\n=== Riepilogo Risultati ===")  # Stampo il titolo della mia tabella riassuntiva.
    print(f"{'VERBO':<8} | {'STATUS':<6} | {'MESSAGGIO'}")  # Preparo le intestazioni della tabella.
    print("-" * 35)  # Disegno una riga divisoria.
    for v, s, r in results:  # Rileggo la lista dei miei appunti...
        print(f"{v:<8} | {s:<6} | {r}")  # ...e stampo ogni risultato in modo ordinato.

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
    print_team_banner()  
    print_tool_banner()  
    
    while True:  
        print('\n\n   --->Digita exit per uscire <---\n')  
        host = input('Inserisci l\'IPv4 che vuoi analizzare: ')
        if host == 'exit': 
            break  
        port = input('Inserisci la porta che vuoi analizzare: ')
        if port == 'exit': 
            break 
        path = input('Inserisci la Directory: ')
        if path == 'exit':  
            break 
        else:  
            test_phpmyadmin(host, port, path)  # Altrimenti, lancio la mia funzione di test sull'indirizzo scelto.