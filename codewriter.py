from fastmcp import FastMCP
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from datetime import datetime
import re
import os

# Initialize MCP
mcp = FastMCP("CodeWriter")

# Register as MCP Tool
@mcp.tool()
def generate_python_code(prompt: str, filename: str = "generated_code.py", run: bool = False) -> str:
    """
    Generate Python code using Ollama based on the given prompt.
    - Extracts only Python code from the LLM output.
    - Saves it to the specified filename.
    - Optionally runs the code.
    """
    llm = ChatGroq(model="qwen-qwq-32b")
    result = llm.invoke(prompt)
    raw_output = result.content

    # Extract Python code block (if in markdown format)
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", raw_output, re.DOTALL)
    code = code_blocks[0].strip() if code_blocks else raw_output.strip()

    # Save code
    with open(filename, "w") as f:
        f.write(code)

    result_msg = f"✅ Code written to `{filename}`."

    if run:
        exit_code = os.system(f"python {filename}")
        result_msg += f"\n🚀 Code executed. Exit code: {exit_code}"

    return result_msg

# Start the MCP server (for use with Claude or LangGraph)
if __name__ == "__main__":
    mcp.run(transport="stdio")
