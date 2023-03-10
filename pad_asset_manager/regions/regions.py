import json
import os

from .region import Region


class Regions:
    _regions = {}

    def __getattr__(self, name):
        return self._regions[name]

    def load(self, file_name):
        with open(file_name, "r") as regions_data_file:
            regions_data_as_json = json.load(regions_data_file)
        for region_identifier in regions_data_as_json:
            region_data = regions_data_as_json[region_identifier]
            new_region = Region(region_data["name"])
            self._regions[region_identifier] = new_region


regions = Regions()
regions.load(os.path.join(os.path.dirname(__file__), "data", "regions.json"))
