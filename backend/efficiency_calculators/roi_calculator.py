class ROICalculator:
    """
    Calculates ROI based on provided cost and income data.
    """

    def calculate_roi(self, optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences):        
        if num_inferences == float('inf'):
            return (original_cost_per_inference - new_cost_per_inference) / new_cost_per_inference
        
        total_cost_old = original_cost_per_inference * num_inferences
        total_costs_new = new_cost_per_inference * num_inferences + optimization_cost
        roi = (total_cost_old - total_costs_new) / total_costs_new
        return roi

    def calculate_break_even_point(self, optimization_cost, new_cost_per_inference, original_cost_per_inference):
        """
        Calculates the number of inferences needed for a positive ROI

        Income must exceed costs for positive ROI
        original_CostPerInference * number_inferences > OptimizationCost + new_CostPerInference * number_inferences
        number_inferences > OptimizationCost / (original_CostPerInference - new_CostPerInference)
        """
        if new_cost_per_inference >= original_cost_per_inference:
            return float('inf')

        break_even_point = optimization_cost / (original_cost_per_inference - new_cost_per_inference)
        return int(break_even_point)
    
    def calculate_roi_evolution(self, optimization_cost, original_cost_per_inference, new_cost_per_inference, inference_numbers=None):
        """
        Calculates ROI for a range of inference numbers.
        """
        if inference_numbers is None:
            break_even_point = self.calculate_break_even_point(optimization_cost, new_cost_per_inference, original_cost_per_inference)
            if break_even_point == float('inf') or break_even_point < 0:
                # If no positive ROI, default inference range
                inference_numbers = range(0, 2000001, 10000)
            else:
                max_inference = int(break_even_point * 40)
                # Handle the case where max_inference is too small
                if max_inference < 50:
                    max_inference = 50
                
                step = max(max_inference//200, 1)
                inference_numbers = range(0, max_inference + 1, step)

        roi_evolution = []
        for num_inferences in inference_numbers:
            roi = self.calculate_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences)
            roi_evolution.append((num_inferences, roi))

        return roi_evolution