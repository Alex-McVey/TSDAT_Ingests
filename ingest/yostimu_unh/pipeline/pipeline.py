import os
import cmocean
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from typing import Dict
from tsdat import DSUtil
from utils import IngestPipeline, format_time_xticks


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    MODAQ GROUP YOSTIMU INGESTION PIPELINE

    Ingest for the UNH Living Bridge MODAQ results. Specifically the _YostIMU files

    --------------------------------------------------------------------------------"""

    def hook_customize_raw_datasets(
        self, raw_dataset_mapping: Dict[str, xr.Dataset]
    ) -> Dict[str, xr.Dataset]:
        return raw_dataset_mapping

    def hook_customize_dataset(
        self, dataset: xr.Dataset, raw_mapping: Dict[str, xr.Dataset]
    ) -> xr.Dataset:
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")

        with plt.style.context(style_file):

            start_date = pd.to_datetime(dataset.time.data[0]).strftime("%Y-%m-%d")
            final_date = pd.to_datetime(dataset.time.data[-1]).strftime("%Y-%m-%d")
            filename = DSUtil.get_plot_filename(dataset, "accel_data", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:
                fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)
                fig.suptitle(
                    f"Acceleration Observations from {start_date} to {final_date}")

                dataset.accel_x.plot(
                    ax=ax,
                    x="time",
                    c=mcolors.to_rgb('blue'),
                    label="Acceleration: X",
                )
                dataset.accel_y.plot(
                    ax=ax,
                    x="time",
                    c=mcolors.to_rgb('red'),
                    label="Acceleration: Y",
                )
                dataset.accel_z.plot(
                    ax=ax,
                    x="time",
                    c=mcolors.to_rgb('green'),
                    label="Acceleration: Z",
                )

                ax.set_title("")  # Remove bogus title created by xarray
                ax.legend(ncol=1)  # , bbox_to_anchor=(1, -0.05)
                ax.set_ylabel("Acceleration (m/s^2)")
                ax.set_xlabel("Time (UTC)")
                # format_time_xticks(ax)
                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
