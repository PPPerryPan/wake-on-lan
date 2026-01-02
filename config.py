# ==================== Configuration Settings (easy to modify) ====================
# Delay range (seconds): Random delay time range between each MAC address
# Format: (minimum_seconds, maximum_seconds)
# Example: (1, 5) means random interval between 1-5 seconds
DELAY_RANGE = (1, 3)

# List of MAC addresses to send WOL packets to
MAC_ADDRESSES = [
        "4c:e9:e4:55:91:bd",      # Standard format (colon-separated)
        "70-3a-a6-1e-ef-5a",     # Standard format (dash-separated)
        "aaaa-bbbb-ccdd",        # Switch format
        "a1b2c3d4e5f6",          # No separator
        "AA:BB:CC:DD:EE:FF",     # Uppercase format
        "aa:aa-bb:11-dd:ee",     # Mixed separators (: and -)
        "4c-e9:e4-55:91-bd",     # Mixed separators
]

WOL_PORT = 9
BROADCAST_ADDRESS = '255.255.255.255'
# ============================================================
