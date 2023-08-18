import pandas as pd
import numpy as np


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

    return len(boundaries) - 1  # worst rating if index does not fall in boundaries


def calculate_compound_rating(ratings, weights, meanings, mode='mean'):
    """
    Calculates a compound rating based on individual ratings and their weights.

    Args:
    ratings : list of individual ratings
    weights : list of weights corresponding to the ratings
    meanings : array representing different ratings
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


def value_to_index(value, ref, high_better):
    """
    Convert a value to an index by normalizing it with a reference value.
    If the metric is higher better, index is value divided by reference value,
    otherwise index is reference value divided by value.

    Args:
    value : value to be converted
    ref : reference value for normalization
    metric : name of the metric
    high_better: whether a higher value is better or not for the metric

    Returns:
    index
    """
    if pd.isnull(value) or value is None:
        return None

    try:
        return value / ref if high_better else ref / value
    except:
        return 0


def calculate_ratings(metrics, metrics_ref, boundaries, weights, higher_better, meanings, rating_mode='mean', index=True):
    """
    Assigns an energy efficiency label based on the metrics.

    Args:
    metrics : dictionary of metrics
    metrics_ref : reference metrics for normalization
    boundaries : boundary intervals for each metric
    weights: weights for each metric
    higher_better: which of the metrics are better if they have a higher value
    meanings : array representing different ratings
    rating_mode : method to calculate compound rating
    index : if True, convert metric values to indices before assigning label

    Returns:
    compound rating and dictionary of individual ratings
    """
    weights = list(weights.values())
    if index:
        metrics = {metric: value_to_index(value, metrics_ref[metric], metric in higher_better) for metric, value in metrics.items()}

    metrics_to_rating = (
        {metric:
            assign_rating(value, boundaries[metric])
            for metric, value in metrics.items()}
    )

    ratings = list(metrics_to_rating.values())

    # Transforma els ratings de les mètriques (0, 1, ...) al valor real del resultat (A, B, ...)
    metrics_to_rating = (
        {metric: meanings[value] for metric, value in metrics_to_rating.items()}
    )
    return calculate_compound_rating(ratings, weights, meanings, rating_mode), metrics_to_rating
