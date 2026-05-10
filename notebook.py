import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Explore dbt
    """)
    return


@app.cell
def _():
    import marimo as mo
    import duckdb

    # Create a DuckDB connection
    DEV_URL = ".storage/dev/dev_warehouse.duckdb"
    PROD_URL = ".storage/prod/prod_warehouse.duckdb"
    engine = duckdb.connect(PROD_URL)
    return engine, mo


@app.cell
def _():
    # To close the connection when using dbt
    # engine.close(); del engine;
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SHOW TABLES FROM prod_warehouse
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SHOW TABLES FROM prod_warehouse
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM dev_bobthebuilder.dim_exercise
        group by all
        ORDER BY 1
        -- WHERE event_date != event_date_utc7
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SHOW TABLES FROM dev_warehouse;


        DROP TABLE dev_bobthebuilder.dim_date;
        DROP TABLE dev_bobthebuilder.dim_exercise;
        DROP TABLE dev_bobthebuilder.dim_user;
        DROP TABLE dev_bobthebuilder.fact_workout_set;
        -- silver_stg_exercise
        -- silver_stg_user
        -- silver_stg_workout_log
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        WITH t1 AS (
        	SELECT DATE('2026-01-01') AS col1
        )

        select col1, (col1 + INTERVAL 1 YEAR)::DATE AS col2, CURRENT_DATE
        from t1
        """
    )
    return


if __name__ == "__main__":
    app.run()
