import os
import xarray as xr
from utils import expand, set_env
from ingest.loadcells_unh import Pipeline

parent = os.path.dirname(__file__)


def test_loadcells_unh_pipeline():
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_loadcells_unh.yml", parent),
        expand("config/storage_config_loadcells_unh.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/2021_10_27_16_11_LoadCells.tdms", parent))
    expected = xr.open_dataset(
        expand("tests/data/expected/unh.modaq_group_loadcells.nc", parent))
    xr.testing.assert_allclose(output, expected)
