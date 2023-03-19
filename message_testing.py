import ds_messenger as dm
import Profile as Pr


dming = dm.DirectMessenger("168.235.86.101", "GUIusername", "GUIpassword")
data = dming.send("this is working now for now", "RizzyWeather")

# Retrieve ALLLLLL
'''
data = dming.retrieve_all()

profile = Pr.Profile()
profile.load_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
for i in data:
    new_message = Pr.Message(i.message, i.recipient, i.timestamp)
    profile.add_author(i.recipient)
    profile.add_message(new_message)

profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
'''

'''
# Retrieve NEWWWWW
data = dming.retrieve_new()

profile = Pr.Profile()
profile.load_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
for i in data:
    new_message = Pr.Message(i.message, i.recipient, i.timestamp)
    profile.add_author(i.recipient)
    profile.add_message(new_message)

profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
'''