"""
Main entry point for the
Bayesian Market-Making & Optimal Pricing Simulator.
"""

from simulator import MarketSimulator

from metrics import (
    calculate_pnl,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    count_fills,
    calculate_average_execution_price,
    calculate_average_inventory,
)


def main():

    print("=" * 60)
    print(
        " BAYESIAN MARKET-MAKING & "
        "OPTIMAL PRICING SIMULATOR"
    )
    print("=" * 60)

    simulator = MarketSimulator(
        steps=2000,
        initial_price=100.0,
        market_volatility=0.50,
        seed=42,
    )

    results = simulator.run()

    # ---------------------------------------------
    # Portfolio Performance
    # ---------------------------------------------

    portfolio_values = (
        results[
            "portfolio_value"
        ].values
    )

    pnl = calculate_pnl(
        portfolio_values
    )

    sharpe = calculate_sharpe_ratio(
        portfolio_values
    )

    max_drawdown = (
        calculate_max_drawdown(
            portfolio_values
        )
    )

    # ---------------------------------------------
    # Trading Statistics
    # ---------------------------------------------

    fills = count_fills(
        results["fill_side"]
    )

    average_execution_price = (
        calculate_average_execution_price(
            results[
                "execution_price"
            ].values
        )
    )

    average_inventory = (
        calculate_average_inventory(
            results["inventory"].values
        )
    )

    final_inventory = (
        results[
            "inventory"
        ].iloc[-1]
    )

    final_fair_value = (
        results[
            "fair_value"
        ].iloc[-1]
    )

    final_market_price = (
        results[
            "market_price"
        ].iloc[-1]
    )

    # ---------------------------------------------
    # Display Results
    # ---------------------------------------------

    print()
    print("Simulation Results")
    print("-" * 60)

    print(
        f"Initial Portfolio       : "
        f"{portfolio_values[0]:.2f}"
    )

    print(
        f"Final Portfolio         : "
        f"{portfolio_values[-1]:.2f}"
    )

    print(
        f"Total P&L               : "
        f"{pnl:.2f}"
    )

    print(
        f"Sharpe Ratio            : "
        f"{sharpe:.4f}"
    )

    print(
        f"Maximum Drawdown        : "
        f"{max_drawdown * 100:.2f}%"
    )

    print(
        f"Final Market Price      : "
        f"{final_market_price:.4f}"
    )

    print(
        f"Final Bayesian Fair Value: "
        f"{final_fair_value:.4f}"
    )

    print(
        f"Final Inventory         : "
        f"{final_inventory}"
    )

    print(
        f"Average Absolute Inventory: "
        f"{average_inventory:.4f}"
    )

    print(
        f"Total Fills             : "
        f"{fills}"
    )

    print(
        f"Average Execution Price: "
        f"{average_execution_price:.4f}"
    )

    print("-" * 60)

    print()
    print("Core Model Components")
    print("-" * 60)

    print("✓ Bayesian inference")
    print("✓ Fair-value estimation")
    print("✓ Expected-value calculation")
    print("✓ Dynamic bid/ask quoting")
    print("✓ Inventory-aware pricing")
    print("✓ Risk management")
    print("✓ Portfolio P&L analysis")

    print("=" * 60)


if __name__ == "__main__":
    main()
