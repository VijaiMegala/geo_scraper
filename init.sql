-- CREATE DATABASE geospatial_data;

\c geospatial_data;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS geo_features (
    id SERIAL PRIMARY KEY,
    feature_id TEXT UNIQUE NOT NULL,
    properties JSONB,
    geom GEOMETRY(POLYGON, 4326) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_geo_features_geom 
ON geo_features USING GIST (geom);
