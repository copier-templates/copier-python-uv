# CI Flow (GitHub Actions)

This document shows the CI flow used in `.github/workflows/test.yml`.

```mermaid
flowchart TD
  classDef trigger fill:#1F2937,stroke:#111827,color:#FFFFFF,font-weight:bold,stroke-width:3px;
  classDef checkout fill:#0369A1,stroke:#024873,color:#FFFFFF,stroke-width:2px;
  classDef setup fill:#10B981,stroke:#059669,color:#FFFFFF,stroke-width:2px;
  classDef cache fill:#F59E0B,stroke:#D97706,color:#FFFFFF,stroke-width:2px;
  classDef test fill:#8B5CF6,stroke:#7C3AED,color:#FFFFFF,stroke-width:2px;
  classDef artifact fill:#EF4444,stroke:#DC2626,color:#FFFFFF,stroke-width:2px;
  classDef summary fill:#6B7280,stroke:#4B5563,color:#FFFFFF,stroke-width:2px;
  classDef matrixItem fill:#1E293B,stroke:#0F172A,color:#FFFFFF;
  classDef note fill:#FEF08A,stroke:#FACC15,color:#000000,stroke-width:2px;

  A["🚀 GitHub Actions Trigger"]:::trigger
  A -->|push or<br/>pull_request| Matrix

  subgraph Matrix["🖥️  Test Matrix"]
    direction TB
    M1["ubuntu-latest<br/>Python 3.10-3.13"]:::matrixItem
    M2["macOS-latest<br/>Python 3.10-3.13"]:::matrixItem
  end

  Matrix -->|runs in parallel| B["📥 Checkout Repository"]:::checkout
  B --> C["⚙️ Set up Python Environment"]:::setup
  C --> D["📦 Install Build Tools"]:::setup
  D --> E["💾 Cache UV Dependencies"]:::cache
  E --> F["🧪 Run Tests"]:::test
  F -->|conditional| G["📤 Upload Artifacts"]:::artifact
  G --> H["📋 Print Summary"]:::summary

  NOTE["⚠️  Note: Strategy matrix runs jobs in parallel<br/>fail-fast: false (all jobs complete)"]:::note
  NOTE -.-> F
```

## Workflow Summary

The CI pipeline triggers on every push and pull request, running tests across multiple OS and Python version combinations. Key features:

- **Parallel Testing**: Matrix strategy tests on Ubuntu and macOS with Python 3.10-3.13
- **Dependency Caching**: UV dependencies are cached for faster runs
- **Test Execution**: Comprehensive test suite via pytest
- **Artifact Upload**: Test results and logs uploaded conditionally
- **No Early Exit**: `fail-fast: false` ensures all matrix jobs complete

## Key Stages

| Stage | Purpose |
|-------|---------|
| 🚀 Trigger | Initiates workflow on code changes |
| 📥 Checkout | Retrieves repository code |
| ⚙️ Setup | Configures Python environment |
| 💾 Cache | Optimizes dependency installation |
| 🧪 Tests | Executes test suite |
| 📤 Artifacts | Captures test results |
| 📋 Summary | Reports final status |
