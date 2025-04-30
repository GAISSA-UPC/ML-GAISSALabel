from api.models import ROIAnalysis, AnalysisMetricValue, ExpectedMetricReduction

class ROIMetricsCalculator:
    """
    Calculates metrics values after applying expected reductions based on tactics.
    """

    def calculate_metrics_for_analysis(self, analysis_id):
        """
        Calculates metrics for a specific ROI analysis.
        
        Args:
            analysis_id: The ID of the ROI analysis to calculate metrics for
            
        Returns:
            Dictionary containing metric information: metric_id, metric_name, description, unit, 
            baseline_value, expected_reduction_percent, new_expected_value
        """
        try:
            # Get the ROI analysis
            analysis = ROIAnalysis.objects.select_related(
                'model_architecture',
                'tactic_parameter_option'
            ).get(id=analysis_id)
            
            # Get the metric values
            metric_values = AnalysisMetricValue.objects.filter(
                analysis=analysis
            ).select_related('metric')
            
            results = []
            
            for metric_value in metric_values:
                try:
                    # Get the necessary data
                    expected_reduction = ExpectedMetricReduction.objects.get(
                        model_architecture=analysis.model_architecture,
                        tactic_parameter_option=analysis.tactic_parameter_option,
                        metric=metric_value.metric
                    )
                    
                    reduction_percent = expected_reduction.expectedReductionValue * 100
                    
                    # Calculate the new value 
                    baseline_value = metric_value.baselineValue
                    new_expected_value = baseline_value * (1 - (reduction_percent / 100))
                    
                    # Create a result dictionary
                    result = {
                        'metric_id': metric_value.metric.id,
                        'metric_name': metric_value.metric.name,
                        'description': metric_value.metric.description,
                        'unit': metric_value.metric.unit,
                        'baseline_value': baseline_value,
                        'expected_reduction_percent': reduction_percent,
                        'new_expected_value': new_expected_value,
                    }
                    
                    results.append(result)
                    
                except ExpectedMetricReduction.DoesNotExist:
                    print(f"No expected reduction found for metric {metric_value.metric.id} in analysis {analysis_id}. It will be skipped.")
            
            return results
            
        except ROIAnalysis.DoesNotExist:
            print(f"ROI Analysis with ID {analysis_id} does not exist")
            return []
        except Exception as e:
            print(f"Error calculating metrics for ROI analysis {analysis_id}: {e}")
            return []