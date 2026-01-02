# Wake-on-LAN (WOL) Utility

A Python utility for sending Wake-on-LAN magic packets to wake up devices on a network, featuring batch processing and random delayed transmission to prevent circuit tripping.

## Project Structure

The project is organized into a modular structure for better maintainability:

```
wake-on-lan/
├── config.py          # Configuration settings (MAC addresses, delay range, etc.)
├── wol_utils.py       # Core WOL functionality (packet creation, transmission)
├── main.py           # Main entry point for running the utility
├── __init__.py       # Package initialization (for programmatic use)
└── README.md         # This documentation
```

## Features

- **Batch WOL Packet Sending**: Send wake-up packets to multiple devices in one operation
- **Flexible MAC Address Support**: Compatible with various MAC address formats
- **Random Delayed Transmission**: Staggers packet delivery to prevent simultaneous power surges
- **Configurable Settings**: Easy-to-modify parameters for delay range, port, and broadcast address
- **Error Handling**: Provides feedback on successful and failed transmission attempts
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modular Design**: Clean separation between configuration, core functionality, and execution
- **Package Support**: Can be imported as a Python package for use in other projects

## Supported MAC Address Formats

The utility accepts MAC addresses in the following formats:

- Colon-separated: `4c:e9:e4:55:91:bd`
- Dash-separated: `70-3a-a6-1e-ef-5a`
- Switch format: `aaaa-bbbb-ccdd`
- No separator: `a1b2c3d4e5f6`
- Uppercase format: `AA:BB:CC:DD:EE:FF`
- Mixed separators: `aa:aa-bb:11-dd:ee`

## Random Delayed Transmission

### Purpose
Prevents circuit tripping caused by simultaneous power surges when multiple computers start up at once.

### How It Works
Computers draw 200-500 watts during startup; 10 simultaneous startups create 2000-5000 watt surges, exceeding typical 1500-2000 watt circuit limits.

### Implementation
1. Configurable `DELAY_RANGE` (e.g., `(1, 3)` seconds)
2. Random delay generated per device with `random.uniform()`
3. Staggered transmission via `time.sleep(delay)`

## Configuration

Open `config.py` and modify the configuration settings to match your needs:

```python
# Delay range (seconds): Random delay time range between each MAC address
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
        # Add more MAC addresses as needed
]

WOL_PORT = 9  # Standard WOL port
BROADCAST_ADDRESS = '255.255.255.255'  # Network broadcast address
```

## Installation

1. Ensure Python 3 is installed on your system
2. Clone or download this repository
3. Navigate to the project directory

## Usage

### Basic Usage

Run the `main.py` script to send WOL packets to all MAC addresses in the `MAC_ADDRESSES` list:

```bash
python main.py
```

### Output Example

```
====== Preparing to send WOL packets, total 7 MAC addresses ======
Sending to: 4ce9-e455-91bd
Sending to: 703a-a61e-ef5a
Sending to: aaaa-bbbb-ccdd
Sending to: a1b2-c3d4-e5f6
Sending to: aabb-ccdd-eeff
Sending to: aaaa-bb11-ddee
Sending to: 4ce9-e455-91bd
====== Sending completed: 7 succeeded, 0 failed ======
```

### Programmatic Usage

You can import and use the functions in your own Python scripts:

```python
# Import directly from the package
from wake_on_lan import send_wol, wake_on_lan

# Send WOL packets with custom delay range
mac_list = ["4c:e9:e4:55:91:bd", "70-3a-a6-1e-ef-5a"]
success, failed = send_wol(mac_list, delay_range=(2, 5))

print(f"Success: {len(success)}, Failed: {len(failed)}")

# Send to a single MAC address
wake_on_lan("4c:e9:e4:55:91:bd")

# Normalize a MAC address
from wake_on_lan import normalize_mac
normalized = normalize_mac("AA:BB:CC:DD:EE:FF")
print(normalized)  # Output: aabbccddeeff
```

## How It Works

1. **MAC Address Normalization**: Converts any supported format to a standardized 12-digit hex string
2. **Magic Packet Creation**: Generates a WOL magic packet (6 bytes of `0xFF` followed by the MAC address repeated 16 times)
3. **Broadcast Transmission**: Sends the packet to the broadcast address on the specified port (default: 9)
4. **Random Delay**: Waits a random time between transmissions to prevent power surges

## Troubleshooting

- **Failed Transmissions**: Check MAC address format, network connectivity, and ensure WOL is enabled on the target device
- **No Devices Waking Up**: Verify the broadcast address is correct for your network
- **Power Surge Issues**: Increase the delay range in `config.py` to spread out device startup times

## Requirements

- Python 3.x
- No additional dependencies required (uses standard library modules: `socket`, `re`, `time`, `random`)

## License

MIT License - feel free to use and modify for personal or commercial projects.
