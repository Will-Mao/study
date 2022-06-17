import yaml


def set_yaml_data(key, value):
    try:
        with open("data.yaml", "r+") as f1:
            result = yaml.safe_load(f1.read())
            # for r in result:
            result[key] = value
        with open("data.yaml", "w+") as f2:
            yaml.safe_dump(result, f2)
    except FileNotFoundError:
        pass


def get_yaml_data(key):
    try:
        with open("data.yaml", "r+") as f:
            result = yaml.safe_load(f.read())
            value = result[key]
            return value
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    set_yaml_data('Release', 'v8v111')
    # get_yaml_data('Release')