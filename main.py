import streamlit as st
import time
# import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Advanced Multi-Unit Converter", layout="wide")

# Conversion Units Data Structure
conversion_units = {
    # -------------------- 1. Area --------------------
    "Area": {
        "base": "Square Meter",
        "units": {
            "Square Kilometer": 1_000_000,      # 1 km² = 1,000,000 m²
            "Square Meter": 1,                 # Base unit
            "Square Mile": 2_589_988,          # 1 mi² ≈ 2,589,988 m²
            "Square Yard": 0.836127,           # 1 yd² ≈ 0.836127 m²
            "Square Foot": 0.092903,           # 1 ft² ≈ 0.092903 m²
            "Square Inch": 0.00064516,         # 1 in² ≈ 0.00064516 m² (corrected)
            "Hectare": 10_000,                 # 1 ha = 10,000 m²
            "Acre": 4046.86                    # 1 acre ≈ 4,046.86 m²
        }
    },

    # -------------------- 2. Data Transfer Rate --------------------
    "Data Transfer Rate": {
        "base": "Bit per second",
        "units": {
            # Common decimal-based units
            "Bit per second": 1,
            "Kilobit per second": 1_000,         # 1 kbps = 1,000 bps
            "Megabit per second": 1_000_000,     # 1 Mbps = 1,000,000 bps
            "Gigabit per second": 1_000_000_000, # 1 Gbps = 1,000,000,000 bps
            "Byte per second": 8,               # 1 B/s = 8 bps
            "Kilobyte per second": 8_000,        # 1 kB/s = 8,000 bps (decimal kilo)

            # Additional binary & larger units
            "Kibit per second": 1024,            # 1 Kibit/s = 1024 bps
            "Mebibit per second": 1_048_576,     # 1 Mibit/s = 1,048,576 bps
            "Gibibit per second": 1_073_741_824, # 1 Gibit/s = 1,073,741,824 bps
            "Tebibit per second": 1_099_511_627_776,  # 1 Tibit/s = 2^40 bps
            "Megabyte per second": 8_000_000,     # 1 MB/s = 1,000,000 B/s = 8,000,000 bps
            "Gigabyte per second": 8_000_000_000, # 1 GB/s = 1,000,000,000 B/s
            "Terabit per second": 1_000_000_000_000,   # 1 Tbps = 1e12 bps
            "Terabyte per second": 8_000_000_000_000   # 1 TB/s = 8e12 bps
        }
    },

    # -------------------- 3. Digital Storage --------------------
    "Digital Storage": {
        "base": "Byte",
        "units": {
            # 1 Byte = 8 bits
            "Bit": 0.125,             # 1 bit = 1/8 Byte
            "Byte": 1,                # Base unit
            "Kilobyte": 1_000,        # decimal kilo
            "Megabyte": 1_000_000,
            "Gigabyte": 1_000_000_000,
            "Terabyte": 1_000_000_000_000,

            "Kibibyte": 1024,         # binary kibi
            "Mebibyte": 1_048_576,
            "Gibibyte": 1_073_741_824,
            "Tebibyte": 1_099_511_627_776
        }
    },

    # -------------------- 4. Energy --------------------
    "Energy": {
        "base": "Joule",
        "units": {
            "Joule": 1,
            "Kilojoule": 1000,         # 1 kJ = 1000 J
            "Calorie": 4.184,         # 1 cal ≈ 4.184 J (small calorie)
            "Kilocalorie": 4184,      # 1 kcal (food Calorie) = 4184 J
            "Watt-hour": 3600,        # 1 Wh = 3600 J
            "Kilowatt-hour": 3_600_000, # 1 kWh = 3.6e6 J
            "Btu": 1055.06            # 1 BTU ≈ 1055.06 J
        }
    },

    # -------------------- 5. Frequency --------------------
    "Frequency": {
        "base": "Hertz",
        "units": {
            "Hertz": 1,
            "Kilohertz": 1_000,
            "Megahertz": 1_000_000,
            "Gigahertz": 1_000_000_000
        }
    },

    # -------------------- 6. Fuel Economy --------------------
    "Fuel Economy": {
        "base": "Kilometers per Liter",
        "units": {
            "Kilometers per Liter": 1,
            "Miles per Gallon (US)": 2.35214583
            # "Liters per 100 km": (not a direct scalar, needs reciprocal formula)
        }
    },

    # -------------------- 7. Length --------------------
    "Length": {
        "base": "Meter",
        "units": {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Mile": 1609.34,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254
        }
    },

    # -------------------- 8. Mass --------------------
    "Mass": {
        "base": "Kilogram",
        "units": {
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 1e-6,
            "Metric Ton": 1000,
            "Pound": 0.453592,
            "Ounce": 0.0283495
        }
    },

    # -------------------- 9. Plane Angle --------------------
    "Plane Angle": {
        "base": "Radian",
        "units": {
            "Radian": 1,
            "Degree": 57.295779513,      # 1 rad ≈ 57.2958°
            "Gradian": 63.6619772368,   # 1 rad ≈ 63.662 grad
            "Revolution": 0.159154943   # 1 rad ≈ 1/(2π) revolutions
        }
    },

    # -------------------- 10. Pressure --------------------
    "Pressure": {
        "base": "Pascal",
        "units": {
            "Pascal": 1,
            "Kilopascal": 1_000,
            "Bar": 100_000,
            "Atmosphere": 101_325,
            "PSI": 6_894.76,
            "Torr": 133.322
        }
    },

    # -------------------- 11. Speed --------------------
    "Speed": {
        "base": "Meter per second",
        "units": {
            "Meter per second": 1,
            "Kilometer per hour": 3.6,      # 1 m/s = 3.6 km/h
            "Mile per hour": 2.236936,     # 1 m/s ≈ 2.236936 mph
            "Knot": 1.943844,              # 1 m/s ≈ 1.943844 knots
            "Foot per second": 3.28084     # 1 m/s ≈ 3.28084 ft/s
        }
    },

    # -------------------- 12. Temperature --------------------
    "Temperature": {
        "base": "Kelvin",
        "units": {
            "Celsius": "C",
            "Fahrenheit": "F",
            "Kelvin": "K"
        }
    },

    # -------------------- 13. Time --------------------
    "Time": {
        "base": "Second",
        "units": {
            "Second": 1,
            "Millisecond": 0.001,
            "Microsecond": 1e-6,
            "Minute": 60,
            "Hour": 3600,
            "Day": 86400,
            "Week": 604800
        }
    },

    # -------------------- 14. Volume --------------------
    "Volume": {
        "base": "Liter",
        "units": {
            "Liter": 1,
            "Milliliter": 0.001,
            "Cubic meter": 1000,           # 1 m³ = 1000 L
            "Gallon (US)": 3.785411784,    # 1 US gal ≈ 3.7854 L
            "Gallon (Imperial)": 4.54609,  # 1 Imp gal ≈ 4.54609 L
            "Cubic foot": 28.3168          # 1 ft³ ≈ 28.3168 L
        }
    }
}

# Conversion Functions
def convert_temperature(value, from_unit, to_unit):
    conversions = {
        ('Celsius', 'Fahrenheit'): lambda x: (x * 9/5) + 32,
        ('Fahrenheit', 'Celsius'): lambda x: (x - 32) * 5/9,
        ('Celsius', 'Kelvin'): lambda x: x + 273.15,
        ('Kelvin', 'Celsius'): lambda x: x - 273.15,
        ('Fahrenheit', 'Kelvin'): lambda x: (x - 32) * 5/9 + 273.15,
        ('Kelvin', 'Fahrenheit'): lambda x: (x - 273.15) * 9/5 + 32
    }
    return conversions[(from_unit, to_unit)](value)

def convert_value(value, from_unit, to_unit, category):
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    base_value = value * conversion_units[category]["units"][from_unit]
    converted_value = base_value / conversion_units[category]["units"][to_unit]
    return converted_value

# App Header
st.title("📚 Advanced Multi-Unit Converter")

# Main Conversion Interface
category = st.selectbox("Select Category", list(conversion_units.keys()))

if category in conversion_units:
    units = list(conversion_units[category]["units"].keys())
    col1, col2, col3 = st.columns(3)
    
    with col1:
        value = st.number_input("Enter Value", min_value=0.0, step=0.1)
    with col2:
        from_unit = st.selectbox("From", units)
    with col3:
        to_unit = st.selectbox("To", units)

    # Voice Input
    audio_bytes = audio_recorder()
    if audio_bytes:
        try:
            # Process audio input here
            pass
        except Exception as e:
            st.error("Error processing audio input")

    # Conversion and Results
    if value:
        try:
            result = convert_value(value, from_unit, to_unit, category)
            st.success(f"**Result:** {value} {from_unit} = {result:.4f} {to_unit}")
            
            # Add to history
            st.session_state.history.append({
                'category': category,
                'input': f"{value} {from_unit}",
                'output': f"{result:.4f} {to_unit}",
                'time': time.strftime("%H:%M:%S")
            })            
            
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")

# History Management Functions
def clear_all_history():
    st.session_state.history = []

# Conversion History Section
history_col1, history_col2 = st.columns([3, 1])

with history_col1:
    st.subheader("📜 Conversion History")

with history_col2:
    if st.button("🗑️ Clear All History", help="Delete all conversion history"):
        clear_all_history()

# Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display History
if not st.session_state.history:
    st.info("No conversion history available")
else:
    for index, entry in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"{entry['time']} - {entry['category']}", expanded=False):
            # Display input and output
            st.write(f"**Input:** {entry['input']}")
            st.write(f"**Output:** {entry['output']}")

# Documentation & Info
with st.sidebar:
    st.header("📘 Documentation")
    st.markdown("""
        **Features:**
        - 14 conversion categories
        - Real-time results
        - Conversion history
        - Voice input
        - Interactive graphs
        
        **Usage:**
        1. Select category
        2. Enter value
        3. Select units
        4. View results
    """)
    
    st.header("ℹ️ Unit Information")
    if category in conversion_units:
        selected_unit = st.selectbox("Select Unit", conversion_units[category]["units"].keys())
        st.caption(f"Base unit: {conversion_units[category]['base']}")
        if category != "Temperature":
            base_value = conversion_units[category]["units"][selected_unit]
            st.write(f"1 {selected_unit} = {base_value} {conversion_units[category]['base']}")

# Footer
st.markdown("""
---
*Created with **Streamlit** ❤️ by **Syed Uns Haider Zaidi***
""")
