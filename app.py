import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

# --- PAGE SETUP ---
# I'm using layout="wide" because the dashboard has a lot of columns
st.set_page_config(page_title="NexGen Logistics Tool", page_icon="📦", layout="wide")

# --- STUDENT SIDEBAR ---
with st.sidebar:
    # Truck icon for logistics theme
    st.image("https://cdn-icons-png.flaticon.com/512/759/759163.png", width=80)
    st.markdown("### Developed By")
    st.markdown("**Name:** SURABHI SINGH")
    st.markdown("**ID:** 22BCE10724") 
    st.info("Status: Prototype Build v1.0")

# --- STEP 1: LOAD DATA ---
@st.cache_data
def load_all_data():
    """
    Reading all the generated CSVs from Step 1.
    I'm merging them here so I don't have to do it repeatedly later.
    """
    try:
        orders_df = pd.read_csv('data/orders.csv')
        fleet_df = pd.read_csv('data/vehicle_fleet.csv')
        feedback_df = pd.read_csv('data/customer_feedback.csv')
        # costs_df isn't strictly needed for the main view, but good to have
        costs_df = pd.read_csv('data/cost_breakdown.csv')
    except:
        st.error("Error: CSV files missing. Did you run data_generator.py?")
        return None, None

    # --- NLP SENTIMENT ANALYSIS ---
    # I used TextBlob here because it gives a simple polarity score (-1 to 1).
    # This helps me turn text comments into a number for the algorithm.
    feedback_df['Sentiment'] = feedback_df['Feedback_Text'].astype(str).apply(
        lambda x: TextBlob(x).sentiment.polarity
    )
    
    # Calculate average sentiment per customer
    cust_scores = feedback_df.groupby('Customer_ID')['Sentiment'].mean().reset_index()
    
    # Merge sentiment back into the main orders table
    # Using left join so we keep orders even if the customer has no feedback yet
    merged_df = pd.merge(orders_df, cust_scores, on='Customer_ID', how='left')
    
    # Fill NaNs with 0 (Neutral) for new customers
    merged_df['Sentiment'] = merged_df['Sentiment'].fillna(0)
    
    return merged_df, fleet_df

# Run the loader
main_df, fleet_df = load_all_data()

# --- STEP 2: THE ALGORITHM ---
def calculate_best_route(order_details, user_priorities):
    """
    This is my custom logic to decide the best vehicle.
    It takes the user's slider inputs (weights) and ranks the options.
    """
    # Assuming a standard distance for this simulation
    dist = 150 
    
    # These are the 3 modes available in the fleet
    possibilities = [
        {"Mode": "Standard Truck", "Cost": 50, "Hours": 2.5, "Emission": 250},
        {"Mode": "Express Bike",   "Cost": 80, "Hours": 1.2, "Emission": 40},
        {"Mode": "Electric Van",   "Cost": 60, "Hours": 3.0, "Emission": 0}
    ]
    
    ranked_list = []
    
    for p in possibilities:
        # Calculate a weighted score (Lower score = Better match)
        # I multiply Time by 20 to bring it to the same scale as Cost
        score = (p['Cost'] * user_priorities['cost']) + \
                (p['Hours'] * 20 * user_priorities['speed']) + \
                (p['Emission'] * 0.1 * user_priorities['green'])
        
        # --- CHURN PROTECTION LOGIC ---
        # If the customer is angry (Sentiment < -0.1), we MUST NOT be slow.
        # So I add a huge penalty to any slow option (> 2 hours).
        if order_details['Sentiment'] < -0.1 and p['Hours'] > 2.0:
            score += 500 # This effectively forces the algorithm to choose the fast bike
            p['Note'] = "Risk: Customer is angry"
        else:
            p['Note'] = "OK"
            
        p['Final_Score'] = score
        ranked_list.append(p)
    
    # Sort the list so the lowest score (best option) is at the top
    return pd.DataFrame(ranked_list).sort_values('Final_Score')

# --- STEP 3: THE DASHBOARD UI ---

st.title("🚛 NexGen Smart-Switch Engine")
st.markdown("### From Reactive to Prescriptive Logistics")
st.markdown("This tool helps us decide **how** to ship an order by balancing Cost, Speed, and Carbon Footprint.")

st.divider()

# Top KPI Row
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Pending Orders", len(main_df))
kpi2.metric("Avg Sentiment Score", f"{main_df['Sentiment'].mean():.2f}")
kpi3.metric("Fleet Available", len(fleet_df))

st.markdown("---")

# Main Working Area
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("1. Control Panel")
    st.write("Adjust these based on current business goals:")
    
    # Sliders
    p_cost = st.slider("Priority: Save Cost", 0.0, 1.0, 0.5)
    p_speed = st.slider("Priority: Fast Delivery", 0.0, 1.0, 0.5)
    p_green = st.slider("Priority: Sustainability", 0.0, 1.0, 0.5)
    
    st.write("---")
    st.subheader("2. Pick an Order")
    # Dropdown
    my_order_id = st.selectbox("Select Order ID:", main_df['Order_ID'].head(10))
    
    # Get the specific row for this order
    curr_order = main_df[main_df['Order_ID'] == my_order_id].iloc[0]
    
    # Show basic info
    st.info(f"Customer: {curr_order['Customer_ID']}\n\nValue: ${curr_order['Order_Value_USD']}")

    # Sentiment Warning
    s_score = curr_order['Sentiment']
    if s_score < -0.1:
        st.error(f"⚠️ High Churn Risk! (Score: {s_score:.2f})")
    else:
        st.success(f"✅ Customer Happy (Score: {s_score:.2f})")

with right_col:
    st.subheader("3. AI Recommendation")
    
    # Run the custom function
    my_weights = {'cost': p_cost, 'speed': p_speed, 'green': p_green}
    result_table = calculate_best_route(curr_order, my_weights)
    
    # Pick the winner (first row)
    winner = result_table.iloc[0]
    
    # Dynamic Color based on choice
    if "Electric" in winner['Mode']:
        color = "green"
    elif "Express" in winner['Mode']:
        color = "orange"
    else:
        color = "blue"
        
    st.markdown(f":{color}[**Recommended Mode:**] **{winner['Mode']}**")
    st.markdown(f"Reasoning: Best balance for your selected priorities.")
    
    # Show the data table
    st.dataframe(result_table[['Mode', 'Cost', 'Hours', 'Emission', 'Note']], use_container_width=True)

# Chart Section
st.markdown("---")
st.subheader("Customer Risk Analysis")
st.caption("Visualizing high-value orders vs. customer sentiment.")

# Scatter plot
fig = px.scatter(
    main_df, 
    x="Order_Value_USD", 
    y="Sentiment", 
    color="Priority",
    size="Order_Value_USD",
    title="Value vs Sentiment Matrix"
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center'>Created by <b>SURABHI SINGH - 22BCE10724</b></div>", unsafe_allow_html=True)