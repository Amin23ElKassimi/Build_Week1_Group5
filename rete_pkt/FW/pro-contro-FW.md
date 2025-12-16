# Analisi Comparativa: Architettura a Doppio Firewall vs Singolo Firewall

Questa analisi confronta le due topologie di rete discusse per il laboratorio di sicurezza:
1.  **Architettura a Doppio Firewall**.
2.  **Architettura a Singolo Firewall**.

---

## 1. Architettura a Doppio Firewall
**Riferimento Schema:**

In questa configurazione, i firewall sono disposti in serie:
`Internet` -> **[Firewall Perimetrale]** -> `DMZ` -> **[Firewall Interno]** -> `LAN`.

Questa soluzione rispecchia fedelmente lo scenario Packet Tracer originale e la richiesta opzionale della consegna ("potete comprarlo e montarlo").

### Pro
* **Difesa in profondità:** È il vantaggio principale. Se un attaccante compromette il firewall esterno (pfSense1), ottiene accesso solo alla DMZ. Per raggiungere la rete interna (Kali), deve superare un secondo firewall distinto.
* **Isolamento Forte:** La rete interna è fisicamente (o virtualmente) segregata. Un errore di configurazione sul primo firewall non espone direttamente la LAN.
* **Diversificazione (Security by Diversity):** In scenari reali, si possono usare vendor diversi (es. Cisco sul perimetro, pfSense all'interno). Se un exploit colpisce un brand, l'altro rimane sicuro.

### Contro
* **Complessità di Gestione:** Richiede la manutenzione di due sistemi operativi, due set di regole e tabelle di routing complesse. Il troubleshooting è più difficile.
* **Doppio NAT:** Il traffico in uscita dalla LAN viene tradotto due volte (NAT su pfSense2, poi NAT su pfSense1). Questo può causare problemi con protocolli specifici (es. VoIP, VPN IPsec, alcuni giochi online).
* **Consumo Risorse:** Richiede l'esecuzione di due macchine virtuali distinte per i firewall, aumentando il carico su CPU e RAM dell'host.

---

## 2. Architettura a Singolo Firewall
**Riferimento Schema:**

In questa configurazione, un unico firewall gestisce tre interfacce indipendenti:
1.  **WAN** (Internet)
2.  **DMZ** (Server Web / Meta2)
3.  **LAN** (Rete Interna / Kali)

### Pro
* **Gestione Centralizzata:** Tutte le regole di sicurezza (chi va dove) sono visibili in un'unica dashboard. È più facile avere una visione d'insieme del traffico.
* **Efficienza:** Elimina il "doppio salto" e il doppio NAT, riducendo la latenza e semplificando il routing.
* **Risparmio Risorse:** Richiede una sola macchina virtuale per gestire l'intera rete, ideale per laboratori con hardware limitato.
* **Standard PMI:** È la configurazione più diffusa nelle piccole e medie imprese per bilanciare costi e sicurezza.

### Contro
* **Single Point of Failure (SPOF):** Se il firewall si guasta o si blocca durante un aggiornamento, cade l'intera rete (sia Internet che l'accesso ai server).
* **Rischio "Errore Umano":** Se si sbaglia una regola sulla DMZ (es. permettendo traffico verso *Any* invece che *Internet*), si rischia di esporre inavvertitamente la LAN. Manca il "secondo muro" di sicurezza.
* **Compromissione Totale:** Se un attaccante ottiene i privilegi di `root` sul firewall, ha accesso immediato a tutte le sottoreti (DMZ e LAN) senza ulteriori ostacoli.

---

## 3. Tabella Riassuntiva

| Caratteristica | Doppio Firewall | Singolo Firewall |
| :--- | :--- | :--- |
| **Livello di Sicurezza** | ⭐⭐⭐⭐⭐ (Alto - Ridondante) | ⭐⭐⭐ (Buono - Basato su regole) |
| **Facilità Configurazione**| ⭐⭐ (Bassa - Routing complesso) | ⭐⭐⭐⭐ (Alta - Centralizzata) |
| **Resilienza** | Alta (Due livelli di protezione) | Bassa (Punto singolo di fallimento) |
| **Fedeltà alla Consegna** | Alta (Usa il "secondo firewall") | Media (Interpreta la DMZ logicamente) |

---
