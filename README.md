# Enterprise Data Governance & Quality Agent (MCP)

[![CI Pipeline](https://github.com/richardwijaya04/enterprise-data-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/richardwijaya04/enterprise-data-agent/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastMCP](https://img.shields.io/badge/protocol-Model%20Context%20Protocol-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An autonomous Model Context Protocol (MCP) server engineered for enterprise data governance, automated data contract verification, PII redaction, and data quality profiling using DuckDB and Pydantic.

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client[AI Client / Claude / Cursor] -->|JSON-RPC via stdio / SSE| Server[FastMCP Server Core]
    
    subgraph Governance Tools
        Server --> Tool1[Tool: validate_table_schema]
        Server --> Tool2[Tool: sanitize_sensitive_payload]
        Server --> Tool3[Tool: inspect_data_quality]
    end

    subgraph Core Engines
        Tool1 --> Inspector[Schema Drift Inspector]
        Tool2 --> PIIGuard[PII Compliance Engine]
        Tool3 --> Profiler[Data Quality Profiler]
    end

    Inspector -->|In-Memory Analytics| DuckDB[(DuckDB / Parquet Lakehouse)]
    Profiler -->|SQL Analytics| DuckDB
    PIIGuard -->|Regex Sanitation| RedactedText[Sanitized Payload]
✨ Key Features
Schema Drift Detection (validate_table_schema): Validates physical table schemas against strict TableContract definitions to catch missing columns, unexpected fields, and type mismatches.

PII Sanitation & Guardrails (sanitize_sensitive_payload): High-performance engine to detect and redact sensitive data (Emails, Credit Cards, Phone Numbers) prior to LLM processing.

Automated Data Quality Profiling (inspect_data_quality): Calculates null entry percentages, identifies duplicate rows, and computes an overall data health score.

🚀 Quickstart Guide
Prerequisites
Python 3.12+

uv package manager

1. Installation & Environment Setup
Bash
git clone [https://github.com/richardwijaya04/enterprise-data-agent.git](https://github.com/richardwijaya04/enterprise-data-agent.git)
cd enterprise-data-agent

# Pin Python version and sync virtual environment
uv python pin 3.12
uv sync --all-extras --dev
source .venv/bin/activate
2. Generate Synthetic Test Warehouse
Bash
uv run python -m enterprise_data_agent.core.mock_data
3. Run Automated Testing Suite
Bash
uv run pytest --cov=src
4. Container Deployment (Docker)
Bash
# Build lightweight multi-stage image
docker build -t enterprise-data-agent .

# Run containerized MCP server
docker run -p 8000:8000 enterprise-data-agent
🧪 Engineering Standards
Testing: TDD methodology with pytest (>85% coverage enforced via CI)

Code Hygiene: Strict formatting and linting via ruff

CI/CD: Automated GitHub Actions build & test pipeline
