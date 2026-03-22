"""
Video Game Data Analysis Package

This package provides data cleaning, platform mapping, and visualization utilities 
for video game sales and ratings analysis. Only for the https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings dataset

Modules:
--------
cleaning.py - Data cleaning and missing value imputation functions
platform_dictionaries.py - Platform code conversion and mapping utilities  
visualizations.py - Plotting and chart generation functions

Usage:
------
import sys
sys.path.append('../src')

import visualizations
    visualizations.distributions

from visualizations import distributions

"""

from .cleaning import fill_missing_values
from .platform_dictionaries import (
    get_platform_full_name,
    get_platform_generation, 
    get_platform_type,
    get_platform_company
)
from .visualizations import (
    distributions,
    region_sales,
    platform_companies,
    game_genres,
    esrb_ratings,
    critic_user_score
)

__all__ = [
    # Cleaning functions
    'fill_missing_values',
    
    # Platform dictionary functions
    'get_platform_full_name',
    'get_platform_generation',
    'get_platform_type', 
    'get_platform_company',
    
    # Visualization functions
    'distributions',
    'region_sales',
    'platform_companies',
    'game_genres',
    'esrb_ratings',
    'critic_user_score'
]

__version__ = '1.0.0'
__author__ = 'Enric Peñalver Hill'
__description__ = 'A comprehensive toolkit for video game market data analysis, for Video Game Sales with Ratings (Kaggle Dataset)'