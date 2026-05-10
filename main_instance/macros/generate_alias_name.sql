{% macro generate_alias_name(custom_alias_name, node) -%}
  
{# Get the folder path (e.g., 'silver/stg_users.sql') #}
{%- set path_parts = node.path.split('/') -%}
{# The first part of the path is the folder name (e.g., 'silver' or 'gold') #}
{%- set folder_name = path_parts[0] -%}

{%- if target.name == 'dev' -%}
  {# 
      In Dev mode, prefix the table name with the folder name.
      Format: silver__stg_users or gold__dim_users
  #}
  {{ folder_name }}__{{ custom_alias_name if custom_alias_name else node.name }}
{%- else -%}
  {# In Prod, keep the clean table name #}
  {{ custom_alias_name if custom_alias_name else node.name }}
{%- endif -%}

{%- endmacro %}