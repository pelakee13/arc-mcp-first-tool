#!/usr/bin/env python3
"""
arc_helper.py — Arc Testnet CLI Helper
=======================================
A beginner-friendly tool for the Arc Architects Program.

Network details sourced from Arc Docs (https://docs.arc.io):
  RPC URL  : https://rpc.testnet.arc.network
  Chain ID : 5042002
  Currency : USDC
  Explorer : https://testnet.arcscan.app

Usage:
  python arc_helper.py info
  python arc_helper.py sanity
  python arc_helper.py balance <wallet_address>
"""

import sys
from web3 import Web3

# ---------------------------------------------------------------------------
# Arc Testnet constants (from Arc Docs — do not change)
# ---------------------------------------------------------------------------
ARC_RPC_URL  = "https://rpc.testnet.arc.network"
ARC_CHAIN_ID = 5042002
ARC_CURRENCY = "USDC"
ARC_EXPLORER = "https://testnet.arcscan.app"
ARC_NAME     = "Arc Testnet"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def connect() -> Web3:
    """Create and return a Web3 instance connected to Arc Testnet."""
    w3 = Web3(Web3.HTTPProvider(ARC_RPC_URL))
    return w3


def print_header(title: str) -> None:
    """Print a simple section header."""
    width = 52
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_ok(msg: str) -> None:
    print(f"  [OK]  {msg}")


def print_err(msg: str) -> None:
    print(f"  [ERR] {msg}")


def print_info(label: str, value) -> None:
    print(f"  {label:<20} {value}")


# ---------------------------------------------------------------------------
# Feature 1 — Network Info
# ---------------------------------------------------------------------------

def cmd_info() -> None:
    """Connect to Arc Testnet and display network information."""
    print_header("Arc Testnet — Network Info")

    w3 = connect()

    # Check basic connectivity
    if not w3.is_connected():
        print_err("Could not connect to Arc Testnet.")
        print_err(f"RPC: {ARC_RPC_URL}")
        print_err("Check your internet connection and try again.")
        sys.exit(1)

    print_ok("Connected to Arc Testnet")
    print()

    # Pull live data from the node
    chain_id    = w3.eth.chain_id
    latest_block = w3.eth.block_number
    block        = w3.eth.get_block("latest")
    gas_price    = w3.eth.gas_price

    print_info("Network:",      ARC_NAME)
    print_info("RPC URL:",      ARC_RPC_URL)
    print_info("Chain ID:",     chain_id)
    print_info("Currency:",     ARC_CURRENCY)
    print_info("Explorer:",     ARC_EXPLORER)
    print()
    print_info("Latest block:", latest_block)
    print_info("Block hash:",   block["hash"].hex()[:20] + "...")
    print_info("Timestamp:",    block["timestamp"])
    print_info("Gas price:",    f"{w3.from_wei(gas_price, 'gwei')} gwei")
    print()


# ---------------------------------------------------------------------------
# Feature 2 — Balance Check
# ---------------------------------------------------------------------------

def cmd_balance(address: str) -> None:
    """Check the USDC balance of a wallet address on Arc Testnet."""
    print_header("Arc Testnet — Balance Check")

    # Validate and checksum the address
    if not Web3.is_address(address):
        print_err(f"'{address}' is not a valid Ethereum-style address.")
        print_err("Addresses must be 42 characters starting with 0x.")
        sys.exit(1)

    checksum_address = Web3.to_checksum_address(address)
    print_info("Address:", checksum_address)

    w3 = connect()

    if not w3.is_connected():
        print_err("Could not connect to Arc Testnet. Check your internet connection.")
        sys.exit(1)

    print_ok("Connected to Arc Testnet")
    print()

    # Fetch balance (returned in wei, the smallest unit)
    balance_wei  = w3.eth.get_balance(checksum_address)
    balance_usdc = w3.from_wei(balance_wei, "ether")  # Arc uses 18-decimal USDC

    print_info("Balance (wei):", balance_wei)
    print_info(f"Balance ({ARC_CURRENCY}):", f"{balance_usdc:.6f} {ARC_CURRENCY}")
    print()

    if balance_wei == 0:
        print("  Tip: This address has no balance on Arc Testnet.")
        print(f"       Visit {ARC_EXPLORER} to inspect the address on-chain.")
    print()


# ---------------------------------------------------------------------------
# Feature 3 — Sanity Check
# ---------------------------------------------------------------------------

def cmd_sanity() -> None:
    """Verify we are connected to the correct Arc Testnet network."""
    print_header("Arc Testnet — Sanity Check")

    w3 = connect()

    # --- Check 1: connectivity ---
    connected = w3.is_connected()
    if connected:
        print_ok(f"RPC reachable           → {ARC_RPC_URL}")
    else:
        print_err(f"RPC unreachable         → {ARC_RPC_URL}")
        sys.exit(1)

    # --- Check 2: chain ID matches ---
    live_chain_id = w3.eth.chain_id
    if live_chain_id == ARC_CHAIN_ID:
        print_ok(f"Chain ID correct        → {live_chain_id}")
    else:
        print_err(f"Chain ID MISMATCH!")
        print_err(f"  Expected : {ARC_CHAIN_ID}")
        print_err(f"  Got      : {live_chain_id}")
        print_err("You may be connected to the wrong network.")
        sys.exit(1)

    # --- Check 3: node is producing blocks ---
    block_number = w3.eth.block_number
    if block_number > 0:
        print_ok(f"Node is live            → latest block #{block_number}")
    else:
        print_err("Node returned block #0 — it may not be synced.")
        sys.exit(1)

    print()
    print("  All checks passed. You are on Arc Testnet. Ready to build!")
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

HELP_TEXT = """
arc-testnet-helper  —  Arc Architects Program Starter Tool
-----------------------------------------------------------
Commands:
  info                  Show network info (RPC, Chain ID, latest block)
  sanity                Verify you are connected to the correct network
  balance <address>     Check wallet balance on Arc Testnet

Examples:
  python arc_helper.py info
  python arc_helper.py sanity
  python arc_helper.py balance 0xYourWalletAddressHere
"""

def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(HELP_TEXT)
        sys.exit(0)

    command = args[0].lower()

    if command == "info":
        cmd_info()

    elif command == "sanity":
        cmd_sanity()

    elif command == "balance":
        if len(args) < 2:
            print_err("'balance' requires a wallet address.")
            print_err("Usage: python arc_helper.py balance <address>")
            sys.exit(1)
        cmd_balance(args[1])

    else:
        print_err(f"Unknown command: '{command}'")
        print(HELP_TEXT)
        sys.exit(1)


if __name__ == "__main__":
    main()
