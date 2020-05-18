config = dict(local="mysql+pymysql://rik:X0chi@localhost/raa_new",
              remote="mysql+pymysql://rik:X0chi@remotehost/raa_new")  # change this when we know the remote host

# how to update for user? Cookies?
default_preferences = {'perpage':20, }

def get_config(host="local",config=config):
    config = config['local']
    if host == "remote":
        config = config['remote']
    return config


