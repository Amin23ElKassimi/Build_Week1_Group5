# Configurazione con un Singolo Firewall
**Obiettivo:** Creare un'architettura di rete sicura centralizzata su un unico firewall pfSense che gestisce tre zone: Internet (WAN), Zona Demilitarizzata (DMZ) e Rete Interna (LAN).

---

## 1. Piano di Indirizzamento IP (Statico)

Definiamo le reti per evitare conflitti:

* **Interfaccia WAN (Internet):**
    * Rete: `192.168.1.x` (o quella del tuo router fisico).
    * Configurazione: **DHCP** (per semplicità di accesso a Internet).

* **Interfaccia DMZ (OPT1 - Server):**
    * Rete: `192.168.100.0/24`
    * **pfSense (Gateway):** `192.168.100.1`
    * **Meta2 (Server Web):** `192.168.100.50`

* **Interfaccia LAN (Internal - Client):**
    * Rete: `192.168.11.0/24`
    * **pfSense (Gateway):** `192.168.11.1`
    * **Kali Linux:** `192.168.11.100` (o DHCP)

---

## 2. Configurazione Macchine Virtuali (Cavi Virtuali)

Prima di avviare le VM, configuriamo le schede di rete su VirtualBox/VMware.

### VM: pfSense (Il Cuore della Rete)
Questa VM deve avere **3 Schede di Rete**:
1.  **Adapter 1 (WAN):** Scheda con Bridge (Bridged Adapter).
2.  **Adapter 2 (LAN):** Rete Interna -> Nome: `theta_net` (Per Kali).
3.  **Adapter 3 (OPT1):** Rete Interna -> Nome: `DMZ_net` (Per Meta2).

### VM: Kali Linux (Client Sicuro)
1.  **Adapter 1:** Rete Interna -> Nome: `theta_net`.

### VM: Meta2 (Server Vittima)
1.  **Adapter 1:** Rete Interna -> Nome: `DMZ_net`.

---

## 3. Configurazione Base pfSense (Console)

Avvia pfSense. Una volta caricato, vedrai il menu testuale.

### A. Assegnazione Interfacce
1.  Seleziona **Option 1** (Assign Interfaces).
2.  Il sistema rileverà 3 interfacce (es. `em0`, `em1`, `em2`).
    * **WAN:** `em0`
    * **LAN:** `em1`
    * **OPT1:** `em2` (Ti chiederà se vuoi aggiungere una nuova interfaccia, dì di sì).
3.  Salva.

### B. Configurazione IP
Seleziona **Option 2** (Set interface IP address).

1.  **WAN:** Lascia DHCP.
2.  **LAN:**
    * IP Address: `192.168.11.1`
    * Subnet: `24`
    * Gateway: *Invio (Nessuno)*
    * DHCP Server: **y** (Sì, comodo per Kali). Range: `.100` - `.200`.
3.  **OPT1 (che diventerà DMZ):**
    * IP Address: `192.168.100.1`
    * Subnet: `24`
    * Gateway: *Invio (Nessuno)*
    * DHCP Server: **n** (No, usiamo IP statico su Meta2).

---

## 4. Configurazione Avanzata pfSense (Web GUI)

Accedi a Kali Linux. Il firewall assegnerà un IP automatico. Apri Firefox e vai su `https://192.168.11.1`.
Login: `admin` / `pfsense`.

### A. Rinominare l'interfaccia OPT1
1.  Vai su **Interfaces > OPT1**.
2.  **Enable:** Spunta la casella "Enable Interface".
3.  **Description:** Cambia da `OPT1` a `DMZ`.
4.  **IPv4 Configuration:** Static IPv4 (dovrebbe essere già settato).
5.  Clicca **Save** e **Apply Changes**.

### B. Sbloccare la WAN (Per Lab)
1.  Vai su **Interfaces > WAN**.
2.  In fondo, **deseleziona** (togli la spunta):
    * `Block private networks...`
    * `Block bogon networks...`
3.  **Save** e **Apply**.

---

## 5. Configurazione Meta2 (Static IP)

Avvia Meta2. Login: `msfadmin` / `msfadmin`.

1.  Edita il file di rete:
    `sudo nano /etc/network/interfaces`

2.  Modifica `eth0` per renderla statica:
    ```bash
    auto eth0
    iface eth0 inet static
    address 192.168.100.50
    netmask 255.255.255.0
    gateway 192.168.100.1
    dns-nameservers 8.8.8.8
    ```

3.  Salva (`Ctrl+O`, `Invio`) ed Esci (`Ctrl+X`).
4.  Riavvia: `sudo reboot`.
5.  **Test:** Prova a pingare il gateway `ping 192.168.100.1`. (Se non risponde ancora è normale, mancano le regole firewall).

---

## 6. Regole di Sicurezza (Firewall Rules)

Questa è la parte che rende la configurazione sicura.

### A. Regole Interfaccia DMZ (Proteggere la LAN)
Vai su **Firewall > Rules > DMZ**.
Crea le regole in questo ordine preciso (dall'alto in basso):

1.  **Regola 1: BLOCCO verso LAN** (Impedisce a Meta2 di attaccare Kali)
    * **Action:** Block
    * **Protocol:** Any
    * **Source:** DMZ net
    * **Destination:** LAN net (`192.168.11.0/24`)
    * **Description:** Block DMZ to LAN

2.  **Regola 2: Permesso Internet** (Permette a Meta2 di uscire)
    * **Action:** Pass
    * **Protocol:** Any
    * **Source:** DMZ net
    * **Destination:** Any
    * **Description:** Allow DMZ to Internet

*Clicca **Apply Changes**.*

### B. Regole Interfaccia LAN
Vai su **Firewall > Rules > LAN**.
Assicurati che esista la regola "Default allow LAN to any rule".
* *Nota:* Kali, essendo sulla LAN, può connettersi sia a Internet che alla DMZ (per simulare l'attacco).

### C. Port Forwarding (Esporre Meta2 all'esterno)
Vai su **Firewall > NAT > Port Forward**.
Clicca **Add**:

* **Interface:** WAN
* **Protocol:** TCP
* **Destination Port Range:** HTTP (80)
* **Redirect Target IP:** `192.168.100.50`
* **Redirect Target Port:** HTTP (80)
* **Description:** Forward Web to Meta2

*Clicca **Save** e **Apply Changes**.*

---

## 7. Verifica Finale e Test

1.  **Test Navigazione (Kali):**
    * Apri Firefox su Kali e vai su `google.com`. -> **Deve funzionare.**

2.  **Test Accesso Web Esterno:**
    * Dal tuo PC fisico (reale), apri il browser e digita l'IP WAN di pfSense (es. `192.168.1.x`).
    * Dovresti vedere la pagina di Meta2/Metasploitable. -> **Deve funzionare.**

3.  **Test Sicurezza (Isolamento):**
    * Vai sulla console di Meta2.
    * Digita `ping 192.168.11.100` (IP di Kali).
    * -> **NON DEVE funzionare** (Bloccato dalla Regola 1 della DMZ).
