import pymongo

client_url = "mongodb://localhost:27017/"
db_name = "simulations_mini"
collection_name = "services"


class Service:
    def __init__(self, data):
        self.id = data['_id']
        self.acceptable_latency = data['acceptable_latency']
        self.average_instructions_per_second = data['average_instructions_per_second']
        self.layer = data['layer']


# Define a class to represent a Service Configuration
class ServiceConfiguration:
    def __init__(self, data):
        self.id = data['_id']
        self.services = [Service(service_data) for service_data in data['services']]


# Define a class to manage Service Configurations
class ServiceConfigurationManager:
    def __init__(self, client_url, db_name, collection_name):
        self.client = pymongo.MongoClient(client_url)  # Change the connection string as needed
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_configuration_by_id(self, config_id):
        config_data = self.collection.find_one({'_id': config_id})
        if config_data:
            return ServiceConfiguration(config_data)
        else:
            return None

    def get_all_configurations(self):
        configurations = []
        cursor = self.collection.find({})
        for config_data in cursor:
            configurations.append(ServiceConfiguration(config_data))
        return configurations

    def close_connection(self):
        self.client.close()


def get_all_services(config_id):
    service_config_manager = ServiceConfigurationManager(client_url, db_name, collection_name)
    config = service_config_manager.get_configuration_by_id(config_id)
    return config.services
