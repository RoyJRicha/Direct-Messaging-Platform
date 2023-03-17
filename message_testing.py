import ds_messenger as dm


dming = dm.DirectMessenger("168.235.86.101", "RizzyWeather", "weatherpass")
dming.retrieve_all()