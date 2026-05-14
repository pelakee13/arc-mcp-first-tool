# arc-testnet-helper

A beginner-friendly Python CLI tool for the **Arc Architects Program**.  
Connect to Arc Testnet, check network info, verify your connection, and look up wallet balances — all from your terminal.

---

## Network Details

| Parameter    | Value                            |
|--------------|----------------------------------|
| Network      | Arc Testnet                      |
| RPC URL      | `https://rpc.testnet.arc.network`|
| Chain ID     | `5042002`                        |
| Currency     | USDC                             |
| Block Explorer | [testnet.arcscan.app](https://testnet.arcscan.app) |

> Source: [Arc Docs — Node Providers](https://docs.arc.io/arc/tools/node-providers)

---

## Prerequisites

- Python 3.8 or higher
- pip (comes with Python)
- An internet connection

---

## Installation

**1. Clone or download this repo**

```bash
git clone https://github.com/your-username/arc-testnet-helper.git
cd arc-testnet-helper
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

That's it! No API keys or accounts needed.

---

## Usage

### Show help

```bash
python arc_helper.py --help
```

### 1. Check network info

Displays RPC URL, Chain ID, latest block number, and gas price.

```bash
python arc_helper.py info
```

**Example output:**

```
====================================================
  Arc Testnet — Network Info
====================================================
  [OK]  Connected to Arc Testnet

  Network:             Arc Testnet
  RPC URL:             https://rpc.testnet.arc.network
  Chain ID:            5042002
  Currency:            USDC
  Explorer:            https://testnet.arcscan.app

  Latest block:        3847201
  Block hash:          0x4a9f2c1b8e3d7f0a12...
  Timestamp:           1747123456
  Gas price:           0.001 gwei
```

---

### 2. Sanity check

Verifies you are connected to the correct Arc Testnet (checks RPC, Chain ID, and block production).

```bash
python arc_helper.py sanity
```

**Example output:**

```
====================================================
  Arc Testnet — Sanity Check
====================================================
  [OK]  RPC reachable           → https://rpc.testnet.arc.network
  [OK]  Chain ID correct        → 5042002
  [OK]  Node is live            → latest block #3847201

  All checks passed. You are on Arc Testnet. Ready to build!
```

---

### 3. Check wallet balance

Look up the balance of any wallet address.

```bash
python arc_helper.py balance 0xYourWalletAddressHere
```

**Example output:**

```
====================================================
  Arc Testnet — Balance Check
====================================================
  Address:             0xAbCd...1234 (checksummed)
  [OK]  Connected to Arc Testnet

  Balance (wei):       1000000000000000000
  Balance (USDC):      1.000000 USDC
```

> **Note:** Arc Testnet uses USDC as its native currency with 18 decimal places (standard EVM convention).

---

## Project Structure

```
arc-testnet-helper/
├── arc_helper.py      # Main CLI tool (all features in one file)
├── requirements.txt   # Python dependencies
├── .gitignore         # Files to exclude from git
└── README.md          # This file
```

---

## How It Works

`arc_helper.py` uses [web3.py](https://web3py.readthedocs.io/) to communicate with the Arc Testnet node over HTTP RPC. Every command:

1. Creates a `Web3` connection to `https://rpc.testnet.arc.network`
2. Calls standard JSON-RPC methods (`eth_chainId`, `eth_blockNumber`, `eth_getBalance`, etc.)
3. Prints the results in a human-readable format

No wallet signing, no private keys, no gas — all read-only.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'web3'` | Run `pip install -r requirements.txt` |
| `Could not connect to Arc Testnet` | Check your internet connection |
| `Chain ID MISMATCH` | You may be using a different RPC — ensure you use `https://rpc.testnet.arc.network` |
| `not a valid Ethereum-style address` | Addresses must start with `0x` and be 42 characters long |

---

## Resources

- [Arc Docs](https://docs.arc.io)
- [Arc Testnet Explorer](https://testnet.arcscan.app)
- [web3.py Documentation](https://web3py.readthedocs.io/)
- [Arc Architects Program](https://arc.io)

---

## License

MIT — fork it, build on it, ship it.
