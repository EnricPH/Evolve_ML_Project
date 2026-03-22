import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def distributions(df, cols):
    """
    Plot distribution histograms for multiple numeric columns.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data to visualize
    cols : list
        List of column names to plot distributions for. Columns must be numeric.
        
    Returns:
    --------
    None
        Displays a grid of distribution plots
    
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If cols list is empty
        If any specified column is missing from DataFrame
        If any specified column is not numeric
        
    Examples:
    ---------
    >>> distributions(df, ['NA_Sales', 'EU_Sales', 'JP_Sales'])
    >>> distributions(df, ['Critic_Score', 'User_Score'])
    """
    
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    if not cols.tolist():
        raise ValueError("Columns list cannot be empty")
    
    # Check if all columns exist in DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"The following columns are missing from the DataFrame: {missing_cols}")
    
    # Check if all columns are numeric
    non_numeric_cols = [col for col in cols if not pd.api.types.is_numeric_dtype(df[col])]
    if non_numeric_cols:
        raise ValueError(f"The following columns are not numeric: {non_numeric_cols}. Please provide only numeric columns.")
    
    # Check if we have enough columns for the subplot grid
    n_cols = len(cols)
    if n_cols > 10:
        raise ValueError(f"Maximum 10 columns supported. Received {n_cols} columns.")
    
    # Color palette
    colors_list = ['dimgray', 'navy', 'blue', 'red', 'brown', 'green', 'yellow', 'indianred', 'yellowgreen', 'firebrick']
    
    # Create subplot grid (5 rows, 2 columns max)
    fig, axes = plt.subplots(5, 2, figsize=(15, 20))
    axes = axes.flatten()  # Convert to 1D array for easy iteration
    
    # Plot distributions
    for i, (col, color) in enumerate(zip(cols, colors_list)):
        # Calculate appropriate number of bins (avoid too many bins for small datasets)
        unique_count = df[col].nunique()
        bins = max(10, unique_count // 2)  # Minimum 10 bins, adjust based on data
        
        sns.histplot(df[col], ax=axes[i], color=color, bins=min(bins, 50))  # Cap at 50 bins
        axes[i].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        axes[i].grid(True, alpha=0.3)
        axes[i].set_xlabel(col)
        
    # Hide any unused subplots
    for i in range(len(cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()


def region_sales(df):
    """
    Plot regional sales distribution and evolution over time.
    
    Creates two visualizations:
    1. Pie chart showing global market share by region
    2. Line chart showing sales evolution by region with 3-year moving average
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing sales data with required columns:
        - 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales' (regional sales columns)
        - 'Year_of_Release' (for temporal analysis)
        
    Returns:
    --------
    None
        Displays a matplotlib figure with two subplots
        
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If required sales columns are missing
        If 'Year_of_Release' column is missing
        If no valid sales data exists in the DataFrame
    """
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check for required sales columns
    required_sales_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    missing_sales_cols = [col for col in required_sales_cols if col not in df.columns]
    if missing_sales_cols:
        raise ValueError(f"Missing required sales columns: {missing_sales_cols}")
    
    # Check for Year_of_Release column
    if 'Year_of_Release' not in df.columns:
        raise ValueError("Required column 'Year_of_Release' is missing from DataFrame")
    
    # Check if there's any sales data to plot
    total_sales = df[required_sales_cols].sum().sum()
    if total_sales == 0:
        raise ValueError("No sales data available in the specified regional columns")
    
    # Check if there's temporal data for the line chart
    if df['Year_of_Release'].isna().all():
        raise ValueError("No valid year data available for temporal analysis")
    
    # Set style
    plt.style.use('default')
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 1. Global market share by region (Pie chart)
    regional_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    axes[0].pie(regional_sales.values, labels=regional_sales.index, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('Global Market Share by Region')

    # 2. Sales evolution by region across years
    yearly_regional_sales = df.groupby('Year_of_Release')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()

    # Apply rolling average to smooth the lines
    window_size = 3  # 3-year moving average
    yearly_regional_sales_smoothed = yearly_regional_sales.rolling(window=window_size, center=True).mean()

    yearly_regional_sales_smoothed.plot(ax=axes[1], linewidth=2.5, alpha=0.8)
    axes[1].set_title(f'Sales Evolution by Region (1980-2020)\n({window_size}-Year Moving Average)')
    axes[1].set_ylabel('Sales (Millions)')
    axes[1].set_xlabel('Year')
    axes[1].legend(bbox_to_anchor=(1, 1), loc='upper left')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def platform_companies(df):
    """
    Plot platform company analysis including market share, regional sales, and sales evolution.
    
    Creates three visualizations:
    1. Pie chart showing market share by company (top 3 companies + others)
    2. Bar chart showing top companies sales by region
    3. Line chart showing sales evolution by company with 3-year moving average
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing sales data with required columns:
        - 'Platform_Company' (company names)
        - 'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales' (sales columns)
        - 'Year_of_Release' (for temporal analysis)
        
    Returns:
    --------
    None
        Displays a matplotlib figure with three subplots
        
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If required columns are missing
        If no valid sales data exists in the DataFrame
        If no platform company data is available
    """
    
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check for required columns
    required_cols = ['Platform_Company', 'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year_of_Release']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check if there's any sales data to plot
    total_sales = df['Global_Sales'].sum()
    if total_sales == 0:
        raise ValueError("No sales data available in the DataFrame")
    
    # Check if platform company data exists
    if df['Platform_Company'].isna().all():
        raise ValueError("No platform company data available")
    
    # Check if there's temporal data for the line chart
    if df['Year_of_Release'].isna().all():
        raise ValueError("No valid year data available for temporal analysis")
    
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Total sales by company (Pie chart)
    # Group small slices into "Others" category
    sales_by_company = df.groupby('Platform_Company')['Global_Sales'].sum().sort_values(ascending=False)
    # Define threshold for grouping (e.g., keep top 5, group rest as "Others")
    top_n = 3
    top_companies = sales_by_company.head(top_n)
    other_sales = sales_by_company.iloc[top_n:].sum()
    # Create new series with "Others"
    final_sales = pd.concat([top_companies, pd.Series({'Others': other_sales})])

    axes[0,0].pie(final_sales.values, labels=final_sales.index, autopct='%1.1f%%', startangle=90, colors=['dodgerblue', 'red', 'green', 'orange'])
    axes[0,0].set_title('Market Share by Company\n(Categories <5% grouped as "Other")')

    # 2. Top companies sales by region (spans both bottom cells)
    top_companies = df['Platform_Company'].value_counts().head(3).index
    company_regional = df[df['Platform_Company'].isin(top_companies)].groupby('Platform_Company')[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()

    # Create a subplot that spans both bottom cells

    company_regional.T.plot(kind='bar', ax=axes[0,1], color=['green', 'red', 'dodgerblue'])
    axes[0,1].set_title('Top Platform Companies Sales by Region')
    axes[0,1].set_ylabel('Sales (Millions)')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].legend(bbox_to_anchor=(1, 1), loc='upper left')
    axes[0,1].grid(True, alpha=0.3)

    # 2. Sales evolution by company (top right)
    yearly_company_sales = df.groupby(['Year_of_Release', 'Platform_Company'])['Global_Sales'].sum().unstack().fillna(0)
    main_companies = ['Nintendo', 'Sony', 'Microsoft', 'Atari', 'Sega']
    colors = ['red', 'dodgerblue', 'green', 'brown', 'purple']

    # Apply rolling average to smooth the lines
    window_size = 3  # 3-year moving average
    yearly_company_sales_smoothed = yearly_company_sales.rolling(window=window_size, center=True).mean()

    ax_big = fig.add_subplot(2, 1, 2)  # 2 rows, 1 column, second position
    for i, company in enumerate(main_companies):
        if company in yearly_company_sales_smoothed.columns:
            ax_big.plot(yearly_company_sales_smoothed.index, yearly_company_sales_smoothed[company], 
                    label=company, color=colors[i], linewidth=2.5, alpha=0.8)

    ax_big.set_title(f'Sales Evolution by Company (1980-2020)\n({window_size}-Year Moving Average)', fontsize=14)
    ax_big.set_xlabel('Year')
    ax_big.set_ylabel('Global Sales (Milions)')
    ax_big.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax_big.grid(True, alpha=0.3)

    # Hide the original bottom axes since we're using the big one
    axes[1,0].set_visible(False)
    axes[1,1].set_visible(False)

    plt.tight_layout()
    plt.show()


def game_genres(df):
    """
    Plot game genre analysis including market share, regional sales, and sales trends over time.
    
    Creates three visualizations:
    1. Pie chart showing market share by genre (genres <3% grouped as "Other")
    2. Bar chart showing top genres sales by region
    3. Line chart showing top 5 genres sales trend with 3-year moving average
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing sales data with required columns:
        - 'Genre' (game genre categories)
        - 'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales' (sales columns)
        - 'Year_of_Release' (for temporal analysis)
        
    Returns:
    --------
    None
        Displays a matplotlib figure with three subplots
        
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If required columns are missing
        If no valid sales data exists in the DataFrame
        If no genre data is available
    """
    
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check for required columns
    required_cols = ['Genre', 'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year_of_Release']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check if there's any sales data to plot
    total_sales = df['Global_Sales'].sum()
    if total_sales == 0:
        raise ValueError("No sales data available in the DataFrame")
    
    # Check if genre data exists
    if df['Genre'].isna().all():
        raise ValueError("No genre data available")
    
    # Check if there's temporal data for the line chart
    if df['Year_of_Release'].isna().all():
        raise ValueError("No valid year data available for temporal analysis")
    
    # Set style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Market share by genre (Pie chart)
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)

    # Group small genres as "Other"
    percentages_genre = (genre_sales / genre_sales.sum()) * 100
    small_genres = percentages_genre[percentages_genre < 3].index

    if len(small_genres) > 0:
        other_genre_sales = genre_sales[small_genres].sum()
        main_genres = genre_sales[~genre_sales.index.isin(small_genres)]
        final_genre_sales = pd.concat([main_genres, pd.Series({'Other': other_genre_sales})])
    else:
        final_genre_sales = genre_sales

    axes[0,0].pie(final_genre_sales.values, labels=final_genre_sales.index, autopct='%1.1f%%', startangle=90)
    axes[0,0].set_title('Market Share by Genre\n(Categories <3% grouped as "Other")')

    # 2. Top genres by region
    # Get top 6 genres by total sales across all regions
    genre_regional = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    genre_regional['Total_Sales'] = genre_regional.sum(axis=1)
    top_6_genres = genre_regional.nlargest(6, 'Total_Sales')
    top_6_genres.drop('Total_Sales',axis=1,inplace=True)
    # Display the top 6 genres
    top_6_genres.T.plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('Top Genres Sales by Region')
    axes[0,1].set_ylabel('Sales (Millions)')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()

    # 3. Genre popularity trend over years (spans both bottom cells)
    genre_yearly = df.groupby(['Year_of_Release', 'Genre'])['Global_Sales'].sum().unstack().fillna(0)
    top_5_genres = genre_sales.head(5).index

    # Apply rolling average to smooth the lines
    window_size = 3  # 3-year moving average
    genre_yearly_smoothed = genre_yearly.rolling(window=window_size, center=True).mean()

    # Create a subplot that spans both bottom cells
    ax_big = fig.add_subplot(2, 1, 2)  # 2 rows, 1 column, second position
    genre_yearly_smoothed[top_5_genres].plot(ax=ax_big, linewidth=2.5, alpha=0.8)
    ax_big.set_title(f'Top 5 Genres Sales Trend Over Time\n({window_size}-Year Moving Average)')
    ax_big.set_ylabel('Global Sales (Millions)')
    ax_big.set_xlabel('Year')
    ax_big.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax_big.grid(True, alpha=0.3)

    # Hide the original bottom axes since we're using the big one
    axes[1,0].set_visible(False)
    axes[1,1].set_visible(False)

    plt.tight_layout()
    plt.show()


def esrb_ratings(df):
    """
    Plot ESRB rating analysis including distribution, regional sales, and popularity trends over time.
    
    Creates three visualizations:
    1. Pie chart showing game distribution by ESRB rating (ratings <1% grouped as "Other")
    2. Bar chart showing top ratings sales by region
    3. Line chart showing rating popularity trend with 3-year moving average
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing sales and rating data with required columns:
        - 'Rating' (ESRB rating categories)
        - 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales' (sales columns)
        - 'Year_of_Release' (for temporal analysis)
        
    Returns:
    --------
    None
        Displays a matplotlib figure with three subplots
        
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If required columns are missing
        If no valid sales data exists in the DataFrame
        If no rating data is available
    """
    
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check for required columns
    required_cols = ['Rating', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year_of_Release']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check if there's any sales data to plot
    total_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().sum()
    if total_sales == 0:
        raise ValueError("No sales data available in the DataFrame")
    
    # Check if rating data exists
    if df['Rating'].isna().all():
        raise ValueError("No rating data available")
    
    # Check if there's temporal data for the line chart
    if df['Year_of_Release'].isna().all():
        raise ValueError("No valid year data available for temporal analysis")
    
    # Set style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Rating distribution pie chart - group categories with less than 5%
    rating_counts = df['Rating'].value_counts()
    total_games = rating_counts.sum()
    # Calculate percentages and identify small categories
    percentages = (rating_counts / total_games) * 100
    small_categories = percentages[percentages < 1].index
    # Group small categories into "Other"
    if len(small_categories) > 0:
        other_count = rating_counts[small_categories].sum()
        main_categories = rating_counts[~rating_counts.index.isin(small_categories)]
        final_ratings = pd.concat([main_categories, pd.Series({'Other': other_count})])
    else:
        final_ratings = rating_counts

    axes[0,0].pie(final_ratings.values, labels=final_ratings.index, autopct='%1.1f%%', startangle=90, colors=['dodgerblue', 'darkorange', 'forestgreen', 'cyan'])
    axes[0,0].set_title('Game Distribution by ESRB Rating\n(Categories <1% grouped as "Other")')

    # 2. Top genres by region
    # Get top 6 genres by total sales across all regions
    rating_regional = df.groupby('Rating')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    rating_regional['Total_Sales'] =rating_regional.sum(axis=1)
    top_4_rating =rating_regional.nlargest(4, 'Total_Sales')
    top_4_rating.drop('Total_Sales',axis=1,inplace=True)
    # Display the top 6 genres
    top_4_rating.T.plot(kind='bar', ax=axes[0,1], color=['dodgerblue', 'darkorange', 'forestgreen', 'cyan'])
    axes[0,1].set_title('Top Ratings Sales by Region')
    axes[0,1].set_ylabel('Sales (Millions)')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()


    # 4. Rating trend over years
    rating_yearly = df.groupby(['Year_of_Release', 'Rating']).size().unstack().fillna(0)

    # Apply rolling average to smooth the lines
    window_size = 3  # 3-year moving average
    rating_yearly_smoothed = rating_yearly.rolling(window=window_size, center=True).mean()
    ax_big = fig.add_subplot(2, 1, 2)
    rating_yearly_smoothed.plot(ax= ax_big, linewidth=2.5, alpha=0.8, 
                            color=['red', 'dodgerblue', 'cyan', 'forestgreen', 'purple', 'darkorange'])
    ax_big.set_title(f'ESRB Rating Popularity Over Time\n({window_size}-Year Moving Average)')
    ax_big.set_ylabel('Number of Games Released')
    ax_big.set_xlabel('Year')
    ax_big.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax_big.grid(True, alpha=0.3)

    # Hide the original bottom axes since we're using the big one
    axes[1,0].set_visible(False)
    axes[1,1].set_visible(False)


    plt.tight_layout()
    plt.show()


def critic_user_score(df):
    """
    Plot critic vs user score comparisons across different categories.
    
    Creates four visualizations comparing critic and user scores:
    1. Average scores by platform type
    2. Average scores by platform company (companies <10 critic score grouped as "Other")
    3. Average scores by genre
    4. Average scores by ESRB rating
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing score data with required columns:
        - 'Critic_Score', 'User_Score' (score columns)
        - 'Platform_Type', 'Platform_Company', 'Genre', 'Rating' (categorical columns)
        
    Returns:
    --------
    None
        Displays a matplotlib figure with four subplots
        
    Raises:
    -------
    ValueError
        If input DataFrame is empty
        If required columns are missing
        If no valid score data exists in the DataFrame
    """
    
    # Input validation
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check for required columns
    required_cols = ['Critic_Score', 'User_Score', 'Platform_Type', 'Platform_Company', 'Genre', 'Rating']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check if there's any score data to plot
    if df['Critic_Score'].isna().all() and df['User_Score'].isna().all():
        raise ValueError("No score data available in the DataFrame")
    
    # Check if categorical data exists
    categorical_cols = ['Platform_Type', 'Platform_Company', 'Genre', 'Rating']
    for col in categorical_cols:
        if df[col].isna().all():
            raise ValueError(f"No data available for {col}")
    
    # Set style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))


    # 1. Average scores by platform type
    platform_critic_avg = df.groupby('Platform_Type')['Critic_Score'].mean().sort_values(ascending=False)
    platform_user_avg = df.groupby('Platform_Type')['User_Score'].mean()
    width = 0.35
    x = np.arange(len(platform_critic_avg))
    axes[0,0].bar(x - width/2, platform_critic_avg.values, width, label='Critic Score', color='darkgreen', alpha=0.8)
    axes[0,0].bar(x + width/2, platform_user_avg.loc[platform_critic_avg.index].values, width, label='User Score', color='springgreen', alpha=0.8)
    axes[0,0].set_title('Average Scores by Platform Type')
    axes[0,0].set_xlabel('Platform Type')
    axes[0,0].set_ylabel('Average Score')
    axes[0,0].set_xticks(x)
    axes[0,0].set_xticklabels(platform_critic_avg.index, rotation=45)
    axes[0,0].legend()


    # 2. Scores by Company - Group low-scoring companies as "Other"
    rating_critic_avg = df.groupby('Platform_Company')['Critic_Score'].mean().sort_values(ascending=False)
    rating_user_avg = df.groupby('Platform_Company')['User_Score'].mean()

    # Filter companies with critic score >= 10, group others as "Other"
    threshold = 10
    major_companies = rating_critic_avg[rating_critic_avg >= threshold]
    other_critic_avg = rating_critic_avg[rating_critic_avg < threshold].mean()
    other_user_avg = rating_user_avg[rating_critic_avg < threshold].mean()

    # Combine major companies with "Other"
    final_critic_avg = pd.concat([major_companies, pd.Series({'Other': other_critic_avg})])
    final_user_avg = pd.concat([rating_user_avg[major_companies.index], pd.Series({'Other': other_user_avg})])

    x = np.arange(len(final_critic_avg))
    axes[0,1].bar(x - width/2, final_critic_avg.values, width, label='Critic Score', color='mediumblue', alpha=0.8)
    axes[0,1].bar(x + width/2, final_user_avg.values, width, label='User Score', color='cornflowerblue', alpha=0.8)
    axes[0,1].set_title('Average Scores by Platform Company')
    axes[0,1].set_xlabel('Platform Company')
    axes[0,1].set_ylabel('Average Score')
    axes[0,1].set_xticks(x)
    axes[0,1].set_xticklabels(final_critic_avg.index, rotation=45)
    axes[0,1].legend()

    # 2. Average scores by genre
    genre_critic_avg = df.groupby('Genre')['Critic_Score'].mean().sort_values(ascending=False)
    genre_user_avg = df.groupby('Genre')['User_Score'].mean()

    x = np.arange(len(genre_critic_avg))
    axes[1,0].bar(x - width/2, genre_critic_avg.values, width, label='Critic Score', color='brown', alpha=0.8)
    axes[1,0].bar(x + width/2, genre_user_avg.loc[genre_critic_avg.index].values, width, label='User Score', color='darkorange', alpha=0.8)
    axes[1,0].set_title('Average Scores by Genre')
    axes[1,0].set_xlabel('Genre')
    axes[1,0].set_ylabel('Average Score')
    axes[1,0].set_xticks(x)
    axes[1,0].set_xticklabels(genre_critic_avg.index, rotation=45)
    axes[1,0].legend()


    # 3. Scores by ESRB rating
    rating_critic_avg = df.groupby('Rating')['Critic_Score'].mean().sort_values(ascending=False)
    rating_user_avg = df.groupby('Rating')['User_Score'].mean()

    x = np.arange(len(rating_critic_avg))
    axes[1,1].bar(x - width/2, rating_critic_avg.values, width, label='Critic Score', color='purple', alpha=0.8)
    axes[1,1].bar(x + width/2, rating_user_avg.loc[rating_critic_avg.index].values, width, label='User Score', color='mediumorchid', alpha=0.8)
    axes[1,1].set_title('Average Scores by ESRB Rating')
    axes[1,1].set_xlabel('ESRB Rating')
    axes[1,1].set_ylabel('Average Score')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(rating_critic_avg.index)
    axes[1,1].legend()


    plt.tight_layout()
    plt.show()