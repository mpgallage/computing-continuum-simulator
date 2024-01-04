import pymongo

client_url = "mongodb://localhost:27017/"
db_name = "simulations"
collection_name = "networks_edge_only"

# Define classes to represent the hierarchy
class GuestMachine:
    def __init__(self, data):
        self.idle_cpu_utilization = data['idle_cpu_utilization']
        self.max_cpu_utilization = data['max_cpu_utilization']
        self.max_instructions_per_second = data['max_instructions_per_second']
        self.net_delay_request = data['net_delay_request']
        self.net_delay_response = data['net_delay_response']
        self.layer = data['layer']


class HostMachine:
    def __init__(self, data):
        self.guest_machines = [GuestMachine(guest) for guest in data['guest_machines']]


class Configuration:
    def __init__(self, data):
        self.iot_devices = data['iot_devices']
        self.edge_devices = data['edge_devices']
        self.fog_devices = data['fog_devices']
        self.cloud_devices = data['cloud_devices']
        self.edge = [HostMachine(host) for host in data['edge']]
        self.fog = [HostMachine(host) for host in data['fog']]
        self.cloud = [HostMachine(host) for host in data['cloud']]


class NetworkConfigurationManager:
    def __init__(self, client_url, db_name, collection_name):
        self.client = pymongo.MongoClient(client_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_configuration_by_id(self, config_id):
        config_data = self.collection.find_one({'_id': config_id})
        if config_data:
            return Configuration(config_data)
        else:
            return None

    def get_all_configurations(self):
        configs = []
        cursor = self.collection.find({})
        for config_data in cursor:
            configs.append(Configuration(config_data))
        return configs

    def close_connection(self):
        self.client.close()


def get_all_devices_combined(config_id):
    network_config_manager = NetworkConfigurationManager(client_url, db_name, collection_name)
    config = network_config_manager.get_configuration_by_id(config_id)
    return config.edge + config.fog + config.cloud
