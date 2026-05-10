{{
  config(
    materialized='table',
  )
}}

SELECT
  exercise_id,
  exercise_name,
  category,
  muscle_group,
  {{ dw_audit() | indent(2, false) }}
FROM {{ ref('stg_exercise') }}