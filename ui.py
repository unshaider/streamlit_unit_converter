import streamlit as st
import time

st.set_page_config(page_title="Advanced Multi-Unit Converter", layout="wide", page_icon="📐")

# Custom CSS for styling
st.markdown("""
<style>    
    .conversion-card {
        background: var(--card-background);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .history-entry {
        background: var(--card-background);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stNumberInput>div>div>input {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    .st-bm {
        background-color: var(--card-background) !important;
    }
</style>
""", unsafe_allow_html=True)


# Conversion units data structure and conversion function definitions
conversion_units = {
    "Length": {"units": {"meter": 1.0, "kilometer": 0.001, "mile": 0.000621371}},
    "Weight": {"units": {"gram": 1.0, "kilogram": 0.001, "pound": 0.00220462}},
    "Temperature": {"units": {"celsius": 1, "fahrenheit": 33.8}}  # Placeholder values for demonstration
}

def convert_value(value, from_unit, to_unit, category):
    units = conversion_units[category]["units"]
    try:
        # Simple conversion except for special cases like temperature who needs custom logic.
        if category == "Temperature":
            # Add proper temperature conversion logic here
            raise NotImplementedError("Temperature conversion not implemented")
        return value * units[from_unit] / units[to_unit]
    except KeyError:
        raise ValueError("Invalid unit selected for the chosen category")

# App Header
st.title("🔢 Advanced Multi-Unit Converter")
st.caption("Convert between 14 different measurement categories with precision and style")

# Main Conversion Interface
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        category = st.selectbox(
            "**SELECT CATEGORY**",
            list(conversion_units.keys()),
            help="Choose the type of measurement you want to convert"
        )
    
    units = list(conversion_units[category]["units"].keys())
    
    with st.form("conversion_form"):
        conv_col1, conv_col2, conv_col3, conv_col4 = st.columns([2, 2, 2, 1])
        with conv_col1:
            value = st.number_input(
                "**INPUT VALUE**",
                min_value=0.0,
                step=0.1,
                format="%.4f"
            )
        with conv_col2:
            from_unit = st.selectbox("**FROM**", units)
        with conv_col3:
            to_unit = st.selectbox("**TO**", units)
        with conv_col4:
            st.write("")  # Spacer
            convert_btn = st.form_submit_button("🔄 Convert", use_container_width=True)

# Conversion Result Display
if convert_btn and value:
    try:
        with st.spinner("Converting..."):
            time.sleep(0.3)  # Simulate processing time
            result = convert_value(value, from_unit, to_unit, category)
            
            with st.container():
                st.markdown(f"""
                <div class="conversion-card">
                    <div style="font-size: 1.2rem; color: #64748b; margin-bottom: 0.5rem;">
                        {category} Conversion
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--primary);">
                        {value:.2f} {from_unit} = 
                        <span style="color: var(--secondary);">{result:.4f}</span> {to_unit}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Add to history
            st.session_state.history.append({
                'category': category,
                'input': f"{value} {from_unit}",
                'output': f"{result:.4f} {to_unit}",
                'time': time.strftime("%H:%M:%S")
            })
            
    except Exception as e:
        st.error(f"🚨 Conversion error: {str(e)}")

# Conversion History Section
st.subheader("📖 Conversion History", anchor="history")
if "history" not in st.session_state:
    st.session_state.history = []

if not st.session_state.history:
    st.info("🌱 No conversion history available. Perform your first conversion to see results here.")
else:
    with st.container():
        for index, entry in enumerate(reversed(st.session_state.history[-5:])):
            st.markdown(f"""
            <div class="history-entry">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 600; color: var(--primary);">{entry['category']}</span>
                        <span style="color: #64748b; font-size: 0.9rem;">{entry['time']}</span>
                    </div>
                    <span style="font-size: 0.9rem; color: #64748b;">#{len(st.session_state.history)-index}</span>
                </div>
                <div style="margin: 0.5rem 0; font-size: 1.1rem;">
                    ➡️ {entry['input']} <br>
                    ✅ {entry['output']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("🧹 Clear All History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 2rem;">
    Developed with ❤️ by <strong>Syed Uns Haider Zaidi</strong><br>
    <div style="margin-top: 0.5rem;">
        <a href="#" style="color: var(--primary); text-decoration: none; margin: 0 0.5rem;">Documentation</a> •
        <a href="#" style="color: var(--primary); text-decoration: none; margin: 0 0.5rem;">GitHub</a> •
        <a href="#" style="color: var(--primary); text-decoration: none; margin: 0 0.5rem;">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)