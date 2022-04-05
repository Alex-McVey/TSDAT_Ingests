import re

from typing import AnyStr, Dict
from utils import IngestSpec, expand
from . import Pipeline


mapping: Dict["AnyStr@compile", IngestSpec] = {
    # Mapping for Raw Data -> Ingest
    re.compile(r".*LoadCells.tdms"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_loadcells_unh.yml", __file__),
        storage_config=expand("config/storage_config_loadcells_unh.yml", __file__),
        name="loadcells_unh",
    ),
    # Mapping for Processed Data -> Ingest (so we can reprocess plots)
    re.compile(r".*load_cell0.png"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_loadcells_unh.yml", __file__),
        storage_config=expand("config/storage_config_loadcells_unh.yml", __file__),
        name="plot_loadcells_unh",
    ),
}
