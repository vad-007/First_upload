import yfinance as yf
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set environment variable for API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

os.environ["GROQ_API_KEY"] = api_key

# Initialize the agent with the Groq model and YFinanceTools
agent_finance = Agent(
    name="finance agent",
    model=Groq(id="gemma2-9b-it"),
    tools=[YFinanceTools()],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
    api_key=api_key  # Assuming the Agent class requires an api_key parameter
)

try:
    # Fetch the current stock price of SBI using yfinance
    ticker = yf.Ticker("SBIN.NS")  # SBI's ticker symbol on NSE
    stock_info = ticker.info
    current_price = stock_info['currentPrice']
    
    # Print the current stock price
    print(f"Current stock price of SBI: {current_price}")
    
    # Alternatively, use the agent to print the response
    response = agent_finance.print_response(f"The current stock price of SBI is {current_price}")
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")
    