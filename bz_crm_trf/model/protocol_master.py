from odoo import api, fields, models, _

class ProtocolMaster(models.Model):
    _name = "protocol.master"

    process_type = fields.Selection([
        ('accessibility_test', 'Accessibility Test'), ('bypass_diode_thermal_test', 'Bypass Diode Thermal Test'),
        ('damp_test', 'Damp Heat Test 1000H'), ('humidity_test', 'Humidity Freeze Test'),
        ('thermal_test', 'Thermal Cycling Test'), ('conduit_test', 'Conduit Bending Test'),
        ('susceptibility_test', 'Cut Susceptibility Test'), ('dmtl', 'DMLT'), ('el', 'EL'),
        ('bypass_test', 'Bypass diode functionality'), ('hot_spot_test', 'Hot-Spot Endurance Test'),
        ('determination_test', 'Maximum power Determination'), ('performance_af_test', 'Performance af Low Irradiance'),
        ('performance_stc_test', 'Performance af STC'), ('performance_nmot_test', 'Performance at NMOT'),
        ('coefficient_test', 'Temperature Coefficient'), ('bifaciality_test', 'Bifaciality Testing'),
        ('ground_continuity_test', 'Ground Continuity Test'), ('hail_test', 'Hail Test'),
        ('impulse_voltage_test', 'Impulse Voltage Test'),
        ('insulation_resistance_test', 'Insulation Resistance Test/Dielectric Current Withstand Test'),
        ('insulation_thickness_test', 'Insulation Thickness Test'), ('ir_thermography_test', 'IR Thermography'),
        ('module_breakage_test', 'Module Breakage Test'), ('outdoor_exposure_test', 'Outdoor Exposure Test'),
        ('partial_discharge_test', 'Partial Discharge Test'), ('peel_test', 'Peel Test'),
        ('potential_induced_test', 'Potential Induced Degradation'),
        ('reverse_current_test', 'Reverse Current Overload Test'),
        ('rot_retention_test', 'ROT-Retention of junction box on mounting surface'),
        ('rot_cord_test', 'ROT-Cord Anchorage_Pull test'),
        ('rot_anchorage_torque', 'ROT _Cord Anchorage_Torque Test'), ('smlt', 'SMLT'),
        ('uv_preconditioning_test', 'UV Preconditioning'), ('visual_inspection', 'Visual Inspection'),
        ('wet_leakage_current', 'Wet Leakage Current Test')
    ])

    standard = fields.Many2one('standards', string="Standard", required=True)
    resistance = fields.Char(string='Resistance')
    humidity = fields.Char(string='Humidity')
    voltage = fields.Char(string='Voltage')
    temperature = fields.Float(string='Temperature')
    voltage_temperature = fields.Char(string='Voltage Temperature')
    trade_size_conduit = fields.Float(string='Trade Size of Conduit')
    velocity = fields.Float(string='Velocity')
    average_pressure = fields.Float(string='Average Pressure')
    applied_current = fields.Char(string='Applied Current')
    no_of_diode = fields.Float(string='No of Bypass Diode')
    irradiance = fields.Float(string='Irradiance')
    p_max = fields.Char(string='Pmax')
    sweep_duration = fields.Float(string='Sweep Duration')
    diameter = fields.Float(string='Diameter')
    maximum_system_voltage = fields.Float(string='Maximum System Voltage')
    leakage_current = fields.Char(string='Leakage Current')
    module_application_class = fields.Char(string='Module Application Class')
    impactor_weight = fields.Float(string='Impactor Weight')
    irradiation_dosage = fields.Char(string='Irradiation dosage')
    maximum_system_voltage = fields.Float(string='Maximum System Voltage')
    maximum_over_current_protection = fields.Char(string='Maximum over-current protection rating (Iocpr)')
    force = fields.Char(string='Force')
    diameter_of_wire = fields.Float(string='Diameter of wire')
    uv_wave_length_irradiance = fields.Char(string='UV Wave Length & Irradiance')
    diode_voltage = fields.Float(string='Diode Voltage')
    relative_humidity = fields.Char(string='Relative Humidity')
    stc_measured_parameters = fields.Char(string='STC Measured Parameters Impp (A)')
    conduit_diameter = fields.Char(string='Conduit Diameter')
    total_no_cycle = fields.Float(string='Total No Cycle')
    no_of_blocking = fields.Integer(string='No of Blocking Diode')
    voc = fields.Char(string='Voc')
    sweep_direction = fields.Float(string='Sweep Direction')
    test_current_25_i = fields.Char(string='Test Current (2.5 x IOCPR )')
    weight = fields.Float(string='Weight')
    application_class = fields.Char(string='Application Class')
    system_voltage = fields.Float(string='System Voltage')
    impactor_height = fields.Float(string='Impactor Height')
    module_area = fields.Char(string='Module Area')
    test_current_135 = fields.Char(string='Test Current (1.35 x IOCPR )')
    angle = fields.Char(string='Angle')
    torque = fields.Float(string='Torque')
    module_dimension = fields.Char(string='Module Dimension')
    module_temperature = fields.Float(string='Module Temperature')
    no_of_cycles = fields.Integer(string='No. of Cycles')
    time_ave = fields.Float(string='Time(Ave)')
    applied_weight_Kg = fields.Char(string='Applied Weight in Kg')
    time_duration = fields.Float(string='Time Duration')
    ambient_temperature = fields.Float(string='Ambient Temperature')
    number_of_cell = fields.Integer(string='Number of Cell')
    isc = fields.Char(string='Isc')
    load_IV_voltage = fields.Char(string='Load IV Voltage')
    impulse_voltage_volt = fields.Char('Impulse Voltage in Volt')
    no_thickness_layers = fields.Integer(string='No. of Thickness Layers')
    no_of_cell = fields.Integer(string='No. of Cell')
    impact_diameter = fields.Char(string='Impact Diameter')
    width = fields.Float(string='Width')
    test_time = fields.Float(string='Test Time')
    visible_defect = fields.Char(string='Visible Defect')
    water_resistivity = fields.Char(string='Water Resistivity')
    diode_case_temperature = fields.Char(string='Diode case Temperature')
    recovery_time = fields.Float(string='Recovery Time')
    avg_current_A = fields.Float(string='Avg Current (A)')
    force_load_N = fields.Char(string='Force load in N')
    IV_point = fields.Char(string='IV Point')
    max_time_duration = fields.Float(string='Max Time duration of Test')
    immp = fields.Char(string='Immp')
    distance = fields.Float(string='Distance')
    time_pulse_duration = fields.Float(string='Time Pulse Duration')
    broken_particle_size = fields.Float(string='Broken Particle Size')
    extinction_voltage = fields.Char(string='Extinction Voltage')
    length_of_measurement = fields.Char(string='Length of Measurement')
    irradiance_50 = fields.Float(string='Irradiance ≤ 50 w/m2')
    total_no_cycle = fields.Integer(string='Total No. of Cycle')
    marking = fields.Char(string='Marking')
    water_temperature = fields.Float(string='Water Temperature')
    diode_junction_temperature = fields.Float(string='Diode Junction Temperature')
    temperature_during_recovery_period = fields.Float(string='Temperature during recovery period')
    max_allowed_cycle_time = fields.Float(string='Max Allowed Cycle Time')
    no_of_thermal_cycles = fields.Integer(string='No. of Thermal Cycles')
    time_duration_s = fields.Float(string='Time Duration in s')
    vmmp = fields.Char(string='Vmmp')
    alternative_name1 = fields.Char(string='α(%/°C)')
    insulation_thickness = fields.Char(string='Insulation Thickness')
    charge_intensity = fields.Char(string='Charge Intensity')
    max_system_voltage = fields.Char(string='Max System Voltage')
    test_current_125_isc = fields.Char(string='Test Current = 1.25*Isc')
    total_no_hours = fields.Integer(string='Total no. of hours')
    ff = fields.Char(string='FF')
    efficiency = fields.Float(string='Efficiency')
    alternative_name2 = fields.Char(string='β( % / oC)')
    alternative_name3 = fields.Char(string='ƴ(%/oC)')
    irradiance_50_w_m2 = fields.Char(string='Irradiance ≤ 50 w/m2')
    name_plate_verification = fields.Char(string='Name Plate Verification')
    current = fields.Char(string='Current')
    thermal_resistance_between_diode_junction = fields.Char(
        string='Thermal Resistance Between Diode Junction & Diode case Temperature')
    diode_power_drop = fields.Char(string='Diode Power Drop')
    temperature_during_humidity_period = fields.Float(string='Temperature During Humidity Period')
