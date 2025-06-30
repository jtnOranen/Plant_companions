import streamlit as st
import json
from main import normalize_plant_name, optimize_layout
from visualise import plot_grid

# === Load data ===
with open("companion_plants_full.json", "r", encoding="utf-8") as f:
    companion_data = json.load(f)

st.title("🌱 Plant Companion Optimizer")

# Give 1/3 width to config, 2/3 to grid
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("Configuration")
    rows = st.number_input("Number of rows", min_value=1, max_value=10, value=3)
    cols = st.number_input("Number of columns", min_value=1, max_value=10, value=3)
    total_cells = rows * cols

    st.subheader("Enter your plants")
    plant_inputs = []
    for i in range(total_cells):
        plant = st.text_input(f"Plant #{i+1}", "", key=f"plant_{i}")
        if plant:
            normalized = normalize_plant_name(plant)
            if normalized not in companion_data:
                st.warning(f"{normalized} not in database, given neutral values.")
            plant_inputs.append(normalized)

    while len(plant_inputs) < total_cells:
        plant_inputs.append(None)

    run_optimization = st.button("Optimize Layout")

with right_col:
    st.header("Resulting Grid")
    if 'run_optimization' not in st.session_state:
        st.session_state.run_optimization = False

    if run_optimization:
        st.session_state.run_optimization = True

    if st.session_state.run_optimization:
        best_grid, best_score = optimize_layout(plant_inputs, companion_data, rows, cols)
        st.success(f"✅ Best total score: {best_score}")
        fig = plot_grid(best_grid, rows, cols, best_score, show=False)
        st.pyplot(fig)
