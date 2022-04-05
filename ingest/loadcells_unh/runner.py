from ingest.loadcells_unh import Pipeline
from utils import expand, set_env


if __name__ == "__main__":
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_loadcells_unh.yml", __file__),
        expand("config/storage_config_loadcells_unh.yml", __file__),
    )
    pipeline.run(expand("tests/data/input/2021_10_27_16_11_LoadCells.tdms", __file__))
