import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DVD Rental Business Intelligence",
    page_icon="🎬",
    layout="wide"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    film = pd.read_csv("film_master_clean.csv")
    category = pd.read_csv("category_performance.csv")
    customer = pd.read_csv("customer.csv")
    monthly = pd.read_csv("monthly_clean.csv")
    staff = pd.read_csv("staff.csv")
    store = pd.read_csv("store_performance.csv")
    geographic = pd.read_csv("geographic.csv")
    inventory = pd.read_csv("inventory.csv")

    return (
        film,
        category,
        customer,
        monthly,
        staff,
        store,
        geographic,
        inventory
    )


(
    film,
    category,
    customer,
    monthly,
    staff,
    store,
    geographic,
    inventory
) = load_data()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def show_metric(label, value):
    """
    Display one KPI metric.
    """
    st.metric(
        label=label,
        value=value
    )


def create_bar_chart(
    data,
    x,
    y,
    title,
    x_title=None,
    y_title=None,
    horizontal=False
):
    """
    Create a reusable Plotly bar chart.
    """

    if horizontal:
        fig = px.bar(
            data,
            x=x,
            y=y,
            orientation="h",
            title=title
        )
    else:
        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title
        )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def create_line_chart(
    data,
    x,
    y,
    title,
    x_title=None,
    y_title=None
):
    """
    Create a reusable Plotly line chart.
    """

    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("DVD Rental BI")

page = st.sidebar.selectbox(
    "Navigate",
    [
        "Overview",
        "Film & Category",
        "Customers",
        "Time Trends",
        "Store & Staff",
        "Geographic",
        "Inventory"
    ]
)


# ==========================================
# PAGE 1 — OVERVIEW
# ==========================================

if page == "Overview":

    st.title("Business Overview")

    st.write(
        "A high-level view of DVD rental business performance."
    )

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_revenue = film["total_rental_revenue"].sum()
    total_rentals = film["total_rentals"].sum()
    total_customers = customer["customer_id"].nunique()
    total_films = film["film_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Total Revenue",
            f"${total_revenue:,.2f}"
        )

    with col2:
        show_metric(
            "Total Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Unique Customers",
            f"{total_customers:,}"
        )

    with col4:
        show_metric(
            "Total Films",
            f"{total_films:,}"
        )

    st.divider()

    # --------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------

    st.subheader("Monthly Revenue")

    create_line_chart(
        monthly,
        x="date",
        y="total_revenue",
        title="Monthly Revenue Trend",
        x_title="Month",
        y_title="Revenue"
    )

    # --------------------------------------
    # MONTHLY RENTALS
    # --------------------------------------

    st.subheader("Monthly Rentals")

    create_line_chart(
        monthly,
        x="date",
        y="total_rentals",
        title="Monthly Rental Trend",
        x_title="Month",
        y_title="Rentals"
    )


# ==========================================
# PAGE 2 — FILM & CATEGORY
# ==========================================

elif page == "Film & Category":

    # --------------------------------------
    # PAGE-SPECIFIC SIDEBAR FILTER
    # --------------------------------------

    st.sidebar.header("Film Filters")

    categories = sorted(
        film["category"]
        .dropna()
        .unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Film Category",
        options=categories,
        default=categories
    )

    # Apply filter

    filtered_film = film[
        film["category"].isin(selected_categories)
    ]

    filtered_category = category[
        category["category"].isin(selected_categories)
    ]

    # --------------------------------------
    # PAGE TITLE
    # --------------------------------------

    st.title("Film & Category Performance")

    st.write(
        "Analyze film revenue, rental demand, and category performance."
    )

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_revenue = filtered_film[
        "total_rental_revenue"
    ].sum()

    total_rentals = filtered_film[
        "total_rentals"
    ].sum()

    number_of_films = filtered_film[
        "film_id"
    ].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

    with col2:
        show_metric(
            "Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Films",
            f"{number_of_films:,}"
        )

    st.divider()

    # --------------------------------------
    # TOP FILMS BY REVENUE
    # --------------------------------------

    st.subheader("Top 10 Films by Revenue")

    top_revenue = (
        filtered_film
        .sort_values(
            "total_rental_revenue",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        top_revenue,
        x="total_rental_revenue",
        y="film_title",
        title="Top 10 Films by Rental Revenue",
        x_title="Revenue",
        y_title="Film",
        horizontal=True
    )

    # --------------------------------------
    # TOP FILMS BY RENTALS
    # --------------------------------------

    st.subheader("Top 10 Films by Rentals")

    top_rentals = (
        filtered_film
        .sort_values(
            "total_rentals",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        top_rentals,
        x="total_rentals",
        y="film_title",
        title="Top 10 Most Rented Films",
        x_title="Rentals",
        y_title="Film",
        horizontal=True
    )

    # --------------------------------------
    # CATEGORY REVENUE
    # --------------------------------------

    st.subheader("Revenue by Category")

    category_revenue = filtered_category.sort_values(
        "total_revenue",
        ascending=True
    )

    create_bar_chart(
        category_revenue,
        x="total_revenue",
        y="category",
        title="Revenue by Film Category",
        x_title="Revenue",
        y_title="Category",
        horizontal=True
    )

    # --------------------------------------
    # CATEGORY RENTALS
    # --------------------------------------

    st.subheader("Rentals by Category")

    category_rentals = filtered_category.sort_values(
        "total_rentals",
        ascending=True
    )

    create_bar_chart(
        category_rentals,
        x="total_rentals",
        y="category",
        title="Rentals by Film Category",
        x_title="Rentals",
        y_title="Category",
        horizontal=True
    )


# ==========================================
# PAGE 3 — CUSTOMERS
# ==========================================

elif page == "Customers":

    # --------------------------------------
    # PAGE-SPECIFIC SIDEBAR FILTERS
    # --------------------------------------

    st.sidebar.header("Customer Filters")

    countries = sorted(
        customer["country"]
        .dropna()
        .unique()
    )

    selected_countries = st.sidebar.multiselect(
        "Country",
        options=countries,
        default=countries
    )

    filtered_customer = customer[
        customer["country"].isin(selected_countries)
    ]

    # City filter depends on selected countries

    cities = sorted(
        filtered_customer["city"]
        .dropna()
        .unique()
    )

    selected_cities = st.sidebar.multiselect(
        "City",
        options=cities,
        default=cities
    )

    filtered_customer = filtered_customer[
        filtered_customer["city"].isin(selected_cities)
    ]

    # --------------------------------------
    # PAGE TITLE
    # --------------------------------------

    st.title("Customer Analysis")

    st.write(
        "Analyze customer spending, rental activity, and customer behavior."
    )

    # --------------------------------------
    # CUSTOMER KPIs
    # --------------------------------------

    total_customers = filtered_customer[
        "customer_id"
    ].nunique()

    total_spending = filtered_customer[
        "total_amount_spent"
    ].sum()

    total_rentals = filtered_customer[
        "total_rentals"
    ].sum()

    average_spending = (
        filtered_customer["total_amount_spent"].mean()
        if len(filtered_customer) > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Customers",
            f"{total_customers:,}"
        )

    with col2:
        show_metric(
            "Total Spending",
            f"${total_spending:,.2f}"
        )

    with col3:
        show_metric(
            "Total Rentals",
            f"{total_rentals:,}"
        )

    with col4:
        show_metric(
            "Average Customer Spend",
            f"${average_spending:,.2f}"
        )

    st.divider()

    # --------------------------------------
    # TOP CUSTOMERS BY SPENDING
    # --------------------------------------

    st.subheader("Top 10 Customers by Spending")

    top_spenders = (
        filtered_customer
        .sort_values(
            "total_amount_spent",
            ascending=False
        )
        .head(10)
    )

    top_spenders["customer_name"] = (
        top_spenders["full_name"]
    )

    create_bar_chart(
        top_spenders,
        x="total_amount_spent",
        y="customer_name",
        title="Top 10 Customers by Total Spending",
        x_title="Amount Spent",
        y_title="Customer",
        horizontal=True
    )

    # --------------------------------------
    # TOP CUSTOMERS BY RENTALS
    # --------------------------------------

    st.subheader("Top 10 Customers by Rentals")

    top_renters = (
        filtered_customer
        .sort_values(
            "total_rentals",
            ascending=False
        )
        .head(10)
    )

    top_renters["customer_name"] = (
        top_renters["full_name"]
    )

    create_bar_chart(
        top_renters,
        x="total_rentals",
        y="customer_name",
        title="Top 10 Customers by Rental Activity",
        x_title="Rentals",
        y_title="Customer",
        horizontal=True
    )

    # --------------------------------------
    # CUSTOMER SPENDING DISTRIBUTION
    # --------------------------------------

    st.subheader("Customer Spending Distribution")

    fig = px.histogram(
        filtered_customer,
        x="total_amount_spent",
        nbins=20,
        title="Distribution of Customer Spending",
        labels={
            "total_amount_spent": "Total Amount Spent"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# PAGE 4 — TIME TRENDS
# ==========================================

elif page == "Time Trends":

    st.title("Time Trends")

    st.write(
        "Analyze how revenue, rentals, and customer activity "
        "change over time."
    )

    # --------------------------------------
    # SIDEBAR FILTER
    # --------------------------------------

    st.sidebar.header("Time Filters")

    monthly["date"] = pd.to_datetime(monthly["date"])

    min_date = monthly["date"].min().date()
    max_date = monthly["date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # --------------------------------------
    # APPLY DATE FILTER
    # --------------------------------------

    if len(selected_dates) == 2:

        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])

        filtered_monthly = monthly[
            (monthly["date"] >= start_date)
            & (monthly["date"] <= end_date)
        ]

    else:

        filtered_monthly = monthly.copy()

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_revenue = filtered_monthly[
        "total_revenue"
    ].sum()

    total_rentals = filtered_monthly[
        "total_rentals"
    ].sum()

    total_customers = filtered_monthly[
        "unique_customers"
    ].sum()

    average_revenue_per_rental = (
        total_revenue / total_rentals
        if total_rentals > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

    with col2:
        show_metric(
            "Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Customer Activity",
            f"{total_customers:,}"
        )

    with col4:
        show_metric(
            "Avg Revenue / Rental",
            f"${average_revenue_per_rental:,.2f}"
        )

    st.divider()

    # --------------------------------------
    # REVENUE TREND
    # --------------------------------------

    st.subheader("Revenue Trend")

    create_line_chart(
        filtered_monthly,
        x="date",
        y="total_revenue",
        title="Monthly Revenue",
        x_title="Month",
        y_title="Revenue"
    )

    # --------------------------------------
    # RENTAL TREND
    # --------------------------------------

    st.subheader("Rental Trend")

    create_line_chart(
        filtered_monthly,
        x="date",
        y="total_rentals",
        title="Monthly Rentals",
        x_title="Month",
        y_title="Rentals"
    )

    # --------------------------------------
    # CUSTOMER TREND
    # --------------------------------------

    st.subheader("Customer Activity")

    create_line_chart(
        filtered_monthly,
        x="date",
        y="unique_customers",
        title="Monthly Unique Customers",
        x_title="Month",
        y_title="Customers"
    )

    # --------------------------------------
    # AVERAGE REVENUE PER RENTAL
    # --------------------------------------

    st.subheader("Average Revenue per Rental")

    trend_data = filtered_monthly.copy()

    trend_data["avg_revenue"] = (
        trend_data["total_revenue"]
        / trend_data["total_rentals"]
    )

    create_line_chart(
        trend_data,
        x="date",
        y="avg_revenue",
        title="Average Revenue per Rental",
        x_title="Month",
        y_title="Average Revenue"
    )

# ==========================================
# PAGE 5 — STORE & STAFF
# ==========================================

elif page == "Store & Staff":

    st.title("Store & Staff Performance")

    st.write(
        "Analyze revenue, rentals, and customer activity "
        "across stores and staff."
    )

    # --------------------------------------
    # SIDEBAR FILTER
    # --------------------------------------

    st.sidebar.header("Store & Staff Filters")

    stores = sorted(
        staff["store_id"].dropna().unique()
    )

    selected_stores = st.sidebar.multiselect(
        "Store",
        options=stores,
        default=stores
    )

    filtered_staff = staff[
        staff["store_id"].isin(selected_stores)
    ]

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_revenue = filtered_staff[
        "total_revenue_collected"
    ].sum()

    total_rentals = filtered_staff[
        "total_rental_processed"
    ].sum()

    total_customers = filtered_staff[
        "unique_customer_served"
    ].sum()

    number_of_staff = filtered_staff[
        "staff_name"
    ].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

    with col2:
        show_metric(
            "Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Customers Served",
            f"{total_customers:,}"
        )

    with col4:
        show_metric(
            "Staff",
            f"{number_of_staff:,}"
        )

    st.divider()

    # --------------------------------------
    # STORE PERFORMANCE
    # --------------------------------------

    st.subheader("Store Performance")

    filtered_store = store[
        store["store_id"].isin(selected_stores)
    ]

    create_bar_chart(
        filtered_store.sort_values(
            "total_revenue",
            ascending=True
        ),
        x="total_revenue",
        y="store_id",
        title="Revenue by Store",
        x_title="Revenue",
        y_title="Store",
        horizontal=True
    )

    # --------------------------------------
    # STAFF REVENUE
    # --------------------------------------

    st.subheader("Staff Revenue Performance")

    create_bar_chart(
        filtered_staff.sort_values(
            "total_revenue_collected",
            ascending=True
        ),
        x="total_revenue_collected",
        y="staff_name",
        title="Revenue Collected by Staff",
        x_title="Revenue",
        y_title="Staff",
        horizontal=True
    )

    # --------------------------------------
    # STAFF RENTALS
    # --------------------------------------

    st.subheader("Staff Rental Activity")

    create_bar_chart(
        filtered_staff.sort_values(
            "total_rental_processed",
            ascending=True
        ),
        x="total_rental_processed",
        y="staff_name",
        title="Rentals Processed by Staff",
        x_title="Rentals",
        y_title="Staff",
        horizontal=True
    )

    # --------------------------------------
    # CUSTOMERS SERVED
    # --------------------------------------

    st.subheader("Customers Served by Staff")

    create_bar_chart(
        filtered_staff.sort_values(
            "unique_customer_served",
            ascending=True
        ),
        x="unique_customer_served",
        y="staff_name",
        title="Unique Customers Served",
        x_title="Customers",
        y_title="Staff",
        horizontal=True
    )

# ==========================================
# PAGE 6 — GEOGRAPHIC
# ==========================================

elif page == "Geographic":

    st.title("Geographic Performance")

    st.write(
        "Analyze rental revenue, rental activity, and "
        "customer distribution by location."
    )

    # --------------------------------------
    # COUNTRY FILTER
    # --------------------------------------

    st.sidebar.header("Geographic Filters")

    countries = sorted(
        geographic["country"].dropna().unique()
    )

    selected_countries = st.sidebar.multiselect(
        "Country",
        options=countries,
        default=countries
    )

    filtered_geo = geographic[
        geographic["country"].isin(selected_countries)
    ]

    # --------------------------------------
    # CITY FILTER
    # --------------------------------------

    cities = sorted(
        filtered_geo["city"].dropna().unique()
    )

    selected_cities = st.sidebar.multiselect(
        "City",
        options=cities,
        default=cities
    )

    filtered_geo = filtered_geo[
        filtered_geo["city"].isin(selected_cities)
    ]

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_revenue = filtered_geo[
        "total_revenue"
    ].sum()

    total_rentals = filtered_geo[
        "total_rentals"
    ].sum()

    total_customers = filtered_geo[
        "unique_customers"
    ].sum()

    number_of_cities = filtered_geo[
        "city"
    ].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

    with col2:
        show_metric(
            "Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Customers",
            f"{total_customers:,}"
        )

    with col4:
        show_metric(
            "Cities",
            f"{number_of_cities:,}"
        )

    st.divider()

    # --------------------------------------
    # TOP CITIES BY REVENUE
    # --------------------------------------

    st.subheader("Top 10 Cities by Revenue")

    top_cities = (
        filtered_geo
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        top_cities.sort_values(
            "total_revenue",
            ascending=True
        ),
        x="total_revenue",
        y="city",
        title="Top 10 Cities by Revenue",
        x_title="Revenue",
        y_title="City",
        horizontal=True
    )

    # --------------------------------------
    # TOP COUNTRIES BY REVENUE
    # --------------------------------------

    st.subheader("Revenue by Country")

    country_performance = (
        filtered_geo
        .groupby("country")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_rentals=("total_rentals", "sum"),
            unique_customers=("unique_customers", "sum")
        )
        .reset_index()
    )

    create_bar_chart(
        country_performance.sort_values(
            "total_revenue",
            ascending=True
        ),
        x="total_revenue",
        y="country",
        title="Revenue by Country",
        x_title="Revenue",
        y_title="Country",
        horizontal=True
    )

    # --------------------------------------
    # RENTALS BY COUNTRY
    # --------------------------------------

    st.subheader("Rentals by Country")

    create_bar_chart(
        country_performance.sort_values(
            "total_rentals",
            ascending=True
        ),
        x="total_rentals",
        y="country",
        title="Rental Activity by Country",
        x_title="Rentals",
        y_title="Country",
        horizontal=True
    )


# ==========================================
# PAGE 7 — INVENTORY
# ==========================================

elif page == "Inventory":

    st.title("Inventory Analysis")

    st.write(
        "Analyze inventory levels, rental demand, and "
        "rental duration across films."
    )

    # --------------------------------------
    # SIDEBAR FILTER
    # --------------------------------------

    st.sidebar.header("Inventory Filters")

    categories = sorted(
        inventory["category"].dropna().unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Category",
        options=categories,
        default=categories
    )

    filtered_inventory = inventory[
        inventory["category"].isin(selected_categories)
    ]

    # --------------------------------------
    # KPIs
    # --------------------------------------

    total_inventory = filtered_inventory[
        "inventory_count"
    ].sum()

    total_rentals = filtered_inventory[
        "total_rentals"
    ].sum()

    total_revenue = filtered_inventory[
        "total_revenue"
    ].sum()

    average_duration = filtered_inventory[
        "avg_rental_duration"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Inventory Units",
            f"{total_inventory:,}"
        )

    with col2:
        show_metric(
            "Rentals",
            f"{total_rentals:,}"
        )

    with col3:
        show_metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

    with col4:
        show_metric(
            "Avg Rental Duration",
            f"{average_duration:.1f} days"
        )

    st.divider()

    # --------------------------------------
    # HIGHEST INVENTORY
    # --------------------------------------

    st.subheader("Films with Highest Inventory")

    highest_inventory = (
        filtered_inventory
        .sort_values(
            "inventory_count",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        highest_inventory.sort_values(
            "inventory_count",
            ascending=True
        ),
        x="inventory_count",
        y="film_title",
        title="Top 10 Films by Inventory",
        x_title="Inventory Units",
        y_title="Film",
        horizontal=True
    )

    # --------------------------------------
    # HIGHEST DEMAND
    # --------------------------------------

    st.subheader("Highest Rental Demand")

    highest_demand = (
        filtered_inventory
        .sort_values(
            "total_rentals",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        highest_demand.sort_values(
            "total_rentals",
            ascending=True
        ),
        x="total_rentals",
        y="film_title",
        title="Top 10 Films by Rental Demand",
        x_title="Rentals",
        y_title="Film",
        horizontal=True
    )

    # --------------------------------------
    # LOWEST DEMAND
    # --------------------------------------

    st.subheader("Lowest Rental Demand")

    lowest_demand = (
        filtered_inventory
        .sort_values(
            "total_rentals",
            ascending=True
        )
        .head(10)
    )

    create_bar_chart(
        lowest_demand.sort_values(
            "total_rentals",
            ascending=False
        ),
        x="total_rentals",
        y="film_title",
        title="10 Films with Lowest Rental Demand",
        x_title="Rentals",
        y_title="Film",
        horizontal=True
    )

    # --------------------------------------
    # RENTAL DURATION
    # --------------------------------------

    st.subheader("Average Rental Duration")

    duration_data = (
        filtered_inventory
        .dropna(subset=["avg_rental_duration"])
        .sort_values(
            "avg_rental_duration",
            ascending=False
        )
        .head(10)
    )

    create_bar_chart(
        duration_data.sort_values(
            "avg_rental_duration",
            ascending=True
        ),
        x="avg_rental_duration",
        y="film_title",
        title="Top 10 Films by Average Rental Duration",
        x_title="Average Days",
        y_title="Film",
        horizontal=True
    )
