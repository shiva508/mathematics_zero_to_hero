"""Mock data for the store assistant lab.

This file is provided complete - you do not need to edit it.
"""

ORDERS = {
    "ORD-001": {
        "status": "shipped",
        "total": "$129.00",
        "items": ["wireless mouse", "usb-c cable"],
    },
    "ORD-002": {
        "status": "processing",
        "total": "$58.50",
        "items": ["notebook"],
    },
    "ORD-003": {
        "status": "delivered",
        "total": "$412.00",
        "items": ["mechanical keyboard", "monitor stand"],
    },
}

INVENTORY = {
    "wireless mouse": {"stock": 42, "price": "$24.00"},
    "usb-c cable": {"stock": 0, "price": "$9.00"},
    "notebook": {"stock": 130, "price": "$4.50"},
    "mechanical keyboard": {"stock": 7, "price": "$89.00"},
    "monitor stand": {"stock": 15, "price": "$34.00"},
}
