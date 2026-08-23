# ⚡ Power Consumption Calculator

A web-based application for calculating electrical power and energy consumption for **single-phase AC, three-phase AC, and DC circuits**.

Built using **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

## Features

* Calculate power and energy for different circuit types
* Supports single-phase AC, three-phase AC, and DC circuits
* Calculates real, reactive, and apparent power for AC circuits
* Calculates energy consumption based on operating time
* Stores calculation history using SQLite
* View previous calculations and basic statistics
* Export calculation history as a CSV file
* Delete individual calculations or clear the complete history
* Simple responsive web interface

## Calculations

### Single-Phase AC

* Real Power: `P = V × I × PF`
* Reactive Power: `Q = V × I × sin(cos⁻¹(PF))`
* Apparent Power: `S = V × I`
* Energy: `E = P × time`

### Three-Phase AC

* Real Power: `P = √3 × V × I × PF`
* Reactive Power: `Q = √3 × V × I × sin(cos⁻¹(PF))`
* Apparent Power: `S = √3 × V × I`
* Energy: `E = P × time`

### DC

* Power: `P = V × I`
* Energy: `E = P × time`

Power is displayed in **W/kW**, while energy is displayed in **Wh/kWh**.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Data Processing:** Pandas
* **Version Control:** Git & GitHub

## Project Structure

```text
power-consumption-calculator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── calculations/
│   ├── __init__.py
│   └── power_calculator.py
│
├── database/
│   ├── __init__.py
│   └── db_manager.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── history.html
│
└── static/
    └── style.css
```

The SQLite database is created locally inside the `instance/` directory when the application runs and is intentionally excluded from version control.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rounakroychoudhury/power-consumption-calculator.git
cd power-consumption-calculator
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## How It Works

The application is divided into three main parts:

### Power Calculator

`calculations/power_calculator.py`

Handles input validation and the electrical calculations for each circuit type.

### Database Manager

`database/db_manager.py`

Handles SQLite database operations, including saving calculations, retrieving history, and generating statistics.

### Flask Application

`app.py`

Connects the calculation logic and database to the web interface through Flask routes.

## Example

For a single-phase AC circuit with:

```text
Voltage:       230 V
Current:       10 A
Power Factor:  0.8
Duration:      5 hours
```

The application calculates approximately:

```text
Real Power:      1.84 kW
Reactive Power:  1.38 kVAR
Apparent Power:  2.30 kVA
Energy:          9.20 kWh
```

## Future Improvements

Some possible improvements for the project include:

* Adding user authentication
* Adding graphical energy-consumption reports
* Supporting custom electricity tariff calculations
* Adding more circuit/load types
* Deploying the application online

## Author

**Rounak Roychoudhury**

Electrical Engineering
Dr. B. C. Roy Engineering College, Durgapur

## License

This project is open source and available for learning and educational purposes.