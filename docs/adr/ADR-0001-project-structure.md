# ADR-0001: Project Structure

## Status

Accepted

## Context

QuantForge Engine is designed as a modular quantitative trading framework.

The project must support:

- Multiple exchanges
- Multiple strategies
- Multiple indicators
- Backtesting
- Live trading
- Paper trading
- Optimization
- Reporting

Without requiring architectural changes.

## Decision

The project adopts a layered architecture.
src/quantforge/

    core/

    config/

    domain/

    providers/

    indicators/

    analysis/

    strategy/

    risk/

    execution/

    backtest/

    optimizer/

    reporting/

    utils/
    
Each layer has a single responsibility.

Dependencies always flow downward.

No upward dependency is allowed.

## Consequences

- High maintainability
- Easy testing
- Loose coupling
- High scalability