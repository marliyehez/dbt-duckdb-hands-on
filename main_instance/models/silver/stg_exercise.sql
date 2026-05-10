{{
  config(
    materialized='view'
  )
}}

SELECT
  regexp_extract(exercise_id::VARCHAR, '\d+')::INTEGER as exercise_id,
  exercise_name::VARCHAR AS exercise_name,
  category::VARCHAR AS category,
  muscle_group::VARCHAR AS muscle_group,
  {{ dw_audit() | indent(2, false) }}
FROM {{ source('bronze.main_source', 'raw_exercise') }}
