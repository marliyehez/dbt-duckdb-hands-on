{{ 
  config(
    materialized='view'
  ) 
}}

WITH
raw_source AS (
  SELECT * FROM {{ source('bronze.main_source', 'raw_log') }}
),

flattened AS (
  SELECT
    log_id,
    user_id,
    regexp_extract(exercise_id, '\d+')::INTEGER as exercise_id,
    exercise_name,
    timestamp::TIMESTAMP AS event_timestamp,
    UNNEST(sets) AS set_data
  FROM raw_source
)

SELECT
  -- Create a unique ID for each set
  hash(log_id || (set_data->>'weight_kg') || (set_data->>'reps')) AS set_id,
  log_id,
  user_id,
  exercise_id,
  exercise_name,
  event_timestamp,
  (set_data->>'weight_kg')::FLOAT AS weight_kg,
  (set_data->>'reps')::INTEGER AS reps,
  ((set_data->>'weight_kg')::FLOAT * (set_data->>'reps')::INTEGER) AS volume_kg,
  {{ dw_audit() | indent(2, false) }}
FROM flattened