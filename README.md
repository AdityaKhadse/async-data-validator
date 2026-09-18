# Async Data Validator & Cleaner

An asynchronous ingestion, validation, and serialization pipeline built with Python 3.11+, Pydantic v2 schemas, and asyncio concurrency primitives.

## Features
- **Strict Schema Enforcement:** Automatic type casting, email verification, and range bounds using Pydantic v2.
- **Custom Field Validation:** Normalizes and sanitizes messy input fields (e.g., automated name trimming and title-casing).
- **Concurrency Control:** Utilizes `asyncio.Semaphore` to throttle simultaneous record processing and protect memory during high-volume ingestion.
- **Structured Error Aggregation:** Captures and normalizes validation errors per record into standardized payloads without throwing unhandled exceptions.

## Installation

```bash
git clone https://github.com/AdityaKhadse/async-data-validator.git
cd async-data-validator
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -e ".[dev]"