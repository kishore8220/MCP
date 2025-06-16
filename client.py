from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["math_server.py"], ## Ensure correct absolute path
                "transport":"stdio",
            
            },
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            },
            "time": {
                "command":"python",
                "args":["checktime.py"],
                "transport":"stdio"
            },
            "file_oraganzier":{
                "command":"python",
                "args":["file_oragnizer.py"],
                "transport":"stdio"
            },
            # "nvd_data":{
            #     "command":"python",
            #     "args":["vul.py"],
            #     "transport":"stdio"
            # },
            "codewriter":{
                "command":"python",
                "args":["codewriter.py"],
                "transport":"stdio"
            }

        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    # model = ChatOllama(model="qwen3")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)
    
    time_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what date today?"}]}
    )
    print("Weather response:", time_response['messages'][-1].content)

    file_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Help me to organize my /home/kishore/project@sq1/yoga_app folder?"}]}
    )
    print("Weather response:", file_response['messages'][-1].content)

    # nvd_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "Tell me about CVE-2025-5100 and analyze"}]}
    # )
    # print("NVD response:", nvd_response['messages'][-1].content)

    # code_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "Write a code for Panlidrome and execuete as well?"}]}
    # )
    # print("Weather response:", code_response['messages'][-1].content)


asyncio.run(main())