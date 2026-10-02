# Enterprise Data Governance & Quality Agent (MCP)

[![CI Pipeline](https://github.com/richardwijaya04/enterprise-data-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/richardwijaya04/enterprise-data-agent/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-MCP%20Server-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An autonomous Model Context Protocol (MCP) server for enterprise data governance, automated data contract verification, PII redaction, and data quality profiling, built with DuckDB and Pydantic.

## 🏗️ System Architecture

```mermaid
graph TD
    Client["AI Client (Claude / Cursor)"] -->|"JSON-RPC via stdio / SSE"| Server["FastMCP Server Core"]

    subgraph Tools["Governance Tools"]
        Tool1["validate_table_schema"]
        Tool2["sanitize_sensitive_payload"]
        Tool3["inspect_data_quality"]
    end

    subgraph Engines["Core Engines"]
        Inspector["Schema Drift Inspector"]
        PIIGuard["PII Compliance Engine"]
        Profiler["Data Quality Profiler"]
    end

    Server --> Tool1
    Server --> Tool2
    Server --> Tool3

    Tool1 --> Inspector
    Tool2 --> PIIGuard
    Tool3 --> Profiler

    Inspector -->|"In-Memory Analytics"| DuckDB[("DuckDB / Parquet Lakehouse")]
    Profiler -->|"SQL Analytics"| DuckDB
    PIIGuard -->|"Regex Sanitization"| Redacted["Sanitized Payload"]
```

## ✨ Key Features

- **Schema Drift Detection** (`validate_table_schema`): Validates physical table schemas against strict `TableContract` definitions to catch missing columns, unexpected fields, and type mismatches.
- **PII Sanitization & Guardrails** (`sanitize_sensitive_payload`): High-performance engine that detects and redacts sensitive data (emails, credit card numbers, phone numbers) before LLM processing.
- **Automated Data Quality Profiling** (`inspect_data_quality`): Calculates null percentages, identifies duplicate rows, and computes an overall data health score.

## 🚀 Quickstart Guide

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Installation & Environment Setup

```bash
git clone https://github.com/richardwijaya04/enterprise-data-agent.git
cd enterprise-data-agent

# Pin Python version and sync virtual environment
uv python pin 3.12
uv sync --all-extras --dev
source .venv/bin/activate
```

### 2. Generate Synthetic Test Warehouse

```bash
uv run python -m enterprise_data_agent.core.mock_data
```

### 3. Run Automated Test Suite

```bash
uv run pytest --cov=src
```

### 4. Container Deployment (Docker)

```bash
# Build lightweight multi-stage image
docker build -t enterprise-data-agent .

# Run containerized MCP server
docker run -p 8000:8000 enterprise-data-agent
```

## 🧪 Engineering Standards

- **Testing**: TDD methodology with `pytest` (>85% coverage enforced via CI)
- **Code Hygiene**: Strict formatting and linting via `ruff`
- **CI/CD**: Automated GitHub Actions build & test pipeline

## 📄 License

Released under the [MIT License](LICENSE).
