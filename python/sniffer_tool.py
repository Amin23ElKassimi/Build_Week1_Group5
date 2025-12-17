#IMPORTANTE: AVVIA IL PROGRAMMA IN MODALITÀ AMMINISTRATORE

from scapy.all import sniff, IP, TCP
import sys

def analizza_pacchetto(packet):
    """
    Funzione di callback che viene eseguita per ogni pacchetto catturato.
    """
    # Controlliamo se il pacchetto ha un livello IP
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Info base
        info = f"[+] Pacchetto: {src_ip} -> {dst_ip}"
        
        # Se c'è un livello TCP, mostriamo le porte e i flag
        if TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            flags = packet[TCP].flags
            info += f" | Protocollo: TCP | Porte: {sport} -> {dport} | Flags: {flags}"
            
            # Se c'è un payload (dati), proviamo a mostrarlo
            if packet[TCP].payload:
                try:
                    # Tentiamo di decodificare il payload in stringa
                    payload_data = bytes(packet[TCP].payload).decode('utf-8', errors='ignore')
                    if payload_data:
                        info += f"\n    Dati: {payload_data.strip()}"
                except:
                    pass
        
        print(info)
        print("-" * 60)

def avvia_sniffer():
    print("--- Sniffer per Metasploitable ---")
    target_ip = input("Inserisci l'IP della Metasploitable: ")
    target_port = input("Inserisci la porta (es. 21, 80, 445): ")
    interface = "eth0" # Solitamente eth0 su Kali, controlla con 'ip a'

    print(f"\n[*] In ascolto su {interface}...")
    print(f"[*] Filtro: host {target_ip} and port {target_port}")
    
    # La stringa di filtro BPF (Berkeley Packet Filter)
    bpf_filter = f"host {target_ip} and port {target_port}"

    try:
        # sniff() cattura i pacchetti. 
        # filter: applica il filtro BPF
        # prn: esegue la funzione 'analizza_pacchetto' per ogni pacchetto trovato
        # store: 0 significa che non li salviamo in memoria (per evitare di riempire la RAM)
        sniff(iface=interface, filter=bpf_filter, prn=analizza_pacchetto, store=0)
    except KeyboardInterrupt:
        print("\n[!] Sniffer interrotto.")
    except Exception as e:
        print(f"\n[!] Errore: {e}")

if __name__ == "__main__":
    avvia_sniffer()