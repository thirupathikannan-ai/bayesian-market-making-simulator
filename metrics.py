"""
Performance and risk metrics for the
Bayesian market-making simulator.
"""

import numpy as np


def calculate_pnl(
    portfolio_values,
):
    """
    Calculate total profit and loss.
    """

    values = np.asarray(
        portfolio_values,
        dtype=float,
    )

    if len(values) == 0:
        return 0.0

    return (
        values[-1]
        - values[0]
    )


def calculate_returns(
    portfolio_values,
):
    """
    Calculate percentage portfolio returns.
    """

    values = np.asarray(
        portfolio_values,
        dtype=float,
    )

    if len(values) < 2:
        return np.array([])

    previous = values[:-1]

    current = values[1:]

    safe_previous = np.where(
        previous == 0,
        1e-12,
        previous,
    )

    return (
        current - previous
    ) / safe_previous


def calculate_sharpe_ratio(
    portfolio_values,
    periods_per_year=252,
):
    """
    Calculate annualized Sharpe ratio.
    """

    returns = calculate_returns(
        portfolio_values
    )

    if len(returns) < 2:
        return 0.0

    volatility = np.std(
        returns,
        ddof=1,
    )

    if volatility == 0:
        return 0.0

    return (
        np.mean(returns)
        / volatility
        * np.sqrt(periods_per_year)
    )


def calculate_max_drawdown(
    portfolio_values,
):
    """
    Calculate maximum portfolio drawdown.
    """

    values = np.asarray(
        portfolio_values,
        dtype=float,
    )

    if len(values) == 0:
        return 0.0

    running_max = np.maximum.accumulate(
        values
    )

    safe_running_max = np.where(
        running_max == 0,
        1e-12,
        running_max,
    )

    drawdowns = (
        values - running_max
    ) / safe_running_max

    return abs(
        np.min(drawdowns)
    )


def count_fills(
    fill_sides,
):
    """
    Count executed trades.
    """

    return sum(
        side != "NONE"
        for side in fill_sides
    )


def calculate_average_execution_price(
    execution_prices,
):
    """
    Calculate average execution price.
    """

    prices = np.asarray(
        execution_prices,
        dtype=float,
    )

    prices = prices[
        np.isfinite(prices)
    ]

    if len(prices) == 0:
        return 0.0

    return float(
        np.mean(prices)
    )


def calculate_average_inventory(
    inventory,
):
    """
    Calculate average absolute inventory.
    """

    values = np.asarray(
        inventory,
        dtype=float,
    )

    if len(values) == 0:
        return 0.0

    return float(
        np.mean(np.abs(values))
    )
