import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Database connection
conn = sqlite3.connect("food_data.db")
cursor = conn.cursor()

# Sidebar navigation
st.sidebar.title("🍽️ Navigation")
app_mode = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📊 Data Overview",
    "🔍 Filter & Search",
    "📈 Analytics & Insights",
    "🧮 SQL Query Results",
    "🛠️ CRUD Operations",
    "ℹ️ About Creator"
])

# ---------------- HOME ----------------
if app_mode == "🏠 Home":
    st.title("Local Food Wastage Management System")
    st.image(r"c:\Users\91997\Downloads\download.jfif")
    st.subheader("Connecting surplus food providers with those in need")
    st.markdown("""
    **Project Goals:**
    - Reduce food wastage locally
    - Enable NGOs and individuals to access surplus food
    - Provide insights for food redistribution
    
    **Skills Applied:**  
    `Python` | `SQL` | `Streamlit` | `Data Analysis`

    **Domain:**  
    Food Management | Waste Reduction | Social Good
    """)

# ---------------- DATA OVERVIEW ----------------
elif app_mode == "📊 Data Overview":
    st.header("📂 Dataset Overview")
    tabs = st.tabs(["Providers", "Receivers", "Food Listings", "Claims"])   

    with tabs[0]:
        st.subheader("Providers Data")
        df1 = pd.read_sql_query("select * from providers ",conn)
        st.dataframe(df1)


    with tabs[1]:
        st.subheader("Receivers Data")    
        df2 = pd.read_sql_query("select * from receivers ",conn)
        st.dataframe(df2)
       

    with tabs[2]:
        st.subheader("Food Listings Data")
        df3 = pd.read_sql_query("select * from food_listings",conn)
        st.dataframe(df3)
        
    with tabs[3]:
        st.subheader("Claims Data")
        df4 = pd.read_sql_query("select * from claims",conn)
        st.dataframe(df4)

      
# ---------------- FILTER & SEARCH -------------
    # -------- Providers Table --------
elif app_mode == "🔍 Filter & Search":
    st.header("🔎 Filter and Search Food Listings")

    st.subheader("🏢 Providers")
    df1 = pd.read_sql_query("SELECT * FROM providers", conn)
    if not df1.empty:
        col1, col2 = st.columns(2)
        name_filter = col1.text_input("Search by Name (Providers)")
        type_filter = col2.selectbox("Provider_ID", ["All"] + sorted(df1["Provider_ID"].dropna().unique().tolist()))

        filtered_df1 = df1.copy()
        if name_filter:
            filtered_df1 = filtered_df1[filtered_df1["Name"].str.contains(name_filter, case=False, na=False)]
        if type_filter != "All":
            filtered_df1 = filtered_df1[filtered_df1["Provider_ID"] == type_filter]

        st.dataframe(filtered_df1.reset_index(drop=True))
    else:
        st.warning("No providers data found.")

    # -------- Receivers Table --------
    st.subheader("🤝 Receivers")
    df2 = pd.read_sql_query("SELECT * FROM receivers", conn)
    if not df2.empty:
        col1, col2 = st.columns(2)
        name_filter = col1.text_input("Search by Name (Receivers)")
        city_filter = col2.selectbox("City", ["All"] + sorted(df2["City"].dropna().unique().tolist()))

        filtered_df2 = df2.copy()
        if name_filter:
            filtered_df2 = filtered_df2[filtered_df2["Name"].str.contains(name_filter, case=False, na=False)]
        if city_filter != "All":
            filtered_df2 = filtered_df2[filtered_df2["City"] == city_filter]

        st.dataframe(filtered_df2.reset_index(drop=True))
    else:
        st.warning("No receivers data found.")

    # -------- Food Listings Table --------
    st.subheader("🍲 Food Listings")
    df3 = pd.read_sql_query("SELECT * FROM food_listings", conn)
    if not df3.empty:
        df3["Food_ID"] = df3["Food_ID"].astype(str)
        col1, col2, col3, col4 = st.columns(4)
        city_filter = col1.selectbox("City", ["All"] + sorted(df3["Location"].dropna().unique().tolist()))
        provider_type_filter = col2.selectbox("Provider Type", ["All"] + sorted(df3["Provider_Type"].dropna().unique().tolist()))
        food_type_filter = col3.selectbox("Food Type", ["All"] + sorted(df3["Food_Type"].dropna().unique().tolist()))
        meal_type_filter = col4.selectbox("Meal Type", ["All"] + sorted(df3["Meal_Type"].dropna().unique().tolist()))

        filtered_df3 = df3.copy()
        if city_filter != "All":
            filtered_df3 = filtered_df3[filtered_df3["Location"] == city_filter]
        if provider_type_filter != "All":
            filtered_df3 = filtered_df3[filtered_df3["Provider_Type"] == provider_type_filter]
        if food_type_filter != "All":
            filtered_df3 = filtered_df3[filtered_df3["Food_Type"] == food_type_filter]
        if meal_type_filter != "All":
            filtered_df3 = filtered_df3[filtered_df3["Meal_Type"] == meal_type_filter]

        st.dataframe(filtered_df3.reset_index(drop=True))
    else:
        st.warning("No food listings data found.")

        
    # -------- Claims Table --------
    st.subheader("📦 Claims")
    df4 = pd.read_sql_query("SELECT * FROM claims", conn)

    if not df4.empty:
    # Ensure IDs are strings for consistent search
        if "Food_ID" in df4.columns:
            df4["Food_ID"] = df4["Food_ID"].astype(str)
        if "Receiver_ID" in df4.columns:
            df4["Receiver_ID"] = df4["Receiver_ID"].astype(str)

        df4.fillna("Unknown", inplace=True)

        col1, col2, col3 = st.columns(3)

    # Search by Receiver ID
        receiver_filter = col1.text_input("Search by Receiver ID")

    # Search by Food ID
        food_filter = col2.text_input("Search by Food ID")

    # Status filter
        if "Status" in df4.columns:
            status_options = ["All"] + sorted(df4["Status"].dropna().unique().tolist())
        else:
            status_options = ["All"]
        status_filter = col3.selectbox("Filter by Status", status_options)

    # Apply filters
        filtered_df4 = df4.copy()
        if receiver_filter:
            filtered_df4 = filtered_df4[
                filtered_df4["Receiver_ID"].str.contains(receiver_filter, case=False, na=False)
        ]
        if food_filter:
            filtered_df4 = filtered_df4[
                filtered_df4["Food_ID"].str.contains(food_filter, case=False, na=False)
        ]
        if status_filter != "All" and "Status" in filtered_df4.columns:
            filtered_df4 = filtered_df4[filtered_df4["Status"] == status_filter]

        st.dataframe(filtered_df4.reset_index(drop=True))
    else:
        st.warning("No claims data found.")


# ---------------- ANALYTICS ----------------
elif app_mode == "📈 Analytics & Insights":
    st.header("📊 Data Analysis & Insights")
    try:
        df3 = pd.read_sql_query("SELECT * FROM food_listings", conn)
        df4 = pd.read_sql_query("SELECT * FROM claims", conn)
        df1 = pd.read_sql_query("SELECT * FROM providers", conn)

        # Ensure consistent dtypes
        df3["Food_ID"] = df3["Food_ID"].astype(str)
        df4["Food_ID"] = df4["Food_ID"].astype(str)
        df1["Provider_ID"] = df1["Provider_ID"].astype(str)
        df3["Provider_ID"] = df3["Provider_ID"].astype(str)

        # Handle missing values
        df3.fillna("Unknown", inplace=True)
        df4.fillna("Unknown", inplace=True)
        df1.fillna("Unknown", inplace=True)

        # 1. Most Claimed Meal Type
        st.subheader("1️⃣ Most Claimed Meal Type")
        claims_merged = df4.merge(df3, on="Food_ID", how="left")
        meal_counts = claims_merged["Meal_Type"].value_counts()
        fig1, ax1 = plt.subplots()
        meal_counts.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_xlabel("Meal Type")
        ax1.set_ylabel("Number of Claims")
        ax1.set_title("Most Claimed Meal Types")
        st.pyplot(fig1)

        # 2. Top Food Donating Providers
        st.subheader("2️⃣ Top Food Donating Providers")
        top_providers = (
            df3.groupby("Provider_ID")["Quantity"]
            .sum()
            .reset_index()
            .merge(df1[["Provider_ID", "Name"]], on="Provider_ID", how="left")
            .sort_values(by="Quantity", ascending=False)
            .head(10)
        )

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.bar(top_providers["Name"], top_providers["Quantity"], color='orange', edgecolor='black')
        ax2.set_xlabel("Provider Name")
        ax2.set_ylabel("Total Quantity Donated")
        ax2.set_title("Top 10 Food Donating Providers")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ Error: {e}")


# ---------------- SQL QUERIES --------------

elif app_mode == "🧮 SQL Query Results":
    st.header("🧾 SQL Query-Based Reports")

    sql_queries ={
         "1. How many food providers and recivers are there in each city?":
                 """
                 SELECT City, COUNT(*) AS Total,'Providers' AS Type
                 FROM providers
                 GROUP BY City

                 UNION ALL

                 SELECT City, COUNT(*) AS Total,'Receivers' AS Type
                 FROM receivers
                 GROUP BY City;
                 """,
             "2.Which type of food provider (restaurant, grocery store etc) contributes the most food?":
                 """
                 SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
                 FROM food_listings
                 GROUP BY Provider_Type
                 ORDER BY Total_Quantity DESC;
                 """,

             "3.What is the contact information of food providers in specific city?":
                 """
                 SELECT Name, Contact
                 FROM providers
                 WHERE City = 'East Sheena';
                 """,

             "4.Which receivers have claimed the most food?":
                 """
                 SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
                 FROM claims c
                 JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
                 GROUP BY r.Name
                 ORDER BY Total_Claims DESC;
                 """,

             "5.What is the total quantity of food available from all providers?":
                 """
                 SELECT SUM(Quantity) AS Total_Food_Quantity
                 FROM food_listings
                 """,

             "6.Which city has the highest number of food listings?":
                 """
                 SELECT Location AS City, COUNT(*) AS Total_Listings
                 FROM food_listings
                 GROUP BY Location
                 ORDER BY Total_Listings DESC;
                 """,

             "7.What are most commonly available food types?":
                 """
                 SELECT Food_Type, COUNT(*) AS Count
                 FROM food_listings
             GROUP BY Food_Type
                 ORDER BY Count DESC;
                 """,

             "8.How many food claims have been made for each food item?":
                 """
                 SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
                 FROM claims c
                 JOIN food_listings f ON c.Food_ID = f.Food_ID
                 ORDER BY Total_Claims DESC;
                 """,

             "9.Which provider has had the highest number of successful food claims?":
                 """
                 SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
                 FROM claims c
                 JOIN food_listings f ON c.Food_ID = f.Food_ID
                 JOIN providers p ON f.Provider_ID = p.Provider_ID
                 WHERE c.Status = 'Completed'
                 GROUP BY p.Name
                 ORDER BY Successful_Claims DESC;
                 """,

             "10.What percentage of food claims are completed vs. pending vs. canceled?":
                 """
                 SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage 
                 FROM claims
                 GROUP BY Status;
                 """,

             "11.What is the average quantity of food claimed per receiver?":
                 """
                 SELECT r.Name, AVG(f.Quantity) AS Avg_Claimed_Quantity
                 FROM claims c
                 JOIN food_listings f ON c.Food_ID = f.Food_ID
                 JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
                 GROUP BY r.Name;
                 """,

             "12.Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?":
                 """
                 SELECT f.Meal_Type, COUNT(*) AS Claim_Count
                 FROM claims c
                 JOIN food_listings f ON c.Food_ID = f.Food_ID
                 GROUP BY f.Meal_Type
                 ORDER BY Claim_Count DESC;
                 """,

             "13.What is the total quantity of food donated by each provider?":
                 """
                 SELECT p.Name, SUM(f.Quantity) AS Total_Donated
                 FROM food_listings f
                 JOIN providers p ON f.Provider_ID = p.Provider_ID+
                
                 GROUP BY p.Name
                 ORDER BY Total_Donated DESC;
                 """,

             "14.How many expired food items are still listed?":
                  """
                  SELECT COUNT(*) AS Expired_Items
                  FROM food_listings
                  WHERE Expiry_Date < Date('now');
                  """,

             "15.What are the toP 5 cities with the highest completed claims?":
                  """
                  SELECT f.Location AS City, COUNT(*) AS Completed_Claims
                  FROM claims c
                  JOIN food_listings f ON c.Food_ID = f.Food_ID
                  WHERE c.Status ='Completed'
                  GROUP BY f.Location
                  ORDER BY Completed_Claims DESC
                  LIMIT 5;
                  """,

             "16.What are the top 5 most donated food items?":
                  """
                  SELECT Food_Name, SUM(Quantity) AS Total_Donated
                  FROM food_listings
                  GROUP BY Food_Name
                  ORDER BY Total_Donated DESC
                  LIMIT 5;
                  """,

             "17.How many inactive providers?":
                  """SELECT p.Name, p.City
                  FROM providers p
                  LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID
                  WHERE f.Food_ID IS NULL;
                 """,

             "18.Claims trend over time":
                  """
                  SELECT DATE(Timestamp) AS Claim_Date, COUNT(*) AS Total_Claim
                  FROM claims
                  GROUP BY Claim_Date
                  ORDER BY Claim_Date ASC;
                  """,

             "19.Claims trend by city":
                  """
                  SELECT f.Location AS City, COUNT(*) AS Total_Claims
                  FROM claims c
                  JOIN food_listings f ON c.Food_ID = f.Food_ID
                  GROUP BY f.Location 
                  ORDER BY Total_Claims DESC;
                  """,

             "20.Claims made after food expiry":
                  """
                  SELECT c.Claim_ID, f.Food_Name, f.Expiry_Date, c.Timestamp
                  FROM claims c
                  JOIN food_listings f ON c.Food_ID = f.Food_ID
                  WHERE DATE(c.Timestamp) > DATE(f.Expiry_Date);
                  """,

             "21.Providers without any food listings":
                  """
                  SELECT p.Provider_ID, p.Name, p.City
                  FROM providers p
                  LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID
                  WHERE f.Food_ID IS NULL;
                  """,

             "22.Meal type vs. quantity donated":
                  """
                  SELECT Meal_Type, SUM(Quantity) AS Total_Quantity
                  FROM food_listings
                  GROUP BY Meal_Type
                  ORDER BY Total_Quantity DESC;
                  """,

             "23.Distribution of food types donated":
                  """SELECT Food_Type, COUNT(*) AS Total_Listings
                  FROM food_listings
                  GROUP BY Food_Type
                  ORDER BY Total_Listings DESC;
                 """,

             "24.top 10 food donating providers":
                  """SELECT p.Name, SUM(f.Quantity) AS Total_Quantity
                  FROM food_listings f
                  JOIN providers p ON f.Provider_ID = p.Provider_ID
                  GROUP BY p.Name
                  ORDER BY Total_Quantity DESC
                  LIMIT 10;
                  """,

    }
    query_choice = st.selectbox("Select a query to run:", list(sql_queries.keys()))
    df = pd.read_sql_query(sql_queries[query_choice], conn)
    st.dataframe(df)

# ---------------- CRUD ----------------
elif app_mode == "🛠️ CRUD Operations":
    st.title("🛠️ Manage Records")

    table_choice = st.selectbox("Select Table", ["Food Listings","Providers","Receivers", "Claims"])

    # ================= FOOD LISTINGS =================
    if table_choice == "Food Listings":
        crud_operation = st.selectbox("Choose Operation", ["Add Record", "Update Record", "Delete Record"])

        # ADD
        if crud_operation == "Add Record":
            st.subheader("➕ Add New Food Listing")
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
            provider_type = st.text_input("Provider Type")
            location = st.text_input("Location")
            food_type = st.text_input("Food Type")
            meal_type = st.text_input("Meal Type")
            if st.button("Add Food"):
                cursor.execute("""
                    INSERT INTO food_listings 
                    (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (food_name, quantity, expiry.strftime("%Y-%m-%d"), provider_id, provider_type, location, food_type, meal_type))
                conn.commit()
                st.success(f"✅ Food '{food_name}' added successfully!")

        # UPDATE
        elif crud_operation == "Update Record":
            st.subheader("✏️ Update Food Listing")
            food_id = st.number_input("Enter Food ID to Update", min_value=1, step=1)
            quantity = st.number_input("New Quantity", min_value=1)
            expiry = st.date_input("New Expiry Date", min_value=date.today())
            if st.button("Update Food"):
                cursor.execute("""
                    UPDATE food_listings 
                    SET Quantity = ?, Expiry_Date = ? 
                    WHERE Food_ID = ?
                """, (quantity, expiry.strftime("%Y-%m-%d"), food_id))
                conn.commit()
                st.success(f"✅ Food ID {food_id} updated successfully!")

        # DELETE
        elif crud_operation == "Delete Record":
            st.subheader("🗑️ Delete Food Listing")
            food_id = st.number_input("Enter Food ID to Delete", min_value=1, step=1)
            if st.button("Delete Food"):
                cursor.execute("DELETE FROM food_listings WHERE Food_ID = ?", (food_id,))
                conn.commit()
                st.success(f"✅ Food ID {food_id} deleted successfully!")

    # ================= PROVIDERS =================
    elif table_choice == "Providers":
        crud_operation = st.selectbox("Choose Operation", ["Add Record", "Update Record", "Delete Record"])

        # ADD
        if crud_operation == "Add Record":
            st.subheader("➕ Add New Provider")
            name = st.text_input("Provider Name")
            provider_type = st.text_input("Provider Type")
            contact = st.text_input("Contact")
            location = st.text_input("Location")
            if st.button("Add Provider"):
                cursor.execute("""
                    INSERT INTO providers (Name, Provider_Type, Contact, Location) 
                    VALUES (?, ?, ?, ?)
                """, (name, provider_type, contact, location))
                conn.commit()
                st.success(f"✅ Provider '{name}' added successfully!")

        # UPDATE
        elif crud_operation == "Update Record":
            st.subheader("✏️ Update Provider")
            provider_id = st.number_input("Enter Provider ID to Update", min_value=1, step=1)
            name = st.text_input("New Name")
            contact = st.text_input("New Contact")
            if st.button("Update Provider"):
                cursor.execute("""
                    UPDATE providers 
                    SET Name = ?, Contact = ? 
                    WHERE Provider_ID = ?
                """, (name, contact, provider_id))
                conn.commit()
                st.success(f"✅ Provider ID {provider_id} updated successfully!")

        # DELETE
        elif crud_operation == "Delete Record":
            st.subheader("🗑️ Delete Provider")
            provider_id = st.number_input("Enter Provider ID to Delete", min_value=1, step=1)
            if st.button("Delete Provider"):
                cursor.execute("DELETE FROM providers WHERE Provider_ID = ?", (provider_id,))
                conn.commit()
                st.success(f"✅ Provider ID {provider_id} deleted successfully!")

    # ================= RECEIVERS =================
    elif table_choice == "Receivers":
        crud_operation = st.selectbox("Choose Operation", ["Add Record", "Update Record", "Delete Record"])

        # ADD
        if crud_operation == "Add Record":
            st.subheader("➕ Add New Receiver")
            name = st.text_input("Receiver Name")
            receiver_type = st.text_input("Receiver Type")
            contact = st.text_input("Contact")
            location = st.text_input("Location")
            if st.button("Add Receiver"):
                cursor.execute("""
                    INSERT INTO receivers (Name, Receiver_Type, Contact, Location) 
                    VALUES (?, ?, ?, ?)
                """, (name, receiver_type, contact, location))
                conn.commit()
                st.success(f"✅ Receiver '{name}' added successfully!")

        # UPDATE
        elif crud_operation == "Update Record":
            st.subheader("✏️ Update Receiver")
            receiver_id = st.number_input("Enter Receiver ID to Update", min_value=1, step=1)
            name = st.text_input("New Name")
            contact = st.text_input("New Contact")
            if st.button("Update Receiver"):
                cursor.execute("""
                    UPDATE receivers 
                    SET Name = ?, Contact = ? 
                    WHERE Receiver_ID = ?
                """, (name, contact, receiver_id))
                conn.commit()
                st.success(f"✅ Receiver ID {receiver_id} updated successfully!")

        # DELETE
        elif crud_operation == "Delete Record":
            st.subheader("🗑️ Delete Receiver")
            receiver_id = st.number_input("Enter Receiver ID to Delete", min_value=1, step=1)
            if st.button("Delete Receiver"):
                cursor.execute("DELETE FROM receivers WHERE Receiver_ID = ?", (receiver_id,))
                conn.commit()
                st.success(f"✅ Receiver ID {receiver_id} deleted successfully!")

    # ================= CLAIMS =================
    elif table_choice == "Claims":
        crud_operation = st.selectbox("Choose Operation", ["Add Record", "Update Record", "Delete Record"])

        # ADD
        if crud_operation == "Add Record":
            st.subheader("➕ Add New Claim")
            food_id = st.number_input("Food ID", min_value=1)
            receiver_id = st.number_input("Receiver ID", min_value=1)
            claim_date = st.date_input("Claim Date", min_value=date.today())
            status = st.text_input("Status")
            if st.button("Add Claim"):
                cursor.execute("""
                    INSERT INTO claims (Food_ID, Receiver_ID, Claim_Date, Status) 
                    VALUES (?, ?, ?, ?)
                """, (food_id, receiver_id, claim_date.strftime("%Y-%m-%d"), status))
                conn.commit()
                st.success("✅ Claim added successfully!")

        # UPDATE
        elif crud_operation == "Update Record":
            st.subheader("✏️ Update Claim")
            claim_id = st.number_input("Enter Claim ID to Update", min_value=1, step=1)
            status = st.text_input("New Status")
            if st.button("Update Claim"):
                cursor.execute("""
                    UPDATE claims 
                    SET Status = ? 
                    WHERE Claim_ID = ?
                """, (status, claim_id))
                conn.commit()
                st.success(f"✅ Claim ID {claim_id} updated successfully!")

        # DELETE
        elif crud_operation == "Delete Record":
            st.subheader("🗑️ Delete Claim")
            claim_id = st.number_input("Enter Claim ID to Delete", min_value=1, step=1)
            if st.button("Delete Claim"):
                cursor.execute("DELETE FROM claims WHERE Claim_ID = ?", (claim_id,))
                conn.commit()
                st.success(f"✅ Claim ID {claim_id} deleted successfully!")


# About Creator Section
elif app_mode == "ℹ️ About Creator":
    st.title("ℹ️ About the Creator")
    
    st.markdown("""
**👤 Name:** KUKKAR SEEMA BALASAHEB  
**📧 Email:** kukkarkunal07@gmail.com  
**🌐 LinkedIn:** [Visit Profile](https://www.linkedin.com/in/seema-kukkar-61a51a337?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
    """)

   
    st.markdown("""
### 🙏 Thank You for Visiting!  
This project was created to connect surplus food providers with those in need,  
aiming to **reduce food wastage** and promote **social good**.
    """)
