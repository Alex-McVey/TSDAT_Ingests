import os
import xarray as xr
from utils import expand, set_env
from ingest.yostimu_unh import Pipeline

parent = os.path.dirname(__file__)


def test_yostimu_unh_pipeline():
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_yostimu_unh.yml", parent),
        expand("config/storage_config_yostimu_unh.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/2021_11_1_19_0_YostIMU.tdms", parent))
    expected = xr.open_dataset(
        expand("tests/data/expected/unh.modaq_group_yostimu.nc", parent))
    xr.testing.assert_allclose(output, expected)
