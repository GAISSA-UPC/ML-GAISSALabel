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
    
    def calculate_roi_from_metrics(self, optimization_cost_metrics, original_cost_metrics, new_cost_metrics, num_inferences=100):
        """
        Calculates ROI using GAISSAROICostMetrics objects.
        """
        optimization_cost = self._calculate_total_cost(optimization_cost_metrics)
        new_cost_per_inference = self._calculate_cost_per_inference(new_cost_metrics)
        original_cost_per_inference = self._calculate_cost_per_inference(original_cost_metrics)

        return self.calculate_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences)

    def calculate_break_even_point_from_metrics(self, optimization_cost_metrics, original_cost_metrics, new_cost_metrics):
        """
        Calculates the break-even point using GAISSAROICostMetrics objects.
        """
        optimization_cost = self._calculate_total_cost(optimization_cost_metrics)
        new_cost_per_inference = self._calculate_cost_per_inference(new_cost_metrics)
        original_cost_per_inference = self._calculate_cost_per_inference(original_cost_metrics)

        return self.calculate_break_even_point(optimization_cost, new_cost_per_inference, original_cost_per_inference)

    def _calculate_total_cost(self, cost_metrics):
        """
        Calculates the total cost, including taxes.
        """
        return float(cost_metrics.total_packs * cost_metrics.cost_per_pack * (1 + cost_metrics.taxes))

    def _calculate_cost_per_inference(self, cost_metrics):
        """
        Calculates the cost per inference.
        """
        return self._calculate_total_cost(cost_metrics) / cost_metrics.num_inferences

    def calculate_roi_evolution(self, optimization_cost_metrics, original_cost_metrics, new_cost_metrics, inference_numbers=None):
        """
        Calculates ROI for a range of inference numbers.
        """
        optimization_cost = self._calculate_total_cost(optimization_cost_metrics)
        new_cost_per_inference = self._calculate_cost_per_inference(new_cost_metrics)
        original_cost_per_inference = self._calculate_cost_per_inference(original_cost_metrics)

        if inference_numbers is None:
            break_even_point = self.calculate_break_even_point_from_metrics(optimization_cost_metrics, original_cost_metrics, new_cost_metrics)
            if break_even_point == float('inf') or break_even_point < 0:
                # If no positive ROI, default inference range
                inference_numbers = range(0, 2000001, 10000)
            else:
                max_inference = int(break_even_point * 20)
                inference_numbers = range(0, max_inference + 1, max_inference//200)

        roi_evolution = []
        for num_inferences in inference_numbers:
            roi = self.calculate_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences)
            roi_evolution.append((num_inferences, roi))

        return roi_evolution
