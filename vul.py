from mcp.server.fastmcp import FastMCP
import requests
import json
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

mcp = FastMCP("CVEAssistant")
model = ChatGroq(model="qwen-qwq-32b")


NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

@mcp.tool()
def get_cve_details(cve_id: str) -> str:
    """Fetch CVE details from NVD."""
    response = requests.get(f"{NVD_API}?cveId={cve_id}")
    if response.status_code != 200:
        return f"Failed to fetch CVE data for {cve_id}."
    
    cve_data = response.json()
    try:
        item = cve_data["vulnerabilities"][0]["cve"]
        desc = item["descriptions"][0]["value"]
        severity = item.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "N/A")
        score = item.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A")
        return f"CVE: {cve_id}\nSeverity: {severity} (Score: {score})\nDescription: {desc}"
    except Exception as e:
        return f"Error parsing CVE data: {str(e)}"

@mcp.tool()
def analyze_cve_with_ai(cve_description: str) -> str:
    """Use LLM to analyze a vulnerability, its exploitability, and mitigation strategies."""
    prompt = f"""
You are a cybersecurity expert. Based on the following CVE description, provide a thorough analysis with the following structure:

1. 📌 **Simplified Explanation**: Describe the vulnerability in non-technical language.
2. 🔓 **Exploitability**: Discuss how easily this vulnerability could be exploited, what is needed (local access, remote attacker, etc.), and potential impact.
3. 🛡️ **Mitigation Strategies**: List concrete ways to mitigate or remediate the vulnerability (e.g., patches, config changes, input validation, firewall rules, etc.).

---
CVE Description:
{cve_description}
---
Only include the analysis — no additional messages or markdown formatting.
"""

    response = model.invoke(prompt)
    return response.content.strip()


# Run MCP
if __name__ == "__main__":
    mcp.run(transport="stdio")
