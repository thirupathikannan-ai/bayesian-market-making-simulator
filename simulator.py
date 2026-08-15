"""
Market simulation engine.

Generates a synthetic market price process and
simulates an inventory-aware Bayesian market maker.
"""

import numpy as np
import pandas as pd

from market_maker import MarketMaker


class MarketSimulator:

    def __init__(
        self,
        steps=2000,
        initial_price=100.0,
        market_volatility=0.50,
        seed=42,
    ):

        self.steps = steps
        self.initial_price = initial_price
        self.market_volatility = (
            market_volatility
        )

        self.rng = np.random.default_rng(
            seed
        )

    # -------------------------------------------------
    # Market Generation
    # -------------------------------------------------

    def generate_market_prices(self):
        """
        Generate a synthetic random-walk market.
        """

        prices = np.zeros(self.steps)

        prices[0] = self.initial_price

        for t in range(1, self.steps):

            price_change = self.rng.normal(
                0,
                self.market_volatility,
            )

            prices[t] = max(
                0.01,
                prices[t - 1]
                + price_change,
            )

        return prices

    # -------------------------------------------------
    # Fill Probability
    # -------------------------------------------------

    def calculate_fill_probability(
        self,
        distance_from_market,
        volatility,
    ):
        """
        Approximate probability that a quote is filled.

        Quotes further away from the market have a
        lower probability of execution.
        """

        scale = max(
            volatility,
            0.01,
        )

        probability = np.exp(
            -abs(
                distance_from_market
            ) / scale
        )

        return float(
            np.clip(
                probability,
                0.05,
                0.95,
            )
        )

    # -------------------------------------------------
    # Run Simulation
    # -------------------------------------------------

    def run(self):

        prices = (
            self.generate_market_prices()
        )

        market_maker = MarketMaker(
            initial_fair_value=self.initial_price,
            prior_variance=4.0,
            observation_variance=9.0,
            base_spread=0.10,
            inventory_penalty=0.05,
            volatility_multiplier=0.20,
            max_inventory=20,
            order_size=1,
        )

        records = []

        previous_price = prices[0]

        for t, market_price in enumerate(
            prices
        ):

            # -----------------------------------------
            # Bayesian Update
            # -----------------------------------------

            fair_value, uncertainty = (
                market_maker.update_fair_value(
                    market_price
                )
            )

            # -----------------------------------------
            # Estimate Local Volatility
            # -----------------------------------------

            price_change = (
                market_price
                - previous_price
            )

            volatility = abs(
                price_change
            )

            # -----------------------------------------
            # Generate Quotes
            # -----------------------------------------

            bid, ask = (
                market_maker.generate_quotes(
                    fair_value,
                    volatility,
                )
            )

            # -----------------------------------------
            # Expected Value
            # -----------------------------------------

            if np.isfinite(bid):

                bid_fill_probability = (
                    self.calculate_fill_probability(
                        market_price - bid,
                        max(volatility, 0.05),
                    )
                )

                bid_expected_value = (
                    market_maker.calculate_expected_value(
                        bid,
                        fair_value,
                        bid_fill_probability,
                    )
                )

            else:

                bid_fill_probability = 0.0
                bid_expected_value = 0.0

            if np.isfinite(ask):

                ask_fill_probability = (
                    self.calculate_fill_probability(
                        ask - market_price,
                        max(volatility, 0.05),
                    )
                )

                # For a sell quote, profit is:
                # quote price - fair value

                ask_expected_value = (
                    ask_fill_probability
                    * (ask - fair_value)
                )

            else:

                ask_fill_probability = 0.0
                ask_expected_value = 0.0

            # -----------------------------------------
            # Simulate Order Flow
            # -----------------------------------------

            random_number = (
                self.rng.random()
            )

            fill_side = "NONE"
            execution_price = np.nan

            # Market participant buys from our ask
            if (
                random_number
                < ask_fill_probability
                and np.isfinite(ask)
            ):

                if market_maker.execute_sell(
                    ask,
                    1,
                ):

                    fill_side = "SELL"
                    execution_price = ask

            # Market participant sells to our bid
            elif (
                random_number
                > 1.0
                - bid_fill_probability
                and np.isfinite(bid)
            ):

                if market_maker.execute_buy(
                    bid,
                    1,
                ):

                    fill_side = "BUY"
                    execution_price = bid

            # -----------------------------------------
            # Portfolio Value
            # -----------------------------------------

            portfolio_value = (
                market_maker.portfolio_value(
                    market_price
                )
            )

            # -----------------------------------------
            # Record Simulation State
            # -----------------------------------------

            records.append(
                {
                    "time": t,
                    "market_price": market_price,
                    "fair_value": fair_value,
                    "uncertainty": uncertainty,
                    "volatility": volatility,
                    "bid": bid,
                    "ask": ask,
                    "bid_expected_value":
                        bid_expected_value,
                    "ask_expected_value":
                        ask_expected_value,
                    "inventory":
                        market_maker.inventory,
                    "inventory_ratio":
                        market_maker.inventory_ratio(),
                    "cash":
                        market_maker.cash,
                    "portfolio_value":
                        portfolio_value,
                    "fill_side": fill_side,
                    "execution_price":
                        execution_price,
                }
            )

            previous_price = market_price

        return pd.DataFrame(records)
