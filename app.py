import os
import streamlit as st
import psycopg2

st.title("🌍 International Debt Analysis Dashboard")

st.write(
    "Explore international external debt using "
    "PostgreSQL, SQL queries, and interactive visualizations."
)

conn = psycopg2.connect(
    host="localhost",
    database="international_debt",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)

st.success("PostgreSQL connected successfully!")

cursor_kpi = conn.cursor()

cursor_kpi.execute("""
SELECT COUNT(DISTINCT country_code)
FROM countries
WHERE country_code NOT IN (
    'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
    'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
    'IDX', 'LDC', 'MNA', 'LIC'
);
""")

country_count = cursor_kpi.fetchone()[0]

cursor_kpi.execute("""
SELECT MIN(year), MAX(year)
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World';
""")

min_year, max_year = cursor_kpi.fetchone()

latest_year = max_year


cursor_kpi.execute("""
SELECT SUM(value)
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World'
  AND year = %s
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  );
""", (latest_year,))

total_debt_latest = cursor_kpi.fetchone()[0]


st.subheader("📌 Dashboard Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", country_count)
col2.metric("Years Covered", f"{min_year}–{max_year}")
col3.metric(
    "Total External Debt",
    f"${total_debt_latest / 1_000_000_000_000:.2f}T"
)

st.subheader("📊 Debt Analysis Questions")

question = st.selectbox(
    "Select an analysis:",
    [
        "Top 10 Countries by External Debt in 2024",
        "Total External Debt by Year (2000–2024)",
        "Average External Debt by Country",
        "Retrieve All Distinct Country Names",
        "Count Total Number of Countries",
        "Count Total Number of Indicators",
        "Display First 10 Records",
        "Debt Greater Than 1 Billion USD",
        "Minimum, Maximum and Average Debt",
        "Count Total Number of Records",
        "Total Global Debt",
        "List All Unique Indicator Names",
        "Number of Records for Each Country",
        "Total Debt for Each Country",
        "Top 10 Countries by Total Debt",
        "Total Debt for Each Indicator",
        "Highest Contributing Indicator",
        "Country with Lowest Total Debt",
        "Total Debt by Country and Indicator",
        "Number of Indicators per Country",
        "Countries Above Global Average Debt",
        "Rank Countries Based on Total Debt",
        "Top 5 Indicators by Total Debt",
        "Country Percentage Contribution",
        "Top 3 Countries per Indicator",
        "Difference Between Maximum and Minimum Debt",
        "Top 10 Countries Debt View",
        "Debt Category (High / Medium / Low)",
        "Cumulative Debt per Country",
        "Indicators Above Overall Average Debt",
        "Countries Contributing More Than 5% of Global Debt",
        "Most Dominant Indicator for Each Country"
        
    ]
)
if question == "Top 10 Countries by External Debt in 2024":

    st.subheader("Top 10 Countries by External Debt in 2024")

    cursor = conn.cursor()

    query = """
    SELECT
        c.country_name,
        d.country_code,
        d.year,
        d.value
    FROM debt_data d
    INNER JOIN countries c
        ON d.country_code = c.country_code
    WHERE d.series_code = 'DT.DOD.DECT.CD'
      AND d.counterpart_area_name = 'World'
      AND d.year = 2024
      AND d.country_code NOT IN (
          'EAP',
          'ECA',
          'IDA',
          'LAC',
          'LMY',
          'LMC',
          'MIC',
          'SSA',
          'UMC',
          'SAS',
          'IDX',
          'LDC',
          'MNA',
          'LIC'
      )
    ORDER BY d.value DESC
    LIMIT 10;
    """

    cursor.execute(query)

    results = cursor.fetchall()
    top10_total = sum(row[3] for row in results)

    st.metric(
        "Combined Debt of Top 10 Countries",
        f"${top10_total / 1_000_000_000_000:.2f}T"
    )

    for row in results:
        st.write(
            f"Country: {row[0]} | "
            f"Code: {row[1]} | "
            f"Year: {row[2]} | "
            f"External Debt: ${row[3]:,.0f}"
        )


elif question == "Total External Debt by Year (2000–2024)":

    st.subheader("Total External Debt by Year (2000–2024)")

    cursor2 = conn.cursor()

    query2 = """
    SELECT
        year,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year BETWEEN 2000 AND 2024
    GROUP BY year
    ORDER BY year;
    """

    cursor2.execute(query2)

    yearly_results = cursor2.fetchall()

    for row in yearly_results:
        st.write(
            f"Year: {row[0]} | "
            f"Total Debt: ${row[1]:,.0f}"
        )

    st.subheader("External Debt Trend (2000–2024)")

    yearly_chart = {
        row[0]: row[1]
        for row in yearly_results
    }

    st.line_chart(yearly_chart)

elif question == "Average External Debt by Country":

    st.subheader("Average External Debt by Country")

    cursor3 = conn.cursor()

    query3 = """
    SELECT
        c.country_name,
        AVG(d.value) AS average_debt
    FROM debt_data d
    INNER JOIN countries c
        ON d.country_code = c.country_code
    WHERE d.series_code = 'DT.DOD.DECT.CD'
      AND d.counterpart_area_name = 'World'
      AND d.year BETWEEN 2000 AND 2024
      AND d.country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY c.country_name
    ORDER BY average_debt DESC
    LIMIT 10;
    """

    cursor3.execute(query3)

    average_results = cursor3.fetchall()

    for row in average_results:
        st.write(
            f"Country: {row[0]} | "
            f"Average External Debt: ${row[1]:,.0f}"
        )

    st.subheader("Average External Debt Comparison")

    average_chart = {
        row[0]: row[1]
        for row in average_results
    }

    st.bar_chart(average_chart)

elif question == "Retrieve All Distinct Country Names":

    st.subheader("All Distinct Country Names")

    cursor4 = conn.cursor()

    query4 = """
    SELECT DISTINCT country_name
    FROM countries
    WHERE country_code NOT IN (
        'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
        'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
        'IDX', 'LDC', 'MNA', 'LIC'
    )
    ORDER BY country_name;
    """

    cursor4.execute(query4)

    country_results = cursor4.fetchall()

    for row in country_results:
        st.write(row[0])


elif question == "Count Total Number of Countries":

    st.subheader("Total Number of Countries")

    cursor5 = conn.cursor()

    query5 = """
    SELECT COUNT(DISTINCT country_code) AS total_countries
    FROM countries
    WHERE country_code NOT IN (
        'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
        'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
        'IDX', 'LDC', 'MNA', 'LIC'
    );
    """

    cursor5.execute(query5)

    country_count_result = cursor5.fetchone()

    st.metric(
        "Total Countries",
        country_count_result[0]
    )

elif question == "Count Total Number of Indicators":

    st.subheader("Total Number of Indicators")

    cursor6 = conn.cursor()

    query6 = """
    SELECT COUNT(DISTINCT indicator_code) AS total_indicators
    FROM indicators;
    """

    cursor6.execute(query6)

    indicator_count_result = cursor6.fetchone()

    st.metric(
        "Total Indicators",
        indicator_count_result[0]
    )

elif question == "Display First 10 Records":

    st.subheader("First 10 Records")

    cursor7 = conn.cursor()

    query7 = """
    SELECT *
    FROM debt_data
    LIMIT 10;
    """

    cursor7.execute(query7)

    first_10_results = cursor7.fetchall()

    for row in first_10_results:
        st.write(row)



elif question == "Debt Greater Than 1 Billion USD":

    st.subheader("Records with Debt Greater Than 1 Billion USD")

    cursor8 = conn.cursor()

    query8 = """
    SELECT *
    FROM debt_data
    WHERE value > 1000000000
    LIMIT 100;
    """

    cursor8.execute(query8)

    debt_results = cursor8.fetchall()

    column_names = [desc[0] for desc in cursor8.description]

    import pandas as pd

    df8 = pd.DataFrame(debt_results, columns=column_names)

    st.write("Showing the first 100 matching records")
    st.dataframe(df8, width="stretch")

    cursor8.close()

elif question == "Minimum, Maximum and Average Debt":

    st.subheader("Minimum, Maximum and Average Debt")

    cursor9 = conn.cursor()

    query9 = """
    SELECT
        MIN(value) AS minimum_debt,
        MAX(value) AS maximum_debt,
        AVG(value) AS average_debt
    FROM debt_data;
    """

    cursor9.execute(query9)

    debt_summary = cursor9.fetchone()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Minimum Debt",
        f"${debt_summary[0]:,.0f}"
    )

    col2.metric(
        "Maximum Debt",
        f"${debt_summary[1]:,.0f}"
    )

    col3.metric(
        "Average Debt",
        f"${debt_summary[2]:,.0f}"
    )

elif question == "Count Total Number of Records":

    st.subheader("Total Number of Records")

    cursor10 = conn.cursor()

    query10 = """
    SELECT COUNT(*) AS total_records
    FROM debt_data;
    """

    cursor10.execute(query10)

    record_count_result = cursor10.fetchone()

    st.metric(
        "Total Records",
        record_count_result[0]
    )


elif question == "Total Global Debt":

    st.subheader("Total Global Debt")

    cursor11 = conn.cursor()

    query11 = """
    SELECT SUM(value) AS total_global_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      );
    """

    cursor11.execute(query11)

    global_debt_result = cursor11.fetchone()

    st.metric(
        "Total Global Debt",
        f"${global_debt_result[0]:,.0f}"
    )


elif question == "List All Unique Indicator Names":

    st.subheader("All Unique Indicator Names")

    cursor12 = conn.cursor()

    query12 = """
    SELECT DISTINCT indicator_name
    FROM indicators
    ORDER BY indicator_name;
    """

    cursor12.execute(query12)

    indicator_results = cursor12.fetchall()

    for row in indicator_results:
        st.write(row[0])

elif question == "Number of Records for Each Country":

    st.subheader("Number of Records for Each Country")

    cursor13 = conn.cursor()

    query13 = """
    SELECT
        country_name,
        COUNT(*) AS total_records
    FROM debt_data
    WHERE country_code NOT IN (
        'EAP',
        'ECA',
        'IDA',
        'LAC',
        'LMY',
        'LMC',
        'MIC',
        'SSA',
        'UMC',
        'SAS',
        'IDX',
        'LDC',
        'MNA',
        'LIC'
    )
    GROUP BY country_name
    ORDER BY total_records DESC;
    """

    cursor13.execute(query13)

    country_record_results = cursor13.fetchall()

    for row in country_record_results:
        st.write(
            f"Country: {row[0]} | "
            f"Records: {row[1]}"
        )


##Intermediate Query #11 Find the total debt for each country.


elif question == "Total Debt for Each Country":

    st.subheader("Total Debt for Each Country")

    cursor15 = conn.cursor()

    query15 = """
    SELECT
        country_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY total_debt DESC;
    """

    cursor15.execute(query15)

    total_debt_results = cursor15.fetchall()

    for row in total_debt_results:
        st.write(
            f"Country: {row[0]} | "
            f"Total Debt: ${row[1]:,.0f}"
        )

#12.Find the top 10 countries with the highest total debt.

elif question == "Top 10 Countries by Total Debt":

    st.subheader("Top 10 Countries by Total Debt (2024)")

    cursor16 = conn.cursor()

    query16 = """
    SELECT
        country_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """

    cursor16.execute(query16)

    top_total_debt_results = cursor16.fetchall()

    for row in top_total_debt_results:
        st.write(
            f"Country: {row[0]} | "
            f"Total Debt: ${row[1]:,.0f}"
        )

#14.Calculate total debt for each indicator.


elif question == "Total Debt for Each Indicator":

    st.subheader("Total Debt for Each Indicator (2024)")

    cursor17 = conn.cursor()

    query17 = """
    SELECT
        series_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code LIKE 'DT.%'
      AND counterpart_area_name = 'World'
      AND year = 2024
    GROUP BY series_name
    ORDER BY total_debt DESC;
    """

    cursor17.execute(query17)

    indicator_debt_results = cursor17.fetchall()

    for row in indicator_debt_results:
        st.write(
            f"Indicator: {row[0]} | "
            f"Total Debt: ${row[1]:,.0f}"
        )



#15 — Identify the indicator contributing the highest total debt.

elif question == "Highest Contributing Indicator":

    st.subheader("Indicator Contributing the Highest Total Debt (2024)")

    cursor18 = conn.cursor()

    query18 = """
    SELECT
        series_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code LIKE 'DT.%'
      AND counterpart_area_name = 'World'
      AND year = 2024
    GROUP BY series_name
    ORDER BY total_debt DESC
    LIMIT 1;
    """

    cursor18.execute(query18)

    highest_indicator_result = cursor18.fetchone()

    if highest_indicator_result:
        st.write(
            f"Indicator: {highest_indicator_result[0]} | "
            f"Total Debt: ${highest_indicator_result[1]:,.0f}"
        )



#16 — Find the country with the lowest total debt.

elif question == "Country with Lowest Total Debt":

    st.subheader("Country with Lowest Total Debt (2024)")

    cursor19 = conn.cursor()

    query19 = """
    SELECT
        country_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY total_debt ASC
    LIMIT 1;
    """

    cursor19.execute(query19)

    lowest_debt_result = cursor19.fetchone()

    if lowest_debt_result:
        st.write(
            f"Country: {lowest_debt_result[0]} | "
            f"Total Debt: ${lowest_debt_result[1]:,.2f}"
        )
    else:
        st.warning("No records found.")


#17.Calculate total debt for each country and indicator combination.


elif question == "Total Debt by Country and Indicator":

    st.subheader("Total Debt by Country and Indicator (2024)")

    cursor20 = conn.cursor()

    query20 = """
    SELECT
        country_name,
        series_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code LIKE 'DT.%'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name, series_name
    ORDER BY total_debt DESC
    LIMIT 20;
    """

    cursor20.execute(query20)

    results20 = cursor20.fetchall()

    cursor20.close()

    if results20:
        import pandas as pd

        df20 = pd.DataFrame(
            results20,
            columns=["Country", "Indicator", "Total Debt"]
        )

        st.write("Showing the top 20 records")
        st.dataframe(
            df20,
            width="stretch",
            hide_index=True
        )

    else:
        st.warning("No records found.")


#18.Count how many indicators each country has.

elif question == "Number of Indicators per Country":

    st.subheader("Number of Indicators per Country")

    cursor21 = conn.cursor()

    query21 = """
    SELECT
        country_name,
        COUNT(DISTINCT series_name) AS indicator_count
    FROM debt_data
    WHERE country_code NOT IN (
        'EAP',
        'ECA',
        'IDA',
        'LAC',
        'LMY',
        'LMC',
        'MIC',
        'SSA',
        'UMC',
        'SAS',
        'IDX',
        'LDC',
        'MNA',
        'LIC'
    )
    GROUP BY country_name
    ORDER BY indicator_count DESC;
    """

    cursor21.execute(query21)

    indicator_country_results = cursor21.fetchall()

    if indicator_country_results:
        for row in indicator_country_results:
            st.write(
                f"Country: {row[0]} | "
                f"Indicators: {row[1]}"
            )
    else:
        st.warning("No records found.")

#19.Display countries whose total debt is above the global average.

elif question == "Countries Above Global Average Debt":

    st.subheader("Countries Above Global Average Debt (2024)")

    cursor22 = conn.cursor()

    query22 = """
    SELECT
        country_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    HAVING SUM(value) > (
        SELECT AVG(country_total)
        FROM (
            SELECT
                SUM(value) AS country_total
            FROM debt_data
            WHERE series_code = 'DT.DOD.DECT.CD'
              AND counterpart_area_name = 'World'
              AND year = 2024
              AND country_code NOT IN (
                  'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
                  'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
                  'IDX', 'LDC', 'MNA', 'LIC'
              )
            GROUP BY country_name
        ) AS country_totals
    )
    ORDER BY total_debt DESC;
    """

    cursor22.execute(query22)

    above_average_results = cursor22.fetchall()

    if above_average_results:
        for row in above_average_results:
            st.write(
                f"Country: {row[0]} | "
                f"Total Debt: ${row[1]:,.0f}"
            )
    else:
        st.warning("No countries found above the global average.")

#20.Rank countries based on total debt (highest to lowest).

elif question == "Rank Countries Based on Total Debt":

    st.subheader("Countries Ranked by Total Debt (2024)")

    cursor23 = conn.cursor()

    query23 = """
    SELECT
        country_name,
        SUM(value) AS total_debt,
        RANK() OVER (
            ORDER BY SUM(value) DESC
        ) AS debt_rank
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY debt_rank;
    """

    cursor23.execute(query23)
    ranking_results = cursor23.fetchall()

    if ranking_results:
        for row in ranking_results:
            st.write(
                f"Rank: {row[2]} | "
                f"Country: {row[0]} | "
                f"Total Debt: ${row[1]:,.0f}"
            )
    else:
        st.warning("No ranking results found.")

#21.Find the top 5 indicators contributing most to global debt.

elif question == "Top 5 Indicators by Total Debt":

    st.subheader("Top 5 Indicators by Total Debt (2024)")

    cursor24 = conn.cursor()

    query24 = """
    SELECT
        series_name,
        SUM(value) AS total_debt
    FROM debt_data
    WHERE series_code LIKE 'DT.%'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY series_name
    ORDER BY total_debt DESC
    LIMIT 5;
    """

    cursor24.execute(query24)
    top_indicator_results = cursor24.fetchall()

    if top_indicator_results:
        for rank, row in enumerate(top_indicator_results, start=1):
            st.write(
                f"Rank: {rank} | "
                f"Indicator: {row[0]} | "
                f"Total Debt: ${row[1]:,.0f}"
            )
    else:
        st.warning("No indicator results found.")

        
#22.Calculate percentage contribution of each country to total global debt.

elif question == "Country Percentage Contribution":

    st.subheader("Country Percentage Contribution to Global Debt (2024)")

    cursor25 = conn.cursor()

    query25 = """
    SELECT
        country_name,
        SUM(value) AS total_debt,
        ROUND(
            (
                SUM(value) * 100.0 /
                SUM(SUM(value)) OVER ()
            )::numeric,
            2
        ) AS percentage_contribution
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY percentage_contribution DESC;
    """

    cursor25.execute(query25)
    percentage_results = cursor25.fetchall()

    if percentage_results:
        for row in percentage_results:
            st.write(
                f"Country: {row[0]} | "
                f"Total Debt: ${row[1]:,.0f} | "
                f"Contribution: {row[2]}%"
            )
    else:
        st.warning("No country contribution results found.")

#23.Identify the top 3 countries for each indicator based on debt.

elif question == "Top 3 Countries per Indicator":

    st.subheader("Top 3 Countries per Indicator (2024)")

    cursor26 = conn.cursor()

    query26 = """
    WITH ranked_data AS (
        SELECT
            country_name,
            series_name,
            value,
            RANK() OVER (
                PARTITION BY series_name
                ORDER BY value DESC
            ) AS country_rank
        FROM debt_data
        WHERE series_code LIKE 'DT.%'
          AND counterpart_area_name = 'World'
          AND year = 2024
          AND country_code NOT IN (
              'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
              'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
              'IDX', 'LDC', 'MNA', 'LIC'
          )
    )
    SELECT
        country_name,
        series_name,
        value,
        country_rank
    FROM ranked_data
    WHERE country_rank <= 3
    ORDER BY series_name, country_rank;
    """

    cursor26.execute(query26)

    top3_results = cursor26.fetchall()

    if top3_results:
        for row in top3_results:
            st.write(
                f"Country: {row[0]} | "
                f"Indicator: {row[1]} | "
                f"Value: ${row[2]:,.2f} | "
                f"Rank: {row[3]}"
            )
    else:
        st.warning("No top 3 country results found.")

#24.Find the difference between maximum and minimum debt for each country.

elif question == "Difference Between Maximum and Minimum Debt":

    st.subheader("Difference Between Maximum and Minimum Debt (2000–2024)")

    cursor27 = conn.cursor()

    query27 = """
    SELECT
        country_name,
        MAX(value) AS maximum_debt,
        MIN(value) AS minimum_debt,
        MAX(value) - MIN(value) AS debt_difference
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year BETWEEN 2000 AND 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY country_name
    ORDER BY debt_difference DESC;
    """

    cursor27.execute(query27)

    difference_results = cursor27.fetchall()

    if difference_results:
        for row in difference_results:
            st.write(
                f"Country: {row[0]} | "
                f"Maximum Debt: ${row[1]:,.2f} | "
                f"Minimum Debt: ${row[2]:,.2f} | "
                f"Debt Difference: ${row[3]:,.2f}"
            )
    else:
        st.warning("No debt difference results found.")

#25. Top 10 Countries by Highest Debt
        
elif question == "Top 10 Countries Debt View":

    st.subheader("Top 10 Countries by External Debt (2024)")

    cursor28 = conn.cursor()

    query28 = """
    SELECT
        country_name,
        total_debt
    FROM top_10_countries_debt
    ORDER BY total_debt DESC;
    """

    cursor28.execute(query28)

    top10_view_results = cursor28.fetchall()

    if top10_view_results:
        for rank, row in enumerate(top10_view_results, start=1):
            st.write(
                f"Rank: {rank} | "
                f"Country: {row[0]} | "
                f"Total Debt: ${row[1]:,.2f}"
            )
    else:
        st.warning("No records found in the top 10 countries view.")


#26.Categorize countries into High / Medium / Low Debt based on thresholds.

elif question == "Debt Category (High / Medium / Low)":

    st.subheader("Debt Category by Country (2024)")

    cursor29 = conn.cursor()

    query29 = """
    SELECT
        country_name,
        value AS external_debt,
        CASE
            WHEN value >= 500000000000 THEN 'High Debt'
            WHEN value >= 100000000000 THEN 'Medium Debt'
            ELSE 'Low Debt'
        END AS debt_category
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    ORDER BY external_debt DESC;
    """

    cursor29.execute(query29)

    category_results = cursor29.fetchall()

    if category_results:
        for row in category_results:
            st.write(
                f"Country: {row[0]} | "
                f"External Debt: ${row[1]:,.2f} | "
                f"Category: {row[2]}"
            )
    else:
        st.warning("No debt category results found.")

#27.Use window functions to calculate cumulative debt per country.

elif question == "Cumulative Debt per Country":

    st.subheader("Cumulative Debt per Country")

    cursor30 = conn.cursor()

    query30 = """
    SELECT
        country_name,
        year,
        value AS external_debt,
        SUM(value) OVER (
            PARTITION BY country_name
            ORDER BY year
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_debt
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    ORDER BY country_name, year;
    """

    cursor30.execute(query30)

    cumulative_results = cursor30.fetchall()

    st.write(f"Total records: {len(cumulative_results):,}")

    for row in cumulative_results:
        st.write(
            f"Country: {row[0]} | "
            f"Year: {row[1]} | "
            f"External Debt: ${row[2]:,.0f} | "
            f"Cumulative Debt: ${row[3]:,.0f}"
        )

#28.Find indicators where average debt is higher than overall average debt.

elif question == "Indicators Above Overall Average Debt":

    st.subheader("Q28: Indicators Above Overall Average Debt")

    cursor31 = conn.cursor()

    query31 = """
    SELECT
        series_name,
        AVG(value) AS indicator_average_debt
    FROM debt_data
    WHERE series_code LIKE 'DT.%'
      AND counterpart_area_name = 'World'
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
    GROUP BY series_name
    HAVING AVG(value) > (
        SELECT AVG(value)
        FROM debt_data
        WHERE series_code LIKE 'DT.%'
          AND counterpart_area_name = 'World'
          AND country_code NOT IN (
              'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
              'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
              'IDX', 'LDC', 'MNA', 'LIC'
          )
    )
    ORDER BY indicator_average_debt DESC;
    """

    cursor31.execute(query31)

    indicator_results = cursor31.fetchall()

    st.write(f"Total indicators: {len(indicator_results):,}")

    for row in indicator_results:
        st.write(
            f"Indicator: {row[0]} | "
            f"Average Debt: ${row[1]:,.2f}"
        )

#29.Identify countries contributing more than 5% of global debt

elif question == "Countries Contributing More Than 5% of Global Debt":

    st.subheader("Countries Contributing More Than 5% of Global Debt")

    cursor32 = conn.cursor()

    query32 = """
    SELECT
        country_name,
        value AS external_debt,
        ROUND(
            (
                value / (
                    SELECT SUM(value)
                    FROM debt_data
                    WHERE series_code = 'DT.DOD.DECT.CD'
                      AND counterpart_area_name = 'World'
                      AND year = 2024
                      AND country_code NOT IN (
                          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
                          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
                          'IDX', 'LDC', 'MNA', 'LIC'
                      )
                )
            )::numeric * 100,
            2
        ) AS debt_percentage
    FROM debt_data
    WHERE series_code = 'DT.DOD.DECT.CD'
      AND counterpart_area_name = 'World'
      AND year = 2024
      AND country_code NOT IN (
          'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
          'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
          'IDX', 'LDC', 'MNA', 'LIC'
      )
      AND value > (
          SELECT SUM(value) * 0.05
          FROM debt_data
          WHERE series_code = 'DT.DOD.DECT.CD'
            AND counterpart_area_name = 'World'
            AND year = 2024
            AND country_code NOT IN (
                'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
                'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
                'IDX', 'LDC', 'MNA', 'LIC'
            )
      )
    ORDER BY debt_percentage DESC;
    """

    cursor32.execute(query32)

    contribution_results = cursor32.fetchall()

    st.write(f"Total countries: {len(contribution_results):,}")

    for row in contribution_results:
        st.write(
            f"Country: {row[0]} | "
            f"External Debt: ${row[1]:,.0f} | "
            f"Global Debt Contribution: {row[2]:.2f}%"
        )

#30.Find the most dominant indicator (highest contribution) for each country.

elif question == "Most Dominant Indicator for Each Country":

    st.subheader("Q30: Most Dominant Indicator for Each Country")

    cursor33 = conn.cursor()

    query33 = """
    WITH indicator_totals AS (
        SELECT
            country_name,
            series_name,
            SUM(value) AS total_value
        FROM debt_data
        WHERE year = 2024
          AND series_code LIKE 'DT.%'
          AND counterpart_area_name = 'World'
          AND country_code NOT IN (
              'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
              'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
              'IDX', 'LDC', 'MNA', 'LIC'
          )
        GROUP BY country_name, series_name
    ),
    ranked_indicators AS (
        SELECT
            country_name,
            series_name,
            total_value,
            ROW_NUMBER() OVER (
                PARTITION BY country_name
                ORDER BY total_value DESC, series_name ASC
            ) AS rank
        FROM indicator_totals
    )
    SELECT
        country_name,
        series_name,
        total_value AS dominant_indicator_value
    FROM ranked_indicators
    WHERE rank = 1
    ORDER BY country_name;
    """

    cursor33.execute(query33)

    dominant_results = cursor33.fetchall()

    st.write(f"Total countries: {len(dominant_results):,}")

    for row in dominant_results:
        st.write(
            f"Country: {row[0]} | "
            f"Dominant Indicator: {row[1]} | "
            f"Value: ${row[2]:,.0f}"
        )

