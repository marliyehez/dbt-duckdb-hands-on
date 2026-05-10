{{ 
  config(
    materialized='incremental',
    unique_key='set_id',
  ) 
}}

SELECT
  set_id,
  log_id,
  event_timestamp,
  event_timestamp::DATE AS event_date,
  (event_timestamp + INTERVAL 7 HOUR)::DATE AS event_date_utc7,
  user_id,
  exercise_id,
  weight_kg,
  reps,
  volume_kg,
  {{ dw_audit() | indent(2, false) }}
FROM {{ ref('stg_workout_log') }}

{% if is_incremental() %}
WHERE (event_timestamp + INTERVAL 7 HOUR)::DATE = (CURRENT_DATE-INTERVAL 1 DAY)::DATE
{% endif %}