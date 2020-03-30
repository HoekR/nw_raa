config = {'local' : "mysql+pymysql://rik:X0chi@localhost/raa",
          'remote': "mysql+pymysql://rik:X0chi@remotehost/raa"}

def get_config(host="local"):
    config = config['local']
    if host == "remote":
        config = config['remote']
    return config
