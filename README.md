# Splitwise Clone

## Overview
A web application for tracking shared expenses and splitting bills among friends, groups, and trips.

## Features
- User Registration and Authentication
- Create Groups and Add Members
- Add and Track Expenses
- Settle Debts
- View Expense History

## Setup

### Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)

### Installation
1. Clone the repository
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database
```bash
flask db upgrade
```

6. Run the application
```bash
flask run
```

## Running Tests
```bash
pytest tests/
```

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
