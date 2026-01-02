from config import DELAY_RANGE, MAC_ADDRESSES, WOL_PORT, BROADCAST_ADDRESS
from wol_utils import send_wol


def main():
    """
    Main function to send WOL packets to configured MAC addresses
    """
    mac_address = MAC_ADDRESSES
    
    # Output total number of packets to send
    print(f"====== Preparing to send WOL packets, total {len(mac_address)} MAC addresses ======")
    
    # Use configured delay range, port, and broadcast address
    success, failed = send_wol(
        mac_address, 
        port=WOL_PORT, 
        broadcast=BROADCAST_ADDRESS, 
        delay_range=DELAY_RANGE
    )
    
    print(f"====== Sending completed: {len(success)} succeeded, {len(failed)} failed ======")
    if failed:
        print("\nFailed MAC addresses:")
        for mac, error in failed:
            print(f"  - {mac}: {error}")


if __name__ == "__main__":
    main()
