SELECT
    country_code,
    country_name,
    region,
    income_group
FROM countries
LIMIT 20;


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
ORDER BY d.value DESC
LIMIT 10;


SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT country_code) AS unique_codes,
    COUNT(*) FILTER (WHERE region IS NULL) AS region_null,
    COUNT(*) FILTER (WHERE income_group IS NULL) AS income_group_null
FROM countries;



SELECT
    country_code,
    country_name
FROM countries
WHERE country_code IN ('LMY', 'MIC', 'UMC', 'EAP', 'LMC', 'LAC', 'IDA', 'ECA', 'SSA');



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
      'UMC'
  )
ORDER BY d.value DESC
LIMIT 10;


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
ORDER BY d.value DESC
LIMIT 10;


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
      'MNA'
  )
ORDER BY d.value DESC
LIMIT 10;


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

--Basic Queries

--1.Retrieve all distinct country names from the dataset.

SELECT DISTINCT country_name
FROM countries
ORDER BY country_name;

SELECT DISTINCT country_name
FROM countries
WHERE country_code NOT IN (
    'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
    'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
    'IDX', 'LDC', 'MNA', 'LIC'
)
ORDER BY country_name;

---Q2 — Total number of countries

SELECT COUNT(DISTINCT country_code) AS total_countries
FROM countries
WHERE country_code NOT IN (
    'EAP','ECA','IDA','LAC','LMY','LMC','MIC','SSA',
    'UMC','SAS','IDX','LDC','MNA','LIC'
);

--Q3 — Total number of indicators

SELECT COUNT(DISTINCT indicator_code) AS total_indicators
FROM indicators;

--Q4 — First 10 records

SELECT *
FROM debt_data
LIMIT 10;

-- Basic Question 5: Calculate the total global debt
SELECT
    SUM(value) AS total_global_debt
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World'
  AND year = 2024
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  );

--Q6.How many indicators are present in the dataset?

SELECT *
FROM indicators
LIMIT 5;


SELECT COUNT(DISTINCT indicator_code) AS total_indicators
FROM indicators;


--Q4 — First 10 records

SELECT *
FROM debt_data
LIMIT 10;

--Q8.Which records have an external debt value greater than $1 billion?

SELECT *
FROM debt_data
WHERE value > 1000000000;


--Q9 — Minimum, Maximum, and Average Debt Values

SELECT
    MIN(value) AS minimum_debt,
    MAX(value) AS maximum_debt,
    AVG(value) AS average_debt
FROM debt_data;

--Q10.How many total records are stored in the debt_data table?

SELECT COUNT(*) AS total_records
FROM debt_data;

---Total Global Debt

SELECT SUM(value) AS total_global_debt
FROM debt_data;

---List all unique indicator names

SELECT DISTINCT indicator_name
FROM indicators
ORDER BY indicator_name;

---Q7.Find the number of records for each country.

SELECT
    country_name,
    COUNT(*) AS total_records
FROM debt_data
GROUP BY country_name
ORDER BY total_records DESC;

--aggregate groups such as Middle income and Europe & Central Asia will disappear.
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


-- Q8: Which records have a debt value greater than $1 billion?

SELECT *
FROM debt_data
WHERE value > 1000000000;

--------
--#9.Find the minimum, maximum, and average debt values.

SELECT
    MIN(value) AS minimum_debt,
    MAX(value) AS maximum_debt,
    AVG(value) AS average_debt
FROM debt_data;

--Intermediate #1

-- Question 11: Find the total debt for each country

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

-- Question 12: Top 10 countries with highest total debt

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

-- Question 13: Find the average debt per country
-- Question 13: Find the average debt per country

SELECT
    country_name,
    AVG(value) AS average_debt
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World'
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  )
GROUP BY country_name
ORDER BY average_debt DESC;


--14.Calculate total debt for each indicator.


-- Question 14: Calculate total debt for each indicator

SELECT
    series_name,
    SUM(value) AS total_debt
FROM debt_data
WHERE series_code LIKE 'DT.%'
  AND counterpart_area_name = 'World'
  AND year = 2024
GROUP BY series_name
ORDER BY total_debt DESC;

-- Question 15: Identify the indicator contributing the highest total debt

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

--16.Find the country with the lowest total debt.

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

--q17.Calculate total debt for each country and indicator combination.

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
ORDER BY total_debt DESC;

--18.Count how many indicators each country has.

SELECT
    country_name,
    COUNT(DISTINCT series_name) AS indicator_count
FROM debt_data
WHERE country_code NOT IN (
    'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
    'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
    'IDX', 'LDC', 'MNA', 'LIC'
)
GROUP BY country_name
ORDER BY indicator_count DESC;

--19.Display countries whose total debt is above the global average.

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

--20.Rank countries based on total debt (highest to lowest).

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

---Advanced Question 

--#21.Find the top 5 indicators contributing most to global debt.

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

--22.Calculate percentage contribution of each country to total global debt.

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

--23.Identify the top 3 countries for each indicator based on debt.

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


---24.Find the difference between maximum and minimum debt for each country.
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

--25.Create a view for the top 10 countries with the highest debt.

CREATE OR REPLACE VIEW top_10_countries_debt AS
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

SELECT *
FROM top_10_countries_debt;

--26.Categorize countries into High / Medium / Low Debt based on thresholds.

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


--27.Use window functions to calculate cumulative debt per country.

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

--Verify one country

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
WHERE country_name = 'China'
  AND series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World'
ORDER BY year;
-- Q28: Indicators with average debt above overall average debt

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

---Check the overall average

SELECT
    AVG(value) AS overall_average_debt
FROM debt_data
WHERE series_code LIKE 'DT.%'
  AND counterpart_area_name = 'World'
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  );

--Q29 — Find countries contributing more than 5% of global debt.

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

--30.Find the most dominant indicator (highest contribution) for each country.

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

-----

SELECT
    SUM(value) AS total_debt_2024
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_code = 'WLD'
  AND year = 2024
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  );

-------
--Primary Key & Foreign Key Verification
SELECT
    tc.table_name,
    tc.constraint_type,
    kcu.column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
    AND tc.table_name = kcu.table_name
WHERE tc.table_schema = 'public'
  AND tc.table_name IN (
      'countries',
      'indicators',
      'debt_data'
  )
  AND tc.constraint_type IN (
      'PRIMARY KEY',
      'FOREIGN KEY'
  )
ORDER BY tc.table_name, tc.constraint_type;

-----
--Verify foreign key relationships

SELECT
    tc.table_name AS source_table,
    kcu.column_name AS source_column,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON tc.constraint_name = ccu.constraint_name
    AND tc.table_schema = ccu.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name = 'debt_data';

-------
--Check database normalization


SELECT
    'countries' AS table_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT country_code) AS unique_codes
FROM countries

UNION ALL

SELECT
    'indicators' AS table_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT indicator_code) AS unique_codes
FROM indicators;

----
--Verify data insertion


SELECT COUNT(*) AS total_debt_records
FROM debt_data;

--Check SQL query performance

EXPLAIN ANALYZE
SELECT country_name, SUM(value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;

---PostgreSQL Index Verification

SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('countries', 'indicators', 'debt_data')
ORDER BY tablename, indexname;

--Check query performance for a common filter


EXPLAIN ANALYZE
SELECT country_name, value
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND year = 2024
ORDER BY value DESC
LIMIT 10;

--Create an index

CREATE INDEX IF NOT EXISTS idx_debt_series_year
ON debt_data (series_code, year);

--Compare SQL performance

EXPLAIN ANALYZE
SELECT country_name, value
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND year = 2024
ORDER BY value DESC
LIMIT 10;

---
SELECT
    series_code,
    series_name
FROM debt_data
WHERE series_code LIKE 'DT.%'
GROUP BY series_code, series_name
ORDER BY series_code
LIMIT 20;


SELECT *
FROM top_10_countries_debt
ORDER BY total_debt DESC;


SELECT
    SUM(value) AS total_external_debt_2024
FROM debt_data
WHERE series_code = 'DT.DOD.DECT.CD'
  AND counterpart_area_name = 'World'
  AND year = 2024
  AND country_code NOT IN (
      'EAP', 'ECA', 'IDA', 'LAC', 'LMY',
      'LMC', 'MIC', 'SSA', 'UMC', 'SAS',
      'IDX', 'LDC', 'MNA', 'LIC'
  );













