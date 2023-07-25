import pandas as pd
import numpy as np

# Weightage of different metrics for energy efficiency computation
METRIC_WEIGHTS = {
    'co2_eq_emissions': 0.4,
    'size_efficency': 0.15,
    'datasets_size_efficency': 0.15,
    'downloads': 0.2,
    'performance_score': 0.2
}

# Metrics where a higher value is better
HIGHER_BETTER = [
    'performance_score',
    'size_efficency',
    'datasets_size_efficency',
    'downloads'
]


def weighted_mean(ratings, weights):
    """
    Compute weighted mean of ratings.

    Args:
    ratings : list of ratings
    weights : corresponding weights for the ratings

    Returns:
    weighted mean : weighted mean of ratings
    """
    # Remove NaN values and their corresponding weights
    not_nan_indices = np.isfinite(ratings)
    ratings_clean = np.array(ratings)[not_nan_indices]
    weights_clean = np.array(weights)[not_nan_indices]
    
    # Renormalize the weights
    weights_clean = weights_clean / np.sum(weights_clean)

    # Compute the weighted mean
    mean = np.sum(ratings_clean * weights_clean)
    
    return int(round(mean))


def assign_rating(index, boundaries):
    """
    Assigns a rating based on index value. If index is within certain boundaries, 
    a specific rating is given.

    Args:
    index : index value for which rating is to be assigned
    boundaries : list of boundaries for rating

    Returns:
    rating : assigned rating
    """
    if index is None or pd.isnull(index):
        return np.nan

    for i, (upper, lower) in enumerate(boundaries):
        if upper >= index > lower:
            return i
    return 4    # worst rating if index does not fall in boundaries


def calculate_compound_rating(ratings, weights=None, meanings='ABCDE', mode='mean'):
    """
    Calculates a compound rating based on individual ratings and their weights.

    Args:
    ratings : list of individual ratings
    weights : list of weights corresponding to the ratings
    meanings : string representing different ratings, default is 'ABCDE'
    mode : method to calculate compound rating, default is 'mean'

    Returns:
    compound rating
    """
    if all(x is None or pd.isna(x) for x in ratings):
        return None
    if weights is None:
        weights = [1.0 / len(ratings) for _ in ratings]
    if mode == 'mean':
        return meanings[weighted_mean(ratings, weights)]


def value_to_index(value, ref, metric):
    """
    Convert a value to an index by normalizing it with a reference value.
    If the metric is higher better, index is value divided by reference value,
    otherwise index is reference value divided by value.

    Args:
    value : value to be converted
    ref : reference value for normalization
    metric : name of the metric

    Returns:
    index
    """
    if pd.isnull(value) or value is None:
        return None

    try:
        return value / ref if metric in HIGHER_BETTER else ref / value
    except:
        return 0


def assign_energy_label(metrics, metrics_ref, boundaries, meanings, rating_mode, index=True):
    """
    Assigns an energy efficiency label based on the metrics.

    Args:
    metrics : dictionary of metrics
    metrics_ref : reference metrics for normalization
    boundaries : boundary intervals for each metric
    meanings : string representing different ratings
    rating_mode : method to calculate compound rating
    index : if True, convert metric values to indices before assigning label

    Returns:
    compound rating and dictionary of individual ratings
    """
    weights = list(METRIC_WEIGHTS.values())
    if index:
        metrics = {metric: value_to_index(value, metrics_ref[metric], metric) for metric, value in metrics.items()}

    metrics_to_rating = (
        {metric:
          assign_rating(value, boundaries[metric])
          for metric, value in metrics.items()})
    
    ratings = list(metrics_to_rating.values())
    return calculate_compound_rating(ratings, weights, meanings, rating_mode), metrics_to_rating
