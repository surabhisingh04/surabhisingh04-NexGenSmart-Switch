# 🚛 NexGen Smart-Switch Engine

### Prescriptive Logistics Optimization Prototype

**Developer:** Surabhi Singh (22BCE10724)  
**Submission for:** OFI AI Internship Assessment - Innovation Challenge

---

## 👋 Project Overview

For this assessment, I chose **Option 8 (Own Idea)** because I noticed a gap in the case study: most logistics tools only tell you _what went wrong_ yesterday (Descriptive Analytics). I wanted to build a tool that tells managers _what to do_ tomorrow (Prescriptive Analytics).

**The Concept:**
The "Smart-Switch" is a decision engine that balances three conflicting goals for every single order:

1.  **Saving Cost** (Money)
2.  **Delivery Speed** (Customer Satisfaction)
3.  **Sustainability** (CO2 Emissions)

## 💡 My "Innovation" Feature

While analyzing the data, I realized that blindly choosing the cheapest shipping option often leads to unhappy customers.

To solve this, I built a **Churn Prevention System** using NLP:

- I used the `TextBlob` library to scan historical feedback text.
- If a customer's sentiment score is negative (e.g., they are already angry), the algorithm **automatically overrides** cost-saving rules.
- It forces a faster delivery mode to "save" the relationship, protecting long-term value over short-term savings.

## 🛠️ Tech Stack & Methodology

I built this project using Python 3.11 and the following libraries:

- **Streamlit:** For the interactive web interface (I wanted it to be user-friendly for non-tech managers).
- **Pandas & NumPy:** For merging the 4 disparate datasets (`orders`, `fleet`, `feedback`, `costs`) into a single truth table.
- **TextBlob:** Used for the Sentiment Analysis logic.
- **Plotly Express:** For the "Network Risk" scatter plot visualization.

## 🚀 How to Run This Code

I have included a `data_generator.py` script so you can replicate my exact test environment without needing external CSV downloads.

**Step 1: Clone or Download**

```bash
git clone [https://github.com/YOUR_USERNAME/NexGen-Smart-Switch.git](https://github.com/YOUR_USERNAME/NexGen-Smart-Switch.git)
cd NexGen-Smart-Switch
```
