# PhonePe-Pulse-Project

# PhonePe Pulse: Transaction & User Insights (2018-2024) 

## 📌 Project Overview
This project is an end-to-end Data Engineering and Analysis solution. It extracts data from the PhonePe Pulse GitHub repository, processes it using **Python**, stores it in a **PostgreSQL** database, and visualizes the results through an interactive **Streamlit** dashboard.

## 🛠️ Skills & Technologies
- **Data Extraction:** Scripted JSON parsing from nested GitHub directories.
- **SQL Proficiency:** Designed a relational schema to store Aggregated, Map, and Top data.
- **Data Visualization:** Built interactive charts using **Plotly** and **Streamlit**.

## 📊 Strategic Business Insights
Based on the data analysis, here are the key findings:
1. **Regional Growth:** Southern states like **Karnataka and Telangana** contribute the highest transaction volumes, while Northern states show the fastest *growth rate* in new user registrations.
2. **Payment Trends:** Peer-to-Peer (P2P) transfers are the most common, but **Merchant Payments** show a significant increase during Q3 and Q4 (Festive Season).
3. **App Engagement:** Districts with high app-opening counts but low transaction values are identified as "High Potential" areas for marketing campaigns.

## 🚀 How to Run the Project
1. **Clone the Repo:** "https://github.com/PhonePe/pulse.git"
2. **Install Dependencies:** pip install -r requirements
3. **Run ETL:** Execute the Python script to migrate data to the SQL database.
4. **Launch Dashboard:** "streamlit run app.py"

## 📁 Deliverables
- 'extraction.ipynb': Data extraction and SQL migration logic.
- 'app.py': Streamlit dashboard code.
- 'requirements.txt`: Python dependencies.
