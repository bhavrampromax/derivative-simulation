import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Helper function to calculate payoff for a single option
def option_payoff(spot_price, strike_price, option_type, position, premium):
    if option_type == "call":
        payoff = np.maximum(spot_price - strike_price, 0)  # Payoff for call options
    elif option_type == "put":
        payoff = np.maximum(strike_price - spot_price, 0)  # Payoff for put options

    if position == "short":
        return -payoff + premium  # For short position, subtract payoff from premium
    else:
        return payoff - premium  # For long position, subtract premium from payoff

# Calculate payoff for a custom strategy based on user-defined options
def custom_strategy_payoff(spot_prices, options):
    total_payoff = np.zeros_like(spot_prices)
    for option in options:
        strike = option["strike"]
        premium = option["premium"]
        option_type = option["type"]
        position = option["position"]
        total_payoff += option_payoff(spot_prices, strike, option_type, position, premium)
    return total_payoff

# Main app interface
def main():
    st.title("Custom Option Strategy Payoff Simulator")

    # Spot price and range for payoff calculation
    spot_price = st.sidebar.number_input("Current Spot Price", value=100.0)
    spot_range = np.linspace(spot_price * 0.5, spot_price * 1.5, 100)

    # Number of options
    num_calls = st.sidebar.number_input("Number of Call Options", min_value=0, value=1, step=1)
    num_puts = st.sidebar.number_input("Number of Put Options", min_value=0, value=1, step=1)

    # Collect call option data
    options = []
    for i in range(num_calls):
        st.subheader(f"Call Option {i+1}")
        strike = st.number_input(f"Strike Price for Call {i+1}", value=100.0)
        premium = st.number_input(f"Premium for Call {i+1}", value=2.0)
        position = st.selectbox(f"Position for Call {i+1}", ["long", "short"])
        options.append({"strike": strike, "premium": premium, "type": "call", "position": position})

    # Collect put option data
    for i in range(num_puts):
        st.subheader(f"Put Option {i+1}")
        strike = st.number_input(f"Strike Price for Put {i+1}", value=100.0)
        premium = st.number_input(f"Premium for Put {i+1}", value=2.0)
        position = st.selectbox(f"Position for Put {i+1}", ["long", "short"])
        options.append({"strike": strike, "premium": premium, "type": "put", "position": position})

    # Calculate gross and net payoff
    gross_payoff = custom_strategy_payoff(spot_range, options)
    total_cost = sum([option["premium"] if option["position"] == "long" else -option["premium"] for option in options])
    net_payoff = gross_payoff - total_cost  # Net Payoff = Gross Payoff - Total Cost

    st.write(f"Total cost of setting up the strategy: {total_cost}")

    # Plotting the payoff
    plt.figure(figsize=(10, 5))
    plt.plot(spot_range, gross_payoff, label="Gross Payoff")
    plt.plot(spot_range, net_payoff, label="Net Payoff", linestyle="--")
    plt.xlabel("Stock Price at Expiry")
    plt.ylabel("Payoff")
    plt.title("Custom Option Strategy Payoff")
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":
    main()
