"""
Retail Sales Dashboard
-----------------------
A beginner-friendly data analysis and visualization dashboard built with
Streamlit, Pandas, and Matplotlib for Python Programming coursework.

Author: Student
Course: Python Programming
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal CSS for clean, modern cards and readable layout
st.markdown("""
    <style>
        /* General page layout padding */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        /* Metric card styling */
        div[data-testid="stMetric"] {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 14px 18px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        /* Metric labels */
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.9rem;
            color: #6c757d;
            font-weight: 500;
        }
        /* Metric values */
        div[data-testid="stMetricValue"] > div {
            font-size: 1.5rem;
            color: #212529;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads retail sales dataset from a CSV file and converts columns
    to appropriate data types for analysis.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    # Read CSV using pandas
    df = pd.read_csv(file_path)

    # Convert Date column to datetime format for time-series filtering & plotting
    df['Date'] = pd.to_datetime(df['Date'])

    # Ensure numeric types
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce').fillna(0.0)
    df['Total Sales'] = pd.to_numeric(df['Total Sales'], errors='coerce').fillna(0.0)

    return df


# ==========================================
# 3. KPI DISPLAY FUNCTION
# ==========================================
def display_kpis(df: pd.DataFrame):
    """
    Calculates and displays top-level Key Performance Indicators (KPIs).
    """
    total_revenue = df['Total Sales'].sum()
    total_orders = df['Order ID'].nunique()
    total_units_sold = df['Quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        st.metric("Total Orders", f"{total_orders:,}")
    with col3:
        st.metric("Products Sold", f"{total_units_sold:,}")
    with col4:
        st.metric("Avg Order Value", f"${avg_order_value:,.2f}")


# ==========================================
# 4. DATA VISUALIZATION FUNCTIONS (MATPLOTLIB)
# ==========================================
def plot_sales_by_category(df: pd.DataFrame):
    """
    Chart 1: Horizontal Bar Chart - Total Sales by Product Category
    """
    # Group data by category and sum sales
    category_sales = df.groupby('Category')['Total Sales'].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(category_sales.index, category_sales.values, color='#4A90E2', edgecolor='#2B6CB0')

    # Add data labels inside/beside bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + (category_sales.values.max() * 0.01), bar.get_y() + bar.get_height() / 2,
                f'${width:,.0f}', va='center', ha='left', fontsize=9, color='#333333', fontweight='500')

    ax.set_title("Total Sales by Product Category", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Sales Revenue ($)", fontsize=10)
    ax.set_ylabel("Category", fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


def plot_monthly_sales_trend(df: pd.DataFrame):
    """
    Chart 2: Line Chart - Monthly Sales Trend over time
    """
    # Create Year-Month column for aggregation
    temp_df = df.copy()
    temp_df['YearMonth'] = temp_df['Date'].dt.to_period('M')
    monthly_sales = temp_df.groupby('YearMonth')['Total Sales'].sum()

    # Convert period index to string for plotting
    x_labels = [str(period) for period in monthly_sales.index]
    y_values = monthly_sales.values

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x_labels, y_values, marker='o', linewidth=2.2, color='#2E7D32', markersize=6)

    # Add value annotations
    for i, txt in enumerate(y_values):
        ax.annotate(f"${txt:,.0f}", (x_labels[i], y_values[i]),
                    textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8)

    ax.set_title("Monthly Sales Trend", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Month", fontsize=10)
    ax.set_ylabel("Sales Revenue ($)", fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


def plot_revenue_pie(df: pd.DataFrame):
    """
    Chart 3: Pie Chart - Revenue Contribution by Category
    """
    category_sales = df.groupby('Category')['Total Sales'].sum()

    colors = ['#4A90E2', '#50E3C2', '#F5A623', '#9013FE', '#E94E77']
    fig, ax = plt.subplots(figsize=(6, 4))

    wedges, texts, autotexts = ax.pie(
        category_sales.values,
        labels=category_sales.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors[:len(category_sales)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )

    # Style percentage text inside wedges
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')

    for text in texts:
        text.set_fontsize(9)

    ax.set_title("Revenue Contribution by Category", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    return fig


def plot_sales_by_region(df: pd.DataFrame):
    """
    Chart 4: Vertical Bar Chart - Sales Revenue by Region
    """
    region_sales = df.groupby('Region')['Total Sales'].sum().sort_values(ascending=False)

    colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(region_sales.index, region_sales.values, color=colors[:len(region_sales)], edgecolor='#1E3A8A', width=0.55)

    # Add data label on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='500')

    ax.set_title("Sales by Geographic Region", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Region", fontsize=10)
    ax.set_ylabel("Sales Revenue ($)", fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


# ==========================================
# 5. MAIN APPLICATION
# ==========================================
def main():
    # Header
    st.title("📊 Retail Sales Performance Dashboard")
    st.markdown("An interactive sales analytics dashboard using **Python**, **Pandas**, and **Matplotlib**.")
    st.write("---")

    # Locate dataset
    data_path = os.path.join(os.path.dirname(__file__), "data", "retail_sales.csv")

    try:
        raw_df = load_data(data_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.info("Please make sure 'retail_sales.csv' is placed inside the 'data/' folder.")
        return

    # ------------------------------------------
    # SIDEBAR: INTERACTIVE FILTERS
    # ------------------------------------------
    st.sidebar.header("🔍 Filter Options")
    st.sidebar.markdown("Use the controls below to filter dashboard data:")

    # 1. Date Range Filter
    min_date = raw_df['Date'].min().date()
    max_date = raw_df['Date'].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 2. Region Filter (Multiselect)
    all_regions = sorted(raw_df['Region'].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=all_regions,
        default=all_regions
    )

    # 3. Category Filter (Multiselect)
    all_categories = sorted(raw_df['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Product Category",
        options=all_categories,
        default=all_categories
    )

    # Quick Reset button in sidebar
    if st.sidebar.button("Reset All Filters"):
        st.rerun()

    # Apply filters to dataframe
    filtered_df = raw_df.copy()

    # Filter by Date
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) &
            (filtered_df['Date'].dt.date <= end_date)
        ]
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        # User selected just one date so far
        filtered_df = filtered_df[filtered_df['Date'].dt.date == date_range[0]]

    # Filter by Region
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    else:
        filtered_df = filtered_df.iloc[0:0]  # empty if nothing selected

    # Filter by Category
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
    else:
        filtered_df = filtered_df.iloc[0:0]  # empty if nothing selected

    # ------------------------------------------
    # EMPTY STATE HANDLING
    # ------------------------------------------
    if filtered_df.empty:
        st.warning("⚠️ No sales records found matching the selected filters. Please adjust your filters in the sidebar.")
        return

    # ------------------------------------------
    # SECTION 1: TOP KPI CARDS
    # ------------------------------------------
    display_kpis(filtered_df)
    st.write("")

    # ------------------------------------------
    # SECTION 2: CHARTS (2x2 GRID)
    # ------------------------------------------
    st.subheader("📈 Sales Analytics & Trends")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_sales_by_category(filtered_df))
    with col2:
        st.pyplot(plot_monthly_sales_trend(filtered_df))

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(plot_revenue_pie(filtered_df))
    with col4:
        st.pyplot(plot_sales_by_region(filtered_df))

    st.write("---")

    # ------------------------------------------
    # SECTION 3: SALES DATA TABLE
    # ------------------------------------------
    st.subheader("📋 Sales Records Data Table")
    st.markdown(f"Displaying **{len(filtered_df)}** of **{len(raw_df)}** records based on active filters.")

    # Format dataframe for clean display
    display_df = filtered_df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Unit Price'] = display_df['Unit Price'].map('${:,.2f}'.format)
    display_df['Total Sales'] = display_df['Total Sales'].map('${:,.2f}'.format)

    # Streamlit dataframe with search and sorting enabled
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Download button for filtered CSV data
    csv_export = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_export,
        file_name="filtered_retail_sales.csv",
        mime="text/csv"
    )


if __name__ == '__main__':
    main()

