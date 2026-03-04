# OCI Data Science AI Prototype - Chicago Murals Semantic Search

## Overview

This repository demonstrates a practical, end-to-end AI workflow built inside **Oracle Cloud Infrastructure (OCI) Data Science**.  
The project uses publicly available data from the City of Chicago mural catalog and showcases how to:

- Ingest API-based open data
- Normalize and prepare text data
- Generate embeddings
- Build a FAISS vector index
- Persist artifacts to Object Storage
- Perform semantic search
- Visualize structured and geospatial results

The goal of this project is educational and architectural: to demonstrate how a small team can build enterprise-ready AI prototypes using OCI-native tooling and open data.

---

# Architecture Flow

The notebooks are organized sequentially to reflect a realistic AI pipeline:

1. **Data Ingestion**
2. **Normalization / Feature Preparation**
3. **Embedding Generation**
4. **Vector Index Creation (FAISS)**
5. **Artifact Persistence (Object Storage)**
6. **Semantic Search Querying**
7. **Tabular & Geospatial Visualization**

Each script is intentionally modular to mirror production design patterns.

---

# Project Structure

```
10_ingest_chimural.py
20_normalize_chimural.py
30_embedding_chimural.py
40_build_FAISS_index_chimural.py
42_upload_to_object_storage_chimural.py
50_semantic_search_chimural.py
60_viz_table_chimural.py
62_viz_map_chimural.py
```

The numeric prefixes enforce execution order and make orchestration straightforward.

---

# Detailed Module Notes

## 10_ingest_chimural.py

Purpose:
- Connects to the City of Chicago open data API
- Pulls mural metadata
- Stores raw dataset locally within the OCI notebook session

Key Concepts Demonstrated:
- API-based ingestion without authentication
- Structured JSON retrieval
- Lightweight data landing zone pattern

Enterprise Parallel:
This mirrors ingestion from:
- REST APIs
- SaaS platforms
- External vendor feeds

---

## 20_normalize_chimural.py

Purpose:
- Cleans text fields
- Combines relevant descriptive attributes
- Prepares text corpus for embedding generation

Key Concepts:
- Text normalization
- Field selection for embedding context
- Feature engineering for NLP tasks

Why This Matters:
Embedding quality is heavily dependent on curated text input.  
Well-designed context strings significantly improve semantic retrieval quality.

---

## 30_embedding_chimural.py

Purpose:
- Generates vector embeddings from mural descriptions

Key Concepts:
- Transformer-based embedding models
- Converting text → numeric vector representations
- Storing embeddings alongside metadata

OCI Relevance:
- Can leverage OCI Data Science notebooks
- Compatible with ONNX models
- Extendable to Oracle 26ai vector columns

This stage converts unstructured data into AI-queryable assets.

---

## 40_build_FAISS_index_chimural.py

Purpose:
- Builds a FAISS vector index from embeddings

Key Concepts:
- Approximate nearest neighbor search
- Index type selection
- Tradeoffs between speed and recall

Why FAISS?
- Fast
- Memory efficient
- Production-proven in vector search systems

Enterprise Parallel:
This is conceptually similar to Oracle 26ai vector indexing but implemented here in Python for demonstration and experimentation.

---

## 42_upload_to_object_storage_chimural.py

Purpose:
- Uploads vector index artifacts and datasets to OCI Object Storage

Key Concepts:
- OCI SDK usage
- Artifact persistence
- Separation of compute and storage

Production Design Pattern:
- Notebooks are ephemeral
- Artifacts must be externalized
- Object Storage becomes the persistent layer

This aligns with enterprise cloud governance best practices.

---

## 50_semantic_search_chimural.py

Purpose:
- Accepts a user query
- Embeds the query
- Executes nearest-neighbor search
- Returns relevant murals

Key Concepts:
- Query embedding generation
- Similarity scoring
- Vector search workflow

This demonstrates a foundational Retrieval-Augmented workflow pattern.

---

## 60_viz_table_chimural.py

Purpose:
- Presents search results in structured tabular format

Key Concepts:
- DataFrame transformation
- Readable output formatting
- Bridging AI output with business-friendly presentation

---

## 62_viz_map_chimural.py

Purpose:
- Plots mural search results geographically

Key Concepts:
- Latitude / longitude visualization
- Geospatial presentation of AI results
- Turning embeddings into actionable insight

This step reinforces that AI prototypes should end in visualization and usability.

---

# Key OCI Concepts Demonstrated

## OCI Data Science
- Notebook Sessions
- Conda environments
- Model experimentation

## Object Storage
- Artifact persistence
- Cloud-native storage

## IAM & Security (Implicit)
- Compartment isolation
- Region-specific deployment (tested in us-ashburn-1)
- Policy-driven access

---

# How to Run

1. Provision OCI Data Science Notebook Session
2. Upload project files
3. Configure environment dependencies (transformers, faiss, pandas, oci SDK)
4. Execute scripts in numeric order
5. Provide semantic query input
6. Review results and map visualization

---

# Design Principles Reflected

- Modular execution
- Clear pipeline staging
- Cloud-native artifact management
- Open data experimentation without governance friction
- Small-team feasibility

---

# Extensibility Opportunities

This prototype can be extended to:

- Oracle 26ai vector tables
- OAC dashboards for visualization
- RAG pipelines using LLMs
- Multi-dataset federated search
- Enterprise data catalogs
- Governance workflows

---

# Intended Audience

- Data professionals exploring OCI Data Science
- Teams building AI prototypes with limited headcount
- ERP / analytics professionals transitioning into AI-enabled solutions
- Public sector open data experimentation

---

# Limitations

- Not production hardened
- No automated orchestration
- No CI/CD
- No full IAM documentation
- No performance benchmarking

This is a demonstration project.

---

# Versioning

Initial development was completed locally and validated in OCI (us-ashburn-1 region).

Recommended initial release tag:

v0.1.0 – Functional prototype demonstrating semantic search workflow

---

# License Recommendation

If sharing publicly, consider:

- GPL-3.0 (prevents proprietary repackaging)
- AGPL-3.0 (if hosted as a service)

---

# Final Notes

This repository reflects a practical, hands-on approach to AI in OCI.
It emphasizes:

- Real data
- Real architecture decisions
- Real cloud integration

It is designed to show that meaningful AI capability does not require a large research team — only thoughtful architecture and disciplined execution.

---

If presenting this project publicly, consider including:

- An architecture diagram
- A short demo video
- A discussion of FAISS index tradeoffs
- A comparison to Oracle 26ai vector indexing

This transforms the repo from code sample into thought leadership artifact.

