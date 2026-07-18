# ADR-0002: Layer Dependency

## Rule

Dependencies are one-way.

Providers

->

Domain

->

Indicators

->

Analysis

->

Strategy

->

Risk

->

Execution

->

Reporting

Forbidden:

- Provider importing Strategy
- Analysis importing Execution
- Domain importing Provider

Allowed:

- Strategy importing Analysis
- Risk importing Strategy
- Execution importing Risk
