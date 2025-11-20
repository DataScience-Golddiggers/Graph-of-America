# Relazione Tecnica: Analisi a Grafo degli Incidenti Cyber

## 1. Introduzione e Obiettivi
Il progetto ha l'obiettivo di analizzare le dinamiche degli incidenti informatici globali attraverso la teoria dei grafi. Partendo da un dataset di operazioni cyber (`cyber-operations-incidents.csv`), il sistema costruisce una rete di interazioni tra paesi (attaccanti e vittime) per identificare gli attori principali, le rotte di attacco più frequenti e le comunità di nazioni che interagiscono maggiormente tra loro.

## 2. Architettura del Sistema
Il progetto è strutturato in una pipeline sequenziale di elaborazione dati, implementata tramite Jupyter Notebooks e moduli di utilità Python.

### Struttura dei Componenti
*   **`data/`**: Contiene i dataset grezzi (CSV) e i file generati (GML per i grafi, CSV per le metriche).
*   **`notebooks/`**:
    *   `02_Cyber_Incidents_Graph.ipynb`: Responsabile della pulizia dati, normalizzazione e costruzione del grafo.
    *   `03_Graph_Visualization_Analysis.ipynb`: Dedicato all'analisi statistica, calcolo delle metriche avanzate e visualizzazione.
*   **`utils/`**:
    *   `llm_client.py`: Modulo client per interagire con un LLM locale (LM Studio) per l'arricchimento semantico dei dati.

## 3. Pipeline di Elaborazione Dati (Notebook 02)

### 3.1 Pulizia e Pre-processing
Il processo inizia con il caricamento del dataset `cyber-operations-incidents.csv`. Viene effettuata una pulizia preliminare rimuovendo i record privi di informazioni sulla vittima (`Victims`), essenziali per definire i nodi del grafo.

### 3.2 Normalizzazione Ibrida (Regex + AI)
Uno degli aspetti più innovativi del progetto è il sistema di normalizzazione dei nomi dei paesi, che utilizza un approccio a due livelli:

1.  **Normalizzazione Euristica**: Una funzione `normalize_state_name` utilizza un dizionario completo (`COUNTRY_MAPPING`) e regole regex per mappare variazioni comuni (es. "PRC", "Beijing") ai nomi standard ISO. Gestisce casi ambigui come le due Coree con logiche di priorità.
2.  **Arricchimento tramite LLM**: Per i record che l'approccio euristico classifica come "Unknown", il sistema invoca il modulo `utils.llm_client`. Questo interroga un modello linguistico locale (es. Qwen via LM Studio) per estrarre il paese dal testo descrittivo non strutturato.

### 3.3 Costruzione del Grafo
Viene costruito un grafo diretto pesato (`nx.DiGraph`) dove:
*   **Nodi**: Paesi normalizzati.
*   **Archi**: Rappresentano un attacco dal paese `Sponsor` al paese `Victims`.
*   **Pesi**: Numero di incidenti registrati tra la coppia di paesi.

Il grafo viene esportato in formato GML (`cyber_incidents_graph.gml`) per garantire la compatibilità con strumenti esterni come Gephi e per l'uso nel notebook successivo.

## 4. Analisi e Visualizzazione (Notebook 03)

### 4.1 Metriche di Centralità
Vengono calcolate diverse metriche per caratterizzare il ruolo di ogni nazione nella rete:
*   **In-Degree**: Volume di attacchi subiti (Vittime principali).
*   **Out-Degree**: Volume di attacchi generati (Attaccanti principali).
*   **Betweenness Centrality**: Identifica i paesi che fungono da "ponte" o intermediari nelle rotte di attacco.
*   **Eigenvector Centrality**: Misura l'influenza di un nodo basata sulla connessione con altri nodi influenti.

### 4.2 Rilevamento delle Comunità
Utilizzando l'algoritmo di **Louvain** (sul grafo convertito in non orientato), il sistema identifica "comunità" di paesi che tendono ad interagire più frequentemente tra loro rispetto al resto della rete. Questo permette di evidenziare blocchi geopolitici o cluster di conflitto regionali.

### 4.3 Analisi dei Clique
Viene effettuata una ricerca dei **Massimi Clique** (sottografi completi) per individuare gruppi di nazioni in cui ognuna ha interagito con tutte le altre, indicando zone di conflitto denso e reciproco.

### 4.4 Visualizzazione
Il notebook produce visualizzazioni avanzate utilizzando `matplotlib` e `seaborn`:
*   Grafici di distribuzione delle metriche (KDE, istogrammi).
*   Matrici di correlazione tra le diverse metriche di centralità.
*   Rappresentazioni del grafo con layout di forza (Spring Layout e Kamada-Kawai), dove i nodi sono colorati in base alla comunità di appartenenza o alla centralità.

## 5. Tecnologie Utilizzate
*   **Linguaggio**: Python
*   **Analisi Grafi**: `NetworkX`, `python-louvain`
*   **Data Science**: `Pandas`, `NumPy`
*   **Visualizzazione**: `Matplotlib`, `Seaborn`
*   **AI/LLM**: Integrazione custom con API locali (LM Studio) tramite `requests`.

## 6. Conclusioni
Il lavoro svolto trasforma dati grezzi sugli incidenti cyber in intelligence strutturata. L'uso combinato di tecniche deterministiche e AI generativa per la pulizia dei dati garantisce un'alta qualità del grafo risultante, mentre l'analisi topologica fornisce insight non banali sulle dinamiche geopolitiche del dominio cyber.
