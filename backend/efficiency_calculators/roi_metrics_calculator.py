from api.models import ROIAnalysis, AnalysisMetricValue, ExpectedMetricReduction, EnergyAnalysisMetricValue
from efficiency_calculators.roi_calculator import ROICalculator

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
                        'higher_is_better': metric_value.metric.higher_is_better,
                    }
                    
                    # If this is an energy metric with cost data, calculate cost savings
                    if metric_value.metric.is_energy_related:
                        try:
                            energy_metric_value = EnergyAnalysisMetricValue.objects.get(id=metric_value.id)
                            # Calculate cost savings with default 10M inferences
                            cost_savings = self.calculate_cost_savings(
                                energy_metric_value, 
                                expected_reduction.expectedReductionValue, 
                                10000000
                            )
                            result['cost_savings'] = cost_savings
                            
                            # Calculate ROI evolution data points (useful for chart display)
                            roi_evolution_data = self.calculate_roi_evolution_data(
                                energy_metric_value, 
                                expected_reduction.expectedReductionValue
                            )
                            result['roi_evolution_chart_data'] = roi_evolution_data
                            
                        except EnergyAnalysisMetricValue.DoesNotExist:
                            # This is an energy-related metric but without the cost data
                            print(f"Energy metric {metric_value.metric.id} does not have cost data.")
                            pass
                    
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
    
    def calculate_cost_savings(self, energy_metric_value, reduction_factor, num_inferences):
        """
        Calculate cost savings based on energy reduction.
        
        Args:
            energy_metric_value (the EnergyAnalysisMetricValue instance), reduction_factor, num_inferences
            
        Returns:
            Dictionary with cost savings information
        """
        try:
            baseline_energy_joules = energy_metric_value.baselineValue
            new_energy_joules = baseline_energy_joules * (1 - reduction_factor)
            
            # Convert Joules to kWh for cost calculation (1 kWh = 3,600,000 J)
            joules_to_kwh = 1 / 3600000
            baseline_energy_kwh = baseline_energy_joules * joules_to_kwh
            new_energy_kwh = new_energy_joules * joules_to_kwh
            
            # Calculate costs
            energy_cost_rate = float(energy_metric_value.energy_cost_rate)
            baseline_cost_per_inference = baseline_energy_kwh * energy_cost_rate
            new_cost_per_inference = new_energy_kwh * energy_cost_rate
            
            implementation_cost = float(energy_metric_value.implementation_cost)
            
            # Use the ROICalculator for consistent ROI calculations
            roi_calculator = ROICalculator()
            roi = roi_calculator.calculate_roi(
                implementation_cost, 
                new_cost_per_inference, 
                baseline_cost_per_inference, 
                num_inferences
            )
            infinite_roi = roi_calculator.calculate_roi(
                implementation_cost, 
                new_cost_per_inference, 
                baseline_cost_per_inference, 
                float('inf')
            )
            
            # Calculate break-even point
            break_even_inferences = roi_calculator.calculate_break_even_point(
                implementation_cost,
                new_cost_per_inference,
                baseline_cost_per_inference
            )
            if break_even_inferences == float('inf'):
                break_even_inferences = "Infinity"
            else:
                break_even_inferences = int(break_even_inferences)
            
            # Calculate total costs for the given number of inferences
            total_baseline_cost = baseline_cost_per_inference * num_inferences
            total_new_cost = new_cost_per_inference * num_inferences + implementation_cost
            
            total_savings = total_baseline_cost - total_new_cost
                
            return {
                'baseline_energy_joules': baseline_energy_joules,
                'new_energy_joules': new_energy_joules,
                'energy_reduction_joules': baseline_energy_joules - new_energy_joules,
                'energy_reduction_percentage': reduction_factor * 100,
                'baseline_cost_per_inference': baseline_cost_per_inference,
                'new_cost_per_inference': new_cost_per_inference,
                'total_baseline_cost': total_baseline_cost,
                'total_new_cost': total_new_cost,
                'implementation_cost': implementation_cost,
                'energy_cost_rate': energy_cost_rate,
                'total_savings': total_savings,
                'roi': roi,
                'infinite_roi': infinite_roi,
                'break_even_inferences': break_even_inferences,
                'num_inferences': num_inferences
            }
            
        except Exception as e:
            return {
                'error': f"Error calculating cost savings: {str(e)}"
            }

    def calculate_roi_evolution_data(self, energy_metric_value, reduction_factor):
        """
        Calculate ROI evolution data points for a chart using the direct ROICalculator interface.
        
        Args:
            energy_metric_value (the EnergyAnalysisMetricValue instance), reduction_factor
            
        Returns:
            List of dictionaries with inferences and ROI values for each point
        """
        try:
            baseline_energy_joules = energy_metric_value.baselineValue
            new_energy_joules = baseline_energy_joules * (1 - reduction_factor)
            
            # Convert Joules to kWh for cost calculation (1 kWh = 3,600,000 J)
            joules_to_kwh = 1 / 3600000
            baseline_energy_kwh = baseline_energy_joules * joules_to_kwh
            new_energy_kwh = new_energy_joules * joules_to_kwh
            
            # Calculate costs
            energy_cost_rate = float(energy_metric_value.energy_cost_rate)
            baseline_cost_per_inference = baseline_energy_kwh * energy_cost_rate
            new_cost_per_inference = new_energy_kwh * energy_cost_rate
            
            implementation_cost = float(energy_metric_value.implementation_cost)
            
            roi_calculator = ROICalculator()
            roi_evolution = roi_calculator.calculate_roi_evolution(
                implementation_cost,
                baseline_cost_per_inference, 
                new_cost_per_inference
            )
            
            # Format the results
            data_points = []
            for inferences, roi in roi_evolution:
                data_points.append({
                    'inferences': inferences,
                    'roi': roi
                })
                
            return data_points
            
        except Exception as e:
            print(f"Error calculating ROI evolution data: {e}")
            return []