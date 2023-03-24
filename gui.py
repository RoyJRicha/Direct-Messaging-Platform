import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from typing import Text
import os
import platform
import subprocess
import Profile as Profile
import ds_messenger as dm
import time
import datetime


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        try:
            print(self.posts_tree.selection())
            index = int(self.posts_tree.selection()[0])
            self.selection = index
        except IndexError:
            index = self.selection
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)
        #except IndexError:
            #pass
        

    def reset_tree(self):
        self.posts_tree.delete(*self.posts_tree.get_children())


    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str, timestamp:str):
        self.entry_editor.config(state='normal')
        self.entry_editor.tag_configure('blue_rounded_edge_timestamp', foreground='black', background='white', borderwidth=1, relief='ridge', font=('Arial', 8, 'normal'), justify='right')
        self.entry_editor.insert(1.0, timestamp + '\n', 'blue_rounded_edge_timestamp')
        self.entry_editor.tag_configure('blue_rounded_edge', foreground='black', background='#00D6EF', borderwidth=1, relief='ridge', font=('Arial', 11, 'normal'), justify='right')
        self.entry_editor.insert(1.0, message + '\n', 'blue_rounded_edge')
        self.entry_editor.config(state='disabled')

    def insert_contact_message(self, message:str, timestamp:str):
        self.entry_editor.config(state='normal')
        self.entry_editor.tag_configure('green_rounded_edge_timestamp', foreground='black', background='white', borderwidth=1, relief='ridge', font=('Arial', 8, 'normal'), justify='left')
        self.entry_editor.insert(1.0, timestamp + '\n', 'green_rounded_edge_timestamp')
        self.entry_editor.tag_configure('green_rounded_edge', foreground='black', background='#A4FF9A', borderwidth=1, relief='ridge', font=('Arial', 11, 'normal'), justify='left')
        self.entry_editor.insert(1.0, message + '\n', 'green_rounded_edge')
        self.entry_editor.config(state='disabled')

    '''
    import datetime
    import time

    time = datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %I:%M %p")

    print(time)
    '''

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', tk.END).strip()

    def set_text_entry(self):
        self.message_editor.delete(1.0, tk.END)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        # self.message_editor.bind('<Return>', abc())
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, state="disabled")
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)
    
    '''
    def abc():
        print('ENTER')
    '''


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self.body = Body(root)
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        self.save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        self.save_button.config(state=tk.DISABLED)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        self.save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # FIX THIS TO ALLOW THE ENTER BUTTON TO BE PRESSED TO SEND
        # save_button.bind("<Return>", self.send_click)
        # self.body.message_editor.bind("<Return>", lambda event: "break")
        # self.body.message_editor.bind('<Return>', lambda event: (self.send_click, "break"))
        # self.body.message_editor.bind('<Return>', lambda event: save_button.invoke())

        self.footer_label = tk.Label(master=self, text=f"Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

        #self.body.get_text_entry.bind("<Return>", lambda event: self.send_click())


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.new_file_path = None
        self.my_os = platform.system()
        self.message_timer_number = None
        self.contact_timer_number = None
        self.recipient_timer_number = None
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()


    def list_contacts(self):
        self.body.reset_tree()
        if self.new_file_path:
            if self.result is True:
                self.check_new()
            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            # print(profile._messages)
            # friends_lst = Profile.Profile.get_friends(self.profile)
            # print(friends_lst)
            contacts = profile.friends
            for contact in contacts:
                self.body.insert_contact(contact)

        # SUPPOSED TO BE ABLE REFRESH THE CONTACTS LIST, NOT WORKING FIX
        if self.contact_timer_number is not None:
          self.root.after_cancel(self.contact_timer_number)
        # make a new after call
        self.contact_timer_number = self.root.after(2000, self.list_contacts)
    
    # FIX THIS
    '''
    def list_new_contacts(self):
        friends_profile = Profile.Profile()
        friends_profile.load_profile(self.new_file_path)
        dming_friends = dm.DirectMessenger(friends_profile.dsuserver, friends_profile.username, friends_profile.password)
        data = dming_friends.retrieve_new()
        friends_profile.save_profile(self.new_file_path)
        for friend in data:
            new_friend = Profile.Message(friend.message, friend.recipient, friend.timestamp)
            friends_profile
        contacts = friends_profile.friends
    '''

    def list_contact_messages(self):
        self.body.entry_editor.config(state='normal')
        cur_pos = self.body.entry_editor.yview()[0]
        self.body.entry_editor.delete('1.0', tk.END)
        if self.new_file_path:
            if self.result is True:
                self.check_new()
            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            messages = profile._messages
            sent_messages = profile._sent_messages
            all_messages_lst = []
            for entry in messages:
                if self.recipient == entry['author']:
                    all_messages_lst.append(entry)
            for sent in sent_messages:
                if self.recipient == sent['recipient']:
                    all_messages_lst.append(sent)
            sorted_message_lst = sorted(all_messages_lst, key=lambda x: float(x["timestamp"]), reverse=True)
            for dm in sorted_message_lst:
                if "author" in dm:
                    time = datetime.datetime.fromtimestamp(float(dm['timestamp'])).strftime("%d/%m/%Y %I:%M %p")
                    self.body.insert_contact_message(dm['message'], time)
                elif "recipient" in dm:
                    time = datetime.datetime.fromtimestamp(float(dm['timestamp'])).strftime("%d/%m/%Y %I:%M %p")
                    self.body.insert_user_message(dm['message'], time)
        self.body.entry_editor.config(state='disabled')
        # cancel the previous after call, if it exists
        if self.message_timer_number is not None:
            self.root.after_cancel(self.message_timer_number)
        # make a new after call
        self.body.entry_editor.yview(tk.MOVETO, cur_pos)

        self.message_timer_number = self.root.after(250, self.list_contact_messages)

    def send_message(self):
        # You must implement this
        text = self.body.get_text_entry()
        print('Message', text)
        self.body.set_text_entry()
        if (text != "") and (text.isspace() is False):
            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            profile.save_profile(self.new_file_path)
            server = profile.dsuserver
            username = profile.username
            password = profile.password
            dming = dm.DirectMessenger(server, username, password)
            result = dming.send(text, self.recipient)
            if result is True:
                # self.body.insert_user_message(text)
                timestamp = str(time.time())
                store_new_message = Profile.Sent(text, self.recipient, timestamp)
                profile.add_author(self.recipient)
                profile.add_sent_messages(store_new_message)
                profile.save_profile(self.new_file_path)
            else:
                messagebox.showerror("Error", "       Connection Error:\n\nCannot Send Messages")
            

    def add_contact(self):
        if self.new_file_path:
            self.contact_window = tk.Toplevel(self.root)
            self.contact_window.title("Add Contact")
            self.contact_window.resizable(False, False)
            self.contact_window.grab_set()

            # Set color of new window
            # self.contact_window.configure(background="#4285f4")

            # Add Titles, Labels, Entries, and Buttons to the new window
            title = tk.Label(self.contact_window, text="Add Contact", font=("Impact", 16))
            # title.place(relx=0.5, rely=0.0, anchor="center")
            title.grid(row=0, column=1)

            tk.Label(self.contact_window, text="Name", font=("Verdana", 10)).grid(row=2, column=0)
            contact_entry = tk.Entry(self.contact_window)
            contact_entry.grid(row=2, column=1)

            tk.Button(self.contact_window, text="Save", command=self.new_contact_saver).grid(row=10, column=0, columnspan=2)
            tk.Button(self.contact_window, text="Cancel", command=self.cancel_window_2).grid(row=11, column=0, columnspan=2)

            self.new_contact_entry = contact_entry
        else:
            messagebox.showerror("Error", "Load File Before Adding Contacts")

    def new_contact_saver(self):
        new_contact = self.new_contact_entry.get()
        print('TYPE', new_contact)

        profile = Profile.Profile()
        profile.load_profile(self.new_file_path)
        profile.save_profile(self.new_file_path)
        profile.add_author(new_contact)
        profile.save_profile(self.new_file_path)

        self.contact_window.destroy()


    def cancel_window_2(self):
        self.contact_window.destroy()


    def recipient_selected(self, recipient):
        self.body.entry_editor.config(state='normal')
        self.body.entry_editor.delete('1.0', tk.END)
        self.recipient = recipient
        print(self.recipient)
        self.list_contact_messages()
        self.body.entry_editor.config(state='disabled')


    def configure_server(self):
        '''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        '''
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        # Create a new window to prompt for user info
        if self.new_file_path:
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Configure Profile")
            self.edit_window.resizable(False, False)
            self.edit_window.grab_set()

            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            # Set color of new window
            # self.edit_window.configure(background="#4285f4")

            # Add Titles, Labels, Entries, and Buttons to the new window
            title = tk.Label(self.edit_window, text="  Configure Your Profile", font=("Impact", 16))
            # title.place(relx=0.5, rely=0.0, anchor="center")
            title.grid(row=0, column=1, columnspan=1)

            tk.Label(self.edit_window, text="Current", font=("Verdana 13 underline")).grid(row=2, column=1)
            tk.Label(self.edit_window, text="New", font=("Verdana 13 underline")).grid(row=2, column=2)
            tk.Label(self.edit_window, text=" ", font=("Verdana 13")).grid(row=2, column=3)

            tk.Label(self.edit_window, text="IP Address:", font=("Verdana", 10)).grid(row=4, column=0)
            tk.Label(self.edit_window, text=profile.dsuserver, font=("Verdana", 10)).grid(row=4, column=1)
            ip_entry = tk.Entry(self.edit_window)
            ip_entry.grid(row=4, column=2)

            tk.Label(self.edit_window, text="Username:", font=("Verdana", 10)).grid(row=6, column=0)
            tk.Label(self.edit_window, text=profile.username, font=("Verdana", 10)).grid(row=6, column=1)
            self.user_entry = tk.Entry(self.edit_window)
            self.user_entry.grid(row=6, column=2)

            tk.Label(self.edit_window, text="Password:", font=("Verdana", 10)).grid(row=8, column=0)
            tk.Label(self.edit_window, text=profile.password, font=("Verdana", 10)).grid(row=8, column=1)
            self.pass_entry = tk.Entry(self.edit_window, show="*")
            self.pass_entry.grid(row=8, column=2)

            self.pass_entry.configure(state="disabled")
            self.user_entry.bind("<KeyRelease>", self.username_entry_change)
            # self.pass_entry.configure(state="disabled")
            '''
            if (username_entry.get() == "") or (username_entry.get().isspace() is True):
                pass_entry.configure(state="disabled")
            else:
                pass_entry.configure(state="normal")
            '''
            

            tk.Button(self.edit_window, text="Save", command=self.edit_saver, bg="#A6E6EE").grid(row=10, column=0, columnspan=2)
            tk.Button(self.edit_window, text="Cancel", command=self.cancel_window_3, bg="#EC9898").grid(row=10, column=1, columnspan=2)

            # Save the Entry widgets as instance variables so you can access their values later
            self.new_username_entry = self.user_entry
            self.new_password_entry = self.pass_entry
            self.new_ip_entry = ip_entry
        else:
            messagebox.showerror("Error", "Load File Before Configuring")

    '''
    def enable_password_entry(self, event):
        self.pass_entry.configure(state="normal")
    '''

    def username_entry_change(self, event):
        if len(self.user_entry.get().strip()) > 0:
            self.pass_entry.configure(state="normal")
        else:
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.configure(state="disabled")

    def edit_saver(self):
        edited_username = self.new_username_entry.get()
        edited_password = self.new_password_entry.get()
        edited_ip = self.new_ip_entry.get()
        error = False
        error_code = ""

        print('IP Address:', edited_ip)
        print('Username:', edited_username)
        print('Password', edited_password)


        edited_profile = Profile.Profile()
        edited_profile.load_profile(self.new_file_path)
        edited_profile.save_profile(self.new_file_path)
        if (edited_ip.isspace() is False) and (edited_ip != "") and (" " not in edited_ip):
            print('Saved IP Address:', edited_ip)
            edited_profile.dsuserver = edited_ip
            self.result = True
        elif (edited_ip.isspace() is True) or (" " in edited_ip):
            error = True
            error_code += "IP Address Includes Spaces\n"
        if (edited_username.isspace() is False) and (edited_username != "") and (" " not in edited_username):
            print('Saved Username:', edited_username)
            edited_profile.username = edited_username
        elif (edited_username.isspace() is True) or (" " in edited_username):
            error = True
            error_code += "Username Includes Spaces\n"
        if (edited_password.isspace() is False) and (edited_password != "") and (" " not in edited_password):
            print('Saved Password', edited_password)
            edited_profile.password = edited_password
        elif (edited_password.isspace() is True) or (" " in edited_password):
            error = True
            error_code += "Password Includes Spaces\n"
        
        if error is True:
            messagebox.showerror("Error", error_code)
        else:
            edited_profile.save_profile(self.new_file_path)
            self.edit_window.destroy()

        


    def cancel_window_3(self):
        self.edit_window.destroy()


    def publish(self, message:str):
        # You must implement this!
        pass

    
    def check_new(self):
        self.result = True
        if self.new_file_path:
            check_profile = Profile.Profile()
            check_profile.load_profile(self.new_file_path)
            dming = dm.DirectMessenger(check_profile.dsuserver, check_profile.username, check_profile.password)
            data = dming.retrieve_new()
            if data is not False:
                self.result = True
                check_profile.save_profile(self.new_file_path)
                for entry in data:
                    new_message = Profile.Message(entry.message, entry.recipient, entry.timestamp)
                    check_profile.add_author(entry.recipient)
                    check_profile.add_message(new_message)
                check_profile.save_profile(self.new_file_path)
            elif data is False:
                self.result = False
                # Fix later to give a more precise error, like ip address or connection, and more
                messagebox.showerror("Error", "       Connection Error:\n\nCannot Load New messages")


    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file_creator)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close_gui)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


    def close_gui(self):
        main.destroy()

    def check_recipient_selected(self):
        if self.recipient:
            self.footer.save_button.config(state=tk.NORMAL)
        elif self.recipient is None:
            self.footer.save_button.config(state=tk.DISABLED)

        if self.recipient_timer_number is not None:
          self.root.after_cancel(self.recipient_timer_number)
        # make a new after call
        self.recipient_timer_number = self.root.after(100, self.check_recipient_selected)


    def open_file(self):
        file_path = filedialog.askopenfilename(parent=self.root)
        if file_path:
            try:
                # Do something with the file
                self.new_file_path = file_path
                self.list_contacts()
            except Profile.DsuFileError:
                self.new_file_path = None
                messagebox.showerror("Error", "Not a .dsu File")

            if (self.new_file_path):
                self.recipient = None
                self.check_recipient_selected()


    def new_file_creator(self):
        # Open a dialog box to get the filename and location
        file_path = filedialog.asksaveasfilename(defaultextension=".dsu", filetypes=[('DSU files', '.dsu')])
        # Check if a filename was entered
        if file_path:
            # Saves the file path as a variable for Profile.py to use
            self.new_file_path = file_path
            print(self.new_file_path)
            '''
            # Open the new file in the default text editor
            if self.my_os == 'Windows':
                os.startfile(file_path)
            else:
                subprocess.call(('open', file_path))
            '''
            # Calls the function to open a new window to save profile info
            self.biometrics_window()


    def biometrics_window(self):
        # Create a new window to prompt for user info
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Create Profile")
        self.profile_window.resizable(False, False)
        self.profile_window.grab_set()

        # Set color of new window
        # self.profile_window.configure(background="#4285f4")

        # Add Titles, Labels, Entries, and Buttons to the new window
        title = tk.Label(self.profile_window, text="Create Your Profile", font=("Impact", 16))
        #title.place(relx=0.5, rely=0.0, anchor="center")
        title.grid(row=0, column=1)

        tk.Label(self.profile_window, text="Username", font=("Verdana", 10)).grid(row=2, column=0)
        username_entry = tk.Entry(self.profile_window)
        username_entry.grid(row=2, column=1)

        tk.Label(self.profile_window, text="Password", font=("Verdana", 10)).grid(row=4, column=0)
        password_entry = tk.Entry(self.profile_window, show="*")
        password_entry.grid(row=4, column=1)

        tk.Label(self.profile_window, text="Bio", font=("Verdana", 10)).grid(row=6, column=0)
        bio_entry = tk.Entry(self.profile_window)
        bio_entry.grid(row=6, column=1)

        tk.Label(self.profile_window, text="IP Address", font=("Verdana", 10)).grid(row=8, column=0)
        ip_entry = tk.Entry(self.profile_window)
        ip_entry.grid(row=8, column=1)

        tk.Button(self.profile_window, text="Save", command=self.biomentrics_saver).grid(row=10, column=0, columnspan=2)
        tk.Button(self.profile_window, text="Cancel", command=self.cancel_window).grid(row=11, column=0, columnspan=2)

        # Save the Entry widgets as instance variables so you can access their values later
        self.new_username_entry = username_entry
        self.new_password_entry = password_entry
        self.new_bio_entry = bio_entry
        self.new_ip_entry = ip_entry


    def biomentrics_saver(self):
        # Create the new file
        open(self.new_file_path, 'a').close()

        # Get the values from the Entry widgets
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_bio = self.new_bio_entry.get()
        new_ip_address = self.new_ip_entry.get()

        profile = Profile.Profile()
        profile.save_profile(self.new_file_path)
        profile.username = new_username
        profile.password = new_password
        profile.bio = new_bio
        profile.dsuserver = new_ip_address
        profile.save_profile(self.new_file_path)

        # Close the user info window
        self.profile_window.destroy()
        self.list_contacts()
    
    def cancel_window(self):
        self.profile_window.destroy()


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = ThemedTk(theme="adapta")

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("The Ultimate Messaging App (Better than Discord)")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
