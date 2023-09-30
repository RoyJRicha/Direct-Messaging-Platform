NAME: Roy Richa
Personal EMAIL: royjricha@gmail.com
School EMAIL: rricha@uci.edu

PROJECT SUMMARY:

*Important* - Part 5 was the final part of this project where I implemented the direct messaging system between students over a local server

The following project consists of 5 total parts. Ultimately the project started out as a command line interface that
allows the user to run the python program and enter a number of commands to search for, create, view, or delete specific
files. All of the specific commands are explained in the parts of the project below. The end goal of the project was to create
a messaging interface on a local server for students to communicate with each other over valid profiles on the local server. All
the information ranging from messages sent, messages recieved, times for the messages, the contacts of the current user, etc, are
stored locally on the users machine in JSON formatted text .dsu files. This allows for a user to open up their profile by loading their
profiles file on their local computer, and that profile will automatically load all the previous messages that were sent or recieved
in order of time sent and recieved as well. All error checking functionality is implemented as well such as incorrect file formats
attempted to being loaded, if a user tries to send an improper message, and more. This program also allows users to make "blog posts"
on a local server at UCI as well. These posts include a timestamp, title, name, and the content of the blog post. A feature to this
blog post is that users can use key words as specified in part 4 such as @weather in the content of their blog post. By doing this, the
program will automatically reach out to an API and grab the current weather of the location the user enters and input that information in
their blog post rather than the user having to type the weather out manually for example.

UNIT TESTS: Unit tests were also created for this project to test each and every module individually to ensure smooth and proper functionality
and running times.

START OF PROJECT PART 1:
The purpose of this program is to take a command, directory path, and option from the user then return the directories
and files in that directory based on the option that the user chose.

The program first informs the user of the commands and simple instruction on how to use the programing commands.
It then asks the user to input a command. The simple input of 'Q' will simply exit the code and this means that the 
user would no longer like to search for any directories. The other input of 'L [PATH] [-OPTION] [INPUT FOR OPTION]'
will run the code accordingly depending on the path the user inputs, the option the user inputs, and if applicable, 
the secondary input for a command that the user inputs (for -s and -e). The code also allows for recursive searching
where the user can input not only one option (-r, -f, -s, or -e), but also a recursive option (-r -f, -r -s [FILE NAME],
-r -e [EXTENSTION]). Once again no matter the option or recurssion, the code will act accordingly and print all the files
and directories based on the path inputted by the user.

NEW ADDITIONS FOR PART 1:
The program now takes more commands other than 'L'. It takes 'C, 'D', and 'R'. Each having only one command, 'C' simply
takes in a secondary marker '-n' followed by a name of a file that you would like to create in a specified directory. 'D'
simply deletes a specific file from the file path that you inputted. Finally 'R' simply reads the file from the file path
the user specified.

NEW ADDITIONS for PART 2:
The code now supports both an admin mode and a user mode. The user mode is more intuative, it is more user friendlly where it prompts
the user what to input on each line step by step as well as providing instructions. The admin mode goes to a command line format where
no instructions are provided and errors are printed out as ERROR while in user mode they are detailed error messages to let the user know
what they did wrong. In addition to this modification, three new commands were added, the E, O, and P. For context, this code also added
the ability to create Profiles using the Profile.py module. This lets users create journal like files with a username, password, bio, and
posts. For the C command, it has been expanded (for the user mode) to allow for a username, password, and bio inputs to save to this journal.
For admin mode, it does not prompt the user to do this, instead they can do this using the E command. The E and P commands can only be used 
after the O command which opens and loads a file that has previously been created. The E command allows the user to edit their journal. THis
means edit their username, password, bio, add posts, or even delete posts. The P command simply prints what is in their journal. They can
print all content, or specifically the username, password, bio, specific posts, or all posts. In addition to all this, the program now
supports a wider variaty of error checks to ensure the code works properly for most if not all cases. Of course, as it comes with programming,
there may be cases where the program fails to do its intented task, but much thought and time has been put into this program to ensure that
for most cases the code works as intended.

NEW ADDITIONS FOR PART 3:
This code now supports posting posts and a bio with a username and password to a specific server with a port and IP Address. I'm not going to
go into too much detail, but the UI now supports new commands and new features to allow the user to post things of their choice. Starting with
the new U command, this will display all the contents of a specified profile to the user, and will give them the option to post their bio, a post
with a specified ID, as well as both if they would like. There is also the option to cancel if they would like to return home without posting.
Publishing is also available after doing the E command and adding a new post or editing their bio. That way this gives the user the option to post
their new post to the server, as well as their new bio, or if they edit both, they have the option to post both. If they wouldn't like to, they
can also choose not to publish it to the server. The perks of this code is that it has a huge amount of error checking, I would presume about 97% +
code coverage with the number of error statements and try excepts that I implemented into this code. Many very rare edge cases are also taken care of, 
however I do know that no code is ever perfect, and neither is this, however, I have worked long and hard to make it very optomized for the regular
user as well as ensure the user expereince is smooth and error proof.

NEW ADDITIONS FOR PART 4:
This code now supports many key words such as @weather, @weather_temp, @weather_humidity, @lastfm, and @lastfm_listeners. When a user enters one of 
these key words in their post, assuming all data is entered properly from the user and received properly from the API, the key words will be replaced
with their respective values. There are many error cecks as well as custom error checks in the WebAPI module to ensure no server errors occur during
the process.

NEW ADDITIONS FOR PART 5:
Added the ability to direct message with students across servers using a gui and valid profiles. The gui is very intuative and allows for easy access
to new and old files as well as new and old contacts with or without internet grabbing old messages only without internet and all new and old messages
with internet. It also provides a lot of error checking that ensures the code does not break under special circumstances.