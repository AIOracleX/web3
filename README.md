# OracleX

OracleX is a decentralized AI-powered price prediction platform designed for the DeFi market. It provides accurate, real-time price forecasts for cryptocurrencies and DeFi tokens, empowering users and applications with valuable insights for smarter trading and decision-making.

## Core Features

*   **AI-Driven Predictions:** Leverages advanced machine learning models, including LSTM and Transformer networks, trained on a combination of on-chain and off-chain data.
*   **Ensemble Learning:** Combines predictions from multiple models to enhance accuracy and robustness.
*   **RESTful API:** Offers a developer-friendly API for easy integration with DEX aggregators, trading bots, and other DeFi applications.
*   **ORX Token:** Powers the OracleX ecosystem, used for API access, governance participation, and incentivizing data providers.
*   **Decentralized Governance:** ORX token holders can participate in the governance process, influencing the future development of the platform.

## Technology Stack

*   **Blockchain:** Base (Ethereum L2)
*   **Programming Languages:** Python, Solidity, JavaScript
*   **Machine Learning Libraries:** TensorFlow, PyTorch, scikit-learn
*   **Cloud Platform:** AWS
*   **API Framework:** Flask

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/AIOracleX/web3/]
    ```
2.  Install dependencies:
    ```bash
    cd web3
    pip install -r requirements.txt
    ```

## Usage

1.  Set up environment variables:
    Create a `.env` file based on the provided `.env.example` and fill in your Alchemy API URL.

2.  Run the Flask application:
    ```bash
    python app.py
    ```

Refer to the API documentation for detailed instructions on how to integrate the OracleX price prediction API into your application.

## API Endpoints
* `/predictions/<asset>` (GET): Retrieve price predictions for a specific asset.
* `/predictions/<asset>/history` (GET): Get historical predictions for a specific asset.
* `/metrics` (GET): Get the latest evaluation metrics for each prediction model.
* `/sentiment/<asset>` (GET): Retrieve the current sentiment for a given asset, gathered from social media and news sources.

## Tokenomics

*   **Token Name:** ORX
*   **Total Supply:** 1,000,000,000 ORX
*   **Distribution:**
    *   Team: 7% (1-year lock-up, 3-year vesting)
    *   Liquidity: 93%

## Roadmap

*   **January 2025:** Testnet Launch & Token Issuance
*   **Q2 2025:** Mainnet Launch & Official API Release
*   **Q3 2025:** Partnerships with Major DEX Aggregators
*   **Q4 2025:** Expansion of Prediction Target Assets
*   **2026 & Beyond:** Exploring New Use Cases, Community-Driven Development, DAO Implementation

## Contributing

Contributions to the OracleX project are welcome. Please refer to the contributing guidelines for more information.

## License

This project is licensed under the MIT License.
