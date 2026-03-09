#!/usr/bin/env bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Build frontend
cd frontend
npm ci
npm run build
