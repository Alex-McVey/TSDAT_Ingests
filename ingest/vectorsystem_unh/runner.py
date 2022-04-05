from ingest.vectorsystem_unh import Pipeline
from utils import expand, set_env


if __name__ == "__main__":
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_vectorsystem_unh.yml", __file__),
        expand("config/storage_config_vectorsystem_unh.yml", __file__),
    )
    pipeline.run(expand(
        "C://Projects/TSDAT_Projects/UNH_MODAQ/sample_files/Sample UNH TDMS Files/2021_11_16_0_0_VectorSystemData1.tdms", __file__))
