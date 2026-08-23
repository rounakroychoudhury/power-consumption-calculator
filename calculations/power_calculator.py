"""
Power Calculator Module
Handles all electrical power calculations for single-phase AC, three-phase AC, and DC circuits.
"""

import math

class PowerCalculator:
    """
    A class to calculate electrical power in different circuit types.
    """

    @staticmethod
    def validate_inputs(voltage, current, power_factor=None, duration=None):
        """
        Validate user inputs to make sure they're reasonable.
        
        Parameters:
        - voltage: Voltage in volts (must be > 0)
        - current: Current in amperes (must be > 0)
        - power_factor: Power factor 0-1 (only for AC circuits)
        - duration: Time in hours (must be > 0)
        
        Returns:
        - True if valid, raises error if not
        """
        
        # Check if voltage is positive
        if voltage <= 0:
            raise ValueError("Voltage must be greater than 0")
        
        # Check if current is positive
        if current <= 0:
            raise ValueError("Current must be greater than 0")
        
        # Check power factor if provided (for AC circuits)
        if power_factor is not None:
            if power_factor <= 0 or power_factor > 1:
                raise ValueError("Power Factor must be between 0 and 1")
        
        # Check duration if provided
        if duration is not None:
            if duration <= 0:
                raise ValueError("Duration must be greater than 0")
        
        return True

    @staticmethod
    def calculate_single_phase_ac(voltage, current, power_factor, duration):
        """
        Calculate power for Single-Phase AC Circuit.
        
        Formulas:
        - P (Real Power) = V × I × PF  [in Watts]
        - Q (Reactive Power) = V × I × sin(φ)  [in VAR]
        - S (Apparent Power) = V × I  [in VA]
        - E (Energy) = P × time  [in Wh]
        
        Parameters:
        - voltage: Voltage in volts
        - current: Current in amperes
        - power_factor: Power factor (0-1)
        - duration: Time in hours
        
        Returns:
        - Dictionary with all calculated values
        """
        
        # Validate inputs first
        PowerCalculator.validate_inputs(voltage, current, power_factor, duration)
        
        # Calculate Real Power (P) in Watts
        real_power_watts = voltage * current * power_factor
        real_power_kw = real_power_watts / 1000  # Convert to kW
        
        # Calculate phase angle (φ) from power factor
        # If PF = 0.8, then φ = arccos(0.8)
        phase_angle_rad = math.acos(power_factor)
        
        # Calculate Reactive Power (Q) in VAR
        # Q = V × I × sin(φ)
        reactive_power_var = voltage * current * math.sin(phase_angle_rad)
        reactive_power_kvar = reactive_power_var / 1000  # Convert to kVAR
        
        # Calculate Apparent Power (S) in VA
        # S = V × I
        apparent_power_va = voltage * current
        apparent_power_kva = apparent_power_va / 1000  # Convert to kVA
        
        # Calculate Energy Consumed (E) in Wh and kWh
        # E = P × time
        energy_wh = real_power_watts * duration
        energy_kwh = energy_wh / 1000  # Convert to kWh
        
        # Return all results as a dictionary
        return {
            'circuit_type': 'Single-Phase AC',
            'voltage': voltage,
            'current': current,
            'power_factor': power_factor,
            'duration': duration,
            'real_power_w': round(real_power_watts, 2),
            'real_power_kw': round(real_power_kw, 2),
            'reactive_power_var': round(reactive_power_var, 2),
            'reactive_power_kvar': round(reactive_power_kvar, 2),
            'apparent_power_va': round(apparent_power_va, 2),
            'apparent_power_kva': round(apparent_power_kva, 2),
            'energy_wh': round(energy_wh, 2),
            'energy_kwh': round(energy_kwh, 2)
        }

    @staticmethod
    def calculate_three_phase_ac(voltage, current, power_factor, duration):
        """
        Calculate power for Three-Phase AC Circuit.
        
        Formulas:
        - P (Real Power) = √3 × V × I × PF  [in Watts]
        - Q (Reactive Power) = √3 × V × I × sin(φ)  [in VAR]
        - S (Apparent Power) = √3 × V × I  [in VA]
        - E (Energy) = P × time  [in Wh]
        
        Parameters:
        - voltage: Line voltage in volts (between phases)
        - current: Line current in amperes
        - power_factor: Power factor (0-1)
        - duration: Time in hours
        
        Returns:
        - Dictionary with all calculated values
        """
        
        # Validate inputs first
        PowerCalculator.validate_inputs(voltage, current, power_factor, duration)
        
        # √3 is approximately 1.732
        sqrt3 = math.sqrt(3)
        
        # Calculate Real Power (P) in Watts
        # P = √3 × V × I × PF
        real_power_watts = sqrt3 * voltage * current * power_factor
        real_power_kw = real_power_watts / 1000  # Convert to kW
        
        # Calculate phase angle (φ) from power factor
        phase_angle_rad = math.acos(power_factor)
        
        # Calculate Reactive Power (Q) in VAR
        # Q = √3 × V × I × sin(φ)
        reactive_power_var = sqrt3 * voltage * current * math.sin(phase_angle_rad)
        reactive_power_kvar = reactive_power_var / 1000  # Convert to kVAR
        
        # Calculate Apparent Power (S) in VA
        # S = √3 × V × I
        apparent_power_va = sqrt3 * voltage * current
        apparent_power_kva = apparent_power_va / 1000  # Convert to kVA
        
        # Calculate Energy Consumed (E) in Wh and kWh
        # E = P × time
        energy_wh = real_power_watts * duration
        energy_kwh = energy_wh / 1000  # Convert to kWh
        
        # Return all results as a dictionary
        return {
            'circuit_type': 'Three-Phase AC',
            'voltage': voltage,
            'current': current,
            'power_factor': power_factor,
            'duration': duration,
            'real_power_w': round(real_power_watts, 2),
            'real_power_kw': round(real_power_kw, 2),
            'reactive_power_var': round(reactive_power_var, 2),
            'reactive_power_kvar': round(reactive_power_kvar, 2),
            'apparent_power_va': round(apparent_power_va, 2),
            'apparent_power_kva': round(apparent_power_kva, 2),
            'energy_wh': round(energy_wh, 2),
            'energy_kwh': round(energy_kwh, 2)
        }

    @staticmethod
    def calculate_dc(voltage, current, duration):
        """
        Calculate power for DC Circuit.
        
        Formulas:
        - P (Power) = V × I  [in Watts]
        - E (Energy) = V × I × time  [in Wh]
        
        Note: DC circuits don't have reactive power or power factor.
        
        Parameters:
        - voltage: Voltage in volts
        - current: Current in amperes
        - duration: Time in hours
        
        Returns:
        - Dictionary with all calculated values
        """
        
        # Validate inputs first
        PowerCalculator.validate_inputs(voltage, current, duration=duration)
        
        # Calculate Power (P) in Watts
        # P = V × I
        power_watts = voltage * current
        power_kw = power_watts / 1000  # Convert to kW
        
        # Calculate Energy (E) in Wh and kWh
        # E = P × time = V × I × time
        energy_wh = power_watts * duration
        energy_kwh = energy_wh / 1000  # Convert to kWh
        
        # Return all results as a dictionary
        return {
            'circuit_type': 'DC',
            'voltage': voltage,
            'current': current,
            'power_factor': 1.0,  # DC has no reactive power
            'duration': duration,
            'real_power_w': round(power_watts, 2),
            'real_power_kw': round(power_kw, 2),
            'reactive_power_var': 0,  # No reactive power in DC
            'reactive_power_kvar': 0,
            'apparent_power_va': round(power_watts, 2),  # Same as real power
            'apparent_power_kva': round(power_kw, 2),
            'energy_wh': round(energy_wh, 2),
            'energy_kwh': round(energy_kwh, 2)
        }