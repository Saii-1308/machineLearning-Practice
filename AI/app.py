import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ------------------------------
# Initialization
# ------------------------------
if "traffic_data" not in st.session_state:
    st.session_state.traffic_data = {
        "North": {"vehicles": 10, "wait_time": 0},
        "South": {"vehicles": 15, "wait_time": 0},
        "East": {"vehicles": 7, "wait_time": 0},
        "West": {"vehicles": 12, "wait_time": 0}
    }
    st.session_state.current_green = None
    st.session_state.history = []

# ------------------------------
# Utility Functions
# ------------------------------
def greedy_decision(strategy="vehicle_count"):
    """Greedy selection of next direction"""
    if strategy == "vehicle_count":
        # Choose lane with maximum vehicles
        return max(st.session_state.traffic_data, key=lambda d: st.session_state.traffic_data[d]["vehicles"])
    elif strategy == "wait_time":
        # Choose lane with longest wait
        return max(st.session_state.traffic_data, key=lambda d: st.session_state.traffic_data[d]["wait_time"])

def update_traffic(green_light, green_duration=5):
    """Simulate traffic update after giving green signal"""
    for direction, data in st.session_state.traffic_data.items():
        if direction == green_light:
            # Vehicles cleared while green
            cleared = min(data["vehicles"], green_duration * 2)  # Assume 2 vehicles/sec cleared
            data["vehicles"] -= cleared
            data["wait_time"] = 0
        else:
            # Increase wait time for other directions
            data["wait_time"] += green_duration
            # Randomly increase vehicles arriving
            data["vehicles"] += np.random.randint(0, 5)

def log_history(green_light, step):
    """Save step data for analytics"""
    snapshot = {d: st.session_state.traffic_data[d]["vehicles"] for d in st.session_state.traffic_data}
    st.session_state.history.append({
        "step": step,
        "green_light": green_light,
        **snapshot
    })

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🚦 Dynamic Traffic Light Optimization (Greedy Algorithm)")
st.markdown("""
This app simulates **real-time traffic optimization** using a **greedy approach**.  
The algorithm dynamically selects the next green light based on either:
- **Vehicle Count** *(default)*, or  
- **Longest Waiting Time*
""")

strategy = st.radio("Optimization Strategy:", ["vehicle_count", "wait_time"], format_func=lambda x: "Vehicle Count" if x=="vehicle_count" else "Longest Wait Time")

simulation_steps = st.slider("Simulation Steps", 1, 50, 20)
green_duration = st.slider("Green Light Duration (sec)", 2, 10, 5)

st.divider()
st.subheader("Traffic Simulation")

start_button = st.button("Run Simulation")

if start_button:
    st.session_state.history = []  # reset history

    progress = st.progress(0)
    status_text = st.empty()

    for step in range(simulation_steps):
        # 1. Choose next green signal
        green_light = greedy_decision(strategy)

        # 2. Update traffic
        update_traffic(green_light, green_duration)

        # 3. Log data
        log_history(green_light, step + 1)
        st.session_state.current_green = green_light

        # 4. Visualization update
        df = pd.DataFrame([
            {"Direction": d, "Vehicles": st.session_state.traffic_data[d]["vehicles"], "Wait Time": st.session_state.traffic_data[d]["wait_time"]}
            for d in st.session_state.traffic_data
        ])

        fig = px.bar(df, x="Direction", y="Vehicles", color="Direction", title="Real-Time Vehicle Count")
        status_text.text(f"Step {step + 1}: Green Light → {green_light}")
        st.plotly_chart(fig, use_container_width=True)

        progress.progress((step + 1) / simulation_steps)
        time.sleep(0.5)  # simulate real-time delay

    st.success("Simulation completed! 🎉")

# ------------------------------
# Analytics & History
# ------------------------------
if st.session_state.history:
    st.subheader("Simulation Analytics")

    history_df = pd.DataFrame(st.session_state.history)
    st.write(history_df)

    # Line graph for each direction
    fig2 = px.line(history_df, x="step", y=["North", "South", "East", "West"],
                   title="Vehicle Count Over Time", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Summary
    total_vehicles_cleared = sum([h[st.session_state.current_green] for h in st.session_state.history])
    st.metric("Total Steps", len(history_df))
    st.metric("Final Congestion", sum(history_df.iloc[-1][["North","South","East","West"]]))
