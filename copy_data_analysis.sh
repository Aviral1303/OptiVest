#!/bin/bash

# Make sure the target directories exist
mkdir -p dist/data_analysis

# Copy data_analysis directory to dist
cp -r data_analysis/* dist/data_analysis/

echo "Data analysis directory copied to dist/data_analysis/" 