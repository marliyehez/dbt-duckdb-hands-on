{% macro dw_audit() %}
'{{ invocation_id }}'::VARCHAR AS dw_invocation_id,
CURRENT_TIMESTAMP AS dw_inserted_at
{% endmacro %}