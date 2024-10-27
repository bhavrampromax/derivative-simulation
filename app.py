import time
from flask import Flask, render_template, request
import math

app = Flask(__name__)

def binomial_option_price(S0, K, T, dt, r, sigma, option_type="call"):
    """
    Calculates the option price for a European call/put option using a 1-step binomial tree.
    
    Parameters:
    S0         : Initial stock price
    K          : Strike price
    T          : Time to maturity
    dt         : Time increment (one step)
    r          : Risk-free interest rate
    sigma      : Volatility of the underlying stock
    option_type: "call" for call option, "put" for put option
    
    Returns:
    Option price at time 0, and values at each node
    """

    # Calculate up (u) and down (d) factors
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u  # or math.exp(-sigma * math.sqrt(dt))

    # Calculate the risk-neutral probability
    p = (math.exp(r * dt) - d) / (u - d)

    # Calculate stock prices at each node
    S_up = S0 * u
    S_down = S0 * d

    # Calculate option values at maturity
    if option_type == "call":
        payoff_up = max(0, S_up - K)
        payoff_down = max(0, S_down - K)
    elif option_type == "put":
        payoff_up = max(0, K - S_up)
        payoff_down = max(0, K - S_down)
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")

    # Back-calculate the option price at time 0
    option_value_0 = math.exp(-r * dt) * (p * payoff_up + (1 - p) * payoff_down)

    return option_value_0, {'S_up': S_up, 'S_down': S_down, 'payoff_up': payoff_up, 'payoff_down': payoff_down, 'p': p}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    S0 = float(request.form['S0'])
    K = float(request.form['K'])
    T = float(request.form['T'])
    dt = float(request.form['dt'])
    r = float(request.form['r'])
    sigma = float(request.form['sigma'])
    option_type = request.form['option_type']

    # Calculate option price and node values
    option_price, node_values = binomial_option_price(S0, K, T, dt, r, sigma, option_type)
    time.sleep(3)

    return render_template('result.html', option_price=option_price, node_values=node_values)

if __name__ == '__main__':
    app.run(debug=True)
