@echo off
echo Installing dependencies...
pip install -r backend\requirements.txt -q

echo.
echo Starting Geoscan UAV Planner on http://localhost:8001
echo Press Ctrl+C to stop.
echo.
cd backend
python main.py
