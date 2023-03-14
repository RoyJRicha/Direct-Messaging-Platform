'''
a5.py is responsible for processing
all commands that the user may enter,
such as E, L, P, etc.
'''
# a5.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Roy Richa
# rricha@uci.edu
# 51514923

import os
import re
import sys
import platform
import ui
import Profile
import ds_client
from OpenWeather import OpenWeather
from LastFM import LastFM

fff_count = 0
fff_found = 0
fff_nfound = 0


def biometrics():
    '''
    Creates biometrics
    '''
    ip = input('Enter an IP Address to make future posts to a server: ')
    print()
    un = input('Enter a username (no spaces): ')
    print()
    ps = input('Enter a password (no spaces): ')
    print()
    b = input('Would you like to add a bio (Type Y for yes, type anything else for no)?')
    print()
    if b == 'Y':
        bi = input('Please write a short biography about yourself: ')
        print()
    else:
        bi = ''

    return ip, un, ps, bi


def profile_saver(full_p, ip=None, un=None, ps=None, bi=None):
    '''
    Saves the user profile to Profile.py
    '''
    profile = Profile.Profile()
    profile.save_profile(full_p)
    profile.dsuserver = ip
    profile.username = un
    profile.password = ps
    profile.bio = bi
    profile.save_profile(full_p)

    return profile


def file_loader(path, status, command=None):
    '''
    This is responsible for the O
    command which is loading the
    file that the user requests
    '''
    load = None
    dsu = True
    try:
        if len(command) == 2 or command[0] == 'C':
            load = Profile.Profile()
            load.load_profile(path)
            
            if status == 'user':
                print('Your file has successfully been loaded. The following are your biometrics:\n')
                print(f'IP Address: {load.dsuserver}')
                print(f'Username: {load.username}')
                print(f'Password: {load.password}')
                print(f'Biography: {load.bio}\n')
            elif status == 'admin':
                pass
        else:
            print('ERROR')
    except Profile.DsuProfileError:
        if status == 'user':
            dsu = False
            print('This file does not have the proper contents and has not been stored in the database.\n')
            print('\tPlease enter a valid .dsu file/journal with a valid Profile.\n')
        elif status == 'admin':
            dsu = False
            print('ERROR')
    except Profile.DsuFileError:
        if status == 'user':
            dsu = False
            print('Pleaser enter only a .dsu file along with the path.\n')
        elif status == 'admin':
            dsu = False
            print('ERROR')

    return path, load, dsu


# When command 'C' is inputted, to create a new file
def new_file_creator(path, status, command=None, og_input=None):
    '''
    This is responsible for the C command
    which is creating a file with a custom
    name that the user requests
    '''
    o_profile = ''
    if len(command) >= 4:
        if command[2] == '-n':
            user_file_lst = re.findall(r'-n\s(.*)$', og_input)
            user_file = user_file_lst[0]

            my_os = platform.system()
            if my_os == 'Windows':
                full_path = path + '\\' + user_file + '.dsu'

                if os.path.exists(full_path):
                    if status == 'user':
                        print('This file already exits, your file will be loaded instead!\n')
                    else:
                        pass

                    full_path, o_profile, dsu_profile = file_loader(full_path, status, command)

                elif not os.path.exists(full_path):
                    with open(full_path, 'w') as fp:
                        pass

                    if status == 'user':
                        print()
                        print('Your journal has been created at: ')
                        print(full_path)
                        print()
                        address, username, password, bio = biometrics()

                        if (' ' in username) or (username == '') or (' ' in password) or (password == '') or (' ' in address) or (address == ''):
                            print('Biometrics were not saved due to the following issues:\n')
                            if ' ' in username:
                                print('\tUsername cannot contain spaces\n')
                            if username == '':
                                print('\tUsername is a required feild and cannot be left empty\n')
                            if ' ' in password:
                                print('\tPassword cannot contain spaces\n')
                            if password == '':
                                print('\tPassword is a required feild and cannot be left empty\n')
                            if ' ' in address:
                                print('\tInvalid IP Address, cannot contain space\n')
                            if address == '':
                                print('\tIP Address is a required feild and cannot be left empty\n')
                            print('Profile was not saved, please create a new file, or delete and recreate this file with a proper profile.\n')
                        else:
                            o_profile = profile_saver(full_path, address, username, password, bio)

                    elif status == 'admin':
                        print(full_path)
                        o_profile = profile_saver(full_path)

                else:
                    print('ERROR')

            else:
                full_path = path + '/' + user_file + '.dsu'

                if os.path.exists(full_path):
                    if status == 'user':
                        print('This file already exits, your file was loaded instead!\n')
                    else:
                        pass

                    full_path, o_profile, dsu_profile = file_loader(full_path, status, command)

                elif not os.path.exists(full_path):
                    with open(full_path, 'w') as fp:
                        pass

                    if status == 'user':
                        print()
                        print('Your journal has been created at: ')
                        print(full_path)
                        print()
                        address, username, password, bio = biometrics()

                        if (' ' in username) or (username == '') or (' ' in password) or (password == '') or (' ' in address) or (address == ''):
                            print('Biometrics were not saved due to the following issues:\n')
                            if ' ' in username:
                                print('\tUsername cannot contain spaces\n')
                            if username == '':
                                print('\tUsername is a required feild and cannot be left empty\n')
                            if ' ' in password:
                                print('\tPassword cannot contain spaces\n')
                            if password == '':
                                print('\tPassword is a required feild and cannot be left empty\n')
                            if ' ' in address:
                                print('\tInvalid IP Address, cannot contain space\n')
                            if address == '':
                                print('\tIP Address is a required feild and cannot be left empty\n')
                            print('Profile was not saved, please create a new file, or delete and recreate this file with a proper profile.\n')
                        else:
                            o_profile = profile_saver(full_path, address, username, password, bio)

                    elif status == 'admin':
                        print(full_path)
                        o_profile = profile_saver(full_path)

                else:
                    print('ERROR')

        else:
            print('ERROR')
    else:
        print('ERROR')

    return full_path, o_profile


def uploader(path, profile, port, printer, post_number, status):
    '''
    This is responsible for the U command
    which is uploading a post and/or bio to
    the server that the user requests
    '''
    choice, id_post = ui.upload(path, profile, printer, post_number, status)
    server_address = profile.dsuserver
    username = profile.username
    password = profile.password
    bio = None
    post = None
    dict_element = 'entry'
    id_range = ''
    int_check = ''
    id_check = ''

    if choice == 'bio':
        bio = profile.bio
        ds_client.send(server_address, port, username, password, post , bio)
    elif choice == 'post':
        id_range, int_check, id_check = post_send(profile, id_post, dict_element, server_address, port, username, password, post, bio)
    elif choice == 'both':
        bio = profile.bio
        id_range, int_check, id_check = post_send(profile, id_post, dict_element, server_address, port, username, password, post, bio)
    elif choice == 'none':
        print('Cancelled connection to server, nothing was posted!\n')
    else:
        print('Invalid option. Please enter only one of the options listed above.\n')
        print('Please try again!\n')
    
    if (id_range != '') or (int_check != '') or (id_check != ''):
        print('Contents were not posted due to the following issue(s):\n')
        if id_range != '':
            print(f'\t{id_range}\n')
        if int_check != '':
            print(f'\t{int_check}\n')
        if id_check != '':
            print(f'\t{id_check}\n')


def post_send(profile, id_post, dict_element, server_address, port, username, password, post, bio):
    '''
    Responsible for sending specifically
    the post to the server. This is a function
    used in upload()
    '''
    id_range = ''
    int_check = ''
    id_check = ''
    try:
        if '.' in id_post:
            raise ValueError
        else:
            id_post = int(id_post)
            pass

        try:
            post_lst = Profile.Profile.get_posts(profile)
            post = post_lst[id_post][dict_element]
            result = ds_client.send(server_address, port, username, password, post, bio)
            if result is False:
                print('Unable to connect or publish to the server due to the message(s) above. Please try again!\n')
            else:
                # Success statements were performed in ds_client.py
                pass
        except IndexError:
            id_range = 'Post ID request doesn\'t exist. ID out of range.'
    except ValueError:
        int_check = 'Ensure that you only enter an integer ID for the -post ID.'
    except TypeError:
        id_check = 'ID number was not provided for -post. Make sure to include an ID number for what post you would like to access.'

    return id_range, int_check, id_check


def file_printer(path, profile, contents, status):
    '''
    This is responsible for the P command
    which is printing certain contents from
    a users file
    '''
    error_proof = True
    err_check = ''
    int_check = ''
    all_check = ''
    id_check = ''
    id_range = ''
    ip_cnt = 0
    usr_cnt = 0
    pwd_cnt = 0
    bio_cnt = 0
    pst_cnt = 0
    p_cnt = 0
    all_cnt = 0
    dict_element = 'entry'
    try:
        for check in contents:
            if check[0] == '-ip' and check[1] == None:
                ip_cnt += 1
                pass
            elif check[0] == '-usr' and check[1] == None:
                usr_cnt += 1
                pass
            elif check[0] == '-pwd' and check[1] == None:
                pwd_cnt += 1
                pass
            elif check[0] == '-bio' and check[1] == None:
                bio_cnt += 1
                pass
            elif check[0] == '-posts' and check[1] == None:
                pst_cnt += 1
                pass
            elif check[0] == '-post':
                try:
                    if '.' in check[1]:
                        raise ValueError
                    else:
                        pst_id = int(check[1])
                        p_cnt += 1
                        pass

                    try:
                        post_lst = Profile.Profile.get_posts(profile)
                        p_ID = post_lst[pst_id][dict_element]
                    except IndexError:
                        id_range = 'Post ID request doesn\'t exist. ID out of range.'
                        error_proof = False
                except ValueError:
                    int_check = 'Ensure that you only enter an integer ID for the -post ID.'
                    error_proof = False
                except TypeError:
                    id_check = 'ID number was not provided for -post. Make sure to include an ID number for what post you would like to access.'
            elif check[0] == '-all' and check[1] == None:
                all_cnt += 1
                pass
            else:
                err_check = 'One or more of your commands were invalid, please try again.'
                error_proof = False

        if all_cnt >= 1 and (ip_cnt != 0 or usr_cnt != 0 or pwd_cnt != 0 or bio_cnt != 0 or pst_cnt != 0 or p_cnt != 0):
            all_check = 'The -all option can only be entered as a command on its own, not in addition to any other options'
            error_proof = False
        else:
            pass

        if (error_proof is True) and (ip_cnt < 2 and usr_cnt < 2 and pwd_cnt < 2 and bio_cnt < 2 and pst_cnt < 2 and p_cnt < 2 and all_cnt < 2):
            for text in contents:
                if text[0] == '-ip':
                    if status == 'user':
                        print(f'IP Address: {profile.dsuserver}')
                    elif status == 'admin':
                        print(profile.dsuserver)
                elif text[0] == '-usr':
                    if status == 'user':
                        print(f'Username: {profile.username}')
                    elif status == 'admin':
                        print(profile.username)
                elif text[0] == '-pwd':
                    if status == 'user':
                        print(f'Password: {profile.password}')
                    elif status == 'admin':
                        print(profile.password)
                elif text[0] == '-bio':
                    if status == 'user':
                        print(f'Bio: {profile.bio}')
                    elif status == 'admin':
                        print(profile.bio)
                elif text[0] == '-posts':
                    if status == 'user':
                        posts_lst = Profile.Profile.get_posts(profile)
                        print('ID # | Post:')
                        p_ID = 0
                        for p in posts_lst:
                            print(f'{p_ID}    | {p[dict_element]}')
                            p_ID += 1
                    elif status == 'admin':
                        posts_lst = Profile.Profile.get_posts(profile)
                        for p in posts_lst:
                            print(p['entry'])
                elif text[0] == '-post':
                    if status == 'user':
                        post_lst = Profile.Profile.get_posts(profile)
                        print(f'Post {pst_id}: {post_lst[pst_id][dict_element]}')
                    elif status == 'admin':
                        try:
                            post_lst = Profile.Profile.get_posts(profile)
                            print(post_lst[pst_id][dict_element])
                        except IndexError:
                            if status == 'user':
                                print('Post ID requested doesn\'t exist')
                            elif status == 'admin':
                                print('ERROR')
                elif text[0] == '-all':
                    if status == 'user':
                        print(f'IP Address: {profile.dsuserver}')
                        print(f'Username: {profile.username}')
                        print(f'Password: {profile.password}')
                        print(f'Bio: {profile.bio}\n')

                        posts_lst = Profile.Profile.get_posts(profile)
                        print('ID # | Post:')
                        p_ID = 0
                        for p in posts_lst:
                            print(f'{p_ID}    | {p[dict_element]}')
                            p_ID += 1
                    elif status == 'admin':
                        print(f'{profile.username}')
                        print(f'{profile.password}')
                        print(f'{profile.bio}')

                        posts_lst = Profile.Profile.get_posts(profile)
                        p_ID = 0
                        for p in posts_lst:
                            print(f'{p[dict_element]}')
                            p_ID += 1
            if status == 'user':
                print()
        elif error_proof is False:
            if status == 'user':
                print('Contents were not printed due to the following issue(s):\n')
                if err_check != '':
                    print(f'\t{err_check}\n')
                if int_check != '':
                    print(f'\t{int_check}\n')
                if all_check != '':
                    print(f'\t{all_check}\n')
                if id_check != '':
                    print(f'\t{id_check}\n')
                if id_range != '':
                    print(f'\t{id_range}\n')

                if (ip_cnt > 1 or usr_cnt > 1 or pwd_cnt > 1 or bio_cnt > 1 or pst_cnt > 1 or p_cnt > 1 or all_cnt > 1):
                    print('\tPlease ensure you enter at most one of each command at a time.\n')
            elif status == 'admin':
                print('ERROR')
        elif (error_proof is True) and (ip_cnt > 1 or usr_cnt > 1 or pwd_cnt > 1 or bio_cnt > 1 or pst_cnt > 1 or p_cnt > 1 or all_cnt > 1):
            if status == 'user':
                print('Contents were not printed due to the following issue(s):\n')
                print('\tPlease ensure you enter at most one of each command at a time.\n')
            elif status == 'admin':
                print('ERROR')
    except AttributeError:
        print('Contents were not printed due to the following issue(s):\n')
        print('\tFile does not contain the proper Profile format to print contents.\n')
        print()
        print('Please try again. Enter only .dsu files with the proper Profile format.\n')


def file_editor(admin_input, path, profile, contents, port, status):
    '''
    This is responsible for the E command
    which is editing certain contents of a 
    users file
    '''
    error_proof = True
    int_check = ''
    err_check = ''
    id_check = ''
    range_check = ''
    ip_space = ''
    usr_space = ''
    pwd_space = ''
    quotes_check = ''
    quotes_empty_check = ''
    ip_cnt = 0
    usr_cnt = 0
    pwd_cnt = 0
    bio_cnt = 0
    add_cnt = 0
    del_cnt = 0
    weather_api_key = "af6472f0ac363c93d26a4f628d577fe1"
    fm_api_key = "441e295d5bbbdf8c61fcea2b4bd20fb0"

    try:
        if (int(admin_input.count('"')) % 2) == 0 or (int(admin_input.count('"')) == 0):
            if contents == []:
                err_check = 'One or more of your commands were invalid, please try again.'
                error_proof = False
            for check in contents:
                if check[0] == '-ip':
                    if (' ' not in check[1]) and (check[1] != ''):
                        ip_cnt += 1
                        pass
                    else:
                        if ' ' in check[1]:
                            ip_space = 'Cannot save IP Address. Ensure there are no spaces in your IP Address.'
                        elif check[1] == '':
                            quotes_empty_check = 'Please ensure not to enter quotes in your input and that your input is not blank.'
                        error_proof = False
                elif check[0] == '-usr':
                    if (' ' not in check[1]) and (check[1] != ''):
                        usr_cnt += 1
                        pass
                    else:
                        if ' ' in check[1]:
                            usr_space = 'Cannot save username. Ensure there are no spaces in your username.'
                        elif check[1] == '':
                            quotes_empty_check = 'Please ensure not to enter quotes in your input and that your input is not blank.'
                        error_proof = False
                elif check[0] == '-pwd':
                    if ' ' not in check[1] and (check[1] != ''):
                        pwd_cnt += 1
                        pass
                    else:
                        if ' ' in check[1]:
                            pwd_space = 'Cannot save password. Ensure there are no spaces in your password.'
                        elif check[1] == '':
                            quotes_empty_check = 'Please ensure not to enter quotes in your input and that your input is not blank.'
                        error_proof = False
                elif check[0] == '-bio':
                    if check[1] != '':
                        bio_cnt += 1
                        pass
                    else:
                        if check[1] == '':
                            quotes_empty_check = 'Please ensure not to enter quotes in your input and that your input is not blank.'
                        error_proof = False
                elif check[0] == '-addpost':
                    if check[1] != '':
                        add_cnt += 1
                        pass
                    else:
                        if check[1] == '':
                            quotes_empty_check = 'Please ensure not to enter quotes in your input and that your input is not blank.'
                        error_proof = False
                elif check[0] == '-delpost':
                    try:
                        if '.' in check[1]:
                            raise ValueError
                            pass
                        del_id = int(check[1])
                        posts_lst = Profile.Profile.get_posts(profile)
                        if del_id <= (len(posts_lst) - 1):
                            del_cnt += 1
                            pass
                        else:
                            range_check = 'Cannot delete post, ID is out of range of the number of posts.'
                            error_proof = False
                    except ValueError:
                        int_check = 'Ensure that you only enter an integer ID for deleting a post.'
                        error_proof = False
                    except TypeError:
                        id_check = 'ID number was not provided for -post. Make sure to include an ID number for what post you would like to access.'
                else:
                    err_check = 'One or more of your commands were invalid, please try again.'
                    error_proof = False
        else:
            quotes_check = 'Please ensure to close off any quotes (") when done inputting an option'
            error_proof = False

        if (error_proof is True) and (ip_cnt < 2 and usr_cnt < 2 and pwd_cnt < 2 and bio_cnt < 2 and add_cnt < 2 and del_cnt < 2):
            for text in contents:
                if text[0] == '-ip':
                    new_ip_address = text[1]
                    profile.dsuserver = new_ip_address
                elif text[0] == '-usr':
                    new_username = text[1]
                    profile.username = new_username
                elif text[0] == '-pwd':
                    new_password = text[1]
                    profile.password = new_password
                elif text[0] == '-bio':
                    new_bio = text[1]
                    profile.bio = new_bio
                elif text[0] == '-addpost':
                    post = text[1]
                    # Check if a keyword (@weather/@lastfm is in a post)
                    if ("@weather" or "@weather_temp" or "@weather_humidity") in post:
                        ccode = input('Enter the country for your weather for your new post: ')
                        zipcode = input('Now enter the zipcode: ')
                        print()
                        weather_post = OpenWeather(zipcode, ccode)
                        weather_post.set_apikey(weather_api_key)
                        weather_post.load_data()
                        post = weather_post.transclude(post)
                        if weather_post.error_code != "":
                            print('\nPost was saved, however, was unable to replace key word @weather, @weather_temp, and/or @weather_humidity due to status code.\n')
                    if ("@lastfm" or "lastfm_listeners") in post:
                        fm_post = LastFM()
                        fm_post.set_apikey(fm_api_key)
                        fm_post.load_data()
                        post = fm_post.transclude(post)
                        if fm_post.error_code != "":
                            print('\nPost was saved, however, was unable to replace key word @lastfm due to status code.\n')

                    new_post = Profile.Post(post)
                    profile.add_post(new_post)
                elif text[0] == '-delpost':
                    posts_lst = Profile.Profile.get_posts(profile)
                    del_id = int(text[1])
                    profile.del_post(del_id)
            if usr_space == '' and pwd_space == '' and ip_space == '' and range_check == '':
                profile.save_profile(path)
                if status == 'user':
                    print('Success, your changes have been saved!\n')
                elif status == 'admin':
                    pass
            if bio_cnt == 1 or add_cnt == 1:
                if bio_cnt == 1 and add_cnt == 0 and usr_cnt == 0 and pwd_cnt == 0:
                    bio_post_choice = input('Would you like to update your new bio for your profile to the server (Y for yes, any other character for no)? ')
                    if bio_post_choice == 'Y':
                        profile_no_post = None
                        ds_client.send(profile.dsuserver, port, profile.username, profile.password, profile_no_post, profile.bio)
                    else:
                        print('Ok, nothing was published to the server. You can do so using the "U" command in the future if you would like')
                elif add_cnt == 1 and bio_cnt == 0 and usr_cnt == 0 and pwd_cnt == 0:
                    post_post_choice = input('Would you like to publish your new post on your profile to the server (Y for yes, any other character for no)? ')
                    if post_post_choice == 'Y':
                        ds_client.send(profile.dsuserver, port, profile.username, profile.password, post)
                    else:
                        print('\nOk, nothing was published to the server. You can do so using the "U" command in the future if you would like\n')
                elif bio_cnt == 1 and add_cnt == 1 and usr_cnt == 0 and pwd_cnt == 0:
                    bio_post_post_choice = input('Would you like to publish your new bio or post (or both) on your profile to the server (Y for yes, any other character for no)? ')
                    if bio_post_post_choice == 'Y':
                        all_posts = Profile.Profile.get_posts(profile)
                        post_number = len(all_posts) - 1
                        printer = False
                        uploader(path, profile, port, printer, post_number, status)
                    else:
                        print('\nOk, nothing was published to the server. You can do so using the "U" command in the future if you would like\n')
        elif error_proof is False:
            if status == 'user':
                print('Changes were not saved due to the following issue(s):\n')
                if err_check != '':
                    print(f'\t{err_check}\n')
                if int_check != '':
                    print(f'\t{int_check}\n')
                if id_check != '':
                    print(f'\t{id_check}\n')
                if ip_space != '':
                    print(f'\t{ip_space}\n')
                if usr_space != '':
                    print(f'\t{usr_space}\n')
                if pwd_space != '':
                    print(f'\t{pwd_space}\n')
                if range_check != '':
                    print(f'\t{range_check}\n')
                if quotes_check != '':
                    print(f'\t{quotes_check}\n')
                if quotes_empty_check != '':
                    print(f'\t{quotes_empty_check}\n')

                if (ip_cnt > 1 or usr_cnt > 1 or pwd_cnt > 1 or bio_cnt > 1 or add_cnt > 1 or del_cnt > 1):
                    print('\tPlease ensure you enter at most one of each command at a time.\n')
            elif status == 'admin':
                print('ERROR')
        elif (error_proof is True) and (ip_cnt > 1 or usr_cnt > 1 or pwd_cnt > 1 or bio_cnt > 1 or add_cnt > 1 or del_cnt > 1):
            if status == 'user':
                print('Changes were not saved due to the following issue(s):\n')
                print('\tPlease ensure you enter at most one of each command at a time.\n')
            elif status == 'admin':
                print('ERROR')
    except AssertionError:
        print('Contents were not edited due to the following issue(s):\n')
        print('\tFile does not contain the proper Profile format to print contents.\n')
        print()
        print('Please try again. Enter only .dsu files with the proper Profile format.\n')


# When command 'R' is inputted, to read a specified file
def file_reader(path, status, command=None):
    '''
    This is responsible for the R
    command which is Reading certain files
    specifically .txt files that the user
    requests
    '''
    if len(command) == 2:
        if path.endswith('.dsu'):
            if os.path.getsize(path) == 0:
                if status == 'user':
                    print('This file is empty, nothing to read.\n')
                elif status == 'admin':
                    print('EMPTY')
            else:
                with open(path, "r") as read_file:
                    data = read_file.read()
                    print(data)
        else:
            if status == 'user':
                print('Please only enter .dsu files to read.\n')
            elif status == 'admin':
                print('ERROR')
    else:
        if status == 'user':
            print('Not valid commands. Please try again.\n')
        elif status == 'admin':
            print('ERROR')


# When command 'D' is inputted, to delete a specified file
def file_deleter(path, status, command=None):
    '''
    This is responsible for the D command
    which allows the user to delete a specific
    .dsu file from their system
    '''
    if len(command) == 2:
        original = path
        if path.endswith('.dsu'):
            os.remove(path)
            if status == 'user':
                print('The following file has successfully been DELETED:\n')
                print(f'\t{original}\n')
            elif status == 'admin':
                print(f'{original} DELETED')
        else:
            if status == 'user':
                print('Invalid file type. Please enter only .dsu files to delete.\n')
            elif status == 'admin':
                print('ERROR')
    else:
        if status == 'user':
            print('Invalid path. Please try again!\n')
        elif status == 'admin':
            print('ERROR')


# When command 'L' is inputted, to go through different L commands
def directory_search(path, status, command=None, user_end=None, files_found=None, file_count=None, file_not_found=None):
    '''
    This is for the L command, responsible
    for allowing the user to search any files, 
    extensions, or even recurssive searching
    throughout their system
    '''
    # First it is necessary to check if the inputted path is valid

    global fff_count
    global fff_found
    global fff_nfound

    valid_parameters = True
    validity = True

    # Get's each item (directories and files) in the specified directory
    try:
        elements = os.listdir(path)

        # Takes elements and separates them into directories and files as lists
        directories = []
        files = []

        for element in elements:
            path_of_element = os.path.join(path, element)

            if os.path.isdir(path_of_element):
                directories.append(path_of_element)
            elif os.path.isfile(path_of_element):
                files.append(path_of_element)

        # Takes all the files first then puts them into another list
        # Takes all directories, puts them into the same list after the files
        # Confirms that output will be in order, files first then directories
        # Then adds files and directories to pathway for final print

        # No option was inputted from the user
        # Will just display all directories and files in said directory
        if len(command) == 2:
            for item in sorted(files):
                print(item)
            for elem in sorted(directories):
                print(elem)

        # Checks for 2 options, either -r or -f
        # Recursive or files only, will produce the output accordingly
        elif len(command) == 3:
            if command[2] == '-r':
                for item in sorted(files):
                    print(item)
                for elem in sorted(directories):
                    print(elem)
                    directory_search(elem, status, command, user_end)
            elif command[2] == '-f':
                for item in sorted(files):
                    print(item)
            else:
                valid_parameters = False

        # This checks for 3 options
        # Either '-r -f', '-s (file name)', or '-e (file extenstion)'
        elif len(command) == 4:
            if (command[2] == '-r') and (command[3] == '-f'):
                for item in sorted(files):
                    print(item)
                for elem in sorted(directories):
                    directory_search(elem, status, command, user_end)
            elif command[2] == '-s':
                file_found = False
                for item in sorted(files):
                    if user_end == os.path.basename(item):
                        print(item)
                        file_found = True
                        break
                if file_found is False:
                    if status == 'user':
                        print('File not found in this directory!\n')
                    elif status == 'admin':
                        print('ERROR')
            elif command[2] == '-e':
                extension_found = 0
                for item in sorted(files):
                    if ('.' + user_end) == os.path.splitext(item)[1]:
                        print(item)
                        extension_found += 1
                if extension_found == 0:
                    if status == 'user':
                        print(f'No files in this directory with this extension!\n')
                    elif status == 'admin':
                        print(f'ERROR')
            else:
                valid_parameters = False

        # This checks for 2 options
        # Either '-r -s (file name)' or '-r -e (file extension)'
        elif len(command) == 5:
            if (command[2] == '-r') and (command[3] == '-s'):

                for item in sorted(files):
                    file_count += 1
                    fff_count += file_count
                    if user_end == os.path.basename(item):
                        print(item)
                        files_found += 1
                        fff_found += files_found
                    else:
                        file_not_found += 1
                        fff_nfound += file_not_found

                for elem in sorted(directories):
                    directory_search(elem, status, command, user_end, files_found, file_count, file_not_found)

            elif (command[2] == '-r') and (command[3] == '-e'):

                for item in sorted(files):
                    file_count += 1
                    fff_count += file_count

                    if ('.' + user_end) == os.path.splitext(item)[1]:
                        print(item)
                        files_found += 1
                        fff_found += files_found
                    else:
                        file_not_found += 1
                        fff_nfound += file_not_found

                for elem in sorted(directories):
                    directory_search(elem, status, command, user_end, files_found, file_count, file_not_found)

            else:
                valid_parameters = False

    # This checks in case the path_exists() doesn't work properly
    # In case of failer, and error is raised, this will catch it
    except FileNotFoundError:
        if status == 'user':
            print('Folder was not found or invalid input, please try again.\n')
        elif status == 'admin':
            print('ERROR')

    if valid_parameters is False:
        if status == 'user':
            print('Invalid command parameters. Please try again!\n')
        elif status == 'admin':
            print('ERROR')

    return fff_count, fff_nfound, fff_found


if __name__ == '__main__':
    ui.main()
