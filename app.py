import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

#1.Title
st.title("PhonePe Pulse Data Analysis")

# 2. Sidebar Navigation 
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to:", ["Home", "Analysis"])

engine = create_engine('postgresql+psycopg2://myfile_b4pj_user:RxzB7LFmv8FVCLhAdmEBBZJeEhHWXhWi@dpg-d5vngiffte5s73ctc9cg-a.singapore-postgres.render.com/myfile_b4pj')

if page == "Home":
    st.subheader(" PhonePe Pulse: India's Digital Payment Overview")
    st.write("Use the sidebar to navigate to the Analysis section.")
   
    state_mapping = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh': 'Andhra Pradesh','arunachal-pradesh': 'Arunachal Pradesh','assam': 'Assam',
        'bihar': 'Bihar','chandigarh': 'Chandigarh','chhattisgarh': 'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu': 'Dadara & Nagar Havelli','delhi': 'NCT of Delhi',
        'goa': 'Goa','gujarat': 'Gujarat','haryana': 'Haryana','himachal-pradesh': 'Himachal Pradesh','jammu-&-kashmir': 'Jammu & Kashmir','jharkhand': 'Jharkhand','karnataka': 'Karnataka',
        'kerala': 'Kerala','ladakh': 'Ladakh','lakshadweep': 'Lakshadweep','madhya-pradesh': 'Madhya Pradesh','maharashtra': 'Maharashtra','manipur': 'Manipur','meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram','nagaland': 'Nagaland','odisha': 'Odisha','puducherry': 'Puducherry','punjab': 'Punjab','rajasthan': 'Rajasthan','sikkim': 'Sikkim','tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana','tripura': 'Tripura','uttar-pradesh': 'Uttar Pradesh','uttarakhand': 'Uttarakhand','west-bengal': 'West Bengal'
    }

    # 2. Year Selector (Specific to Home Page Map)
    map_year = st.selectbox("Select Year to Visualize Map:", [2018, 2019, 2020, 2021, 2022, 2023, 2024], key="home_year")
    # SQL query for the map
    query_map = f'SELECT "State", SUM("Transaction_amount") as total FROM aggregated_transaction WHERE "Year" = \'{map_year}\' GROUP BY "State"'
    df_map = pd.read_sql(query_map, engine)
    df_map['GeoState'] = df_map['State'].map(state_mapping)
   
    # The Plotting Code
    fig = px.choropleth(
        df_map,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='GeoState',
        color='total',
        hover_name='GeoState', # Shows the clean state name on hover
        hover_data={'total': True, 'GeoState': False}, # Shows the amount
        color_continuous_scale='Reds',
    )

    # Focus the map on India
    fig.update_geos(fitbounds="locations", visible=False)
    
    # Adjust layout margins to make the map bigger
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.write("----")
    st.write("### About the project")
    st.write("This dashboard privides a visual journey through the growth of digital payments in India. Navigate to the **Analysis** page to explore specific business case studies and regional trends.")

elif page == "Analysis":
    st.header(" Business Insights & Case Studies")
    #filters
    col1, col2 = st.columns(2)
    with col1:
        states_df = pd.read_sql('SELECT DISTINCT "State" FROM aggregated_transaction ORDER BY "State" ASC', engine)
        selected_state = st.selectbox("Select State:", states_df['State'])
    with col2:
        selected_year = st.selectbox("Select Year:", [2018, 2019, 2020, 2021, 2022, 2023, 2024])

    st.markdown(f" {selected_state.title()} Overview in {selected_year}")
    
    # Create three columns for the metrics
    m1, m2, m3 = st.columns(3)

    # 1. Total Transaction Amount
    query_amt = f'SELECT SUM("Transaction_amount") FROM aggregated_transaction WHERE "State" = \'{selected_state}\' AND "Year" = \'{selected_year}\''
    total_amt = pd.read_sql(query_amt, engine).iloc[0,0]
    
    # 2. Total Registered Users
    query_user = f'SELECT SUM("Registered_Users") FROM map_user WHERE "State" = \'{selected_state}\' AND "Year" = \'{selected_year}\''
    total_user = pd.read_sql(query_user, engine).iloc[0,0]

    # 3. Total App Opens
    query_opens = f'SELECT SUM("App_Opens") FROM map_user WHERE "State" = \'{selected_state}\' AND "Year" = \'{selected_year}\''
    total_opens = pd.read_sql(query_opens, engine).iloc[0,0]

    # Display Metrics with Formatting
    with m1:
        # Formats to Cr (Crores) for Indian context
        st.metric("Total Transaction Value", f"₹{total_amt/10000000:.2f} Cr")
    with m2:
        st.metric("Registered Users", f"{total_user/1000000:.2f} M")
    with m3:
        st.metric("Total App Opens", f"{total_opens/1000000:.2f} M")

    
    st.divider() # Separation line before Scenarios start
    
    scenario = st.selectbox("Choose a Scenario:", [
        "1. Decoding Transaction Dynamics",
        "2. Device Dominance and User Engagement",
        "3. Insurance Engagement Analysis",
        "4. User Engagement and Growth Strategy",
        "5. User Registration Analysis"
    ])
     
    if scenario == "1. Decoding Transaction Dynamics":
      q = st.selectbox("Select Question:", [
        "Top 10 states led by total transaction value (2024)",
        "20 states/UTs had the lowest total transaction volume in 2024",
        "states experienced a revenue decline or market contraction in 2024",
        "states achieved positive growth in 2024 compared to 2023",
        "breakdown of transaction types in {selected_state.title()}",
        "PhonePe's transaction volume grown across India each year"
    ])
    
    #CONNECTION TO  SQL ---
      if q == "Top 10 states led by total transaction value (2024)":
          query =f"""
          SELECT "State", SUM("Transaction_amount") AS Total_Amount 
          FROM aggregated_transaction
          WHERE "Year" = '{selected_year}'
          GROUP BY "State"
          ORDER BY Total_Amount DESC
          LIMIT 10
          """
          df = pd.read_sql(query, engine)
          st.bar_chart(df.set_index('State')) 
          st.info("""
          **:red[Analysis:]** Karnataka, Maharashtra and Telangana are the three leading states which generate more revenues to the buisness where as Tamil Nadu which also a big state comes in 10th place. 
          **:green[Infrastructure:]** In high-traffic states like Maharashtra and Karnataka, the focus must be on **backend resilience** and server capacity to ensure 100% transaction success rates during peak hours.
          **:orange[Connectivity Expansion:]** In states with lower rankings,  the priority should be **digital infrastructure growth**, including better network coverage and merchant onboarding to bridge the digital divide.
          """ )
      elif q== "20 states/UTs had the lowest total transaction volume in 2024":
          query=""" 
          select "State", sum("Transaction_amount") as Total_amount from aggregated_transaction  
          where "Year" = '2024'
          group by "State"
          order by Total_amount asc
          limit 21 
          """
          df = pd.read_sql(query, engine)
          st.dataframe(df) 
          st.info("""
          **📉 Regional Analysis:**
            1. **Lowest Footprint:** **Lakshadweep** and the **North-Eastern states** show the lowest digital payment adoption, indicating a high dependency on cash.
            2. **The Scale Disparity:** While **Chhattisgarh** is on this list, its volume is significantly higher (Trillions) compared to the smaller Union Territories like Lakshadweep (Millions).
            3. **Tourism Gap:** Major tourist destinations like **Goa** show unexpectedly low transaction volumes, suggesting that the tourism sector in these areas may still rely heavily on cash.

          **🚀 Growth Strategies:**
            1. **Financial Literacy Campaigns:** Launch "Cash-to-Digital" educational drives in the North-East to build trust in digital payments.
            2. **Tourism Integration:** In places like Goa and Andaman, PhonePe should partner with local hotels and tour operators to provide **hospitality-focused digital payment incentives**.
            3. **Infrastructure Education:** Provide training to small merchants in low-volume areas to ensure they understand the ease and safety of accepting online transactions.
         """)

      elif q=="states experienced a revenue decline or market contraction in 2024":
           query=""" 
           SELECT "State", SUM(CASE WHEN "Year" = '2023' THEN "Transaction_amount" ELSE 0 END) AS Amt_2023,SUM(CASE WHEN "Year" = '2024' THEN "Transaction_amount" ELSE 0 END) AS Amt_2024
           FROM aggregated_transaction
           WHERE "Year" IN ('2023', '2024')
           GROUP BY "State"
           HAVING SUM(CASE WHEN "Year" = '2024' THEN "Transaction_amount" ELSE 0 END) < SUM(CASE WHEN "Year" = '2023' THEN "Transaction_amount" ELSE 0 END);
           """
           df = pd.read_sql(query, engine)
           st.dataframe(df) 

           st.info("""
           **📈 Market Observation: Consistent Growth**
           The data confirms that **no state experienced a revenue decline** in 2024 compared to 2023. Digital payment adoption continues to follow a strong upward trajectory across all regions.

           **💡 Insight: Positive Momentum**
           This trend indicates that digital payments have become a permanent habit across India. Even in states where the growth curve has flattened, the business volume remains **stable and robust**.

           **🚀 Strategic Recommendations:**
           1. **Localized Growth Campaigns:** Since there is no contraction, the focus should shift to **Expansion**. Launch hyper-local campaigns in districts with relatively lower business volumes to convert the remaining cash-dependent users.
           2. **Transaction Value Optimization:** In states with high but stable volumes, focus on increasing the **Average Transaction Value (ATV)** by promoting high-ticket services like insurance and mutual fund investments.
           3. **Service Diversification:** Use this stable period to integrate more "Strategic Hooks," such as credit offerings or merchant-specific loyalty programs, to ensure long-term customer retention.
           """)

      elif q=="states achieved positive growth in 2024 compared to 2023":
           query=""" 
           SELECT "State", SUM(CASE WHEN "Year" = '2023' THEN "Transaction_amount" ELSE 0 END) AS Amt_2023,SUM(CASE WHEN "Year" = '2024' THEN "Transaction_amount" ELSE 0 END) AS Amt_2024
           FROM aggregated_transaction
           WHERE "Year" IN ('2023', '2024')
           GROUP BY "State"
           HAVING SUM(CASE WHEN "Year" = '2024' THEN "Transaction_amount" ELSE 0 END) > SUM(CASE WHEN "Year" = '2023' THEN "Transaction_amount" ELSE 0 END);
           """ 
           df = pd.read_sql(query, engine)

           if not df.empty:
              # Convert raw amounts to Crores for better readability
              df['2023 (₹ Crores)'] = df['amt_2023'] / 10000000
              df['2024 (₹ Crores)'] = df['amt_2024'] / 10000000

              # Create the chart using the new 'Crore' columns
              fig = px.bar(
                 df, 
                 x="State", 
                 y=["2023 (₹ Crores)", "2024 (₹ Crores)"],
                 barmode="group",
                 title="State-wise Transaction Growth (2023 vs 2024)",
                 labels={"value": "Transaction Value in ₹ Crores", "variable": "Year"},
                 color_discrete_map={"2023 (₹ Crores)": "red", "2024 (₹ Crores)": "green"},
                 text_auto='.2s' # This adds the values on top of the bars automatically!
              )
        
              # Update layout to make the state names easier to read
              fig.update_layout(xaxis_tickangle=-45)
        
              st.plotly_chart(fig, use_container_width=True)
           
              # Display the success message and analysis     
              st.success("""
              **📈 Market Analysis: Remarkable Positive Growth**
              The data shows a **steady and robust increase** in business volume across India from 2023 to 2024. This consistent growth is a powerful indicator of a thriving digital economy.

              **💡 Insight: Digital Literacy & Economic Progress**
              This trend proves that Indian citizens are rapidly becoming digitally literate, embracing online payments as a daily habit. This shift represents a significant milestone in our country's **Economical Growth** and financial inclusion.

              **🚀 Strategic Recommendations:**
              1. **Encourage Digital Habits:** While growth is high, we must continue to incentivize digital transactions through cashback and loyalty programs to reach the final 10% of cash-dependent users.
              2. **Infrastructure Augmentation:** To sustain this momentum, there is an urgent need to **install more network towers** in hilly terrains and remote regions (like the North-East and Himalayan states) where connectivity currently limits growth.
              3. **Rural Awareness:** Continue providing education and awareness programs in rural areas to ensure every citizen can participate safely in the digital economy.
              """)
           
      elif q=="breakdown of transaction types in {selected_state.title()}"	:
           query=f""" 
           SELECT "Transaction_type", sum("Transaction_amount") as total_value
           FROM aggregated_transaction
           WHERE "State" in ('{selected_state}')
           GROUP BY "Transaction_type"
           ORDER BY total_value Desc; 
           """     
           df = pd.read_sql(query, engine)
           import plotly.express as px
           fig=px.pie(df,values='total_value',names='Transaction_type',title='Assam & Meghalaya Payment Breakdown')
           st.plotly_chart(fig) 
           st.info("""
           **📊 Analysis: P2P Dominance in the North-East**
           The data shows that **Peer-to-Peer (P2P) payments** are the overwhelming leader in Assam and Meghalaya, contributing significantly more than all other categories combined.

           **💡 Insight: Social vs. Commercial Usage**
           While the high P2P volume (₹2.82 Trillion) proves that users trust the platform for transferring money, the lower **Merchant Payments** (₹685 Billion) suggest that many local shops and markets in these states may still prefer cash.
 
           **🚀 Strategic Recommendations:**
           1. **Merchant Onboarding:** PhonePe should launch a massive "QR Code Distribution" drive in local markets and small towns across Assam and Meghalaya to convert P2P users into retail shoppers.
           2. **Bill Payment Awareness:** Since 'Recharge & Bill Payments' are relatively low, targeted notifications for electricity and water bill payments could increase usage in this high-frequency category.
           3. **Micro-Insurance/Finance:** Financial Services are currently at the bottom. This presents a 'Blue Ocean' opportunity to introduce low-cost micro-insurance or digital gold products specifically tailored for the North-Eastern demographic.
           """)

      elif q=="PhonePe's transaction volume grown across India each year":  
           query=""" 
           SELECT "Year", SUM("Transaction_count") AS Yearly_Count
           FROM aggregated_transaction
           GROUP BY "Year"
           ORDER BY "Year" ASC;
           """  
           df = pd.read_sql(query, engine)
           st.dataframe(df)   
           st.line_chart(df.set_index('Year'))

           st.success("""
           **🚀 Analysis: Exponential Business Scaling**
           **Hyper-Growth:** Transaction volume has skyrocketed from **108 Crore (1.08 Billion) in 2018** to over **9,930 Crore (99.3 Billion) in 2024**.
           **The Growth Factor:** This represents a massive **92x growth** in transaction count within just seven years.

           **💡 Insight: Mass Market Adoption**
           The consistent upward curve proves that PhonePe has reached every corner of India, handling nearly **10,000 Crore transactions annually** by the end of 2024.

           **🚀 Strategic Recommendations:**
           1. **Infrastructure Resilience:** With volume approaching **10,000 Crore transactions**, PhonePe must prioritize server uptime and backend stability to handle the massive load during peak festive seasons.
           2. **Monetisation:** Now that the platform has achieved massive scale, the focus should shift to increasing revenue per transaction by promoting **Financial Services and Insurance**.
           3. **Rural Penetration:** Continue expanding digital literacy to convert the remaining cash-based transactions into the digital ecosystem.
           """)

    elif scenario == "2. Device Dominance and User Engagement":
        q2 = st.selectbox("Select Question:", [
            "Which mobile brands are the most popular among PhonePe users across India?",
            "How many total registration records exist where zero app activity (App Opens = 0) was recorded?",
            "inactive users state wise",
            "Active users",
            "In which quarter do users engage with the app the most?"
        ])

        if q2 == "Which mobile brands are the most popular among PhonePe users across India?":
            query="""
            SELECT "Brand", sum("Registered_Users") as total_users
            FROM aggregated_user
            GROUP BY "Brand"
            ORDER BY total_users DESC
            LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.write("Top Mobile Brands by User Count")
            st.bar_chart(df.set_index('Brand'))
            st.info(f"""
            ***:red[Key Analysis & Insights:]***
            **:green[Market Leader:]** **Samsung** emerges as the leading brand among the top 10, likely due to its extensive range of devices across all price segments in the Indian market.
            **:orange[Universal Compatibility:]** Interestingly, several other top brands show a remarkably **consistent user count**, indicating that PhonePe's adoption is not restricted by the type of mobile hardware.
            **:purple[Strategic Conclusion:]** This trend demonstrates that the business is **brand-independent**. The PhonePe application is optimized effectively across all **mobile brand platforms**, ensuring a seamless experience regardless of which phone a customer chooses to buy.
            """)

        elif q2 == "How many total registration records exist where zero app activity (App Opens = 0) was recorded?":
          query="""SELECT sum("Registered_Users")
          FROM aggregated_user
          WHERE "App_Opens"=0;
          """
          
          df = pd.read_sql(query, engine)
          st.write("Records with Zero App Opens")
          st.dataframe(df)
          st.info("""
**Key Analysis & Insights:**
*   **Dormant User Base:** The records show registration without activity.
*   **Operational Insight:** This data helps in **Competitive Benchmarking**; focusing on converting these existing users is ***significantly more cost-effective*** than acquiring entirely new ones.
*   **Strategic Goal:** The main objective for the next quarter must be ***High-Volume User Activation***.
""")
        elif q2 == "inactive users state wise":
           query = """
           SELECT "State", SUM("Registered_Users") AS inactive_users
           FROM aggregated_User
           WHERE "App_Opens" = 0
           GROUP BY "State"
           ORDER BY inactive_users DESC;
           """
           df = pd.read_sql(query, engine)
           st.write("States with Lowest App Activity")
           st.bar_chart(df.set_index('State'))

        elif q2 == "Active users":
            query = """
            SELECT "State",SUM("App_Opens") AS total_opens, SUM("Registered_Users") AS total_users,
            ROUND((SUM("App_Opens")::numeric / NULLIF(SUM("Registered_Users"), 0)), 2) AS engagement_ratio
            FROM aggregated_user
            GROUP BY "State"
            ORDER BY engagement_ratio DESC
            LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.write("Top States by Active User Engagement (App Opens)")
            st.bar_chart(df.set_index('State'))

        elif q2 == "In which quarter do users engage with the app the most?":
           query = """
           SELECT "Quarter", sum("App_Opens") total_oppens
           FROM aggregated_user
           GROUP BY "Quarter"
           ORDER BY total_oppens desc;
           """     
           df = pd.read_sql(query, engine)
           st.write("Engagement Trends by Quarter")
           st.line_chart(df.set_index('Quarter'))

    elif scenario == "3. Insurance Engagement Analysis":
      q3 = st.selectbox("Select Question:", [
        "Which specific districts across India are leading in insurance adoption?",
        "Is there a specific time of year when people are more likely to buy insurance? Do we see a spike in a particular quarter?",
        "Which specific districts are the 'Growth Engines' for insurance, contributing the highest share to their state's total insurance revenue?",
        "Is the demand for insurance increasing over time?"
    ])

      if q3 == "Which specific districts across India are leading in insurance adoption?":
           query = """
           SELECT "State", "District", 
           SUM("Insurance_Count") AS Total_policies
           FROM map_insurance
           GROUP BY "State", "District"
           ORDER BY Total_policies DESC
           LIMIT 10;
           """
           df = pd.read_sql(query, engine)
           st.subheader("Top 10 Districts Leading in Insurance Adoption")
           st.bar_chart(df.set_index('District'))
           st.info("""
           ** Insurance Leaders: Simple Analysis**

           **The Huge Winner:** ***Bengaluru Urban*** is the #1 leader in all of India. It has way more insurance policies than any other district.
           **Top 3 Hubs:** After Bengaluru, the districts of ***Pune*** and ***Thane*** are the next biggest fans of buying insurance on the app.
           **State Strength:** ***Maharashtra*** and ***Telangana*** are very strong, with multiple districts appearing in the Top 10 list.
           **What this means:** People in these tech-heavy cities trust digital apps the most for their financial safety.
           """)
    
      elif q3 == "Is there a specific time of year when people are more likely to buy insurance? Do we see a spike in a particular quarter?":
           query = """
           SELECT "Quarter", sum("Insurance_Amount")as Total_value
           FROM map_insurance
           GROUP BY "Quarter"
           ORDER BY Total_value desc;
           """
           df = pd.read_sql(query, engine)
           df['Total_Value_Crores'] = df['Total_value'] / 10000000

           st.subheader("Insurance Spending by Quarter (in Crores)")
           st.bar_chart(df.set_index('Quarter')['Total_Value_Crores'])
           st.info("""
           **📅 When do people buy Insurance?**

           *   **The Big Spike:** **Quarter 4** is the clear winner with **641.54 Crores** in insurance sales.
           *   **The Ranking:** 
           1. **Q4:** 641.54 Crores (Highest)
           2. **Q3:** 487.30 Crores
           3. **Q1:** 443.44 Crores
           4. **Q2:** 429.28 Crores (Lowest)
           *   **What this means:** People tend to buy more insurance at the end of the year. This is the best time for the company to show ads and offers.
           """)
           
    
      elif q3 == "Which specific districts are the 'Growth Engines' for insurance, contributing the highest share to their state's total insurance revenue?":
           query = """
           SELECT "State", "District", 
           SUM("Insurance_Count") AS total_policies, 
           SUM("Insurance_Amount") AS total_value
           FROM map_insurance
           WHERE "Year" = '2024'
           GROUP BY "State", "District"
           ORDER BY total_value DESC
           LIMIT 10;
           """
           df = pd.read_sql(query, engine)
           st.subheader("Top Districts by Insurance Revenue (Growth Engines)")
           st.dataframe(df, use_container_width=True)
           st.bar_chart(df.set_index('District')['total_value'])
           st.info("""
           **🚀 Insurance Growth Engines: 2024 Analysis**

           *   **The Revenue King:** **Bengaluru Urban** is the primary growth engine for India, contributing a massive **58.40 Crores** in insurance revenue in 2024 alone.
           *   **The Top 3 Contributors:** 
           1. **Bengaluru Urban (Karnataka):** 58.40 Crores
           2. **Pune (Maharashtra):** 20.54 Crores
           3. **Chennai (Tamil Nadu):** 13.02 Crores
           *   **Industrial Hubs:** Districts like **Gurugram**, **Ernakulam**, and **Rangareddy** have entered the top list. This shows that insurance is booming in IT and industrial corridors.
           *   **Strategic Insight:** These 10 districts are 'Growth Engines' because they have high **Average Ticket Sizes**. People here are not just buying more policies; they are buying **higher-value** insurance.
           *   **Business Tip:** PhonePe should prioritize these specific districts for **Premium Insurance** partnerships, as the revenue potential here is the highest in the country.
           """)
    
      elif q3 == "Is the demand for insurance increasing over time?":
           query = """
           SELECT "Year", SUM("Insurance_Count") AS total_policies
           FROM map_insurance
           GROUP BY "Year"
           ORDER BY "Year" ASC;
           """
           df = pd.read_sql(query, engine)
           st.subheader("Year-on-Year Insurance Demand Growth")
           st.area_chart(df.set_index('Year')) 

    elif scenario == "4. User Engagement and Growth Strategy":
      q4 = st.selectbox("Select Question:", [
        "Which 10 districts in India have the largest base of registered PhonePe users?",
        "Which districts show a high number of registrations but a low number of app opens?",
        "In which districts are users most active, as measured by the total number of times the app is opened?",
        f"Within {selected_state.title()}, how is the user base distributed across its different districts?"
    ])

      if q4 == "Which 10 districts in India have the largest base of registered PhonePe users?":
        query = """
        SELECT "State", "District", SUM("Registered_Users") AS total_users
        FROM map_user
        GROUP BY "State", "District"
        ORDER BY total_users DESC
        LIMIT 10;
        """
        df = pd.read_sql(query, engine)
        st.subheader("Top 10 Districts by Registered Users")
        st.bar_chart(df.set_index('District')['total_users'])

      elif q4 == "Which districts show a high number of registrations but a low number of app opens?":
        query = """
        SELECT "State", "District", SUM("Registered_Users") AS total_registration, 
        SUM("App_Opens") AS total_apps_opened,
        SUM("Registered_Users") - SUM("App_Opens") AS dormant_users
        FROM map_user
        GROUP BY "State", "District"
        ORDER BY dormant_users DESC
        LIMIT 10;
        """
        df = pd.read_sql(query, engine)
        st.subheader("Districts with High Dormancy (Registrations - App Opens)")
        st.dataframe(df, use_container_width=True)

      elif q4 == "In which districts are users most active, as measured by the total number of times the app is opened?":
        query = """
        SELECT "State", "District", SUM("App_Opens") AS total_apps_opened
        FROM map_user
        GROUP BY "State", "District"
        ORDER BY total_apps_opened DESC
        LIMIT 10;
        """
        df = pd.read_sql(query, engine)
        st.subheader("Top 10 Most Active Districts (App Opens)")
        st.line_chart(df.set_index('District')['total_apps_opened'])

      elif q4 == f"Within {selected_state.title()}, how is the user base distributed across its different districts?":
        query = """
        SELECT "State", "District", SUM("Registered_Users") AS user_base
        FROM map_user
        WHERE "State" = '{selected_state}'
        GROUP BY "State", "District"
        ORDER BY user_base DESC;
        """
        df = pd.read_sql(query, engine)
        st.subheader(f"User Distribution in {selected_state.title()}")
        if not df.empty:
          st.bar_chart(df.set_index('District')['user_base'])

        else:
            st.warning(f"No data availabe for {selected_state.title()}.")  

    elif scenario == "5. User Registration Analysis":
        q5 = st.selectbox("Select Question:", [
            f"Which 10 Pincodes across India recorded the highest number of new registrations (Q4 {selected_year})?",
            "Which specific year-quarter combination saw the absolute peak in registrations?",
            f"Which districts showed a registration decrease in Q4 vs Q1 ({selected_year})?",
            f"Which 10 Pincodes contribute the least to the user base in {selected_state.title()}?"
        ])

        if q5 == f"Which 10 Pincodes across India recorded the highest number of new registrations (Q4 {selected_year})?":
            query = f"""
                SELECT "State", "Pincode", SUM("Registered_User") AS total_new_registrations
                FROM top_user_pincode
                WHERE "Year" = '{selected_year}' AND "Quarter" = 4
                GROUP BY "State", "Pincode"
                ORDER BY total_new_registrations DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.subheader(" Top 10 Pincodes for New Registrations in{selected_year}")
            st.bar_chart(df.set_index('Pincode')['total_new_registrations'])
            st.info(f"""
            **🚀 Digital Hotspots: The Top 10 Pincodes**

            **Growth Leaders:** These 10 pincodes are the **fastest-growing areas** in India. They added more new users in the last quarter than anywhere else.
            **The Winner:** Pincode ***{df.iloc[0]['Pincode']}*** in ***{df.iloc[0]['State'].title()}*** is the #1 area for new registrations.
            **Urban Demand:** Most of these pincodes belong to big cities. This shows that people in busy metro areas are heavily adopting PhonePe for their daily needs.
            **Business Tip:** PhonePe should focus its **newest features and local offers** here, as these users are the most active and ready to try digital services.
            """)

        elif q5 == "Which specific year-quarter combination saw the absolute peak in registrations?":
            query = """
                SELECT "Year", "Quarter", SUM("Registered_User") AS Total_Registrations
                FROM top_user_district
                GROUP BY "Year", "Quarter"
                ORDER BY Total_Registrations DESC
                LIMIT 1;
            """
            df = pd.read_sql(query, engine)
            st.subheader(" Historical Registration Peak")
            st.dataframe(df)
            st.info(f"""
            **🏆 The Big Win: All-Time High Registrations**

            **:yellow[When it happened:]** The biggest jump in new users occurred in **Quarter 2 of 2024**.
            **:yellow[The Big Number:]** PhonePe hit a record-breaking **{df.iloc[0]['total_registrations'] / 10000000:.1f} Crore** registrations in just three months!
            **:yellow[What this means:]** This shows that more people are joining PhonePe now than ever before. Even after many years, the app is still growing at a massive speed.
            **:yellow[Why it matters:]**This peak proves that the system is **very strong** because it handled millions of new sign-ups smoothly. It's the perfect "success story" for your project.
            """)

        elif q5 == f"Which districts showed a registration decrease in Q4 vs Q1 ({selected_year})?":
            query = f"""
                SELECT "State", "District_name", 
                SUM(CASE WHEN "Quarter" = 1 THEN "Registered_User" ELSE 0 END) AS Q1_Users,
                SUM(CASE WHEN "Quarter" = 4 THEN "Registered_User" ELSE 0 END) AS Q4_Users
                FROM top_user_district
                WHERE "Year" = '{selected_year}'
                GROUP BY "State", "District_name"
                HAVING SUM(CASE WHEN "Quarter" = 4 THEN "Registered_User" ELSE 0 END) < 
                       SUM(CASE WHEN "Quarter" = 1 THEN "Registered_User" ELSE 0 END)
                ORDER BY Q4_Users ASC;
            """
            df = pd.read_sql(query, engine)
            st.subheader(" Districts with Declining Registrations {selected_year}(Q1 vs Q4 )")
            st.dataframe(df, use_container_width=True)
            st.info(f"""
            **📉 :red[Strategic Insight:] Registration Trends and Data Anomalies ({selected_year})**

           **:yellow[Critical Data Gaps:]** Several major districts like ***Aurangabad*** and ***Gautam Buddha Nagar*** show a drop to **zero users** in Q4. This likely indicates a **Data Extraction Error** or a delay in the PhonePe Pulse data refresh for these specific regions, rather than a total loss of the user base.
           **:pink[Marginal vs. Major Declines:]**
           **:pink[Marginal:]** Districts like ***Hyderabad*** and ***Thane*** show stable retention with less than a 1% dip, which is normal user churn.
           **:pink[Major:]** ***Jaipur*** shows a significant drop (~1.8 Million users). If this isn't a data error, it suggests a massive shift to competitors or a change in how users are mapped to that district.
           **:black[Operational Risk:]** Identifying these "Decline Zones" is vital for **Fraud Detection** and **User Engagement**. A sudden drop to zero in active districts often triggers a technical audit of the data pipeline.
           **:white[Business Recommendation:]** For districts with genuine minor declines, PhonePe should launch ***Localized Retention Campaigns***. For districts showing 'Zero' users, the first step is a **Data Validation Check** to ensure the Q4 JSON files were fully processed.
           """)

        elif q5 == f"Which 10 Pincodes contribute the least to the user base in {selected_state.title()}?":
            query = f"""
                SELECT "State", "Pincode", SUM("Registered_User") AS user_base
                FROM top_user_pincode
                WHERE "State" = '{selected_state}'
                GROUP BY "State", "Pincode"
                ORDER BY user_base ASC
                LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.subheader("Pincodes with Lowest Engagement in {selected_state.title()}")
            st.bar_chart(df.set_index('Pincode')['user_base'])      
            st.info(f"""
            ***:red[Localized Market Analysis:]***
            **Lowest Engagement Hubs:** Pincode **{df.iloc[0]['Pincode']}** currently has the smallest user footprint with only **{df.iloc[0]['user_base']:,.0f}** registered users. This indicates either a low population density or a heavy reliance on cash in this specific area.
            **Identification of "Shadow Zones":** These pincodes represent 'shadow zones' where digital payment penetration is at its earliest stages. In regions like **{selected_state.title()}**, these are often industrial outskirts or newly developing residential zones.
            **Strategic Recommendation (Marketing):** Instead of broad state-wide ads, PhonePe should deploy **Hyper-Local Campaigns** (offline QR marketing, merchant tie-ups) specifically in these 10 pincodes to drive adoption.
            **Infrastructure Check:** These low numbers might also be due to poor network connectivity. A business recommendation would be to cross-reference this data with telecom signal strength to identify if the barrier is **access or awareness**.
            """)