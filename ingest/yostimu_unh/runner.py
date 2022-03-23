from ingest.yostimu_unh import Pipeline
from utils import expand, set_env

if __name__ == "__main__":
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_yostimu_unh.yml", __file__),
        expand("config/storage_config_yostimu_unh.yml", __file__),
    )
    pipeline.run(expand("C://Projects/TSDAT_Projects/UNH_MODAQ/sample_files/UNH_IMU_LoadCell_Data/2021_11_1_19_0_YostIMU.tdms", __file__))
