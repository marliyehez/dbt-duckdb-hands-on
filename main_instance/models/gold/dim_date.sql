{{
  config(
    materialized='view',
  )
}}

WITH
date_spine AS (
  SELECT range::DATE AS date
  FROM range(
    DATE('2025-01-01'),
    (CURRENT_DATE + INTERVAL 1 YEAR)::DATE, 
    INTERVAL 1 DAY
  )
)

SELECT
  date,
  extract('quarter' from date) AS quarter,
  monthname(date) AS month_name,
  week(date) AS week_of_year,
  dayname(date) AS day_name,
  dayofweek(date) AS day_of_week,
  CASE 
    WHEN dayofweek(date) IN (0, 6) THEN TRUE 
    ELSE FALSE 
  END AS is_weekend,
  {{ dw_audit() | indent(2, false) }}
FROM date_spine