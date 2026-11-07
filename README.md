# 🛒 Retail Sales Dashboard Using CSV and Matplotlib

A clean, functional, and beginner-friendly Retail Sales Dashboard developed for Python Programming coursework. The application reads retail transaction records from a CSV file, performs data aggregation and analysis using **Pandas**, renders interactive charts with **Matplotlib**, and presents everything via an intuitive **Streamlit** web user interface.

---

## 📌 1. Project Overview

This project was built to illustrate real-world Python data handling and visualization techniques without relying on complex enterprise frameworks or external databases.

### Core Objectives:
* **CSV File Handling**: Loading, reading, and gracefully validating structured data from local storage.
* **Data Wrangling with Pandas**: Cleaning, data type conversion, grouping, and aggregations.
* **Data Visualization with Matplotlib**: Creating clear, readable, and properly labeled analytical charts.
* **Interactive Dashboard with Streamlit**: Providing real-time filters and Key Performance Indicator (KPI) metrics.

---

## 🏗️ 2. Project Directory Structure

```text
retail-sales-dashboard/
│
├── app.py                      # Main Streamlit dashboard application
├── data/
│   └── retail_sales.csv        # Dataset containing 75 realistic retail transactions
├── requirements.txt            # Required Python libraries
├── README.md                   # Project documentation and guide
└── .gitignore                  # Git ignore rules for virtual environments & cache
```

---

## 📊 3. Dataset Description

The dataset is stored in `data/retail_sales.csv` and contains **75 realistic retail sales records** with the following schema:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Order ID`** | Integer | Unique identifier for each customer transaction |
| **`Date`** | Date (`YYYY-MM-DD`) | Date when the purchase was made (spans full year 2024) |
| **`Product`** | String | Name of the purchased item (e.g., Wireless Mouse, Office Chair) |
| **`Category`** | String | Product category (`Electronics`, `Furniture`, `Clothing`, etc.) |
| **`Quantity`** | Integer | Number of units purchased |
| **`Unit Price`** | Float | Price per individual unit in USD |
| **`Total Sales`** | Float | Computed total sale amount (`Quantity` × `Unit Price`) |
| **`Region`** | String | Sales territory (`North`, `South`, `East`, `West`) |

---

## ⚙️ 4. Technology Stack & Prerequisites

* **Python 3.9+** (Tested on Python 3.11)
* **Pandas**: Used for CSV reading, data frame operations, datetime parsing, and aggregations.
* **Matplotlib**: Used for plotting bar charts, line plots, and pie charts.
* **Streamlit**: Used for web-based dashboard rendering, KPI cards, sidebar filters, and data tables.

---

## 🚀 5. Installation & Execution Guide

### Step 1: Clone or Navigate to the Project Directory
```bash
cd retail-sales-dashboard
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Dashboard
```bash
streamlit run app.py
```

The application will launch automatically in your default web browser at `http://localhost:8501`.

---

## 📈 6. Dashboard Features & Visualizations Explained

### A. Top-Level KPI Summary Cards
* **Total Revenue**: Sum of all sales revenue (`Total Sales`) matching the active filters.
* **Total Orders**: Count of distinct transactions (`Order ID`).
* **Products Sold**: Cumulative count of items sold (`Quantity`).
* **Average Order Value (AOV)**: Average revenue per order (`Total Revenue / Total Orders`).

---

### B. Matplotlib Visualizations (2x2 Grid)

1. **Total Sales by Product Category (Horizontal Bar Chart)**:
   * **Purpose**: Compares total sales revenue across different product categories.
   * **Implementation**: Uses `df.groupby('Category')['Total Sales'].sum()`, plotted with `ax.barh()`. Direct value annotations appear on each bar for readability.

2. **Monthly Sales Trend (Line Chart)**:
   * **Purpose**: Displays the trajectory of revenue throughout the year to detect seasonality and growth.
   * **Implementation**: Dates are grouped by month using `df['Date'].dt.to_period('M')` and plotted via `ax.plot()` with distinct data markers (`o`) and currency annotations.

3. **Revenue Contribution by Category (Pie Chart)**:
   * **Purpose**: Shows the percentage share of each category relative to total sales.
   * **Implementation**: Uses `ax.pie()` with `autopct='%1.1f%%'`, contrasting segment colors, and custom white divider borders.

4. **Sales by Geographic Region (Vertical Bar Chart)**:
   * **Purpose**: Evaluates regional distribution of revenue across North, South, East, and West territories.
   * **Implementation**: Aggregates sales by region with `df.groupby('Region')` and displays bar heights with `ax.bar()`.

---

### C. Interactive Sidebar Filters
* **Date Range**: Allows filtering between any start and end date using a calendar date picker.
* **Region Filter**: Multiselect dropdown to focus on specific regions or compare multiple.
* **Category Filter**: Multiselect dropdown to inspect specific product lines.
* **Reset Filters Button**: Quickly resets all selections back to defaults.
* **Empty State Handling**: If no transactions match selected criteria, a helpful warning is displayed instead of crashing.

---

### D. Interactive Data Table & Export
* Formatted table displaying filtered transaction records with human-readable currency amounts.
* Interactive sorting by clicking any column header.
* **Download CSV Button**: Enables exporting filtered results to a local CSV file (`filtered_retail_sales.csv`).

---

## 🧠 7. Python Concepts Demonstrated

* **File Operations**: Verifying file paths using `os.path.exists()` and reading structured CSV data.
* **Pandas DataFrames**:
  * Filtering with Boolean masks (`&`, `|`, `.isin()`)
  * Data type conversions with `pd.to_datetime()` and `pd.to_numeric()`
  * Grouping and aggregation with `.groupby()`, `.sum()`, and `.nunique()`
* **Data Visualization**:
  * Object-oriented Matplotlib plotting (`fig, ax = plt.subplots()`)
  * Formatting spines, grids, tick labels, titles, and bar labels
  * Integrating figures seamlessly with Streamlit using `st.pyplot(fig)`
* **Modular Code Structure**:
  * Clean separation of concerns with distinct functions for data loading, KPI calculation, chart plotting, and application flow.
  * Caching dataset loading with `@st.cache_data` to ensure fast rendering.
* **Defensive Programming**:
  * `try-except` blocks to handle missing or malformed data files gracefully.

---

## 📸 8. Dashboard Screenshots

> *Placeholder: Add screenshots of the running dashboard below.*

### Dashboard Overview & KPI Metrics
![Dashboard Overview](docs/screenshots/dashboard_overview.png)
*(Displays top KPI metric cards and two-column Matplotlib analytical charts)*

### Interactive Filters & Data Exploration
![Filters & Table View](docs/screenshots/filters_and_table.png)
*(Shows sidebar filter controls and formatted interactive sales data table with CSV export)*


