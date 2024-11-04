import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar

class Task:  # Represent a task
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed   

    def __str__(self):  # return string representation of the task
        status = "✓ Completed" if self.completed else "✗ Incomplete"  # Fixed from self.complete to self.completed
        return f"{status} {self.title}"    

class TaskManager:  # manage list of task
    def __init__(self, filename='task.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()  # loads tasks from specified json file.

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)  # if file exists it reads the file and creates task objects from data.
                self.tasks = [Task(**task) for task in tasks_data]  # task_data dictionary unpacking method

    def add_task(self, title):
        task = Task(title)  # creates new task object and append to the tasks list
        self.tasks.append(task)

    def edit_task(self, index, new_title):
        # edit the title of a particular task on the basis of index
        if 0 <= index < len(self.tasks):
            self.tasks[index].title = new_title

    def delete_task(self, index):  # removes a task from the list on the basis of index value
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def mark_task_complete(self, index):  # mark a particular task as complete based on index value
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True      

    def save_tasks(self):  # saves current task list to a json file. converts each task to a dictionary 
        with open(self.filename, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f)  # Save tasks to JSON file

class TaskManagerApp:
    # manage user interface
    def __init__(self, root):  # constructor for TaskManagerApp initializes the application with a given root window.
        self.root = root
        self.root.title("Task Manager")     
        self.task_manager = TaskManager()  # initialize a task manager to manage tasks

        self.task_listbox = Listbox(root, selectmode=tk.SINGLE, width=50, height=15)  # create a listbox for displaying tasks
        self.task_listbox.pack(pady=10)

        self.scrollbar = Scrollbar(root)  # create a vertical scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # pack the scrollbar to the right of window
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)  # links scrollbar to the listbox for scrolling
        self.scrollbar.config(command=self.task_listbox.yview)  # configure the scrollbar to control the vertical view of listbox

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Complete", command=self.mark_complete)  # Changed button text for clarity
        self.complete_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(pady=5)

        self.update_task_listbox()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

    def update_task_listbox(self):  # update contents of task list box in GUI
        self.task_listbox.delete(0, tk.END)  # remove all items from the list box
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, str(task))  # convert the task into string representation and insert at task_listbox

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title")  # opens a dialog box prompting the user to enter the title for a new task 
        if title:
            self.task_manager.add_task(title)
            self.update_task_listbox()      

    def edit_task(self):
        selected_index = self.task_listbox.curselection()  # retrieves the index of currently selected task in the list box. returns a tuple of selected indexes

        if selected_index:
            index = selected_index[0]  # if task is selected it retrieves 1st index from tuple
            new_title = simpledialog.askstring("Edit Task", "Enter new task title")
            if new_title:
                self.task_manager.edit_task(index, new_title)
                self.update_task_listbox()
        else:
            messagebox.showwarning("Edit Task", "Please select a task to edit.")  # display a warning message informing the user that they need to select a task to edit

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.task_manager.delete_task(index)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Delete Task", "Please select a task to be deleted.")

    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.task_manager.mark_task_complete(index)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Mark Complete", "Please select a task to mark as complete.")            

    def save_tasks(self):
        self.task_manager.save_tasks()
        messagebox.showinfo("Save Tasks", "Tasks saved successfully")

    def load_tasks(self):
        self.task_manager.load_tasks()
        self.update_task_listbox()
        messagebox.showinfo("Load Tasks", "Tasks loaded successfully")

    def on_closing(self):  # Handle the window close event
        self.save_tasks()  # Save tasks before closing
        self.root.destroy()  # Close the application

if __name__ == "__main__":  # check if script is run directly
    root = tk.Tk()  # creates a new tkinter root window
    app = TaskManagerApp(root)
    root.mainloop()  # starts tkinter event loop, making it user responsive