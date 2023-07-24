'''This programme codes for a task manager'''

# importing the 'os' library
import os

#importing libraries so the date can be stored in a standard format (YYYY/MM/DD)
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#===========================================================tasks.txt===========================================================#
# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Open the tasks.txt file
# Store each line in the Text File in a list as separate items unless they are empty
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Create an empty list called task_list
task_list = []

# Create an empty dictionary
for t_str in task_data: 
    curr_t = {}

    # Split by semicolon each item in the task_list, forming nested lists
    task_components = t_str.split(";")

    # Adds to the empty dictionary new items,
    # # where the keys are pre-defined and the values of the keys are the items in the nested list
    # the items in the nested lists are called by their indexes
    curr_t['task_username'] = task_components[0]
    curr_t['task_title'] = task_components[1]
    curr_t['task_description'] = task_components[2]
    curr_t['curr_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['due_date_time'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['task_completed'] = task_components[5]

#The newly created dictionary curr_t is stored inside the list tasks_list as an item
    task_list.append(curr_t)

task_file.close()

#=========================================================================reg_user=====================================================================#
'''registers new users'''

#Add a new user to the user.txt file
def reg_user():

    # Request input of a new username
    new_username = input("New Username: ")   

    # While the username already exists in the user.txt file the user will be propmpted to insert a new username
    while True:
        if new_username in username_password.keys(): 
            new_username = input('This username already exists. Please enter a new username: ')
        if new_username not in username_password.keys():
            break

    # Request input of a new password and input of password confirmation
    new_password = input("New Password: ")   
    confirm_password = input("Confirm Password: ") 


    # If the new and the confirmed passwords are not the same then the user is asked to input the password again 
    while True:
        if new_password[:] != confirm_password[:]:
            print("Passwords do not match, please make sure the passwords match: ")
            new_password = input("New Password: ")   
            confirm_password = input("Confirm Password: ")  
            
        if new_password[:] == confirm_password[:]:
            break
            
        
    # Check if the new password and confirmed password are the same
    # If they are the same, the function: 
    # - adds the new username and the new password to the username_password dictionary and
    # - adds them to the user.txt file separated by a semicolon
    if new_password[:] == confirm_password[:]:  
        username_password[new_username] = new_password
        print("New user added!")
        
        # Open an empty list called user data where the username and password are stored separate by a semicolon
        # The item is written in the user.txt file on a newline
        with open("user.txt", "w") as out_file:   
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    out_file.close()

#============================================================add_task=============================================================================#

#Allow a user to add a new task to task.txt file
#Prompt a user for the following: 
#   - a username of the person whom the task is assigned to,
#   - a title of a task,
#   - a description of the task and 
#   - the due date of the task

def add_task(): 
    task_username = input("Username of the person whom the task is assigned to: ")
    
    # If the username does not exist in user.txt then the user will be prompted to enter an already existing username
    while True:
        if task_username not in username_password.keys():
            print("User does not exist.")
            task_username = input("Please enter a valid username: ")
        if task_username in list(username_password.keys()):
            break

    task_title = input("Title of task: ")
    task_description = input("Description of task: ")

    # If the date is not in the correct format the user will be prompted to input a date in the correct format 
    while True: 
        try: 
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()

    # creating a dictionary for the new task    
    new_task = {"Username": task_username, "Title": task_title, "Description": task_description, "Due_date": due_date_time, 
    "Assigned_date": curr_date, "Completed": 'No'}
    
    # adding the new task to the task_list
    task_list.append(new_task)

    # adding the new task on the tasks.txt file 
    with open("tasks.txt", "a") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [t['task_username'], t['task_title'], t['task_description'], t['curr_date'].strftime(DATETIME_STRING_FORMAT), 
                         t['due_date_time'].strftime(DATETIME_STRING_FORMAT), t['task_completed']] 

        #joining the inputs via semicolons
        task_list_to_write.append(";".join(str_attrs)) 
        task_file.write("\n".join(task_list_to_write))

    task_file.close()

    print("Task successfully added.")
    
#==========================================================view_all============================================================================#

def view_all():
    # Reads the task from task.txt file and prints to the console.
    
    for index, t in enumerate(task_list): 
        disp_str = f"Task number: \t\t {index+1} \n"
        disp_str += f"Assigned to: \t {t['task_username']}\n"
        disp_str += f"Task: \t\t {t['task_title']}\n"
        disp_str += f"Task Description:{t['task_description']}\n"
        disp_str += f"Due Date: \t {t['due_date_time'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Date Assigned: \t {t['curr_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Completed:\t\t{t['task_completed']}\n\n"
        print(disp_str)

#============================================================Login Section======================================================================#
'''This part of code reads username and password from the user.txt file to allow a user to login'''

# If no user.txt file exists, one is created
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Each item in the user.txt file is turned into a list
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# An empty dictionary username_password is created
# The username and password that are stored in the user.txt file as username;password are split 
# and are respectively stored in the dictionary username_password as key and value
username_password = {}
for user in user_data:
    username, password = user.split(';')[0], user.split(';')[1]
    username_password[username] = password

# The defoault state is the user not logged in. 
# The user is asked to input a username. 
# If the username is not a key in the dictionary username_password (which means it does not exists)
# then the user is prompted to input a new username and a new password through the function reg_user()
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    if curr_user not in list(username_password.keys()):
       print("User does not exist")
       print(reg_user())

# If the username is a key in the dictionary username_password 
# then the user is prompted to input the password that corrsponds to that specific username
# If the password does not match the corrsponding password to the username 
# then the user will have three chances to input the correct password before the programme breaks
    else:
        curr_pass = input("Password: ")

    i = 1
    for i in range(4):
        if username_password[curr_user] != curr_pass:
            curr_pass = input("Wrong password, please enter the correct password: ")
            i +=1
        if username_password[curr_user] == curr_pass:
            print("Login Successful!")
            logged_in = True
            break

#================================================================generate_report====================================================================#

'''This function creates a file called task_overview.txt with some statistics about all the tasks 
and a file called user_overview.txt with some statistics about only the user's tasks. '''

def generate_report(): 
    num_tasks = len(task_list)
    num_users = len(list(username_password.keys()))

    # generating report for the tasks 
    count = 0
    i_count = 0
    overdue_and_incompleted_tasks = 0

    for index, t in enumerate(task_list): 
        if t['task_completed'] == 'Yes': 
            count += 1
        if t['task_completed'] == 'No' and date.today()>t['due_date_time'].date():
            overdue_and_incompleted_tasks += 1            
        if t['task_completed'] == 'No':
            i_count += 1       

    with open('tasks_overview.txt', 'w') as o: 
        o.write(f"Total number of tasks: {num_tasks}\n") 
        o.write(f"Number of completed tasks: {count}\n")
        o.write(f"Number of incompleted tasks: {i_count}\n")
        o.write(f"Number of overdue tasks: {overdue_and_incompleted_tasks}\n")
        o.write(f"Percentage of incompleted tasks: {round(100*(i_count/num_tasks), 2)}\n")
        o.write(f"Percentage of overdue tasks: {round(100*(overdue_and_incompleted_tasks/num_tasks), 2)}\n")

    o.close()

    # generating report for the users
    task_counting = 0
    completed_tasks = 0
    overd_incomp_tasks = 0

    for index, k in enumerate(task_list): 
        if k['task_username'] == curr_user: 
            task_counting += 1
        if k['task_username'] == curr_user and k['task_completed']=='Yes':
            completed_tasks += 1
        if k['task_username'] == curr_user and k['task_completed']=='No' and date.today() > k['due_date_time'].date():
            overd_incomp_tasks += 1

    with open('users_overview.txt', 'w') as u: 
        u.write(f"Number of users: {num_users}\n")
        u.write(f"Total number of tasks: {num_tasks}\n")
        u.write(f"Your total number of tasks: {task_counting}\n")
        u.write(f"Percentage of tasks assigned to you: {round(100*(task_counting/num_tasks), 2)}\n")
        u.write(f"Percentage of tasks assigned to you that have been completed: {round(100*(completed_tasks/num_tasks), 2)}\n")
        u.write(f"Percentage of tasks assigned to you that have not been completed: {round(100*((num_tasks - completed_tasks)/num_tasks), 2)}\n")
        u.write(f"The percentage of the tasks assigned to you that have not yet been completed and are overdue: {round(100*(overd_incomp_tasks/task_counting), 2)}\n")
        
        u.close()
    
    print('''A report has been generated about the users on a text file called users_overview
           and about the tasks on a text file called tasks_overview.''')

#==================================================================display_statistics===========================================================================#
'''If the user is an admin they can display statistics about number of users and tasks.'''

#The info from task_overview.txt and user_overview.txt is output on the screen 
def display_statistics(): 
    print(generate_report())  

    with open('task_overview.txt', 'r') as o: 
        o_file = o.read()
        print(o_file)
    o.close()

    with open('user_overview.txt', 'r') as u: 
        u_file = u.read()
        print(u_file)
    u.close()

#===========================================================view_mine==========================================================================#

# Displays the tasks of the user where a number is assigned to each task (its order in the tasks.txt file)

def view_mine():
    for index, t in enumerate(task_list):
        if t['task_username'] == curr_user:
            disp_str = f"Task number: \t {index+1} \n"
            disp_str += f"Assigned to: \t {t['task_username']}\n"                
            disp_str += f"Task: \t\t {t['task_title']}\n" 
            disp_str += f"Task Description: {t['task_description']}\n"
            disp_str += f"Date Assigned: \t {t['curr_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date_time'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: \t {t['task_completed']}\n"
            print(disp_str)
            
    #The user is prompted to choose a task by its number or to return to the menu by entering -1           
    num = int(input('Enter a task number to view a specific task or enter -1 to go to the menu: '))

    if num == -1: 
        menu = input('''
Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit

Enter: ''').lower()
        if menu == 'r': 
            print(reg_user())

        elif menu == 'a': 
            print(add_task())

        elif menu == 'va': 
            print(view_all())

        elif menu == "vm":
            print(view_mine())

        elif menu == 'gr': 
            print(generate_report())

        elif menu == 'ds' and curr_user == 'admin': 
            print(display_statistics())

        elif menu == 'e':
            print('Bye!!!')
            exit()

        else:
            print("You have made a wrong choice, please try again")


    for index, t in enumerate(task_list):
        if index+1 == num:

            # displaying the task specified by the number 
            disp_str1 = ''
            disp_str1 += f"Task number: \t {index+1} \n"
            disp_str1 += f"Assigned to: \t {t['task_username']}\n"                
            disp_str1 += f"Task: \t\t {t['task_title']}\n" 
            disp_str1 += f"Task Description: {t['task_description']}\n"
            disp_str1 += f"Date Assigned: \t {t['curr_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str1 += f"Due Date: \t {t['due_date_time'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str1 += f"Completed: \t {t['task_completed']}"            
            print(disp_str1)
                       
            # if the task is complete the user can either change the task username or the due date
            if t['task_completed'] == 'Yes':
                Q3 = (input('Do you want to change the username of the person the task is assigned? (Yes/No) ')).lower()
                if Q3 == 'yes': 
                    t['task_username'] = input('New username: ')

                    while True:
                        if task_username not in username_password.keys():
                            print("User does not exist.")
                            task_username = input("Please enter a valid username: ")
                        if task_username in list(username_password.keys()):
                            break

                Q4 = (input('Do you want to change the due date? (Yes/No) ')).lower()
                if Q4 == 'yes':
                    new_due_date = input("Due date of task (YYYY-MM-DD): ")
                    new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    t['due_date_time'] = new_due_date

                if Q3 == 'yes' or Q4 == 'yes':
                    with open("tasks.txt", "a") as task_file:
                        task_list_to_write = []
                        str_attrs = [t['task_username'], t['task_title'], t['task_description'], t['curr_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['due_date_time'].strftime(DATETIME_STRING_FORMAT), t['task_completed']]       
                        task_list_to_write.append('\n' + ";".join(str_attrs) + f';task edited on {date.today()}') #joins the inputs via semicolons
                        task_file.write("\n".join(task_list_to_write))
                    task_file.close()
                    print('Your task has been successfully edited! ')

            #The user can decide to assign a task as completed if it is not complete yet
            #If the task has not been completed then the user can change the due data, the task username, task title and description                
            if t['task_completed'] == 'No':    
                Q1 = (input('Do you want to mark the task as complete? (Yes/No)')).lower()
                if Q1 == 'yes':
                    t['task_completed'] = 'Yes'
                if Q1 == 'no':
                    Q2 = input('Do you want to edit the task? (Yes/No)') 
                    if Q2 == 'yes': 
                        Q3 = input('Do you want to edit the title of the task? (Yes/No)').lower()
                        if Q3 == 'yes':
                            t['task_title'] = input('New task title: ')
                        Q4 = input('Do you want to edit the task description? (Yes/No)').lower()
                        if Q4 == 'yes':
                            t['task_description'] = input('New task description: ')

                    Q3 = (input('Do you want to change the username of the person the task is assigned? (Yes/No) ')).lower()
                    if Q3 == 'yes': 
                        t['task_username'] = input('New username: ')
                    Q4 = (input('Do you want to change the due date? (Yes/No) ')).lower()
                    if Q4 == 'yes':
                        new_due_date = input("Due date of task (YYYY-MM-DD): ")
                        new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        t['due_date_time'] = new_due_date

                with open("tasks.txt", "a") as task_file:
                    task_list_to_write = []
                    str_attrs = [t['task_username'], t['task_title'], t['task_description'],t['curr_date'].strftime(DATETIME_STRING_FORMAT),  
                                t['due_date_time'].strftime(DATETIME_STRING_FORMAT), t['task_completed']]       
                    task_list_to_write.append('\n' + ";".join(str_attrs) + f';task edited on {date.today()}') #joins the inputs via semicolons
                    task_file.write("\n".join(task_list_to_write))
                task_file.close()
                print('Your task has been successfully edited! ')

#*****************************************************************************************************************************************************************#
# presenting the menu to the user and making sure that the user input is converted to lower case

menu = input('''
Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit

Enter: ''').lower()

if menu == 'r': 
    print(reg_user())

elif menu == 'a': 
    print(add_task())

elif menu == 'va': 
    print(view_all())

elif menu == "vm":
    print(view_mine())

elif menu == 'gr': 
    print(generate_report())

elif menu == 'ds' and curr_user == 'admin': 
    print(display_statistics())

elif menu == 'e':
    print('Bye!!!')
    exit()

else:
    print("You have made a wrong choice, please try again")