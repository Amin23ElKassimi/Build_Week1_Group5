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
# - Possibilità di assegnare il tipo di richiesta (Verbo) tramite una variabile input; stessa cosa con la directory. (A RIGA 13)
# - Migliorare la struttura dello script usando le funzioni e "Main():".
# - Rendiamo il programma continuo (ciclo while) in modo da evitare che alla fine di ogni verifica HTTP il programma si spegne, dobbiamo poterlo spegnere noi digitando "exit" per esempio.






import http.client #Importiamo l'estenzione necessaria per parlare con i server web.

host = input('Inserire IP: ') #Input in cui inserire IPv4 che intendiamo visitare.
port = input('Inserire la porta (default: 80): ') #Input in cui inserire la porta che utilizzeremo per collegarci.
verb = input('Inserire la tua richiesta (GET, POST, ): ') #Input in cui inserire il verbo di richiesta da utilizzare.
path = input('Inserire la directory che vuoi analizzare ("/" per la Home): ') #Input in cui inserire il verbo di richiesta da utilizzare.


if port == '': #SE immettiamo un input vuoto allora utilizza in automatico la porta 80
    port = 80
else:
    port = int(port) #ALTRIMENTI utilizza la porta del numero immesso, int() converte la stringa ad intero.

try:
    connection = http.client.HTTPConnection(host, port) #APRE il canale di comunicazione con il server.
    connection.request(verb, path) #Invia la richiesta vera e propria. Il primo valore di request indica il verbo, la seconda indica il path (In questo caso "/" indica la radice ovvero la cartella iniziale, la Home).
    response = connection.getresponse() #Il server risponde e noi salviamo quella risposta nella variabile response.

    body_bytes = response.read() #Assegnamo alla variabile body_bytes la risposta che il server ci da (Risposta grezza, non decodificata)
    body_string = body_bytes.decode('utf-8', errors='replace') # Assegnamo alla variabile body_string la versione DECODIFICATA della risposta    utf-8 --> "traduci byte in caratteri leggibili"  errors='replace' --> "se incontri byte intraducibili non darmi errori, rimpiazzali con ?".

    print(f'body_bytes è {body_bytes}') #Stampa versione codificata della risposta.
    print(f'body_string è {body_string}') #Stampa la versione decodificata della risposta.

    connection.close()
except ConnectionRefusedError: #SE qualcosa non va (IP errato, Server spento etc..) allora stampa "Connessione fallita".
    print("Connessione fallita")

