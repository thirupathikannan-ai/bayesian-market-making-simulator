"""
Bayesian Market-Making & Optimal Pricing Simulator

This module implements:
- Bayesian inference
- Fair-value estimation
- Expected-value calculation
- Inventory-aware reservation pricing
- Dynamic bid/ask quoting
- Inventory and risk management
"""

import numpy as np


class BayesianEstimator:
    """
    Gaussian Bayesian estimator for latent fair value.

    Prior:
        V ~ N(mu, variance)

    Observation:
        X = V + noise

    Noise:
        noise ~ N(0, observation_variance)
    """

    def __init__(
        self,
        prior_mean=100.0,
        prior_variance=4.0,
        observation_variance=9.0,
    ):
        self.mean = float(prior_mean)
        self.variance = float(prior_variance)
        self.observation_variance = float(
            observation_variance
        )

    def update(self, observation):
        """
        Update the posterior distribution using
        one new market observation.

        Returns:
            posterior_mean
            posterior_variance
        """

        prior_precision = 1.0 / self.variance

        observation_precision = (
            1.0 / self.observation_variance
        )

        posterior_variance = 1.0 / (
            prior_precision
            + observation_precision
        )

        posterior_mean = posterior_variance * (
            self.mean * prior_precision
            + observation * observation_precision
        )

        self.mean = posterior_mean
        self.variance = posterior_variance

        return self.mean, self.variance

    def uncertainty(self):
        """Return posterior standard deviation."""

        return np.sqrt(self.variance)


class MarketMaker:
    """
    Inventory-aware Bayesian market maker.

    The market maker:
    1. Observes market prices.
    2. Updates Bayesian fair value.
    3. Calculates uncertainty.
    4. Adjusts reservation price based on inventory.
    5. Calculates expected value.
    6. Generates bid and ask quotes.
    7. Manages inventory and cash.
    """

    def __init__(
        self,
        initial_fair_value=100.0,
        prior_variance=4.0,
        observation_variance=9.0,
        base_spread=0.10,
        inventory_penalty=0.05,
        volatility_multiplier=0.20,
        max_inventory=20,
        order_size=1,
    ):

        self.estimator = BayesianEstimator(
            prior_mean=initial_fair_value,
            prior_variance=prior_variance,
            observation_variance=observation_variance,
        )

        self.base_spread = base_spread
        self.inventory_penalty = inventory_penalty
        self.volatility_multiplier = (
            volatility_multiplier
        )

        self.max_inventory = max_inventory
        self.order_size = order_size

        self.inventory = 0
        self.cash = 10000.0

        self.total_buys = 0
        self.total_sells = 0

    # -------------------------------------------------
    # Bayesian Fair-Value Estimation
    # -------------------------------------------------

    def update_fair_value(self, market_price):
        """
        Update Bayesian posterior using
        the latest market observation.
        """

        fair_value, posterior_variance = (
            self.estimator.update(market_price)
        )

        uncertainty = np.sqrt(
            posterior_variance
        )

        return fair_value, uncertainty

    # -------------------------------------------------
    # Reservation Price
    # -------------------------------------------------

    def calculate_reservation_price(
        self,
        fair_value,
    ):
        """
        Inventory-adjusted reservation price.

        Positive inventory lowers the reservation price,
        encouraging selling.

        Negative inventory raises the reservation price,
        encouraging buying.

        Formula:

            P_res = P_fair - gamma * inventory
        """

        reservation_price = (
            fair_value
            - self.inventory_penalty
            * self.inventory
        )

        return reservation_price

    # -------------------------------------------------
    # Expected Value
    # -------------------------------------------------

    def calculate_expected_value(
        self,
        quote_price,
        fair_value,
        fill_probability=0.50,
    ):
        """
        Calculate simplified expected trading value.

        Expected Value:

            EV = P(fill) * (fair_value - quote)

        For a buy quote:
            EV > 0 when fair value is above the quote.

        For a sell quote:
            EV is interpreted using the reverse price difference.
        """

        price_edge = (
            fair_value - quote_price
        )

        expected_value = (
            fill_probability * price_edge
        )

        return expected_value

    # -------------------------------------------------
    # Dynamic Bid / Ask Quoting
    # -------------------------------------------------

    def generate_quotes(
        self,
        fair_value,
        volatility,
    ):
        """
        Generate inventory-aware bid and ask quotes.

        Spread increases with market uncertainty.
        """

        reservation_price = (
            self.calculate_reservation_price(
                fair_value
            )
        )

        half_spread = (
            self.base_spread
            + self.volatility_multiplier
            * volatility
        )

        bid = (
            reservation_price
            - half_spread
        )

        ask = (
            reservation_price
            + half_spread
        )

        # Inventory risk controls
        if self.inventory >= self.max_inventory:
            bid = np.nan

        if self.inventory <= -self.max_inventory:
            ask = np.nan

        return bid, ask

    # -------------------------------------------------
    # Buy Execution
    # -------------------------------------------------

    def execute_buy(
        self,
        price,
        quantity=None,
    ):
        """
        Execute a buy from a market participant.

        Buying increases inventory and decreases cash.
        """

        if quantity is None:
            quantity = self.order_size

        if quantity <= 0:
            return False

        if (
            self.inventory + quantity
            > self.max_inventory
        ):
            return False

        self.inventory += quantity

        self.cash -= (
            price * quantity
        )

        self.total_buys += quantity

        return True

    # -------------------------------------------------
    # Sell Execution
    # -------------------------------------------------

    def execute_sell(
        self,
        price,
        quantity=None,
    ):
        """
        Execute a sell to a market participant.

        Selling decreases inventory and increases cash.
        """

        if quantity is None:
            quantity = self.order_size

        if quantity <= 0:
            return False

        if (
            self.inventory - quantity
            < -self.max_inventory
        ):
            return False

        self.inventory -= quantity

        self.cash += (
            price * quantity
        )

        self.total_sells += quantity

        return True

    # -------------------------------------------------
    # Portfolio Value
    # -------------------------------------------------

    def portfolio_value(
        self,
        market_price,
    ):
        """
        Mark portfolio to market.
        """

        return (
            self.cash
            + self.inventory * market_price
        )

    # -------------------------------------------------
    # Risk Information
    # -------------------------------------------------

    def inventory_exposure(
        self,
        market_price,
    ):
        """
        Calculate absolute inventory exposure.
        """

        return abs(
            self.inventory * market_price
        )

    def inventory_ratio(self):
        """
        Inventory as a fraction of maximum allowed
        inventory.
        """

        return (
            self.inventory
            / self.max_inventory
      )
