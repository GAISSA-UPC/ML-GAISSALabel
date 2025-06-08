"""
This file contains code adapted from the raphischer/strep project, available at https://github.com/raphischer/strep.
We thank Raphael and the contributors for their original work under the MIT license.

MIT License

Copyright (c) 2023 Raphael Fischer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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


def calculate_ratings(metrics, boundaries, weights, meanings, rating_mode='mean'):
    """
    Assigns an energy efficiency label based on the metrics.

    Args:
    metrics : dictionary of metrics
    boundaries : boundary intervals for each metric
    weights: weights for each metric
    meanings : array representing different ratings
    rating_mode : method to calculate compound rating

    Returns:
    compound rating and dictionary of individual ratings
    """
    weights = list(weights.values())

    metrics_to_rating = (
        {metric:
            assign_rating(value, boundaries[metric])
            for metric, value in metrics.items()}
    )

    ratings = list(metrics_to_rating.values())

    # Transforma els ratings de les mètriques (0, 1, ...) al valor real del resultat (A, B, ...)
    metrics_to_rating = (
        {metric: meanings[value] if value is not np.nan else None for metric, value in metrics_to_rating.items()}
    )
    return calculate_compound_rating(ratings, weights, meanings, rating_mode), metrics_to_rating
