import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def distribution(df, columns, scale=False):
    """
    Visualize the distribution of numerical columns using histograms.

    Optionally applies a signed log transformation to handle skewed data,
    including negative and zero values.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the data.

    columns : list of str
        List of column names to visualize.

    scale : bool, optional (default=False)
        If True, applies a signed log transformation:
            sign(x) * log1p(|x|)
        Useful for handling skewness and negative values.

    Raises
    ------
    ValueError
        If 'columns' is empty or contains non-existent columns.

    TypeError
        If df is not a pandas DataFrame.
    """

    # -------- Error handling --------
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if not columns or not isinstance(columns, list):
        raise ValueError("columns must be a non-empty list of column names")

    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    # -------- Plot setup --------
    n_cols = 2
    n_rows = int(np.ceil(len(columns) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = np.array(axes).flatten()

    # -------- Plot loop --------
    for i, col in enumerate(columns):
        data = df[col].dropna()

        # Check numeric
        if not np.issubdtype(data.dtype, np.number):
            print(f"Skipping non-numeric column: {col}")
            continue

        data = data.values.reshape(-1, 1)

        # Apply transformation if requested
        if scale:
            data = np.sign(data.flatten()) * np.log1p(np.abs(data.flatten()))
        else:
            data = data.flatten()

        data = pd.Series(data)

        # Compute stats
        Q1 = data.quantile(0.25)
        Q2 = data.quantile(0.50)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Plot
        sns.histplot(data, ax=axes[i], bins=15)

        # Mean & median
        axes[i].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        axes[i].axvline(Q2, color='green', linestyle='--', linewidth=2, label='Median')

        # Show IQR only if NOT transformed
        if not scale:
            axes[i].axvline(lower_bound, color='purple', linestyle='-.', linewidth=2, label='Lower bound')
            axes[i].axvline(upper_bound, color='purple', linestyle='-.', linewidth=2, label='Upper bound')

        axes[i].set_title(
            f'Histogram of {col} ({ "signed log" if scale else "original" })',
            fontsize=12,
            fontweight='bold'
        )
        axes[i].grid(True, alpha=0.3)
        axes[i].set_xlabel(col)
        axes[i].legend()

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()


def country(df):
    """
    Perform country-level analysis on retail data.

    Visualizations include:
    - Market share by country (sales contribution)
    - Top countries by sales and cancellations
    - Sales and cancellations trends over time

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing retail transaction data.

    Required columns:
        - Country
        - Quantity
        - TotalPrice
        - InvoiceDate

    Raises
    ------
    ValueError
        If required columns are missing or data is invalid.
    """

    # -------- Input validation --------
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    required_cols = ["Country", "Quantity", "TotalPrice", "InvoiceDate"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if df["Country"].isna().all():
        raise ValueError("No country data available")

    if df["InvoiceDate"].isna().all():
        raise ValueError("No valid date data available")

    # -------- Prepare data --------
    df = df.copy()
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

    df_sales = df[df["Quantity"] > 0]
    df_cancel = df[df["Quantity"] < 0]

    # -------- Plot setup --------
    plt.style.use("default")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Market share by country (Pie)
    country_sales = df_sales.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False)

    percentages = (country_sales / country_sales.sum()) * 100
    small_countries = percentages[percentages < 3].index

    if len(small_countries) > 0:
        other_sales = country_sales[small_countries].sum()
        main_countries = country_sales[~country_sales.index.isin(small_countries)]
        final_sales = pd.concat([main_countries, pd.Series({"Other": other_sales})])
    else:
        final_sales = country_sales

    axes[0,0].pie(final_sales.values, labels=final_sales.index, autopct='%1.1f%%', startangle=90)
    axes[0,0].set_title('Sales Contribution by Country')

    # 2. Cancellation rate per country

    # Total invoices per country
    total_invoices = df.groupby("Country")["Invoice"].nunique()

    # Cancelled invoices per country
    cancel_invoices = df[df["Cancellation"] == 1].groupby("Country")["Invoice"].nunique()

    # Compute rate
    cancel_rate = (cancel_invoices / total_invoices).fillna(0)

    # Take top countries by volume (to avoid noise)
    top_countries = total_invoices.sort_values(ascending=False).head(10).index
    cancel_rate_top = cancel_rate.loc[top_countries].sort_values(ascending=False)

    # Plot
    sns.barplot(x=cancel_rate_top.values, y=cancel_rate_top.index, ax=axes[0,1])

    axes[0,1].set_title("Cancellation Rate by Country (Top 10)")
    axes[0,1].set_xlabel("Cancellation Rate (%)")
    axes[0,1].set_xticklabels([f"{x*100:.1f}%" for x in axes[0,1].get_xticks()])
    axes[0,1].set_ylabel("Country")
    axes[0,1].grid(True, alpha=0.3)

    # 3. Sales & cancellations over time (top countries)
    top_countries = country_sales.head(5).index

    sales_time = df_sales[df_sales["Country"].isin(top_countries)] \
        .groupby(["YearMonth", "Country"])["TotalPrice"].sum().unstack().fillna(0)

    # Create big subplot
    ax_big = fig.add_subplot(2, 1, 2)

    sales_time.plot(ax=ax_big, linewidth=2)

    ax_big.set_title("Sales Over Time - Top Countries")
    ax_big.set_ylabel("Total Value")
    ax_big.set_xlabel("Time")
    ax_big.legend(bbox_to_anchor=(1, 1))
    ax_big.grid(True, alpha=0.3)

    # Hide unused axes
    axes[1,0].set_visible(False)
    axes[1,1].set_visible(False)

    plt.tight_layout()
    plt.show()
  

def weekday(df):
    """
    Visualize total sales and cancellations per weekday.

    Parameters
    ----------
    df : pandas.DataFrame

    Required columns:
        - Quantity
        - TotalPrice
        - Weekday
    """

    # -------- Validation --------
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    required_cols = ["Quantity", "TotalPrice", "Weekday"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # -------- Prepare data --------
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    df_sales = df[df["Quantity"] > 0]
    df_cancel = df[df["Quantity"] < 0]

    sales = df_sales.groupby("Weekday")["TotalPrice"].sum().reindex(weekday_order)
    cancellations = df_cancel.groupby("Weekday")["TotalPrice"].sum().abs().reindex(weekday_order)

    # -------- Plot --------
    plt.figure(figsize=(10,5))

    x = np.arange(len(weekday_order))
    width = 0.4

    plt.bar(x - width/2, sales, width=width, label="Sales")
    plt.bar(x + width/2, cancellations, width=width, label="Cancellations")

    plt.xticks(x, weekday_order, rotation=45)
    plt.title("Sales vs Cancellations per Weekday")
    plt.ylabel("Total Value")
    plt.xlabel("Weekday")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

def customer(customer_df):
    """
    Perform customer-level analysis and visualization.

    Visualizations include:
    - Customer segmentation by spending (Low / Mid / High tier)
    - Distribution of number of orders
    - Distribution of total spending
    - Repeat vs one-time customers

    Parameters
    ----------
    customer_df : pandas.DataFrame

    Required columns:
        - TotalSpent
        - NumOrders

    Raises
    ------
    ValueError
        If required columns are missing or data is invalid.
    """

    # -------- Validation --------
    if customer_df.empty:
        raise ValueError("Input DataFrame is empty")

    required_cols = ["TotalSpent", "NumOrders"]
    missing_cols = [col for col in required_cols if col not in customer_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = customer_df.copy()

    # -------- Customer segmentation (tiers) --------
    df["SpendingTier"] = pd.qcut(
        df["TotalSpent"],
        q=3,
        labels=["Low", "Mid", "High"]
    )

    tier_counts = df["SpendingTier"].value_counts().sort_index()

    # -------- Repeat customers --------
    df["IsRepeat"] = (df["NumOrders"] > 1).astype(int)
    repeat_counts = df["IsRepeat"].value_counts()

    # -------- Plot setup --------
    plt.style.use("default")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Customer tiers
    sns.barplot(x=tier_counts.index, y=tier_counts.values, ax=axes[0,0])
    axes[0,0].set_title("Customer Segmentation by Spending")
    axes[0,0].set_ylabel("Number of Customers")
    axes[0,0].set_xlabel("Spending Tier")
    axes[0,0].grid(True, alpha=0.3)

    # 2. Orders distribution
    sns.histplot(np.log(df["NumOrders"]), bins=15, ax=axes[0,1])
    axes[0,1].set_title("Distribution of Number of Orders (Log)")
    axes[0,1].set_xlabel("Number of Orders")
    axes[0,1].grid(True, alpha=0.3)

    # 3. Spending distribution (log for visualization)
    transformed_spending = np.log(df["TotalSpent"])
    sns.histplot(transformed_spending, bins=30, ax=axes[1,0])
    axes[1,0].set_title("Distribution of Customer Spending (Log)")
    axes[1,0].set_xlabel("Transformed Spending")
    axes[1,0].grid(True, alpha=0.3)

    # 4. Repeat vs one-time
    axes[1,1].pie(
        repeat_counts,
        labels=["One-time", "Repeat"],
        autopct='%1.1f%%'
    )
    axes[1,1].set_title("Customer Types")

    plt.tight_layout()
    plt.show()