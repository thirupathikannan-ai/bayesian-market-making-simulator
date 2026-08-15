# Bayesian Market-Making & Optimal Pricing Simulator
A quantitative trading simulation project that combines Bayesian inference,
fair-value estimation, expected-value analysis, dynamic bid/ask quoting,
and inventory-aware risk management.

## Project Overview

This project implements a simplified quantitative market-making system.

The simulator:

1. Observes synthetic market prices.
2. Updates fair value using Bayesian inference.
3. Estimates uncertainty around fair value.
4. Adjusts the reservation price based on inventory.
5. Generates dynamic bid and ask quotes.
6. Calculates expected value for potential executions.
7. Simulates buy and sell order fills.
8. Tracks cash and inventory.
9. Calculates portfolio P&L and risk metrics.

## Core Concepts

### Bayesian Inference

The model uses a Gaussian prior and Gaussian observation model.

The prior is represented as:

V ~ N(mu, variance)

A market observation is modeled as:

X = V + noise

The Bayesian estimator updates the posterior mean and variance whenever a
new market observation is received.

The posterior mean is used as the estimated fair value.

### Fair-Value Estimation

The Bayesian posterior mean represents the current estimated fair value
of the asset.

The posterior variance is also tracked to measure uncertainty.

Conceptually:

Market Observation
        |
        v
Bayesian Update
        |
        v
Posterior Distribution
        |
        v
Estimated Fair Value

### Expected Value

The simulator calculates the expected value of executing at a quoted price.

For a buy quote:

EV_buy = P(fill) × (Fair Value - Bid)

For a sell quote:

EV_sell = P(fill) × (Ask - Fair Value)

where:

- P(fill) = estimated probability of execution
- Fair Value = Bayesian fair-value estimate
- Bid = proposed buying price
- Ask = proposed selling price

### Bid/Ask Quoting

The market maker calculates an inventory-adjusted reservation price:

Reservation Price =
Fair Value - Inventory Penalty × Inventory

The bid and ask prices are then generated around the reservation price.

Bid = Reservation Price - Half Spread

Ask = Reservation Price + Half Spread

The spread dynamically changes according to market uncertainty.

### Inventory and Risk Management

Inventory is one of the major risks faced by a market maker.

Positive inventory encourages the market maker to sell.

Negative inventory encourages the market maker to buy.

The simulator therefore adjusts its reservation price according to the
current inventory.

A maximum inventory limit is also used to prevent unlimited position
accumulation.

## Market Simulation

The simulator generates a synthetic market-price process using a random
walk.

At every simulation step:

Synthetic Market Price
        |
        v
Bayesian Update
        |
        v
Fair Value + Uncertainty
        |
        v
Inventory Adjustment
        |
        v
Bid / Ask Generation
        |
        v
Fill Probability
        |
        v
Simulated Execution
        |
        v
Inventory + Cash Update
        |
        v
Portfolio Valuation
        |
        v
P&L and Risk Metrics

## Project Structure

bayesian-market-making-simulator/
│
├── README.md
├── main.py
├── market_maker.py
├── simulator.py
├── metrics.py
├── requirements.txt
└── .gitignore

## File Descriptions

### main.py

Main entry point of the project.

Runs the complete market-making simulation and displays the final
performance statistics.

### market_maker.py

Contains the core market-making model.

Implements:

- Bayesian estimator
- Fair-value estimation
- Posterior uncertainty
- Expected-value calculation
- Reservation-price calculation
- Dynamic bid/ask quoting
- Inventory management
- Cash management
- Portfolio valuation

### simulator.py

Implements the synthetic market environment.

Responsibilities include:

- Market-price generation
- Bayesian updates
- Quote generation
- Fill-probability estimation
- Order execution simulation
- Inventory tracking
- Portfolio tracking

### metrics.py

Calculates:

- P&L
- Portfolio returns
- Sharpe ratio
- Maximum drawdown
- Number of fills
- Average execution price
- Average inventory

### requirements.txt

Contains the Python packages required to run the project.

### .gitignore

Contains files and folders that should not be uploaded to GitHub, such as
Python cache files and virtual environments.

## Mathematical Framework

### Bayesian Update

For a Gaussian prior and Gaussian observation noise:

Prior:

V ~ N(mu_prior, sigma_prior²)

Observation:

X ~ N(V, sigma_observation²)

Posterior variance:

1 / sigma_posterior² =
1 / sigma_prior² +
1 / sigma_observation²

Posterior mean:

mu_posterior =
sigma_posterior² ×
(
mu_prior / sigma_prior² +
X / sigma_observation²
)

The posterior mean becomes the estimated fair value.

## Inventory-Aware Pricing

The reservation price is calculated as:

P_reservation =
P_fair - gamma × Inventory

where:

- P_reservation = inventory-adjusted reservation price
- P_fair = estimated fair value
- gamma = inventory penalty
- Inventory = current market-maker position

This mechanism encourages the market maker to reduce excessive inventory.

## Dynamic Spread

The simulator widens the spread when market uncertainty increases.

Conceptually:

Half Spread =
Base Spread +
Volatility Multiplier × Uncertainty

Therefore:

Higher uncertainty
        |
        v
Wider quotes
        |
        v
Greater compensation for risk

## Fill Probability

The simulator uses a simplified distance-based fill-probability model.

Quotes farther away from the current market price have a lower probability
of execution.

This is an educational approximation and is not calibrated to a real
exchange order-flow model.

## Performance Metrics

### P&L

P&L is calculated as:

P&L =
Final Portfolio Value -
Initial Portfolio Value

### Sharpe Ratio

The simulator calculates an annualized Sharpe ratio based on portfolio
returns.

### Maximum Drawdown

Maximum drawdown measures the largest decline from a previous portfolio
peak.

### Inventory Exposure

Inventory exposure is calculated as:

Inventory Exposure =
|Inventory × Market Price|

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/bayesian-market-making-simulator.git

Enter the project directory:

cd bayesian-market-making-simulator

Install dependencies:

pip install -r requirements.txt

## Running the Project

Run the simulator using:

python main.py

The program displays:

- Initial portfolio value
- Final portfolio value
- Total P&L
- Sharpe ratio
- Maximum drawdown
- Final market price
- Final Bayesian fair value
- Final inventory
- Average inventory
- Total fills
- Average execution price

## Technologies

- Python
- NumPy
- Pandas
- Bayesian Statistics
- Probability
- Quantitative Finance
- Algorithmic Trading
- Market Making
- Risk Management
- Market Microstructure

## Key Features

- Bayesian fair-value estimation
- Gaussian posterior updating
- Expected-value calculation
- Dynamic bid/ask pricing
- Inventory-aware pricing
- Inventory limits
- Synthetic market simulation
- Fill-probability modeling
- Cash and portfolio tracking
- P&L calculation
- Sharpe ratio
- Maximum drawdown
- Execution statistics

## Limitations

This project is an educational quantitative trading simulator and does not
represent a complete production trading system.

Current limitations include:

- Synthetic market data
- Simplified price process
- Simplified fill-probability model
- No full limit-order-book simulation
- No queue-position modeling
- No transaction costs
- No exchange fees
- No latency modeling
- No adverse-selection model
- No market-impact calibration
- No real-time exchange connectivity
- No multi-asset portfolio optimization

## Future Improvements

Possible extensions include:

- Full limit-order-book simulation
- Realistic order-arrival processes
- Hawkes-process order modeling
- Transaction-cost modeling
- Adverse-selection modeling
- Queue-position simulation
- Avellaneda-Stoikov market-making model
- Monte Carlo stress testing
- Parameter optimization
- Multi-asset inventory optimization
- Historical market-data backtesting
- Reinforcement-learning market making
- Regime-switching volatility models
- Sensitivity analysis
- Visualization of fair value, inventory, and P&L
- Volatility forecasting
- Order-flow imbalance modeling
- Execution-quality analysis
- Risk-adjusted quote optimization
- Real-time market-data integration

## Quantitative Trading Architecture

Market Observations
        |
        v
Bayesian Inference
        |
        v
Fair Value
        |
        +----------------+
        |                |
        v                v
Market Uncertainty    Inventory
        |                |
        +-------+--------+
                |
                v
       Reservation Price
                |
                v
            Bid / Ask
                |
                v
         Order Execution
                |
                v
        Cash + Inventory
                |
                v
        Portfolio Value
                |
                v
         P&L / Risk Metrics

## Learning Outcomes

This project demonstrates practical understanding of:

- Bayesian probability
- Statistical inference
- Expected value
- Fair-value estimation
- Market making
- Bid/ask spread construction
- Inventory management
- Risk management
- Portfolio valuation
- P&L analysis
- Sharpe ratio
- Maximum drawdown
- Quantitative trading simulation
- Market microstructure

## Disclaimer

This project is intended for educational and research purposes only.

It is not financial advice and should not be used for live trading without
appropriate testing, validation, monitoring, and risk controls.

## Author

### THIRUPATHI KANNAN K

B.E. Electronics and Communication Engineering

Areas of Interest:

- Quantitative Trading
- Quantitative Finance
- Probability and Statistics
- Algorithmic Trading
- Machine Learning
- Market Microstructure
