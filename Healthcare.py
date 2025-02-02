import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np

sb= st.sidebar.radio('Healthcare_Insights',['Home','Dashboard','Analysis & Insights']) #To Display menus

# Connecting the database for Streamlit application
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="root",
  database = 'Healthcare_Data'
)
Healthcare_db = mydb.cursor()

#Creating the conditions for adding the data to the radio button
if sb=='Home':
        st.title('Healthcare Insights Dashboard')
        st.markdown("""
        In modern healthcare, **data is critical** for improving patient care and operational efficiency.  
        This analytical tool is designed to provide actionable insights into healthcare operations, including **total admission count**, **bed occupancy**, and other critical metrics.  
        
        The **dashboard and insights** help healthcare administrators and decision-makers monitor key metrics and trends to improve service quality and efficiency.
        """)
    
        st.markdown("### Key Features and Menus") # Subsections 
        st.markdown("""
        #### Home Dashboard:
        - **Quickview of key performance indicators (KPIs)** such as admission trends,total admission count,
            patients average length of stay and No.of.ICU patients.
        """)
        st.markdown("""
        #### Analysis & Insights:
        - Breakdown of patients and dignosis data's in dropdown.  
        - Visualization of analysis with multiple scenrios such as **Trends in Admission Over Time** ,**Bed Occupancy Analysis** and etc.
        """)

if sb=='Dashboard': #To display the Dashboard in streamlit
    
    # SQL query to get the data for Monthly Patient Admission Trends
    query1 = """
    select DATE_FORMAT(Admit_Date, '%Y-%m') as YearMonth, 
           count(*) as Total_Admissions
    from healthcare_df
    group by DATE_FORMAT(Admit_Date, '%Y-%m')
    order by DATE_FORMAT(Admit_Date, '%Y-%m');
    """
    df1= pd.read_sql(query1,mydb) # Read the data from SQL into a DataFrame
    
    st.title('Dashboard')
    
    with st.container(): #key performance indicators using metric
        col1, col2, col3 = st.columns(3)  # Create 3 columns
    
        #metrics to each column
        col1.metric("Total Admissions", value=7157)
        col2.metric("Patients Average Length of Stay", value="8.2 days")
        col3.metric("No.of.ICU Patients", value="1193")
        
    # Line chart using plotly.express
    fig = px.line(
        df1,
        x='YearMonth',
        y='Total_Admissions',
        title='Trends in Patients Admission Over the Time:',
        labels={'YearMonth': 'Year-Month', 'Total_Admissions': 'Total Admissions'},
        markers=True
    )

    #Customizing the layout
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        title_x=0.0,  # Center the title
        plot_bgcolor='rgba(240, 240, 240, 0.5)'  # Light background
    )
    st.plotly_chart(fig)
    st.markdown("""The line chart shows how the total number of patient admissions has changed over time.""")
    
if sb=='Analysis & Insights':
    options = ["Top 5 common diagnoses","Bed Occupancy Analysis","Length of Stay Distribution",
               "Seasonal Admission Patterns","Trends of ICU admission over the years",
               "Doctors Workload analysis","Trends of Tests","Top Rated Doctors","Quarterly billing Trends",
               "Diagnosis having highest bill","Insurance claims over the time","Season wise diagnosis",
               "Doctors with most missing followups","Avg of Total Billing(Diagnosis based)"
               ] #Dropdowns
    
    selected_option = st.sidebar.selectbox("Analysis & Insights:", options)
    if selected_option == "Top 5 common diagnoses":
        st.title('The top 5 most common diagnoses')
        
        query2 = """
        select  Diagnosis,
               count(*) AS TotalCases
        from healthcare_df
        group by Diagnosis
        order by TotalCases desc
        limit 5;
        """
        df2= pd.read_sql(query2,mydb)
        
        plt.figure(figsize =(5,3))
        plt.bar(df2['Diagnosis'],df2['TotalCases'],color='orange',width =0.7)
        #plt.title('The top 5 most common diagnoses')
        plt.xlabel('Diagnosis')
        plt.ylabel('No. of Cases')
        plt.show()
        st.pyplot(plt)
        st.markdown("""
                    #### Observation & Suggestion:
                     - The bar chart shows the top 5 most common diagnoses in our healthcare dataset. 'Viral Infection' stands out as the most prevalent diagnosis, accounting for the largest portion of cases, followed by 'Flu' and 'Malaria.' 
                     - These insights suggest that respiratory infections are the most common conditions, which could be attributed to seasonal factors.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df2)
        
    elif selected_option == "Bed Occupancy Analysis":
            st.title('Bed Occupancy Analysis')
        
            query3="""
            select  Bed_Occupancy,
            count(*) as TotalOccupancy
            from healthcare_df
            group by Bed_Occupancy
            order by TotalOccupancy,Bed_Occupancy desc"""
        
            df3= pd.read_sql(query3,mydb)
            
            lbls = df3['Bed_Occupancy']
            sizes = df3['TotalOccupancy']
            
            plt.pie(sizes,labels =lbls,
                    autopct = '%.2f%%',startangle = 120)
            #plt.title('Bed Occupany Pie Chart')
            plt.show()
            st.pyplot(plt)
            st.markdown("""
                    #### Key Observation:
                     - The private ward accounts for half of the total bed occupancy,
                     indicating a significant preference or demand for private care.
                """)
            st.write("Here is the data fetched from the database:")
            st.table(df3)

    elif selected_option == "Length of Stay Distribution":
        st.title('Length of Stay Distribution')
        query4="""
            select
            avg(DATEDIFF(Discharge_Date,Admit_Date)) AS Average_Length_of_Stay,
            max(DATEDIFF(Discharge_Date,Admit_Date)) AS Maximum_Length_of_Stay
            from healthcare_df"""
        df4= pd.read_sql(query4,mydb)
        stay = ['Average Length of Stay', 'Maximum Length of Stay']
        values = [df4['Average_Length_of_Stay'].iloc[0], df4['Maximum_Length_of_Stay'].iloc[0]]

        plt.figure(figsize=(8, 4))
        plt.barh(stay,values, color=['skyblue', 'orange'])
        plt.xlabel('Days')
        #plt.title('Length of Stay Distribution')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)
        st.write("Here is the data fetched from the database:")
        st.table(df4)
        st.markdown("""
                    #### Key Observation:
                     - The average length of stay is 8 days,This is plot will help for planning the bed occupany for well ahead for the new admits.
                     - Address the Prolonged Stays,For patients with a longer length of stay, investigate whether
                     these stays are medically necessary or due to delays in discharge planning.
                """)

    elif selected_option == "Seasonal Admission Patterns":
        st.title('Seasonal Admission Patterns')
        query5= """
            select case when month(Admit_Date) between 3 and 5 then 'Spring'
            when month(Admit_Date) between 6 and 8 then 'Summer'
            when month(Admit_Date) between 9 and 11 then 'Autum'
            when month(Admit_Date) >= 12 or month(Admit_Date) <= 2 then 'Winter'
            end as Season,
            year(Admit_Date) AS AdmitYEAR,
            count(Patient_ID) AS COUNT
            from healthcare_df
            group by year(Admit_Date), Season
            order by AdmitYEAR DESC
            """
        df5= pd.read_sql(query5,mydb)
        
        pivot_df = df5.pivot(index='AdmitYEAR', columns='Season', values='COUNT')
        years = pivot_df.index
        seasons = pivot_df.columns
        bar_width = 0.2
        x = np.arange(len(years))  # X positions for the years
        
        # clustered bar chart
        plt.figure(figsize=(10, 6))
        for i, season in enumerate(seasons): # Loops through each season
            plt.bar(x + i * bar_width, pivot_df[season], bar_width, label=season)
        plt.xlabel('Year')
        plt.ylabel('Patient Count')
        #plt.title('Seasonal Admission Patterns')
        plt.xticks(x + bar_width, years, rotation=45)
        plt.legend(title='Season')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - Winter seasons consistently show higher patient admissions across years.
                     - Run a preventative campaigns to Educate the public on seasonal illnesses and prevention strategies before high-admission seasons.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df5)

    elif selected_option == "Trends of ICU admission over the years":
        st.title('ICU admission over the years')
        
        query6= """
            select year(Admit_Date) as Year,
            count(*) as ICU_Admits
            from healthcare_df
            where Bed_Occupancy = 'ICU'
            group by Bed_Occupancy,Year
            order by Year asc
            """
        df6= pd.read_sql(query6,mydb)
        
        plt.figure(figsize =(6,3))
        plt.bar(df6['Year'],df6['ICU_Admits'],color='darkblue',width =0.5)
        plt.xlabel('Year')
        plt.ylabel('No. of ICU Cases')
        plt.xticks(df6['Year'])  # Ensure the years are shown as discrete integers
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)
        st.write("Here is the data fetched from the database:")
        st.table(df6)
        st.markdown("""
                    #### Observation & Suggestion:
                     - The spike in recent years (e.g 2023), it could be attributed to events like automobile acciendts or virus like COVID-19, which caused surges in ICU occupancy globally.
                     - Use these trends to optimize resource allocation for ICU facilities, staffing, and equipment.
                """)

    elif selected_option == "Doctors Workload analysis":
        st.title('Doctors Workload analysis')

        query7= """
            select Doctor,
            count(*) AS TotalCasesHandled
            from healthcare_df
            group by Doctor
            order by TotalCasesHandled desc
            """
        df7= pd.read_sql(query7,mydb)
        
        lbls = df7['Doctor']
        sizes = df7['TotalCasesHandled']
        plt.pie(sizes,labels =lbls,
                    autopct = '%.2f%%',startangle = 120)
        plt.show()
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - Based on the data and the pie chart, the doctors' workloads appear to be evenly distributed.
                     - Management should consider hiring additional backup doctors to effectively handle any sudden surge in patient admissions.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df7)

    elif selected_option == "Trends of Tests":
        st.title('Trends of Tests over the year')
        query8= """select Test,YEAR(Admit_Date) as Year,
                    	count(*) as Total_No_Tests
                    from healthcare_df
                    group by Test,Year
                    order by Total_No_Tests desc"""
            
        df8= pd.read_sql(query8,mydb)
        
        plt.figure(figsize=(10, 6))
        
        for test in df8['Test'].unique(): # Iterate through each test
            test_data = df8[df8['Test'] == test]
            plt.plot(test_data['Year'], test_data['Total_No_Tests'], marker='o', label=test)
        
        plt.xlabel('Year')
        plt.ylabel('Total Number of Tests')
        plt.legend(title='Test', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(df8['Year'])
        plt.tight_layout()
        plt.show()  
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - Blood tests may consistently have higher counts compared to others, indicating their significance or demand in healthcare practices.
                     - For tests with increasing demand, consider training staff for specialized handling and reducing turnaround times.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df8)

    elif selected_option == "Top Rated Doctors":
        st.title('Trends of Tests over the year')
        query9= """SELECT Doctor as Top_Rated_Doctors, avg (Feedback) as Ratings
                	FROM healthcare_df
                    group by Doctor
                    order by Ratings desc
                    limit 3;"""
            
        df9= pd.read_sql(query9,mydb)
        
        plt.figure(figsize =(5,3))
        plt.bar(df9['Top_Rated_Doctors'],df9['Ratings'],color='mediumseagreen',width =0.7)
        plt.xlabel('Doctors')
        plt.ylabel('Ratings')
        plt.show()
        st.pyplot(plt)
        st.write("Here is the data fetched from the database:")
        st.table(df9)
        st.markdown("""
                    #### Observation & Suggestion:
                     - These are the Top 3 highly rated doctors,they serve as role models for best practices and patient care standards.
                     - Involve these top-rated doctors in training or mentoring other staff to elevate overall patient care standards.
                     - Acknowledge and reward top-rated doctors to motivate continued high-quality care.
                """)

    elif selected_option == "Quarterly billing Trends":
        st.title('Quarterly billing Trends')
        query10= """select case when MONTH(Discharge_Date) between 1 and 3 then 'First Quarter'
                               when MONTH(Discharge_Date) between 4 and 6 then 'Second Quarter'
                               when MONTH(Discharge_Date) between 7 and 9 then 'Third Quarter'
                               when MONTH(Discharge_Date) between 10 and 12 then 'Fourth Quarter'
                    end as Quarterly,
                    year(Discharge_Date) as Year,
                    sum(Billing_Amount) as TotalAmount
                    FROM healthcare_df
                    group by  year(Discharge_Date),Quarterly
                    order by TotalAmount desc"""
            
        df10= pd.read_sql(query10,mydb)
        plt.figure(figsize=(10, 6))

        pivot_df = df10.pivot(index='Year', columns='Quarterly', values='TotalAmount')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_df.plot(kind='bar', ax=ax)
        
        # Add title and labels
        plt.title('Total Billing Amount by Quarter and Year')
        plt.xlabel('Year')
        plt.ylabel('Total Billing Amount')
        
        # Show the plot
        plt.xticks(rotation=0)  # Rotate the x-axis labels for better readability
        plt.legend(title='Quarterly')
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)
        st.write("The le7 label you're seeing in the bar plot is represents a long exponential notation as the billing amounts are high in numbers")
        st.write("Here is the data fetched from the database:")
        st.table(df10)
        st.markdown("""
                    #### Observation & Suggestion:
                     - The first quarter (January-March 2024) shows the down on the trends of billing, as hospitals may experienced reduced patient volumes on that particular quarter.
                     - For Future forecasting this stats can be very useful for statistical or machine learning techniques to predict total billing by quarter for future years, helping with budgeting and resource planning.
                """)

    elif selected_option == "Diagnosis having highest bill":
        st.title('Diagnosis having highest bill')
        query11= """select Diagnosis, 
                    sum(Billing_Amount) as BilledAmount
                    FROM healthcare_df
                    group by Diagnosis
                    order by BilledAmount desc"""
            
        df11= pd.read_sql(query11,mydb)
        
        plt.figure(figsize =(7,4))
        plt.bar(df11['Diagnosis'],df11['BilledAmount'],color='firebrick',width =0.7)
        plt.xlabel('Diagnosis')
        plt.ylabel('BilledAmount')
        plt.show()
        st.pyplot(plt)
        st.write("The le8 label you're seeing in the bar plot is represents a long exponential notation as the billing amounts are high in numbers")
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - The bar chart shows that the 'Viral Infection' stands out as the most billed diagnosis, accounting for the largest portion of cases.'.
                     - Administator of billing department should use these data's for better reconciliation.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df11)

    elif selected_option == "Insurance claims over the time":
        st.title('Insurance claims over the time')
        query12= """select DATE_FORMAT(Discharge_Date, '%Y-%m') AS YearMonth, 
                    sum(Health_Insurance_Amount) as Total_Insurance_Claimed
                    FROM healthcare_df
                    group by DATE_FORMAT(Discharge_Date, '%Y-%m')
                    order by Total_Insurance_Claimed desc"""
            
        df12= pd.read_sql(query12,mydb)
        
        plt.figure(figsize =(15,6))
        plt.plot(df12['YearMonth'],df12['Total_Insurance_Claimed'],c='darkviolet',marker='o', markersize=6, linestyle='-', linewidth=2)
        plt.xlabel('YearMonth')
        plt.ylabel('Total_Insurance_Claimed')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
        st.pyplot(plt)
        st.write("The le7 label you're seeing in the bar plot is represents a long exponential notation as the billing amounts are high in numbers")
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - By observing the billing totals for each month, we identified the periods of higher claims. March,2023 shows the higher in claims over the time.
                     - By analyzing Total Insurance Claims over the time , it would be helpful to anticipate these periods in advance and plan for staffing, resource allocation on insurance department.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df12)

    elif selected_option == "Season wise diagnosis":
        st.title('Season wise diagnosis')
        
        query13= """select case when MONTH(Admit_Date) between 3 and 5 then 'Spring'
                    when MONTH(Admit_Date) between 6 and 8 then 'Summer'
                    when MONTH(Admit_Date) between 9 and 11 then 'Autumn'
                    when MONTH(Admit_Date) >= 12 or MONTH(Admit_Date) <= 2 then 'Winter'
               end AS Season,
               Diagnosis,
               COUNT(Patient_ID) AS TotalAdmission
        FROM healthcare_df
        GROUP BY Diagnosis, Season
        ORDER BY Season DESC ,TotalAdmission desc"""
            
        df13= pd.read_sql(query13,mydb)
        
        pivot_df = df13.pivot(index='Diagnosis', columns='Season', values='TotalAdmission')

        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Set the x positions for each Diagnosis group
        x = np.arange(len(pivot_df))
        width = 0.2
        
        # setting the bar for each season as a grouped bar
        ax.bar(x - width * 1.5, pivot_df['Winter'], width, label='Winter', color='skyblue')
        ax.bar(x - width * 0.5, pivot_df['Spring'], width, label='Spring', color='lightgreen')
        ax.bar(x + width * 0.5, pivot_df['Summer'], width, label='Summer', color='yellow')
        ax.bar(x + width * 1.5, pivot_df['Autumn'], width, label='Autumn', color='orange')
        
        # Add labels and title
        ax.set_xlabel('Diagnosis')
        ax.set_ylabel('Total Admissions')
        ax.set_xticks(x)
        ax.set_xticklabels(pivot_df.index, rotation=45)
        ax.legend(title='Season')
        
        # Show the plot
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - The grouped bar plot and data shows there is a siginificant raise in the admission in winter.
                     - Administration should be ready for flu season in Winter, ensuring adequate supplies of vaccines and medical resources for respiratory conditions.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df13)

    elif selected_option == "Doctors with most missing followups":
        st.title('Doctors with most missing followups')

        query14= """
            select Doctor, 
                count(*) as Missing_Followups
            from healthcare_df
            where Followup_Date = 'Not Scheduled'
            group by Doctor
            order by Missing_Followups desc;
            """
        df14= pd.read_sql(query14,mydb)
        
        lbls = df14['Doctor']
        sizes = df14['Missing_Followups']
        colors=['mistyrose','bisque','azure','lightblue','plum','pink','honeydew']
        plt.pie(sizes,labels =lbls,
                    autopct = '%.2f%%',startangle = 120,colors=colors)
        plt.show()
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - The Doctor named Niki Sharma has the highest missing follow-ups followed by Tejas Saxena and Jaya Yaadav.
                     - Doctors with the highest Missing Follow-ups represent areas where follow-up scheduling is lacking. It’s important to understand why this might be occurring—whether it's due to administrative errors, lack of communication with patients, or overwhelming patient loads.
                     - If high missing follow-ups are linked to doctors handling too many patients, consider redistributing the workload or adding administrative support to help manage the scheduling process more effectively.
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df14)

    elif selected_option == "Avg of Total Billing(Diagnosis based)":
        st.title('Avg of Total Billing(Diagnosis based)')
        query15="""
            select Diagnosis,
                   avg(Billing_Amount) as Avg_Bill_Amount
            from healthcare_df
            group by Diagnosis
            order by Diagnosis desc"""
        
        df15= pd.read_sql(query15,mydb)

        plt.figure(figsize=(10, 6))
        plt.barh(df15['Diagnosis'], df15['Avg_Bill_Amount'], color='skyblue')
        
        # Add labels and title
        plt.xlabel('Average Billing Amount ($)')
        plt.ylabel('Diagnosis')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        st.pyplot(plt)
        st.markdown("""
                    #### Key Observation & Suggestion:
                     - Diagnoses Viral Infection and Typhoid are associated with high average billing amounts.
                     - For high-billing diagnoses, provide more cost transparency to patients and their families. Help them understand the treatment process, which will allow them to make more informed decisions about their care..
                """)
        st.write("Here is the data fetched from the database:")
        st.table(df15)
