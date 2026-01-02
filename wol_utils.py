import socket
import re
import time
import random


def normalize_mac(mac):
    """
    Extract and normalize MAC address from any format string
    """
    if not mac:
        raise ValueError("MAC address cannot be empty")
    
    # Validate separators can only be : or -, not other characters (like spaces, dots, etc.)
    # Remove all allowed characters (hex characters and separators), if any characters remain, they are invalid
    allowed_chars = re.sub(r'[0-9a-fA-F:\-]', '', mac)
    if allowed_chars:
        raise ValueError(f"MAC address contains invalid characters, only : or - are allowed as separators, found invalid characters: {repr(allowed_chars)}")
    
    # Extract all hex characters (0-9a-fA-F)
    hex_chars = re.findall(r'[0-9a-fA-F]', mac)
    
    if len(hex_chars) < 12:
        raise ValueError(f"MAC address must contain at least 12 hex characters, currently only {len(hex_chars)} characters: {mac}")
    
    if len(hex_chars) > 12:
        # If more than 12 characters, take only the first 12
        hex_chars = hex_chars[:12]
    
    # Convert to lowercase string
    normalized = ''.join(hex_chars).lower()
    
    # Verify it's exactly 12 characters
    if len(normalized) != 12:
        raise ValueError(f"MAC address normalization failed: {normalized}")
    
    return normalized


def _create_magic_packet(mac):
    """
    Create WOL magic packet
    
    WOL specification:
    - First 6 bytes: 0xFF (sync stream)
    - Next 96 bytes: Target MAC address repeated 16 times
    
    Args:
        mac: Normalized MAC address (12-digit hex string)
        
    Returns:
        WOL magic packet (102 bytes)
    """
    # Convert MAC address to bytes
    mac_bytes = bytes.fromhex(mac)
    
    # Create magic packet: 6 bytes of 0xFF + MAC address repeated 16 times
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    
    return magic_packet


def wake_on_lan(mac_address, port=9, broadcast='255.255.255.255'):
    """
    Send WOL magic packet to wake up device with specified MAC address
    
    Args:
        mac_address: MAC address (supports any format)
        port: WOL port (default 9)
        broadcast: Broadcast address (default 255.255.255.255)
        
    Raises:
        ValueError: If MAC address format is invalid
        socket.error: If network transmission fails
    """
    # Normalize MAC address
    normalized_mac = normalize_mac(mac_address)
    
    # Create magic packet
    magic_packet = _create_magic_packet(normalized_mac)
    
    # Send magic packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast, port))
    finally:
        sock.close()


def send_wol(mac_addresses, port=9, broadcast='255.255.255.255', delay_range=(0, 1)):
    """
    Send WOL magic packets in batch
    
    Args:
        mac_addresses: List of MAC addresses (supports any format)
        port: WOL port (default 9)
        broadcast: Broadcast address (default 255.255.255.255)
        delay_range: Delay range between each MAC address (seconds), default (0, 1)
                     Example: (1, 5) means random interval between 1-5 seconds
        
    Returns:
        List of successfully sent MAC addresses and list of failed MAC addresses
        
    Example:
        # Use 1-5 second random interval
        success, failed = send_wol(mac_list, delay_range=(1, 5))
    """
    success_list = []
    failed_list = []
    
    for mac in mac_addresses:
        try:
            # Normalize MAC address (this is the actual format sent)
            normalized_mac = normalize_mac(mac)
            # Format for display: add dash every 4 characters, e.g., aaaa-bbbb-cccc
            formatted_mac = '-'.join([normalized_mac[i:i+4] for i in range(0, 12, 4)])
            print(f"Sending to: {formatted_mac}")
            wake_on_lan(mac, port, broadcast)
            success_list.append(mac)
            
            # Random delay
            if delay_range[1] > 0:
                delay = random.uniform(delay_range[0], delay_range[1])
                time.sleep(delay)
        except Exception as e:
            failed_list.append((mac, str(e)))
            print(f"  Failed: {e}")
    
    return success_list, failed_list
