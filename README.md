# MonteExchange

A Telegram bot for currency exchange between EUR and RUB, integrated with the Wise payment system.

## Description

MonteExchange is a Telegram bot that facilitates currency exchange between Euro (EUR) and Russian Ruble (RUB). The bot integrates with the Wise API to provide real-time exchange rates and payment processing.

### Features

- Currency exchange between EUR and RUB
- Real-time exchange rates from Wise API
- Automated payment link generation
- Configurable exchange and withdrawal fees
- Admin notifications for new exchange requests
- Health check endpoint for monitoring

## Installation

### Prerequisites

- Python 3.12 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Wise API credentials (Token, Profile ID, Balance ID)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/monteexchange.git
   cd monteexchange
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install uv
   uv sync
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your credentials:
   ```
   BOT_TOKEN=your_telegram_bot_token
   WISE_HOST=https://api.wise.com
   WISE_TOKEN=your_wise_api_token
   PROFILE_ID=your_wise_profile_id
   BALANCE_ID=your_wise_balance_id
   ```

6. Run the bot:
   ```bash
   uv run main.py
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t monteexchange .
   ```

2. Run the container:
   ```bash
   docker run -d --name monteexchange --env-file .env monteexchange
   ```

## Usage

### Bot Commands

- `/start` - Start the bot and get an introduction
- `/exchange` - Start the currency exchange process
- `/rate` - Get the current exchange rate of EUR to RUB
- `/help` - Get help and contact information

### Exchange Process

1. Start the exchange process with `/exchange`
2. Enter the amount you want to exchange in Russian rubles
3. The bot will calculate the exchange rate, fees, and provide a payment link
4. Complete the payment through the provided link
5. The admin will be notified of your exchange request

## Configuration

The following environment variables can be configured:

| Variable | Description | Default |
|----------|-------------|---------|
| BOT_TOKEN | Telegram bot token | Required |
| WISE_HOST | Wise API host | Required |
| WISE_TOKEN | Wise API token | Required |
| PROFILE_ID | Wise profile ID | 27614777 |
| BALANCE_ID | Wise balance ID | 28951646 |
| REFERRAL_LINK | Wise referral link | https://wise.com/invite/ahpc/anastasiiam541 |
| WITHDRAWAL_FEE_IN_EURO | Fee for withdrawals in EUR | 5 |
| EXCHANGE_FEE_IN_PERCENT | Fee for currency exchange in % | 2.5 |
| ADMIN_CHAT_ID | Telegram chat ID for admin notifications | 210408407 |

## Development

### Development Dependencies

Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

### Code Quality

The project uses:
- Black for code formatting
- isort for import sorting
- Ruff for linting
- pre-commit for git hooks

Set up pre-commit:
```bash
pre-commit install
```

## Health Check

The bot includes a health check endpoint at `http://localhost:8080/health` that returns the current version and status of the bot.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
