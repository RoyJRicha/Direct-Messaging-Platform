import ds_messenger as dm
import Profile as Pr


dming = dm.DirectMessenger("168.235.86.101", "RizzyWeather", "weatherpass")
#data = dming.send("don't hide your overwatch profile", "crykor")

data = dming.retrieve_all()

profile = Pr.Profile()
profile.load_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
for i in data:
    new_message = Pr.Message(i.message, i.recipient, i.timestamp)
    profile.add_author(i.recipient)
    profile.add_message(new_message)

profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\WeatherJournal.dsu")
