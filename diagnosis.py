from mcp.server.fastmcp import FastMCP
from langchain_ollama import ChatOllam
from langchain_groq import ChatGroq

# Initialize MCP server
mcp = FastMCP("Diagnosis Matcher")

# Attach Ollama LLM (e.g., qwen:latest or llama3:8b)
mcp.llm = ChatGroq(model="qwen-qwq-32b")


# Diagnosis knowledge base
DIAGNOSES = [
    {"code": "E1151", "description": "Diabetes mellitus type 2 with complications"},
    {"code": "E1151", "description": "Diabetes type 2 with circulation disorder"},
    {"code": "E1151", "description": "Peripheral circulatory disorder associated with type 2 diabetes mellitus"},
    {"code": "E1151", "description": "Peripheral circulatory disorder due to type 2 diabetes mellitus"},
    {"code": "E1151", "description": "Small vessel disease due to type 2 diabetes mellitus"},
    {"code": "E1051", "description": "Diabetes type 1 with peripheral vascular disease"},
    {"code": "E1051", "description": "Diabetes type 1 with small vessel disease"},
    {"code": "E1051", "description": "Peripheral angiopathy due to type 1 diabetes mellitus"},
    {"code": "E1051", "description": "Small vessel disease due to type 1 diabetes mellitus"},
]

@mcp.tool()
def extract_diagnosis_from_text(clinical_text: str) -> str:
    """
    Extract diagnosis code(s) from unstructured clinical notes using reasoning.
    """
    context = "\n".join([f"{d['code']} - {d['description']}" for d in DIAGNOSES])

    prompt = f"""
You are a clinical AI assistant.

Given this clinical note:

"{clinical_text}"

And this list of diagnosis codes:

{context}

Identify and return the most relevant diagnosis code(s) and their description(s) that match the note. Be specific and accurate.
Return only relevant matches.
"""
    return mcp.llm.invoke(prompt)

if __name__ == "__main__":
    mcp.run(transport="stdio")
