import socket
import struct
from datetime import datetime  # <--- Aggiunto per gestire il tempo

# Funzione ausiliaria per formattare il MAC Address
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

# Creazione del socket grezzo
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

print("Mini-Tcpdump avviato con timestamp... (Premi Ctrl+C per uscire)")

try:
    while True:
        # 1. CATTURA DEL PACCHETTO
        raw_data, addr = s.recvfrom(65535)
        
        # --- ACQUISIZIONE DATA E ORA CORRENTE ---
        # formatta l'ora attuale inclusi i microsecondi
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # 2. ANALISI LIVELLO ETHERNET
        dest_mac, src_mac, eth_proto = struct.unpack('! 6s 6s H', raw_data[:14])

        if socket.htons(eth_proto) == 8:
            # 3. ANALISI LIVELLO IP
            version_header_len = raw_data[14]
            ip_header_len = (version_header_len & 15) * 4 
            
            protocol = raw_data[23]
            src_ip = socket.inet_ntoa(raw_data[26:30])
            dst_ip = socket.inet_ntoa(raw_data[30:34])
            transport_start = 14 + ip_header_len 
            
            # 4. ANALISI LIVELLO TRASPORTO
            
            if protocol == 6: # TCP
                src_port, dst_port = struct.unpack('!HH', raw_data[transport_start:transport_start+4])
                print(f"[{timestamp}] [TCP] {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

            elif protocol == 17: # UDP
                src_port, dst_port = struct.unpack('!HH', raw_data[transport_start:transport_start+4])
                print(f"[{timestamp}] [UDP] {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

            elif protocol == 1: # ICMP
                print(f"[{timestamp}] [ICMP/Ping] {src_ip} -> {dst_ip}")
            
            else:
                print(f"[{timestamp}] [IP Altro] {src_ip} -> {dst_ip} (Prot: {protocol})")

except KeyboardInterrupt:
    print("\nSniffer interrotto.")
    s.close()