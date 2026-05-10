{{
  config(
    materialized='table',
  )
}}

SELECT
  user_id,
  user_name,
  email,
  country,
  membership_level,
  is_active,
  created_at as created_timestamp,
  updated_at as last_updated_timestamp,
  {{ dw_audit() | indent(2, false) }}
FROM {{ ref('stg_user') }}
WHERE created_at::DATE <= (current_date - interval 1 day)::DATE
QUALIFY row_number() over (partition by user_id order by updated_at desc) = 1
