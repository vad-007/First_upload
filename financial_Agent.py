from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import yfinance as yf

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

## agent de recherche
agent_search=Agent(
    name="web serach agent",
    role="search web for information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

## finance agent
agent_finace = Agent(
    name="finance agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True)],
    instructions=["use tables to display data ."],
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent=Agent(
    team=[agent_search,agent_finace],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)
#multi_ai_agent.print_response("which stock is best SBI or HDFC")
agent_finace.print_response("what is current stock price of SBI")