import tsdat
import xarray as xr
import nptdms


class tdms_FileHandler(tsdat.AbstractFileHandler):
    """--------------------------------------------------------------------------------
    Custom file handler for reading <some data type> files from a <instrument name>.

    See https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/index.html for more
    examples of FileHandler implementations.

    --------------------------------------------------------------------------------"""

    def read(self, filename: str, **kwargs) -> xr.Dataset:
        """----------------------------------------------------------------------------
        Method to read data in a custom format and convert it into an xarray Dataset.

        Args:
            filename (str): The path to the file to read in.

        Returns:
            xr.Dataset: An xr.Dataset object
        ----------------------------------------------------------------------------"""
        tdms_file = nptdms.TdmsFile.read(filename)
        df = tdms_file.as_dataframe()
        tdms_groups = tdms_file.groups()
        # rename dataframe headers with the group names from groups()
        df.columns = tdms_groups[0].properties.keys()
        data = xr.Dataset.from_dataframe(df)
        data.attrs["name"] = tdms_file.properties["name"]
        # Iterate over all items in the file properties and assign xarray metadata
        for col in df.columns:
            data[col].attrs["units"] = tdms_groups[0].properties[col]
            data[col].attrs["path"] = tdms_file[tdms_groups[0].name][col].path
            data[col].rename({"index": "time"})
        return data
