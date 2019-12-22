import io
import yaml

default_configuration = {
    'device_id' : 'sensor_temp_dev1',
    'timer' : '5',
    'gcp' : {
        'precision' : '5'
    }
}


def factory(file=None):
    if file != None:
        with io.open(file,'r') as stream:
            return yaml.safe_load(stream)
    else:
        return default_configuration
