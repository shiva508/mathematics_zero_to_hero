"""Core Lab - Store Assistant agent.

A customer-service agent for an online store. It looks up order status
and checks product inventory using two function tools.

`get_order_status` is provided as a finished reference tool. Complete
`check_inventory` and the agent definition, then run:

    uv run ask_assistant.py
"""

from google.adk.agents import LlmAgent
import os
from database_store import INVENTORY, ORDERS
from google.adk.tools import ToolContext



def get_order_status(order_id: str) -> dict:
    """Looks up the status of a customer order.

    Args:
        order_id: The order identifier, such as 'ORD-001'.
    """
    order = ORDERS.get(order_id.strip().upper())
    if order is None:
        return {
            "status": "error",
            "error_message": f"Order '{order_id}' was not found.",
        }
    return {
        "status": "success",
        "order_id": order_id.strip().upper(),
        "order_status": order["status"],
        "total": order["total"],
    }

def check_inventory(product_name: str) -> dict:
    """Checks whether a product is in stock and returns its price.

    Args:
        product_name: The name of the product to check.
    """
    # YOUR CODE HERE - Step 2
    # Normalize product_name (strip spaces, lowercase). Then find a
    # product in INVENTORY whose name equals, contains, or is contained
    # by the query - a customer may type "keyboards" or just "keyboard".
    # Return an "error" dict when nothing matches; otherwise return a
    # "success" dict with the matched product name, "stock", and "price".
    normalized_product_name = product_name.strip().lower()
    for name, details in INVENTORY.items():
        if normalized_product_name in name or name in normalized_product_name:
            return {
                "status": "success",
                "product_name": name,
                "stock": details["stock"],
                "price": details["price"]
            }
    return {"status": "error", "error_message": f"Product '{product_name}' was not found."}

store_assistant_agent = LlmAgent(
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    name='store_assistant_agent',
    description='Helps customers with orders and product inventory.',
    instruction=(
        "You are a helpful assistant for an online store. Use the "
        "get_order_status tool to answer questions about orders, and the "
        "check_inventory tool to answer questions about product "
        "availability and pricing. If a tool returns an error, explain "
        "the problem to the customer politely."
    ),
    tools=[get_order_status, check_inventory]
)


def add_to_cart(product_name: str, tool_context: ToolContext) -> dict:
    """Adds a product to the shopping cart.

    Args:
        product_name: The product to add to the cart.
    """
    # YOUR CODE HERE - Challenge 1a
    # Read the current cart from tool_context.state.get("temp:cart", []),
    # append product_name (lowercased), write the list back to
    # tool_context.state["temp:cart"], and return a success dict that
    # includes the new cart size.
    cart = tool_context.state.get("temp:cart", [])
    cart = cart + [product_name.strip().lower()]
    tool_context.state["temp:cart"] = cart
    return {"status": "success", "cart_size": len(cart)}


def get_cart_summary(tool_context: ToolContext) -> dict:
    """Returns the items currently in the shopping cart."""
    # YOUR CODE HERE - Challenge 1b
    # Read "temp:cart" from tool_context.state. For each product, look up
    # its price in INVENTORY. Return a success dict with the list of
    # items (each with its price) and the item count.
    cart = tool_context.state.get("temp:cart", [])
    items = []
    for name in cart:
        product = INVENTORY.get(name)
        price = product["price"] if product else "unknown"
        items.append({"product": name, "price": price})
    return {"status": "success", "items": items, "count": len(items)}

cart_assistant_agent = LlmAgent(
    name="cart_assistant",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Manages a customer's shopping cart.",
    instruction=(
        "You help a customer build a shopping cart. Use add_to_cart to "
        "add each product the customer mentions, then use "
        "get_cart_summary to tell them what is in their cart."
        "respond with a polite message if the customer asks for a product that is not in the inventory."
        "response should be human-like and friendly, and avoid repeating the same phrases."
    ),
    tools=[add_to_cart, get_cart_summary],
)