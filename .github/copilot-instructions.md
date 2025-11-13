# AI Coding Agent Instructions for Graph-of-America

## Project Overview
This is a **cybersecurity graph analysis project** that converts IP-based attack data into country-level network graphs, performs community detection, and analyzes centrality metrics. The project uses Jupyter notebooks for sequential data processing and analysis.

## Critical Architecture Decisions

### Sequential Notebook Pipeline
The analysis follows a strict **two-stage pipeline**:
1. **`00_IP_to_Country_Graph.ipynb`**: IP geolocation → country-pair graph creation
2. **`01_Graph_Analysis_Communities.ipynb`**: Graph analysis, community detection, centrality metrics

**Always run notebooks in order**. Notebook 01 depends on outputs from 00.

### Data Flow Pattern
```
cybersecurity_large_synthesized_data.csv (raw IPs)
  → [00_IP_to_Country_Graph] → 
    - cyber_attacks_with_countries.csv (IP+country enriched)
    - cyber_attacks_graph.gml (NetworkX graph)
    - cyber_attacks_country_graph.csv (edge list)
  → [01_Graph_Analysis_Communities] →
    - community_assignments.csv
    - node_centrality_metrics.csv
    - community_statistics.csv
```

## Environment Setup

### Python Environment
- **Always activate the virtual environment first**: `.venv/` exists in project root
- Activation command: `source .venv/bin/activate`
- Key dependencies (install if missing):
  - `python-louvain` (community detection - already installed)
  - `maxminddb`, `geoip2`, `networkx`, `pandas`, `matplotlib`, `seaborn`

### External Data Dependencies
- **GeoLite2-Country.mmdb**: Required MaxMind database for IP→country conversion
  - Located in: `data/GeoLite2-Country.mmdb`
  - If missing, notebook 00 will fail or return only "XX" country codes
  - Download from MaxMind (free registration required)

## Project-Specific Patterns

### IP Geolocation Strategy (Notebook 00)
```python
# Uses maxminddb with multithreading (10 workers) for scalability
# Pattern: Extract unique IPs → parallel lookup → map back to dataframe
all_ips = pd.concat([df['attacker_ip'], df['target_ip']]).unique()
with ThreadPoolExecutor(max_workers=10) as executor:
    # ... parallel IP lookups with progress tracking
```
- **Unknown IPs return 'XX'** - filter these before graph construction
- Progress tracking prints every 500 IPs processed

### Graph Construction Convention
```python
# ALWAYS use directed graphs with edge weights
G = nx.DiGraph()
G.add_edge(attacker_country, target_country, weight=attack_count)
```
- **Nodes = ISO country codes** (2-letter)
- **Edges = attack routes** (attacker → target)
- **Edge weights = aggregated attack counts**

### Community Detection Approach (Notebook 01)
Uses **Louvain method as primary algorithm**:
```python
# Convert to undirected for community detection
G_undirected = G.to_undirected()
communities = community_louvain.best_partition(G_undirected, weight='weight')
```
- Compares 3 methods: Louvain, Label Propagation, Greedy Modularity
- **Selects highest modularity score**
- Alternative import fallback: `community.community_louvain` vs `community`

### Visualization Style
```python
# Consistent plotting configuration across notebooks
plt.rcParams['figure.figsize'] = (16, 12)  # Notebook 01
plt.rcParams['figure.figsize'] = (12, 8)   # Notebook 00
sns.set_style('whitegrid')
```
- Node sizes proportional to degree centrality
- Edge widths proportional to attack weights
- Color coding: out-degree (attackers) or community assignment

## Common Workflows

### Running Complete Analysis
```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Ensure GeoLite2-Country.mmdb exists in data/
ls data/GeoLite2-Country.mmdb

# 3. Run notebooks sequentially (in VS Code or Jupyter)
# Execute all cells in 00_IP_to_Country_Graph.ipynb
# Then execute all cells in 01_Graph_Analysis_Communities.ipynb
```

### Adding New Analysis
- **New features go in notebook 01** (graph already built)
- **New data sources modify notebook 00** (IP conversion logic)
- Preserve output CSV structure - other tools may depend on column names

### Debugging IP Conversion Issues
1. Check `GeoLite2-Country.mmdb` path and existence
2. Verify `maxminddb` package installed (not `geoip2.database` for current impl)
3. Check progress output - conversion rate should be >1000 IP/sec locally
4. If stuck at 0% successful lookups → database missing/wrong type

## File Structure Conventions

### Empty Directories
- `models/` and `utils/` currently unused - reserved for future extensions
- **Don't auto-populate** without explicit requirements

### Data Directory Organization
- `data/cybersecurity_large_synthesized_data.csv` - **primary input** (never overwrite)
- `data/test.csv` - development subset for testing
- `data/*.csv` (outputs) - regenerate by re-running notebooks
- `data/*.gml` - NetworkX graph serialization (Gephi-compatible)

## Graph Analysis Metrics (Notebook 01)

### Centrality Measures Calculated
```python
centrality_df columns:
- in_degree: incoming attack volume (target countries)
- out_degree: outgoing attack volume (attacker countries)  
- betweenness: bridge nodes in attack routes
- pagerank: influence score (weighted by incoming connections)
```

### Community Analysis Output
```python
community_assignments.csv: {country, community_id}
community_statistics.csv: {community_id, nodes, internal_edges, external_edges, total_attacks, density}
```

## Project-Specific Gotchas

1. **Don't use `nx.write_graphml()`** - project uses GML format for Gephi compatibility
2. **Filter 'XX' countries before graph ops** - they represent failed lookups, not a country
3. **Community detection requires undirected graph** - convert with `.to_undirected()` first
4. **Progress tracking expects specific format** - preserve print patterns for consistency
5. **Spring layout uses fixed seed=42** - ensures reproducible visualizations

## Testing Patterns
- Use `data/test.csv` (16 records) for quick iteration
- Switch to full dataset (`cybersecurity_large_synthesized_data.csv`) for production
- Verify outputs: edge count > 0, country codes != 'XX', modularity > 0.3

## When Adding Dependencies
Update notebook import cells consistently across both files. Current standard imports:
```python
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
```
