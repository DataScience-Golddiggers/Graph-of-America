# Graph of America: Global Cybercrime Network Analysis

<div style="height; overflow:hidden; margin:auto; margin-bottom:2rem" align="center">
  <img src="./docs/images/yay.png" style="width:100%; height:50%; object-fit:cover; object-position:center;" />
</div>


![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![VisualStudioCode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Overleaf](https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&logo=Overleaf&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)
[![License](https://img.shields.io/badge/MIT-green?style=for-the-badge)](LICENSE)

**Graph of America** is a data science project that utilizes **Graph Theory** to analyze the dynamics of global cyber incidents. By modeling cyber operations as a network of interactions between nations (attackers and victims), this system identifies key geopolitical actors, frequent attack vectors, and hidden communities of conflict.

The project features a robust data pipeline that employs **Generative AI (LLMs)** for semantic data cleaning and advanced network analysis algorithms to uncover structural insights within the cyber domain.

## 🚀 Key Features

*   **Graph-Based Modeling**: Transforms cyber incident logs into a directed weighted graph (`Sponsor` → `Victim`), where edge weights represent attack frequency.
*   **Hybrid Data Normalization**: 
    *   **Heuristic Layer**: Uses regex and dictionaries for standardizing common country names.
    *   **AI-Powered Layer**: Integrates with local LLMs (via LM Studio) to extract country entities from unstructured text descriptions when heuristics fail.
*   **Advanced Network Metrics**: Calculates In-Degree, Out-Degree, Betweenness Centrality, and Eigenvector Centrality to characterize nation-state roles.
*   **Community Detection**: Applies the **Louvain algorithm** to identify geopolitical clusters and alliances.
*   **Structural Analysis**: Detects Maximal Cliques to pinpoint dense zones of reciprocal conflict.
*   **Rich Visualization**: Generates publication-ready plots using Matplotlib and Seaborn, including force-directed graph layouts.

## 📂 Project Structure

```
Graph-of-America/
├── data/                   # Raw datasets and generated outputs (CSV, GML, PNG)
│   ├── cyber_incidents_graph.gml      # Exported graph structure
│   └── cyber-operations-incidents.csv # Source dataset
├── docs/                   # Documentation and technical reports
├── models/                 # Additional graph models (Industry, Attack Type, etc.)
├── notebooks/              # Jupyter Notebooks for analysis
│   ├── 02_Cyber_Incidents_Graph.ipynb         # Data cleaning & Graph construction
│   ├── 03_Graph_Visualization_Analysis.ipynb  # Visualization & Statistical Analysis
│   ├── 03.1_Graph_Centrality_Analysis.ipynb   # Deep dive into centrality metrics
│   └── 03.2_Graph_Structurals_Analysis.ipynb  # Structural analysis (Communities, Cliques)
├── utils/                  # Utility scripts
│   └── llm_client.py       # Client for local LLM interaction (LM Studio)
└── requirements.txt        # Python dependencies
```

## 🛠️ Prerequisites

*   **Python 3.8+**
*   **LM Studio** (Optional, for running the AI normalization step):
    *   Used to run local models like `qwen/qwen3-vl-8b`.
    *   Must be configured to serve an OpenAI-compatible server at `http://localhost:1234`.

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/DataScience-Golddiggers/Graph-of-America.git
    cd Graph-of-America
    ```

2.  **Create a virtual environment** (Recommended)
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 📊 Usage

The analysis is divided into sequential notebooks:

### 1. Data Processing & Graph Construction
Run `notebooks/02_Cyber_Incidents_Graph.ipynb`.
*   **Input**: `data/cyber-operations-incidents.csv`
*   **Process**: Cleans data, normalizes country names (calling the LLM if necessary), and builds the network.
*   **Output**: `data/cyber_incidents_graph.gml`

> **Note**: To use the AI normalization, ensure LM Studio is running and the server is started. If not, the script handles connection errors gracefully by marking entries as "Unknown".

### 2. Analysis & Visualization
Run `notebooks/03_Graph_Visualization_Analysis.ipynb` (and 03.1 / 03.2).
*   **Input**: `data/cyber_incidents_graph.gml`
*   **Process**: Calculates centrality metrics, detects communities, and generates visualizations.
*   **Output**: Statistical plots and analysis reports in `data/`.

## 📈 Methodology Highlights

### Hybrid Normalization
We tackle the challenge of dirty data (e.g., "The hackers in Beijing") by first applying strict dictionary mapping. If a location is ambiguous, the `utils.llm_client` sends the text to a local LLM with a strict system prompt to extract only the country name, ensuring high data quality for the graph.

### Network Analysis
*   **Betweenness Centrality**: Used to find "proxy" nations that route attacks between major powers.
*   **Louvain Communities**: Automatically groups nations based on attack patterns, often revealing real-world geopolitical alignments without prior bias.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Authors**: DataScience-Golddiggers
