'''
ui.py is responsible for all
the user interface aspects of
this program. It is responsible
for easy and straight forward instructions
for the user that way they have 
a good experience using the code
'''
# ui.py

# This is responsible for all the user interface between a5, and all other modules

# Roy Richa
# rricha@uci.edu
# 51514923

import os
import re
import sys
import platform
import a5
import Profile

port = 3021
user_cnt = 0
command_status = ''
old_profile = Profile.Profile()


# Extracts the path from the input
def path_extractor(initial_input):
    '''
    Responsible for extracting anything
    from certain strings such as a file path
    or specific commands
    '''
    if (' -r' in initial_input) or (' -f' in initial_input) or (' -s' in initial_input) or (' -e' in initial_input) or (' -n' in initial_input):
        pathway_lst = re.findall(r'[RLCDO] (.*?)(?= -[rfens])', initial_input)
    elif initial_input[0:2] == 'E ':
        pattern = re.compile(r'(\-\w+)\s((("[^"]*"))|(\d+))')
        result = re.findall(pattern, initial_input)
        pathway_lst = [[item[0], item[1].strip('"') if (item[1][0] == '"') else item[4]] for item in result]
    elif initial_input[0:2] == 'P ':
        pattern = re.compile(r"-(\w+)")
        pathway_lst = []
        start = 0
        for m in re.finditer(pattern, initial_input):
            end = m.end()
            option = '-' + m.group(1)
            try:
                next_option_start = initial_input.index("-", end)
                value = initial_input[end:next_option_start].strip()
            except ValueError:
                value = initial_input[end:].strip()
            if value == '':
                value = None
            pathway_lst.append([option, value])
            start = end
    else:
        pathway_lst = re.findall(r'[RLCDO] (.*)$', initial_input)

    return pathway_lst


# Checks if the extracted path exists
def path_exists(path, status):
    '''
    Checks if a path exists, meaning
    a specific directory
    '''
    valid_path = True

    try:
        if os.path.exists(path):
            pass
        elif not os.path.exists(path):
            raise Exception
    # If specified path doesn't exist or incorrect, will ask to try again
    # If user chooses to try again, the code will rerun
    # If user chooses to quit or enters an invalid input, program will quit
    except Exception:
        if status == 'user':
            print(f'"{path}" was not found. Invalid directory. Please try again!\n')
        elif status == 'admin':
            print(f'ERROR')
        valid_path = False

    return valid_path


def instructions():
    '''
    Lists out instructions
    for the program to the user
    '''
    print('L - List all Folders and Files. (optionals commands included)')
    print('R - Read and display the content of any ".dsu" file under a folder')
    print('C - Create a file (or journal) with a ".dsu" extenstion under any folder (with username, password, bio)')
    print('O - Open and load a previously created file/journal to edit or view contents')
    print('E - Edit contents of a previously loaded/created file (IP Address, username, password, bio, add posts, delete posts)')
    print('P - Print contents of a previously loaded/created file (IP Address, username, password, bio, posts, all content)')
    print('U - Upload a new or current bio and/or a post of a loaded/created file')
    print('D - Delete any file (or journal) of your liking that has a ".dsu" extention. ')
    print('Q - Simply quit the program\n')


def command_list(key=None):
    '''
    Calls the instructions,
    specifically for a I 
    command
    '''
    instructions()


def edit_options():
    '''
    Lists the instructions for 
    the E command, easy to read
    and easy to understand
    '''
    print('-ip ~ Edit your IP Address')
    print('-usr ~ Edit your username')
    print('-pwd ~ Edit your password')
    print('-bio ~ Edit your bio')
    print('-addpost ~ Add a new post')
    print('  -> Post Key Words (replace the key words with their following description):')
    print('\t|----------------------------------------------------------------------|')
    print('\t| @weather - Description of the current weather (sunny, cloudy, etc.)  |')
    print('\t| @weather_temp - Current temperature of the weather (in Farenheit)    |')
    print('\t| @weather_humidity - Current humidty of weather (percentage)          |')
    print('\t| @lastfm - Current top #1 artist from around the world                |')
    print('\t| @lastfm_listeners - Current number of listeners of the top #1 artist |')
    print('\t|----------------------------------------------------------------------|')
    print('-delpost ~ Delete an old post (based on post\'s ID number)\n')


def print_options():
    '''
    Lists instructions for the P command
    that way the user knows what to enter
    to print what they want
    '''
    print('-ip ~ Print your IP Address')
    print('-usr ~ Print your username')
    print('-pwd ~ Print your password')
    print('-bio ~ Print your bio')
    print('-posts ~ Print all your posts')
    print('-post ~ Print a specified post based on post ID #')
    print('-all ~ Print all content\n')


def welcome():
    '''
    Initial print message when 
    the program is ran, this only
    triggers once to Welcome the 
    user
    '''
    print('+-----------------------------------------------------------------------------------------------------------+')
    print('| Hello, welcome to My Journal and File Searcher. Enter one of the following commands below to get started! |')
    print('+-----------------------------------------------------------------------------------------------------------+\n')
    instructions()
    print('NOTE - Please do not add any spaces before or after your entries unless shown in the instructions!')
    print()


def upload(upload_path, upload_profile, printer, post_number, status):
    '''
    This gives instructions and
    takes input for the U command
    asking the user what they would
    like to upload to the dsu 
    server
    '''
    if printer is True:
        print()
        print('The following are the contents of your Journal/File:\n')

    if printer is True:
        command = [['-all', None]]
        a5.file_printer(upload_path, upload_profile, command, status)
    if printer is True:
        print('________________________________________________\n')
        print('+----------------------------------------------+')
        print('| OPTIONS - The following are options to post. |')
        print('+----------------------------------------------+\n')
        print('bio ~ Send your current bio to the server')
        print('post ~ Select one of your posts by ID to send to the server')
        print('both ~ Send both your current bio and a post by ID to the server')
        print('none ~ Return home and cancel posting\n')
    elif printer is False:
        print('________________________________________________\n')
        print('+----------------------------------------------+')
        print('| OPTIONS - The following are options to post. |')
        print('+----------------------------------------------+\n')
        print('bio ~ Send your new bio to the server')
        print('post ~ Send you new post to the server')
        print('both ~ Send both your new bio and post to the server')
        print('none ~ Return home and cancel posting\n')
    choice = input('Enter one of the options to post to the server: ')
    print()
    upload_post_id = None
    if printer is True:
        if choice == 'post' or choice == 'both':
            upload_post_id = input('Enter the ID of the post you would like to send to the server: ')
            print()
    elif printer is False:
        if choice == 'post' or choice == 'both':
            upload_post_id = str(post_number)
    return choice, upload_post_id


def main():
    '''
    This is the main function, it gets
    call first from a5.py which triggers
    the instruction and also the command
    processing to tell the program which
    command to go to in a5 after user input
    '''
    global user_cnt
    global command_status
    global old_path
    global old_profile

    port = 3021
    cont = True
    user = 'Default'
    admin = ''
    e_cmd_lst = ['', '', '', '', '']

    if user_cnt == 0:
        welcome()
    else:
        pass

    while cont is True:
        if user_cnt == 0:
            if user in ['Default', 'L', 'R', 'C', 'D', 'Q', 'O', 'E', 'P', 'U']:
                user = input('What would you like to explore or create. Please enter a command (type "I" for list of commands): ')
        else:
            if user in ['Default', 'L', 'R', 'C', 'D', 'Q', 'O', 'E', 'P', 'U', 'I']:
                user = input('Enter any command to continue or quit (type "I" for list of commands): ')

        if user in ['L', 'R', 'C', 'D', 'Q', 'I', 'O', 'E', 'P', 'U']:
            print()
            status = 'user'
            if user == 'I':
                command_list()
                cont = True
                admin = user
            elif user == 'L':
                user_path = input('Enter the path where you would like to list your folders and files: ')
                print()
                print('+-------------------------------------------------------------------------------------+')
                print('| OPTIONAL - Listing includes optional commands for specific searches in this folder! |')
                print('+-------------------------------------------------------------------------------------+\n')
                print('-r ~ Also list all your sub-folders and sub-files (recursive searching)')
                print('-f ~ List only your files')
                print('-s examplefile.extension ~ Find a file with a specific name and extension')
                print('-e extension ~ Find all files with a specific extension (do not include the period in your extenstion [py NOT .py])')
                print('-r -s examplefile.extension ~ Find all files with a specific name and extension recursively')
                print('-r -e extension ~ Find all files with a specific extension recursively (do not include the period in your extenstion [py NOT .py])')
                print('none ~ Just list your folders and files\n')
                list_option = input('Enter an optional command if you would like to specify your search: ')
                print()
                if list_option == 'none':
                    admin = user + ' ' + user_path
                else:
                    admin = user + ' ' + user_path + ' ' + list_option
            elif user == 'R':
                user_path = input('Enter the path to the .dsu file you would like to read, include the file in the path (.dsu files only): ')
                admin = user + ' ' + user_path
            elif user == 'C':
                user_path = input('Enter the path where you would like to create a new Journal/File (do not include the filename): ')
                print()
                file_name = input('What would you like to name your Journal (only include the name, not the extenstion): ')
                print()
                admin = user + ' ' + user_path + ' -n ' + file_name
            elif user == 'D':
                user_path = input('Enter the path where you would like to delete a file or Journal (do not include the filename): ')
                print()
                file_name = input('What is the name of the file you would like to delete (only .dsu files): ')
                print()
                my_os = platform.system()
                if my_os == 'Windows':
                    admin = user + ' ' + user_path + '\\' + file_name
                else:
                    admin = user + ' ' + user_path + '/' + file_name
            elif user == 'O':
                user_path = input('Enter the path where your file is located (do not include the filename): ')
                print()
                file_name = input('Now enter the file you would like to open (include the file and the .dsu extension): ')
                print()
                my_os = platform.system()
                if my_os == 'Windows':
                    admin = user + ' ' + user_path + '\\' + file_name
                else:
                    admin = user + ' ' + user_path + '/' + file_name
            elif (user == 'E'):
                if (command_status == 'O ' or command_status == 'C ' or command_status == 'E ' or command_status == 'P '):
                    edit_options()
                    admin = user
                    cont_ask = True
                    e_count = 0
                    while cont_ask is True:
                        if_invalid = ''
                        yn = ''
                        if e_count == 0:
                            option_name = input('How would you like to edit your Journal/File? Please enter a command from above: ')
                        else:
                            option_name = input('Please enter another command: ')
                        print()
                        if option_name == '-ip':
                            new_ip = input('Enter your new IP Address: ')
                            admin += ' ' + option_name + ' ' + f'"{new_ip}"'
                        elif option_name == '-usr':
                            new_usr = input('Enter your new username: ')
                            admin += ' ' + option_name + ' ' + f'"{new_usr}"'
                        elif option_name == '-pwd':
                            new_pwd = input('Enter your new password: ')
                            admin += ' ' + option_name + ' ' + f'"{new_pwd}"'
                        elif option_name == '-bio':
                            new_bio = input('Enter your new biography: ')
                            admin += ' ' + option_name + ' ' + f'"{new_bio}"'
                        elif option_name == '-addpost':
                            new_post = input('Enter your new post: ')
                            admin += ' ' + option_name + ' ' + f'"{new_post}"'
                        elif option_name == '-delpost':
                            post_id = input('Enter the ID of the post you would like to delete: ')
                            admin += ' ' + option_name + ' ' + f'"{post_id}"'
                        else:
                            if_invalid = input('Invalid command was entered, would you like to try again (y/n)? ')
                            print()
                            proper = True
                            while proper is True:
                                if if_invalid == 'y':
                                    cont_ask = True
                                    proper = False
                                elif if_invalid == 'n':
                                    cont_ask = False
                                    proper = False
                                else:
                                    yn = input('Please only enter (y/n): ')
                                    if yn == 'y':
                                        proper = False
                                        cont_ask = True
                                    elif yn == 'n':
                                        proper = False
                                        cont_ask = False
                                    else:
                                        proper = True
                        print()
                        if (yn != 'n' and (if_invalid != 'n' and if_invalid != 'y')):
                            if_cont = input('Would you like to enter another command and make another edit (y/n)? ')
                            print()
                            v = True
                            while v is True:
                                if if_cont == 'y':
                                    cont_ask = True
                                    v = False
                                elif if_cont == 'n':
                                    cont_ask = False
                                    v = False
                                else:
                                    y_n = input('Please only enter (y/n): ')
                                    if y_n == 'y':
                                        v = False
                                        cont_ask = True
                                    elif y_n == 'n':
                                        v = False
                                        cont_ask = False
                                    else:
                                        v = True
                        e_count += 1

                    print()
                    admin = admin
                else:
                    print('Ensure that you open/load or create a file before trying to edit it.\n')
                    admin = user
            elif (user == 'P'):
                if (command_status == 'O ' or command_status == 'C ' or command_status == 'E ' or command_status == 'P '):
                    print_options()
                    admin = user
                    cont_ask = True
                    p_count = 0
                    while cont_ask is True:
                        if_invalid = ''
                        yn = ''
                        if p_count == 0:
                            option_name = input('What would you like to print from your Journal/File? Please enter a command from above: ')
                        else:
                            option_name = input('Please enter another command: ')
                        print()
                        if option_name == '-ip':
                            admin += ' ' + option_name
                        elif option_name == '-usr':
                            admin += ' ' + option_name
                        elif option_name == '-pwd':
                            admin += ' ' + option_name
                        elif option_name == '-bio':
                            admin += ' ' + option_name
                        elif option_name == '-posts':
                            admin += ' ' + option_name
                        elif option_name == '-post':
                            post_id = input('Enter the ID of the post you would like to see: ')
                            admin += ' ' + option_name + ' ' + f'{post_id}'
                        elif option_name == '-all':
                            admin += ' ' + option_name
                        else:
                            if_invalid = input('Invalid command was entered, would you like to try again [-all can only be entered on its own] (y/n)? ')
                            print()
                            proper = True
                            while proper is True:
                                if if_invalid == 'y':
                                    cont_ask = True
                                    proper = False
                                elif if_invalid == 'n':
                                    cont_ask = False
                                    proper = False
                                else:
                                    yn = input('Please only enter (y/n): ')
                                    if yn == 'y':
                                        proper = False
                                        cont_ask = True
                                    elif yn == 'n':
                                        proper = False
                                        cont_ask = False
                                    else:
                                        proper = True

                        if (yn != 'n' and (if_invalid != 'n' and if_invalid != 'y')):
                            if_cont = input('Would you like to enter another command to print another part of your Journal/File (y/n)? ')
                            print()
                            v = True
                            while v is True:
                                if if_cont == 'y':
                                    cont_ask = True
                                    v = False
                                elif if_cont == 'n':
                                    cont_ask = False
                                    v = False
                                else:
                                    y_n = input('Please only enter (y/n): ')
                                    if y_n == 'y':
                                        v = False
                                        cont_ask = True
                                    elif y_n == 'n':
                                        v = False
                                        cont_ask = False
                                    else:
                                        v = True
                        p_count += 1

                    print()
                    admin = admin
                else:
                    print('Ensure that you open/load or create a file before trying to print its contents\n')
                    admin = user
            elif user == 'U':
                admin = user
                # ip_address = input('Please enter the IP address of the server you would like to post to: ')
            elif user == 'Q':
                admin = user
        # Here I got rid of admin mode for the a5 assignment
        # elif user == 'admin':
            # status = 'admin'
            # user = 'admin'
            # admin = input()
        else:
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('| Invalid input, please enter only one of the following commands: |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n')
            command_list()
            admin = user
            user = 'I'
            status = 'user'

        command = admin[0:2]
        # print(command)

        pathway_lst = path_extractor(admin)
        og_user = admin

        if command == 'Q' and len(admin) == 1:
            if status == 'user':
                print('Goodbye, have a great rest of your day. Happy Searching!\n')
            cont = False

        elif (len(admin) > 2) or (command == 'U'):
            if command == 'L ':
                if len(pathway_lst) > 0:
                    pathway = pathway_lst[0]
                else:
                    pathway = ''

                if ' -s ' in admin:
                    user_end_lst = re.findall(r' -s (.*)$', admin)
                    user_end = user_end_lst[0]

                    new = admin.replace(pathway, '')
                    new = new.replace(user_end, '')
                    command_lst = new.split(' ')
                elif ' -e ' in admin:
                    user_end_lst = re.findall(r' -e (.*)$', admin)
                    user_end = user_end_lst[0]

                    new = admin.replace(pathway, '')
                    new = new.replace(user_end, '')
                    command_lst = new.split(' ')
                else:
                    user_end = None
                    new = admin.replace(pathway, '')
                    command_lst = new.split(' ')

                # Initial check to make sure that the path inputted is valid
                if path_exists(pathway, status) is True:

                    files_found = 0
                    file_count = 0
                    file_not_found = 0

                    a5.fff_count = 0
                    a5.fff_nfound = 0
                    a5.fff_found = 0

                    file_count, file_not_found, files_found = a5.directory_search(pathway, status, command_lst, user_end, files_found, file_count, file_not_found)

                    # This is an exception check for -r -s (file name)
                    # If a file is not in any recursive directory
                    if (len(command_lst) == 5):
                        if (command_lst[2] == '-r' and command_lst[3] == '-s') or (command_lst[2] == '-r' and command_lst[3] == '-e'):
                            # print(f'FCOUNT {file_count}')
                            # print(f'FILENOTFOUND {file_not_found}')
                            if file_count == file_not_found:
                                if command_lst[3] == '-s':
                                    if status == 'user':
                                        print(f'No files with this name found.')
                                    elif status == 'admin':
                                        print('ERROR')
                                elif command_lst[3] == '-e':
                                    if status == 'user':
                                        print(f'No files with this extension found')
                                    elif status == 'admin':
                                        print('ERROR')
                    elif (len(command_lst) > 5):
                        print('ERROR')
                else:
                    pass

                if status == 'user':
                    print()

                cont = True

            # Allows the user to create a new file in a specified directory
            elif command == 'C ':
                if len(pathway_lst) > 0:
                    pathway = pathway_lst[0]
                else:
                    pathway = ''

                new = admin.replace(pathway, '')
                command_lst = new.split(' ')

                # Initial check to make sure that the path inputted is valid
                if path_exists(pathway, status) is True:

                    old_path, old_profile = a5.new_file_creator(pathway, status, command_lst, og_user)

                else:
                    print('File was not created.\n')
                    command = 'N '

            # Allows the user to read '.dsu' files (only)
            elif command == 'R ':
                if len(pathway_lst) > 0:
                    pathway = pathway_lst[0]
                else:
                    pathway = ''

                new = admin.replace(pathway, '')
                command_lst = new.split(' ')

                # Initial check to make sure that the path inputted is valid
                if path_exists(pathway, status) is True:

                    a5.file_reader(pathway, status, command_lst)

            # If the user wants to delete a .dsu file
            elif command == 'D ':
                if len(pathway_lst) > 0:
                    pathway = pathway_lst[0]
                else:
                    pathway = ''

                # Initial check to make sure that the path inputted is valid
                if path_exists(pathway, status) is True:

                    a5.file_deleter(pathway, status, command)

            elif command == 'O ':
                if len(pathway_lst) > 0:
                    pathway = pathway_lst[0]
                else:
                    pathway = ''

                # Initial check to make sure that the path inputted is valid
                if path_exists(pathway, status) is True:

                    old_path, old_profile, dsu = a5.file_loader(pathway, status, command)

                if (path_exists(pathway, status) is False) or (dsu is False):
                    print('File was not loaded.\n')
                    command = 'N '

            elif command == 'E ':
                if (command_status == 'O ' or command_status == 'C ' or command_status == 'E ' or command_status == 'P '):
                    a5.file_editor(admin, old_path, old_profile, pathway_lst, port, status)
                else:
                    if status == 'user':
                        print('File must be created or opening before attempting to edit.')
                    elif status == 'admin':
                        print('ERROR')
            elif command == 'P ':
                if (command_status == 'O ' or command_status == 'C ' or command_status == 'E ' or command_status == 'P '):
                    a5.file_printer(old_path, old_profile, pathway_lst, status)
                else:
                    if status == 'user':
                        print('File must be created or opening before attempting to print contents.')
                    elif status == 'admin':
                        print('ERROR')
            elif command == 'U':
                if (command_status == 'O ' or command_status == 'C ' or command_status == 'E ' or command_status == 'P '):
                    printer = True
                    post_number = None
                    a5.uploader(old_path, old_profile, port, printer, post_number, status)
                else:
                    if status == 'user':
                        print('File must be created or opening before attempting to upload contents.')
                    elif status == 'admin':
                        print('ERROR')
            else:
                if status == 'user':
                    pass
                elif status == 'admin':
                    print('ERROR')

        # If the user inputted an initial command that is invalid
        else:
            if command == 'I':
                if status == 'user':
                    pass
                elif status == 'admin':
                    print('ERROR')
            else:
                if status == 'admin':
                    print('ERROR')
                cont = True
        # print()
        user_cnt += 1
        if (command != 'I') and (command != 'E ') and (command != 'P ') and (command != 'U ') and (command != 'U') and (command != 'E') and (command != 'P') and (user != 'I'):
            command_status = command
            # print(command_status)
