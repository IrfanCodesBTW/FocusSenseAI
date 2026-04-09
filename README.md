# FocusSense AI

FocusSense AI is a Python-based application that tracks a user's focus and emotions in real-time using their webcam. It provides an analyzer and a dashboard to visualize focus trends, session breakdowns, and emotion distribution.

## Features

- **Real-Time Tracking**: Uses OpenCV and DeepFace to detect faces and analyze emotions.
- **Focus Detection**: Determines if the user is focused based on head position relative to the screen center.
- **Data Logging**: Records focus state and emotions periodically into CSV files.
- **Analyzer App**: A command-line interface to view daily summaries, session trends, and personalized recommendations.
- **Dashboard**: A comprehensive CLI dashboard to visualize data with pie charts and insightful metrics.

## Installation

### Requirements
- Python 3.8+
- Webcam

### Setup Instructions

For Windows PowerShell:

```powershell
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

*Note: If PowerShell blocks the execution of the activation script, you can temporarily bypass the policy:*
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Usage

Start by running the tracker to collect data:

```powershell
python tracker.py
```
Press `Q` to stop tracking.

Once you have recorded some sessions, you can use the analyzer or the dashboard to review your statistics:

```powershell
python analyzer.py
# OR
python dashboard.py
```

## Project Structure

- `tracker.py` - Main script for webcam tracking and data collection.
- `analyzer.py` - CLI tool for analyzing trends and getting recommendations.
- `dashboard.py` - Visual dashboard with MATPLOTLIB charts.
- `haarcascade_frontalface_alt.xml` - Model weights for face detection.
- `data/` - Directory where session logs are saved.

## Contributing

Feel free to open issues or submit pull requests.
