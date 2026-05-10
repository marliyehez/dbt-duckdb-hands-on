{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set user_prefix = env_var('DBT_USER', 'anonymous') -%}

    {# 1. Extract folder name from the file path (e.g., 'silver' or 'gold') #}
    {%- set path_parts = node.path.split('/') -%}
    {%- set folder_name = path_parts[0] -%}

    {%- if target.name == 'prod' -%}
        {# 
           In Prod, use the folder name as the schema. 
           If the folder is 'gold', the schema becomes 'gold'.
        #}
        {{ folder_name | trim }}
    {%- else -%}
        {# In Development, everything stays in the dev schema #}
        dev_{{ user_prefix }}
    {%- endif -%}
{%- endmacro %}