# Secure Crypto Portfolio Tracker & Automated Allocator

A secure, modular, and resilient Python-based automation utility designed to update a monthly crypto investment spreadsheet (`crypto_investments.csv`) for LibreOffice Calc.

This project demonstrates strong backend engineering principles, focusing on **API security, infrastructure abuse prevention, and modular design**.

## 🛡️ Security & Architecture Features

* **Zero Hardware/Hardcoded Secrets:** The architecture strictly isolates sensitive API keys. It consumes credentials natively through system environment variables (`COINGECKO_API_KEY`), preventing accidental key exposure on public repositories.
* **Resilient Connection Module (`tracker.py`):** Network logic is fully isolated from the spreadsheet operations. It includes network timeouts (15s) and handles connection anomalies gracefully without crashing the pipeline.
* **Rate-Limit & Anti-Block Protection:** Built-in resilience against `HTTP 429` (Too Many Requests). It implements **exponential backoff retry logic**, scaling waiting periods dynamically to respect the CoinGecko Demo API infrastructure boundaries and prevent IP throttling.
* **Official Authorization Alignment:** Uses the dedicated `x-cg-demo-api-key` header to authenticate tracking request payloads through the official developer standard.
* **Live Formulas Integration:** Instead of printing flat values, the application injects raw, dynamic spreadsheet expressions (`=C2*D2`, `=E2*(1+B2)`). LibreOffice Calc treats them as live formula tokens, preserving calculated cell states naturally during offline sessions.

## 🗂️ Project Structure

```text
├── main.py          # Application orchestrator, data layer integration, and CSV writer
└── tracker.py       # Isolated secure connection engine with error handling and backoff
```

## 🚀 Installation & Local Deployment

### 1. Environment Setup
Clone the workspace and export your official CoinGecko Demo API credentials into your session context:

```bash
export COINGECKO_API_KEY="your_demo_api_key_here"
```

### 2. Manual Test Trigger
Execute the master orchestration sequence manually to verify dataset population:

```bash
python3 main.py
```

### 3. Production Scheduling (Cron Integration)
To automate asset evaluation securely on the 6th day of every month at 09:00 AM without leaking state secrets, register the job profile inside your system deployment environment (`crontab -e`):

```text
0 9 6 * * COINGECKO_API_KEY="your_demo_api_key_here" /usr/bin/python3 /path/to/main.py >> /path/to/update_crypto_investments.log 2>&1
```

## 📊 Monitored Asset Class
The data pipeline safely monitors tracking indices for high-liquidity digital assets and stablecoins including:
* **Stablecoins:** Tether (USDT), USD Coin (USDC)
* **Layer 1 & Ecosystems:** Ethereum (ETH), Solana (SOL), Near Protocol (NEAR), Cardano (ADA), Avalanche (AVAX), Polkadot (DOT), Cosmos (ATOM)
* **Utility Tokens:** Chiliz (CHZ)
