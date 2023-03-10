import json
import os

from .server import Server
from .. import regions


class Servers(object):
    def load(self, file_name):
        with open(file_name, "r") as servers_data_file:
            servers_data_as_json = json.loads(servers_data_file.read())
            for svr in servers_data_as_json:
                # For now I'm arbitrarily choosing the use the iOS url over the Android url.
                new_server = Server(svr["ios_url"])
                for region_identifier in svr["regions"]:
                    region = getattr(regions, region_identifier)
                    region.server = new_server


servers = Servers()
servers.load(os.path.join(os.path.dirname(__file__), "data", "servers.json"))
