import streamlit as st
import sys
import os

# Add src to path
sys.path.append('src')

# Import and run dashboard
try:
    from dashboard_fixed import main
    main()
except ImportError as e:
    st.error(f"Error importing dashboard: {e}")
    st.error("Please check if dashboard_fixed.py exists in src/ directory")
    st.stop()
except Exception as e:
    st.error(f"Error running dashboard: {e}")
    st.stop()