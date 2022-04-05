import os
import xarray as xr
from utils import expand, set_env
from ingest.vectorsystem_unh import Pipeline

parent = os.path.dirname(__file__)


def test_vectorsystem_unh_pipeline():
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_vectorsystem_unh.yml", parent),
        expand("config/storage_config_vectorsystem_unh.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/2021_11_16_0_0_VectorSystemData1.tdms", parent))
    expected = xr.open_dataset(
        expand("tests/data/expected/unh.modaq_group_vectorsystem.nc", parent))
    xr.testing.assert_allclose(output, expected)
