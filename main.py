import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Helper function to calculate payoff for a single option
def option_payoff(spot_price, strike_price, option_type, position, premium):
    if option_type == "call":
        payoff = np.maximum(spot_price - strike_price, 0)
    elif option_type == "put":
        payoff = np.maximum(strike_price - spot_price, 0)
    
    if position == "short":
        return -payoff + premium
    else:
        return payoff - premium

# Strategy functions
def bull_spread_payoff(spot_prices, strike1, strike2, premium1, premium2, option_type="call"):
    if option_type == "call":
        payoff1 = option_payoff(spot_prices, strike1, "call", "long", premium1)
        payoff2 = option_payoff(spot_prices, strike2, "call", "short", premium2)
    else:
        payoff1 = option_payoff(spot_prices, strike1, "put", "long", premium1)
        payoff2 = option_payoff(spot_prices, strike2, "put", "short", premium2)
    return payoff1 + payoff2

def bear_spread_payoff(spot_prices, strike1, strike2, premium1, premium2, option_type="call"):
    if option_type == "call":
        payoff1 = option_payoff(spot_prices, strike1, "call", "short", premium1)
        payoff2 = option_payoff(spot_prices, strike2, "call", "long", premium2)
    else:
        payoff1 = option_payoff(spot_prices, strike1, "put", "short", premium1)
        payoff2 = option_payoff(spot_prices, strike2, "put", "long", premium2)
    return payoff1 + payoff2

def box_spread_payoff(spot_prices, strike1, strike2, premium1, premium2, premium3, premium4):
    call_bull = bull_spread_payoff(spot_prices, strike1, strike2, premium1, premium2, option_type="call")
    put_bear = bear_spread_payoff(spot_prices, strike1, strike2, premium3, premium4, option_type="put")
    return call_bull + put_bear

# Main app interface
def main():
    st.title("Option Strategy Payoff Simulator")

    # Inputs for option parameters
    st.sidebar.header("Option Parameters")
    spot_price = st.sidebar.number_input("Current Spot Price", value=100.0)
    volatility = st.sidebar.number_input("Annual Volatility (%)", value=30.0)
    days_to_maturity = st.sidebar.number_input("Days to Maturity", value=30)

    # Calculate daily volatility
    daily_volatility = volatility / np.sqrt(365)

    # Select strategy
    strategy = st.selectbox("Choose Strategy", ["Bull Spread", "Bear Spread", "Box Spread"])
    st.write(f"Selected Strategy: {strategy}")

    # Strategy-specific inputs
    if strategy in ["Bull Spread", "Bear Spread"]:
        strike1 = st.number_input("Lower Strike Price", value=95.0)
        strike2 = st.number_input("Higher Strike Price", value=105.0)
        premium1 = st.number_input("Premium for Lower Strike Option", value=2.0)
        premium2 = st.number_input("Premium for Higher Strike Option", value=1.0)
        option_type = st.selectbox("Option Type", ["call", "put"])
        
    elif strategy == "Box Spread":
        strike1 = st.number_input("Lower Strike Price", value=95.0)
        strike2 = st.number_input("Higher Strike Price", value=105.0)
        premium1 = st.number_input("Premium for Call at Lower Strike", value=2.0)
        premium2 = st.number_input("Premium for Call at Higher Strike", value=1.0)
        premium3 = st.number_input("Premium for Put at Lower Strike", value=1.5)
        premium4 = st.number_input("Premium for Put at Higher Strike", value=0.5)

    # Simulating stock price paths
    spot_range = np.linspace(spot_price * 0.5, spot_price * 1.5, 100)
    
    # Calculate payoff based on strategy
    if strategy == "Bull Spread":
        payoff = bull_spread_payoff(spot_range, strike1, strike2, premium1, premium2, option_type)
    elif strategy == "Bear Spread":
        payoff = bear_spread_payoff(spot_range, strike1, strike2, premium1, premium2, option_type)
    elif strategy == "Box Spread":
        payoff = box_spread_payoff(spot_range, strike1, strike2, premium1, premium2, premium3, premium4)

    # Calculate total cost of strategy
    if strategy in ["Bull Spread", "Bear Spread"]:
        cost = premium1 - premium2
    elif strategy == "Box Spread":
        cost = premium1 - premium2 + premium3 - premium4
    st.write(f"Total cost of setting up {strategy}: {cost}")

    # Plotting the payoff
    plt.figure(figsize=(10, 5))
    plt.plot(spot_range, payoff, label="Gross Payoff")
    plt.axhline(cost, color="red", linestyle="--", label="Net Payoff")
    plt.xlabel("Stock Price at Expiry")
    plt.ylabel("Payoff")
    plt.title(f"{strategy} Strategy Payoff")
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":
    main()
