"""
Flask Web Application for Power Consumption Calculator
Handles HTTP requests, calculations, and database operations.
"""

from flask import Flask, render_template, request, jsonify, send_file
import csv
import io
from datetime import datetime

# Import our custom modules
from calculations.power_calculator import PowerCalculator
from database.db_manager import DatabaseManager

# Create a Flask application
app = Flask(__name__)

# Initialize the database manager
db = DatabaseManager()

# Configure Flask
app.config['JSON_SORT_KEYS'] = False

# ============================================
# ROUTE 1: HOME PAGE / CALCULATOR
# ============================================

@app.route('/')
def index():
    """
    Display the main calculator page.
    """
    return render_template('index.html')

# ============================================
# ROUTE 2: PERFORM CALCULATION
# ============================================

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Receive form data, perform calculation, save to database, return results.
    """
    try:
        # Get data from the form
        # request.form is like "reading what the user typed in the form"
        circuit_type = request.form.get('circuit_type')
        voltage = float(request.form.get('voltage'))
        current = float(request.form.get('current'))
        duration = float(request.form.get('duration'))
        
        # Power factor is optional (only for AC circuits)
        power_factor = float(request.form.get('power_factor', 1.0))
        
        # Validate that required fields exist
        if not circuit_type or not voltage or not current or not duration:
            return jsonify({
                'success': False,
                'error': 'Please fill in all required fields'
            }), 400
        
        # Perform the calculation based on circuit type
        # This calls the PowerCalculator class we created earlier
        if circuit_type == 'single_phase':
            result = PowerCalculator.calculate_single_phase_ac(
                voltage, current, power_factor, duration
            )
        elif circuit_type == 'three_phase':
            result = PowerCalculator.calculate_three_phase_ac(
                voltage, current, power_factor, duration
            )
        elif circuit_type == 'dc':
            result = PowerCalculator.calculate_dc(
                voltage, current, duration
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid circuit type'
            }), 400
        
        # Save the result to the database
        # This calls the DatabaseManager we created earlier
        calculation_id = db.save_calculation(result)
        
        # Add the ID to the result
        result['id'] = calculation_id
        result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Return the results as JSON (data format)
        return jsonify({
            'success': True,
            'result': result
        })
    
    except ValueError as e:
        # If the user entered text instead of numbers
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    
    except Exception as e:
        # Catch any other errors
        return jsonify({
            'success': False,
            'error': f'Calculation error: {str(e)}'
        }), 500

# ============================================
# ROUTE 3: VIEW CALCULATION HISTORY
# ============================================

@app.route('/history')
def history():
    """
    Display all past calculations.
    """
    # Get all calculations from database
    calculations = db.get_all_calculations()
    
    # Get statistics
    stats = db.get_statistics()
    
    # Pass data to HTML template
    return render_template('history.html', 
                         calculations=calculations,
                         stats=stats)

# ============================================
# ROUTE 4: DELETE A SINGLE CALCULATION
# ============================================

@app.route('/delete/<int:calc_id>', methods=['POST'])
def delete_calculation(calc_id):
    """
    Delete a specific calculation from the database.
    """
    try:
        success = db.delete_calculation(calc_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete calculation'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# ROUTE 5: CLEAR ALL CALCULATIONS
# ============================================

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """
    Delete all calculations from the database.
    """
    try:
        success = db.clear_all_calculations()
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to clear history'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# ROUTE 6: DOWNLOAD HISTORY AS CSV
# ============================================

@app.route('/download-csv')
def download_csv():
    """
    Export all calculations as a CSV file and download it.
    CSV = Comma Separated Values (Excel-like format)
    """
    try:
        # Get all calculations from database
        calculations = db.get_all_calculations()
        
        if not calculations:
            return jsonify({
                'success': False,
                'error': 'No calculations to download'
            }), 400
        
        # Create an in-memory CSV file
        # Think of this as creating a virtual Excel file
        output = io.StringIO()
        
        # Define the column headers
        fieldnames = [
            'ID', 'Circuit Type', 'Voltage (V)', 'Current (A)',
            'Power Factor', 'Duration (h)', 'Real Power (W)', 'Real Power (kW)',
            'Reactive Power (VAR)', 'Reactive Power (kVAR)',
            'Apparent Power (VA)', 'Apparent Power (kVA)',
            'Energy (Wh)', 'Energy (kWh)', 'Timestamp'
        ]
        
        # Create a CSV writer
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write each calculation as a row
        for calc in calculations:
            writer.writerow({
                'ID': calc['id'],
                'Circuit Type': calc['circuit_type'],
                'Voltage (V)': calc['voltage'],
                'Current (A)': calc['current'],
                'Power Factor': calc['power_factor'],
                'Duration (h)': calc['duration'],
                'Real Power (W)': calc['real_power_w'],
                'Real Power (kW)': calc['real_power_kw'],
                'Reactive Power (VAR)': calc['reactive_power_var'],
                'Reactive Power (kVAR)': calc['reactive_power_kvar'],
                'Apparent Power (VA)': calc['apparent_power_va'],
                'Apparent Power (kVA)': calc['apparent_power_kva'],
                'Energy (Wh)': calc['energy_wh'],
                'Energy (kWh)': calc['energy_kwh'],
                'Timestamp': calc['timestamp']
            })
        
        # Create a file-like object from the string
        output.seek(0)
        
        # Send the file to the user for download
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'calculations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors (page not found)"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors (server error)"""
    return render_template('500.html'), 500

# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == '__main__':
    # This line runs the Flask app
    # debug=True means if there's an error, we see it immediately
    print("🚀 Power Consumption Calculator Starting...")
    print("📊 Open your browser and go to: http://localhost:5000")
    
    app.run(debug=True, host='127.0.0.1', port=5000)