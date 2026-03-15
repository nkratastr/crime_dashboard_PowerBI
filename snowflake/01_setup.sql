-- Snowflake setup script: database, warehouse en schemas
-- Uitvoeren als ACCOUNTADMIN

USE ROLE ACCOUNTADMIN;

-- Warehouse
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Database
CREATE DATABASE IF NOT EXISTS CRIME_DB;

USE DATABASE CRIME_DB;

-- Schemas
CREATE SCHEMA IF NOT EXISTS RAW;       -- ruwe CBS data
CREATE SCHEMA IF NOT EXISTS STAGING;   -- dbt staging modellen
CREATE SCHEMA IF NOT EXISTS MARTS;     -- dbt eindmodellen voor Power BI
