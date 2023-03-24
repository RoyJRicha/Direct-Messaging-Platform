import ds_messenger as dm
import Profile as Pr
import time


message = "hiiihihihih"
dming = dm.DirectMessenger("168.235.86.101", "Friend2", "friend")
'''
data = dming.send(message, "Sender")
timestamp = time.time()
profile = Pr.Profile()
profile.load_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\GUITest.dsu")
profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\GUITest.dsu")
new_message = Pr.Sent(message, "Sender", timestamp)
profile.add_author("Sender")
profile.add_sent_messages(new_message)

profile.save_profile("C:\\Users\\rrich\\PythonFiles\\Assignments\\Test Files\\GUITest.dsu")
'''

# Retrieve ALLLLLL
data = dming.retrieve_all()

print(data)
'''
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

'''
import datetime
import time

time = datetime.datetime.fromtimestamp(1679516335.0818863).strftime("%d/%m/%Y %I:%M %p")

print(time)
'''