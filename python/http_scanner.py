# import http.client #Importiamo l'estenzione necessaria per parlare con i server web.

# host = input('Inserire IP: ') #Input in cui inserire IPv4 che intendiamo visitare.
# port = input('Inserire la porta (default: 80): ') #Input in cui inserire la porta che utilizzeremo per collegarci.

# if port == '': #SE immettiamo un input vuoto allora utilizza in automatico la porta 80
#      port = 80
# else:
#      port = int(port) #ALTRIMENTI utilizza la porta del numero immesso, int() converte la stringa ad intero.

# try:
#      connection = http.client.HTTPConnection(host, port) #APRE il canale di comunicazione con il server.
#      connection.request('GET', '/') #Invia la richiesta vera e propria. Il primo valore di request indica il verbo, la seconda indica il path (In questo caso "/" indica la radice ovvero la cartella iniziale, la Home).
#      response = connection.getresponse() #Il server risponde e noi salviamo quella risposta nella variabile response.

#      body_bytes = response.read() #Assegnamo alla variabile body_bytes la risposta che il server ci da (Risposta grezza, non decodificata)
#      body_string = body_bytes.decode('utf-8', errors='replace') # Assegnamo alla variabile body_string la versione DECODIFICATA della risposta    utf-8 --> "traduci byte in caratteri leggibili"  errors='replace' --> "se incontri byte intraducibili non darmi errori, rimpiazzali con ?".

#      #print(f'body_bytes è {body_bytes}') #Stampa versione codificata della risposta.
#      #print(f'body_string è {body_string}') #Stampa la versione decodificata della risposta.
#      print(f'body_string è {response}')

#      connection.close()
# except ConnectionRefusedError: #SE qualcosa non va (IP errato, Server spento etc..) allora stampa "Connessione fallita".
#      print("Connessione fallita")


   


#   PER MIGLIORARE IL CODICE/ HTTP_Scanner V2.0
# - Possibilità di assegnare il tipo di richiesta (Verbo) tramite una variabile input; stessa cosa con la directory. (A RIGA 13) / FATTO MA DA VERIFICARE
# - Migliorare la struttura dello script usando le funzioni e "Main():". / FATTO
# - Rendiamo il programma continuo (ciclo while) in modo da evitare che alla fine di ogni verifica HTTP il programma si spegne, dobbiamo poterlo spegnere noi digitando "exit" per esempio. / DA DISCUTERE






import http.client #Importiamo l'estenzione necessaria per parlare con i server web.




def main():
    print_team_banner()
    print_tool_banner()
    host, port, verb, path = initialize()
    httprequest(host, port, verb, path)


def initialize():
    input_host = input('Inserire IP: ') #Input in cui inserire IPv4 che intendiamo visitare.
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
                input_port = input('Inserire la porta (default: 80): ')   #Faccio immettere uovamente l'input port e ricomincio il ciclo

    input_verb = input('Inserire la tua richiesta (GET, POST, ): ') #Input in cui inserire il verbo di richiesta da utilizzare.
    input_path = input('Inserire la directory che vuoi analizzare ("/" per la Home): ') #Input in cui inserire il verbo di richiesta da utilizzare.
    return input_host , input_port , input_verb , input_path

def httprequest(host, port, verb, path):
    
    try:
        connection = http.client.HTTPConnection(host, port) #APRE il canale di comunicazione con il server.
        connection.request(verb, path) #Invia la richiesta vera e propria. Il primo valore di request indica il verbo, la seconda indica il path (In questo caso "/" indica la radice ovvero la cartella iniziale, la Home).
        response = connection.getresponse() #Il server risponde e noi salviamo quella risposta nella variabile response.

        body_bytes = response.read() #Assegnamo alla variabile body_bytes la risposta che il server ci da (Risposta grezza, non decodificata)
        body_string = body_bytes.decode('utf-8', errors='replace') # Assegnamo alla variabile body_string la versione DECODIFICATA della risposta    utf-8 --> "traduci byte in caratteri leggibili"  errors='replace' --> "se incontri byte intraducibili non darmi errori, rimpiazzali con ?".

        #print(f'body_bytes è {body_bytes}') #Stampa versione codificata della risposta.
        print(f'body_string è {body_string}') #Stampa la versione decodificata della risposta.

        connection.close()
    except ConnectionRefusedError: #SE il server esiste ma per qualche motivo ci rifiuta la connessione allora stampa "Connessione fallita".
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

