class ROICalculator:
    """
    Calculates ROI based on provided cost and benefit data.
    """

    def calculate_roi(self, optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences):
        total_cost_savings = (original_cost_per_inference - new_cost_per_inference) * num_inferences
        total_costs_new = new_cost_per_inference * num_inferences + optimization_cost
        roi = (total_cost_savings - total_costs_new) / total_costs_new
        return roi

    def calculate_positive_roi(self, optimization_cost, new_cost_per_inference, original_cost_per_inference):
        """
        Calculates the number of inferences needed for a positive ROI

        Benefits must exceed costs for positive ROI
        CostSavingsPerInference * number_inferences > OptimizationCost + new_CostPerInference * number_inferences
        number_inferences > OptimizationCost / (CostSavingsPerInference - new_CostPerInference)
        number_inferences > OptimizationCost / ((original_CostPerInference - new_CostPerInference) - new_CostPerInference)
        """
        if new_cost_per_inference >= original_cost_per_inference:
            return float('inf')

        break_even_point = optimization_cost / (original_cost_per_inference - 2 * new_cost_per_inference)
        return int(break_even_point)
    
    def calculate_roi_from_metrics(self, optimization_cost_metrics, original_cost_metrics, new_cost_metrics, num_inferences=100):
        """
        Calculates ROI using ROICostMetrics objects.
        """
        optimization_cost = self._calculate_total_cost(optimization_cost_metrics)
        new_cost_per_inference = self._calculate_cost_per_inference(new_cost_metrics)
        original_cost_per_inference = self._calculate_cost_per_inference(original_cost_metrics)

        return self.calculate_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences)

    def calculate_positive_roi_from_metrics(self, optimization_cost_metrics, original_cost_metrics, new_cost_metrics):
        """
        Calculates the positive ROI point using ROICostMetrics objects.
        """
        optimization_cost = self._calculate_total_cost(optimization_cost_metrics)
        new_cost_per_inference = self._calculate_cost_per_inference(new_cost_metrics)
        original_cost_per_inference = self._calculate_cost_per_inference(original_cost_metrics)

        return self.calculate_positive_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference)

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
            positive_roi_point = self.calculate_positive_roi_from_metrics(optimization_cost_metrics, original_cost_metrics, new_cost_metrics)
            if positive_roi_point == float('inf') or positive_roi_point < 0:
                # If no positive ROI, default inference range
                inference_numbers = range(0, 2000001, 10000)
            else:
                max_inference = int(positive_roi_point * 20)
                inference_numbers = range(0, max_inference + 1, max_inference//200)

        roi_evolution = []
        for num_inferences in inference_numbers:
            roi = self.calculate_roi(optimization_cost, new_cost_per_inference, original_cost_per_inference, num_inferences)
            roi_evolution.append((num_inferences, roi))

        return roi_evolution
