# Air Quality Dashboard 🌍

A web-based interactive dashboard for visualizing and exploring air quality data across different regions and time periods. Built with Python, Dash, and Plotly.

## 🚀 Features

- 📈 Line charts of air quality indicators over time
- 🗺️ Interactive maps showing pollutant levels by station
- 🔄 Change detection between years
- 📊 Station-level data exploration
- 💾 Fast data loading using Parquet files

## 📁 Project Structure

```
├── app.py # Main entry point for the dashboard
├── layout.py # Dash layout and structure
├── callbacks.py # Dash callback functions
├── data_loader.py # Handles loading and preprocessing data
├── convert_csv_to_parquet.py # Utility to convert CSV files to Parquet
├── main_page_plot.py # bar chart and station map 2018
├── plot_change_map.py # bar chart change
├── plot_line_chart.py # line chart 
├── plot_station_map.py # station map
├── assets/
│ └── styles.css # Custom CSS for styling
├── data/
│ └── *.parquet # Cleaned and compressed air quality data
└── README.md # Project description and usage
```

## ⚙️ Setup Instructions

1. **Clone the repo:**
  ```bash
   git clone https://github.com/thientruc1691997/air_quality_dashboard.git
   cd air_quality_dashboard
  ```

2. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```


3. **Run app:**
   
  ```bash
  python app.py
  ```
