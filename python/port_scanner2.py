import socket
from datetime import datetime

def scan_port(target_ip, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        sock.close()

        if result == 0:
            return True
        else:
            return False
    except socket.error:
        return False


def port_scan(target, start_port, end_port):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Host non valido")
        return

    print(f"\nScansione avviata su {target} ({target_ip})")
    print(f"Porte {start_port}–{end_port}")
    print("Ora di inizio:", datetime.now())
    

    open_ports = []

    for port in range(start_port, end_port + 1):
        if scan_port(target_ip, port):
            print(f"[+] Porta {port} APERTA")
            open_ports.append(port)


    print("Scansione completata:", datetime.now())

    if open_ports:
        print("")
        
            
    else:
        print("\nNessuna porta aperta trovata")


if __name__ == "__main__":
    target_host = input("Inserisci IP o hostname: ")
    start = int(input("Porta iniziale: "))
    end = int(input("Porta finale: "))

    port_scan(target_host, start, end)

