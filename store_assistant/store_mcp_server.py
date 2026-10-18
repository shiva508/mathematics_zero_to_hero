"""A small MCP server for Challenge 2.

This file is provided complete - you do not need to edit it. It exposes
one tool, get_shipping_estimate, over the Model Context Protocol. The
agent in challenge2_mcp.py connects to this server over stdio.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shipping")

@mcp.tool()
def get_shipping_estimate(destination: str, weight_kg: float) -> str:
    """Estimates the shipping cost and delivery time for a package.

    Args:
        destination: The destination country code, such as 'US' or 'UK'.
        weight_kg: The package weight in kilograms.
    """
    base_rates = {"US": 5.0, "CA": 8.0, "UK": 12.0, "MX": 9.0}
    base = base_rates.get(destination.upper(), 20.0)
    cost = base + max(0.0, weight_kg - 1.0) * 2.0
    return (
        f"Estimated shipping to {destination.upper()}: "
        f"${cost:.2f}, 3-5 business days."
    )

if __name__ == "__main__":
    mcp.run()