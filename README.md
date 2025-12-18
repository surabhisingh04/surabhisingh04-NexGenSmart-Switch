# 🚛 NexGen Smart-Switch Engine

### Prescriptive Logistics Optimization Prototype

**Developer:** Surabhi Singh (22BCE10724)  
**Submission for:** OFI AI Internship Assessment – Innovation Challenge  
![Dashboard Screenshot](Screenshot%202025-12-19%20041459.png)

---

## Project Overview

For this assessment, I chose **Option 8 (Own Idea)** after identifying a gap in the given case study.  
Most logistics tools focus on **Descriptive Analytics** (what went wrong), while NexGen’s real need is **Prescriptive Analytics** (what should we do next).

The **NexGen Smart-Switch Engine** is designed to recommend the *best fulfillment strategy for each order*, rather than just reporting historical issues.

---

## Core Idea: Smart-Switch Decision Engine

The Smart-Switch engine balances three conflicting logistics objectives **at the order level**:

1. **Cost Optimization** – Reduce unnecessary operational expenses  
2. **Delivery Speed** – Protect customer satisfaction  
3. **Sustainability** – Minimize CO₂ emissions  

Instead of static rules, managers can dynamically adjust priorities and instantly see how recommendations change.

---

## Innovation Highlight: AI-Based Churn Prevention

During analysis, I observed that blindly choosing the cheapest delivery option often increases customer dissatisfaction.

To address this, I implemented a **Churn Prevention System using NLP**:

- Customer feedback text is analyzed using **TextBlob sentiment analysis**
- Each customer receives a sentiment score (−1 to +1)
- If a customer is identified as **at risk** (negative sentiment):
  - The algorithm **overrides cost-first logic**
  - Slower but cheaper delivery modes are penalized
  - Faster delivery options are prioritized to protect long-term customer value

This ensures that **short-term cost savings do not cause long-term customer churn**.

---

## 🛠️ Tech Stack & Methodology

This project was built using **Python 3.11** and the following tools:

- **Streamlit** – Interactive, manager-friendly web application  
- **Pandas & NumPy** – Data cleaning, merging, and feature engineering  
- **TextBlob** – NLP-based sentiment analysis  
- **Plotly Express** – Interactive visualizations (risk vs value analysis)  

### Data Integration
Four datasets are merged into a single decision-ready table:
- `orders.csv`
- `vehicle_fleet.csv`
- `customer_feedback.csv`
- `cost_breakdown.csv`

Missing or incomplete data is handled gracefully to reflect real-world conditions.

---

## How to Run the Project Locally

A synthetic data generator is included so the project can be run without external downloads.

### Step 1:  Clone the Repository

git clone https://github.com/surabhisingh04/surabhisingh04-NexGenSmart-Switch.git
cd surabhisingh04-NexGenSmart-Switch

### Step 2: Install Dependencies

pip install -r requirements.txt

### Step 3: Generate Sample Data

python data_generator.py

### Step 4: Launch the Application

Start the Streamlit app locally using:

python -m streamlit run app.py

