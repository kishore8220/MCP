from mcp.server.fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# Create MCP instance
mcp = FastMCP("Time")

# Tool to get current date and time in IST
@mcp.tool(name="get_current_ist_time")
def get_current_time_ist(format: str = "%Y-%m-%d %H:%M:%S"):
    """
    Returns the current date and time in Asia/Kolkata timezone.
    
    Args:
        format: Optional format string (default: "%Y-%m-%d %H:%M:%S")
    
    Returns:
        Formatted current time in IST.
    """
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    return now.strftime(format)

# Run the MCP using stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
