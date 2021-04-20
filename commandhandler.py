"""
This program handles the commands
passed by the client to server.
"""


import os
import time
import pandas


class CommandHandler:
    """

    Handles all the commands received from the client.
    Acts as helper program to the server.

    Attributes
    ----------
    self.user_id :
        Username of registered user
    self.is_login :
        Login Status of the user
    self.registered_users :
        Container which stores usernames of registered users
    self.logged_in_users : list
        Container which stores usernames of logged in users

    Returns
    -------
    Object
        CommandHandler Object
    """

    ROOT_DIR = "Root/"
    REGISTERED_USERS_CSV_FILE = "AccessSession/registered_users.csv"
    LOGGED_IN_USERS_CSV_FILE = "AccessSession/logged_in_users.csv"
    CSV_HEADING = "username,password\n"

    def __init__(self):
        """
        Parameters
        ----------
        self.user_id : str
            Username of registered user
        self.is_login : bool
            Login status of the user
        self.registered_users : list
            Container which stores usernames of registered users
        self.logged_in_users : list
            Container which stores usernames of logged in users
        self.current_dir : str
            Current Directory Path of the user, by default this is set
            to Root/
        self.char_count : int
            Number of characters should be read each time read_file()
            method is invoked.
        """
        self.user_id = ""
        self.is_login = None
        self.registered_users = None
        self.logged_in_users = None
        self.current_dir = CommandHandler.ROOT_DIR
        self.read_index = {}
        self.char_count = 100

    def commands(self):    
        """
        Returns
        -------
        commands : str
            Returns a description of commands that 
            can be exercised by the user while using this 
            system.
        """

        commands = ["""register : To register as a new user,
                    command:register <username> <password> \n""",
                    """login : To login,
                    command:login <username> <password>""",
                    """quit : To logout,
                    command:quit\n""",
                    """change_folder : To change the current path,
                    command:change_folder <name>\n""",
                    """list : Lists all files in the current path,
                    command:list\n""",
                    """read_file : To read content from the file,
                    command:read_file <name>\n""",
                    """write_file : To write content into the file,
                    command:write_file <name> <content>\n""",
                    """create_folder : To create new folder,
                    command:create_folder <name>\n"""
                ]

        return "".join(commands)

    def access_user_info(self):
        """
        Helper method
        """
        if not os.path.exists("AccessSession"):
            os.mkdir("AccessSession")

        if not os.path.isfile(CommandHandler.REGISTERED_USERS_CSV_FILE):
            with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        if not os.path.isfile(CommandHandler.LOGGED_IN_USERS_CSV_FILE):
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        self.logged_in_users = pandas.read_csv(CommandHandler.LOGGED_IN_USERS_CSV_FILE)
        self.registered_users = pandas.read_csv(CommandHandler.REGISTERED_USERS_CSV_FILE)


    def register(self, user_id, password):
        """
        Registers a new user. The password length specified by the 
        user should be more than 8. 

        Parameters
        ----------
        user_id : str
            Username of the client
        password : str
            Password set by the client

        Returns
        -------
        str
            Success! Registered <username>
        """
        self.access_user_info()
        if user_id in self.registered_users['username'].tolist():
            return "\nUsername not available"
        if len(password) < 8:
            return "\n Password length should be more than 8 characters."
        with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id+","+password+"\n")
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)
        os.mkdir(os.path.join(self.current_dir, user_id))
        self.user_id = user_id
        return "\nSuccess! Registered " + self.user_id

    def login(self, user_id, password):
        """
        Allow the user to login to the system

        Parameters
        ----------
        user_id : str
            Username of the logged in user
        password : str
            Password of the logged in user

        Returns
        -------
        str     
            Success <username> Logged into the system
            
        """

        self.access_user_info()
        if self.is_login:
            return "\nAlready logged in"
        if user_id not in self.registered_users['username'].tolist():
           # print (self.registered_users)
            return "\nYou haven't registered! command: register <username> <password>"
        if password not in self.registered_users['password'].tolist() and user_id in self.registered_users['username'].tolist():
            return "\nSorry, The password you entered is wrong. Please Try Again"
        if user_id in self.logged_in_users['username'].tolist():
            self.is_login = True
            self.user_id = user_id
            self.current_dir = self.current_dir + self.user_id
            return "\nYou logged through another system"
        
        self.is_login = True
        self.user_id = user_id
        self.current_dir = self.current_dir + self.user_id
        with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id + "," + password + "\n")
        return "Success " + self.user_id + " Logged into the system"

    def quit(self):
        """
        Quits the client program. 

        Returns
        -------
        str
            Logged Out     
        """
        
        try:
            self.access_user_info()
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as file:
                file.write(CommandHandler.CSV_HEADING)
                user_ids = self.logged_in_users['username'].tolist()
                passwords = self.logged_in_users['password'].tolist()
                for index, user_id in enumerate(user_ids):
                    if self.user_id != str(user_id):
                        file.write(user_id +","+passwords[index])
            self.is_login = False
            self.user_id = ""
            return "\nLogged Out"
        except KeyError:
            return "\nForced Logged Out through Keyboard Interruption (CTRL-C)"

    def create_folder(self, folder):
        """
        Creates a new folder as specified by the 
        logged in user. If specified folder already exists throws an error.

        Parameters
        ----------
        folder : str
            Folder Name

        Returns
        -------
        str
            Successfully created folder <folder-name>
        """

        if not self.is_login:
            return "\nLogin to continue"
        self.access_user_info()
        path = os.path.join(self.current_dir)
        try:
            os.mkdir(os.path.join(path, folder))
        except FileExistsError:
            return "\nThe folder already exists!"
        return "\nSuccessfully created folder " + folder

    def change_folder(self, folder):
        """
        Change the current path to the path specified by the logged in 
        user. If the specified path does not exist, throws an error.

        Parameters
        ----------
        folder : str
            Folder name

        Returns
        -------
        str
            Successfully moved to folder <current-folder>
        """

        if not self.is_login:
            return "\nLogin to continue"

        self.access_user_info()
        if folder == ".." and self.current_dir != CommandHandler.ROOT_DIR + self.user_id:
            self.current_dir = os.path.dirname(os.path.join(self.current_dir))
            return "\nSuccessfully moved to folder " + self.current_dir
        
        elif folder == ".." and self.current_dir == CommandHandler.ROOT_DIR + self.user_id:
            return "\nCannot Move Back from Root/" + self.user_id + " folder"

        if folder in os.listdir(self.current_dir):
            self.current_dir = os.path.join(self.current_dir, folder)
            return "\nSuccessfully Moved to folder " + self.current_dir
        return "\n No such folder exists"

    
    def write_file(self, filename, data):
        """
        Creates a new file and write content to the created file by the logged in user. 
        If the file already exists the content will be appended to the already existing file.

        Parameters
        ----------
        filename : str
            Name of the name to which content to be written
        data : str
            Content to be written to a file

        Returns
        -------
        str
            Created and Written data to file <filename> successfully
        """

        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue"
        t_file = []
        for file in os.listdir(os.path.join(self.current_dir)):
            if os.path.isfile(os.path.join(self.current_dir, file)):
                t_file.append(file)
            
        writeable_data = ""
        path = os.path.join(self.current_dir, filename)
        for i in data:
            writeable_data += i
        if filename in t_file:
            with open(path, "a+") as file:
                file.write(writeable_data)
            return "\nSuccess Written data to file " + filename + " successfully"
        with open(path, "w+") as file:
            file.write(writeable_data)
        return "\nCreated and written data to file " + filename + " successfully"

    def read_file(self, filename):
        """
        Read the content from the file specified by the logged in user.
        If the file path does not exist, it throws an error message 
        stating No Such file <filename> exists

        Parameters
        ----------
        filename : str
            Name of the file to be read

        Returns
        -------
        str
            Read file from <old_index> to <current_index> are <content>
        """
        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue"
        try:
            t_path = os.path.join(self.current_dir, filename)
            if t_path not in list(self.read_index.keys()):
                self.read_index[t_path] = 0
            with open(t_path, "r") as file:
                content = file.read()
            old_index = str(self.read_index[t_path]*self.char_count)
            index = self.read_index[t_path]
            data = content[index*self.char_count:(index+1)*self.char_count]
            self.read_index[t_path] += 1
            self.read_index[t_path] %= len(content) // self.char_count + 1
            return "\n" + "Reading file from " + old_index + " bytes to " + str(int(old_index)+self.char_count) + " bytes\n"+ data
        except FileNotFoundError:
            "\nNo Such file " + filename + "exists!"
        
        
    def list(self):
        """
        Lists out all the files and
        folders in the user's current file path.

        Returns
        -------
        str
            File   | Size           | Modified Date
            <file> | <size_of_file> | <time_file_modified>
        """

        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue!"
        path = os.path.join(self.current_dir)
        folders = []
        try:
            for file_name in os.listdir(path):
               file_stats = os.stat(os.path.join(path, file_name))
               folders.append([file_name, str(file_stats.st_size), str(time.ctime(file_stats.st_ctime))])
        except NotADirectoryError:
            return "\nNot A Directory"
        details = "\nFile | Size | Modified Date"
        for folder in folders:
            line = " | ".join([folder[0], folder[1], folder[2]]) + "\n"
            details += "-----------------------\n" + line
        return details
