# ⚡ Power Consumption Calculator

A web-based application to calculate electrical power consumption for single-phase AC, three-phase AC, and DC circuits. Built with Python and Flask.

## 🎯 Features

- **Multiple Circuit Types**: Support for Single-Phase AC, Three-Phase AC, and DC circuits
- **Accurate Calculations**: Calculate Real Power, Reactive Power, Apparent Power, and Energy Consumption
- **Calculation History**: Store and view all past calculations
- **Data Export**: Download calculation history as CSV file
- **Statistics**: View aggregate statistics (average power, total energy, etc.)
- **Clean UI**: Intuitive, responsive web interface
- **No Database Setup**: Uses SQLite (automatically created)

## 📊 What It Calculates

### Single-Phase AC Circuit
- **Real Power (P)** = V × I × cos(φ) [in Watts]
- **Reactive Power (Q)** = V × I × sin(φ) [in VAR]
- **Apparent Power (S)** = V × I [in VA]
- **Energy (E)** = P × time [in kWh]

### Three-Phase AC Circuit
- **Real Power (P)** = √3 × V × I × cos(φ) [in Watts]
- **Reactive Power (Q)** = √3 × V × I × sin(φ) [in VAR]
- **Apparent Power (S)** = √3 × V × I [in VA]
- **Energy (E)** = P × time [in kWh]

### DC Circuit
- **Power (P)** = V × I [in Watts]
- **Energy (E)** = V × I × time [in kWh]

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

**Step 1: Clone or download this project**

```bash
cd power-consumption-calculator
```

**Step 2: Create a virtual environment (recommended)**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Run the application**

```bash
python app.py
```

**Step 5: Open in browser**

Go to: **http://localhost:5000**

## 📁 Project Structure

```
power-consumption-calculator/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── calculations/
│   ├── __init__.py
│   └── power_calculator.py     # Core calculation logic
│
├── database/
│   ├── __init__.py
│   └── db_manager.py          # Database operations
│
├── templates/                  # HTML files
│   ├── base.html              # Base template
│   ├── index.html             # Calculator page
│   └── history.html           # History page
│
├── static/
│   └── style.css              # Styling
│
└── instance/
    └── calculator.db          # SQLite database (auto-created)
```

## 🎮 How to Use

### 1. Make a Calculation

- Go to the **Calculator** page
- Select your circuit type (Single-Phase AC, Three-Phase AC, or DC)
- Enter voltage, current, and duration
- For AC circuits, enter power factor (default: 0.8)
- Click **Calculate Power**
- View results immediately

### 2. View History

- Click **History** in the navigation
- See all your past calculations
- View statistics (average power, total energy, etc.)

### 3. Export Data

- Go to **History** page
- Click **Download as CSV** button
- Open in Excel or any spreadsheet application

### 4. Delete Calculations

- In **History** page, click **Delete** next to a calculation
- Or click **Clear All** to remove all calculations

## 📝 Example Calculations

### Example 1: Single-Phase Household Circuit
```
Circuit Type: Single-Phase AC
Voltage: 230 V
Current: 10 A
Power Factor: 0.8
Duration: 5 hours

Results:
- Real Power: 1.84 kW
- Reactive Power: 1.38 kVAR
- Apparent Power: 2.3 kVA
- Energy: 9.2 kWh
```

### Example 2: Three-Phase Industrial Circuit
```
Circuit Type: Three-Phase AC
Voltage: 415 V (line-to-line)
Current: 20 A
Power Factor: 0.85
Duration: 8 hours

Results:
- Real Power: 11.8 kW
- Reactive Power: 7.2 kVAR
- Apparent Power: 14.4 kVA
- Energy: 94.4 kWh
```

### Example 3: DC Circuit (Solar System)
```
Circuit Type: DC
Voltage: 48 V
Current: 50 A
Duration: 6 hours

Results:
- Power: 2.4 kW
- Energy: 14.4 kWh
```

## 🔧 Technical Details

### Technologies Used

- **Backend**: Python 3.8+, Flask 2.3
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Processing**: Pandas, NumPy

### Code Organization

**PowerCalculator Class** (`calculations/power_calculator.py`)
- Validates inputs
- Performs electrical calculations
- Returns results as dictionaries

**DatabaseManager Class** (`database/db_manager.py`)
- Creates SQLite database
- Saves calculations
- Retrieves calculation history
- Exports statistics

**Flask App** (`app.py`)
- Defines web routes
- Handles form submissions
- Serves HTML pages
- Manages CSV exports

### Database Schema

```sql
CREATE TABLE calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circuit_type TEXT NOT NULL,
    voltage REAL NOT NULL,
    current REAL NOT NULL,
    power_factor REAL NOT NULL,
    duration REAL NOT NULL,
    real_power_w REAL NOT NULL,
    real_power_kw REAL NOT NULL,
    reactive_power_var REAL NOT NULL,
    reactive_power_kvar REAL NOT NULL,
    apparent_power_va REAL NOT NULL,
    apparent_power_kva REAL NOT NULL,
    energy_wh REAL NOT NULL,
    energy_kwh REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## ✅ Testing

### Manual Testing Checklist

- [ ] Calculator form displays correctly
- [ ] Single-phase calculation produces correct results
- [ ] Three-phase calculation produces correct results
- [ ] DC calculation works without power factor
- [ ] Invalid inputs show error messages
- [ ] Calculations save to database
- [ ] History page displays all calculations
- [ ] Statistics show correct values
- [ ] CSV export downloads successfully
- [ ] Delete function removes calculations
- [ ] Clear all function deletes all calculations
- [ ] Responsive design works on mobile

### Test Data

**Single-Phase AC (Household)**
- V: 230, I: 10, PF: 0.8, Duration: 5
- Expected P: ~1.84 kW

**Three-Phase AC (Industrial)**
- V: 415, I: 20, PF: 0.85, Duration: 8
- Expected P: ~11.8 kW

**DC (Solar)**
- V: 48, I: 50, Duration: 6
- Expected P: 2.4 kW

## 🐛 Troubleshooting

**Problem: Port 5000 already in use**
```bash
# Change the port in app.py line:
# app.run(debug=True, host='127.0.0.1', port=5001)
```

**Problem: "Module not found" error**
```bash
# Make sure you installed dependencies:
pip install -r requirements.txt
```

**Problem: Database not created**
- The database is created automatically in `instance/` folder
- Make sure the folder has write permissions

**Problem: Flask not found**
```bash
# Activate virtual environment first:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

## 📚 Learning Resources

### Understanding Power Concepts

- **Real Power (P)**: Actual power consumed by resistive loads (measured in Watts)
- **Reactive Power (Q)**: Power wasted in inductive/capacitive elements (measured in VAR)
- **Apparent Power (S)**: Total power supplied by the source (measured in VA)
- **Power Factor (PF)**: Ratio of real to apparent power (0-1, ideally 1.0)
- **Energy**: Power multiplied by time (measured in kWh)

### Code Explanation

**To understand the code:**
1. Start with `power_calculator.py` - pure math, easy to follow
2. Then `db_manager.py` - database operations
3. Finally `app.py` - web routing and integration

## 🎓 Interview Questions You Can Answer

After building this project, you'll be able to explain:

1. **What does your project do?**
   - It calculates electrical power and energy consumption for different circuit types.

2. **Why these technologies?**
   - Flask is lightweight and perfect for learning.
   - SQLite requires no setup.
   - HTML/CSS/JS are standard for web.

3. **How do you validate inputs?**
   - Check for positive values, power factor between 0-1.

4. **How do you store data?**
   - SQLite database with Python's sqlite3 module.

5. **How do you calculate reactive power?**
   - Q = V × I × sin(arccos(PF))

6. **What's the difference between single-phase and three-phase?**
   - Three-phase multiplies by √3 for higher efficiency.

7. **Why use classes?**
   - Organizes code, makes it reusable, easier to test.

## 📄 License

This project is open source and free to use.

## 👤 Author

Built by: Rounak Roychoudhury  
College: Dr. B. C. Roy Engineering College (MAKAUT)  
Program: TCS Ninja 2024

## 🙏 Acknowledgments

- Electrical Engineering concepts from MAKAUT curriculum
- Flask documentation and tutorials
- Python community for amazing libraries

---

**Happy Learning! ⚡**

For any questions or improvements, feel free to modify and experiment with the code!