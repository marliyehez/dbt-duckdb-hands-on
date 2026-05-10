{{
  config(
    materialized='view'
  )
}}

SELECT
  user_id,
  user_name,
  email,
  country,
  upper(membership_level) as membership_level,
  created_at::timestamp as created_at,
  updated_at::timestamp as updated_at,
  case
    when lower(is_active) in ('true', 'active') then true
    else false
  end as is_active,
  {{ dw_audit() | indent(2, false) }}
FROM {{ source('bronze.main_source', 'raw_user') }}