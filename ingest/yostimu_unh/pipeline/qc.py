import numpy as np
from typing import Optional
from tsdat import DSUtil, QualityChecker, QualityHandler
from mhkit import qc
import xarray as xr


class StagnantDataChecker(QualityChecker):
    def run(self, variable_name: str) -> Optional[np.ndarray]:

        # False values in the results array mean the check passed, True values indicate
        # the check failed. Here we initialize the array to be full of False values as
        # an example. Note the shape of the results array must match the variable data.

        # To utilize the qc functions from mhkit, first the data must be sent to a
        # pandas data frame
        data_to_pd = self.ds[variable_name].to_dataframe()

        # Define expected lower bound (no upper bound is specified in this example)
        expected_bound = [0.001, None]

        # Define the moving window, in seconds
        sample_rate = data_to_pd.index.values[0:2]
        window = ((sample_rate[-1] - sample_rate[0]) / np.timedelta64(1, 's')) * 10

        # Run the delta quality control test
        results = qc.check_delta(data_to_pd, expected_bound, window)
        results_array = ~results['mask']
        results_array = results_array.to_numpy()

        return results_array


class StagnantDataHandler(QualityHandler):
    def run(self, variable_name: str, results_array: np.ndarray):

        # Some QualityHandlers only want to run if at least one value failed the check.
        # In this case, we replace all values that failed the check with the variable's
        # _FillValue and (possibly) add an attribute to the variable indicating the
        # correction applied.
        if results_array.any():

            fill_value = DSUtil.get_fill_value(self.ds, variable_name)
            keep_array = np.logical_not(results_array)

            var_values = self.ds[variable_name].data
            replaced_values = np.where(keep_array, var_values, fill_value)
            self.ds[variable_name].data = replaced_values

            self.record_correction(variable_name)
