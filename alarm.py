import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import winsound
from threading import Thread

class Alarm:
    def __init__(self, hour, minute, days):
        self.hour = hour
        self.minute = minute
        self.days = days
        self.is_active = True
        self.thread = None

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Alarm Clock")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.alarms = []  # List to store all alarms
        self.days_vars = []  # Checkbutton variables for days
        self.days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Create GUI elements
        self.create_widgets()
        
        # Update current time
        self.update_time()

    def create_widgets(self):
        # Current time display
        self.time_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 24),
            bg="#f0f0f0"
        )
        self.time_label.pack(pady=10)
        
        # Frame for alarm settings
        settings_frame = tk.Frame(self.root, bg="#f0f0f0")
        settings_frame.pack(pady=10)
        
        # Hour input
        tk.Label(
            settings_frame,
            text="Hour (00-23):",
            bg="#f0f0f0"
        ).grid(row=0, column=0, padx=5)
        
        hour_entry = tk.Entry(
            settings_frame,
            textvariable=self.hour,
            width=5
        )
        hour_entry.grid(row=0, column=1, padx=5)
        
        # Minute input
        tk.Label(
            settings_frame,
            text="Minute (00-59):",
            bg="#f0f0f0"
        ).grid(row=0, column=2, padx=5)
        
        minute_entry = tk.Entry(
            settings_frame,
            textvariable=self.minute,
            width=5
        )
        minute_entry.grid(row=0, column=3, padx=5)

        # Days selection frame
        days_frame = tk.Frame(self.root, bg="#f0f0f0")
        days_frame.pack(pady=5)
        
        # Create checkbuttons for each day
        for i, day in enumerate(self.days):
            var = tk.BooleanVar()
            self.days_vars.append(var)
            tk.Checkbutton(
                days_frame,
                text=day,
                variable=var,
                bg="#f0f0f0"
            ).grid(row=0, column=i, padx=3)
        
        # Set alarm button
        set_button = tk.Button(
            self.root,
            text="Set New Alarm",
            command=self.set_alarm,
            bg="#4CAF50",
            fg="white",
            width=15
        )
        set_button.pack(pady=10)

        # Frame for alarm list
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Scrollable treeview for alarms
        self.alarm_tree = ttk.Treeview(
            list_frame,
            columns=("Time", "Days", "Status"),
            show="headings"
        )
        
        # Configure treeview columns
        self.alarm_tree.heading("Time", text="Time")
        self.alarm_tree.heading("Days", text="Days")
        self.alarm_tree.heading("Status", text="Status")
        
        self.alarm_tree.column("Time", width=100)
        self.alarm_tree.column("Days", width=200)
        self.alarm_tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.alarm_tree.yview
        )
        self.alarm_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.alarm_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame for list actions
        actions_frame = tk.Frame(self.root, bg="#f0f0f0")
        actions_frame.pack(pady=10)

        # Toggle alarm button
        toggle_button = tk.Button(
            actions_frame,
            text="Toggle Alarm",
            command=self.toggle_alarm,
            bg="#FFA500",
            fg="white",
            width=15
        )
        toggle_button.pack(side=tk.LEFT, padx=5)

        # Delete alarm button
        delete_button = tk.Button(
            actions_frame,
            text="Delete Alarm",
            command=self.delete_alarm,
            bg="#f44336",
            fg="white",
            width=15
        )
        delete_button.pack(side=tk.LEFT, padx=5)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def validate_time(self, hour, minute):
        try:
            hour = int(hour)
            minute = int(minute)
            return (0 <= hour <= 23) and (0 <= minute <= 59)
        except ValueError:
            return False

    def get_selected_days(self):
        return [day for day, var in zip(self.days, self.days_vars) if var.get()]

    def set_alarm(self):
        if not self.validate_time(self.hour.get(), self.minute.get()):
            messagebox.showerror("Error", "Please enter valid time!")
            return
        
        selected_days = self.get_selected_days()
        if not selected_days:
            messagebox.showerror("Error", "Please select at least one day!")
            return

        # Create new alarm
        alarm = Alarm(
            int(self.hour.get()),
            int(self.minute.get()),
            selected_days
        )
        self.alarms.append(alarm)
        
        # Start alarm thread
        alarm.thread = Thread(target=self.start_alarm, args=(alarm,))
        alarm.thread.daemon = True
        alarm.thread.start()

        # Add to treeview
        self.update_alarm_list()
        messagebox.showinfo("Success", "Alarm has been set!")

    def update_alarm_list(self):
        # Clear current items
        for item in self.alarm_tree.get_children():
            self.alarm_tree.delete(item)
        
        # Add all alarms
        for alarm in self.alarms:
            time_str = f"{alarm.hour:02d}:{alarm.minute:02d}"
            days_str = ", ".join(alarm.days)
            status = "Active" if alarm.is_active else "Inactive"
            self.alarm_tree.insert("", tk.END, values=(time_str, days_str, status))

    def toggle_alarm(self):
        selected_item = self.alarm_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an alarm to toggle!")
            return
        
        item_index = self.alarm_tree.index(selected_item)
        self.alarms[item_index].is_active = not self.alarms[item_index].is_active
        self.update_alarm_list()

    def delete_alarm(self):
        selected_item = self.alarm_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an alarm to delete!")
            return
        
        item_index = self.alarm_tree.index(selected_item)
        self.alarms[item_index].is_active = False
        del self.alarms[item_index]
        self.update_alarm_list()

    def start_alarm(self, alarm):
        while True:
            if not alarm.is_active:
                break
                
            current_time = datetime.now()
            current_day = self.days[current_time.weekday()]
            
            if (current_time.hour == alarm.hour and 
                current_time.minute == alarm.minute and 
                current_day in alarm.days):
                
                for _ in range(10):  # Beep 10 times
                    if not alarm.is_active:
                        break
                    winsound.Beep(1000, 1000)
                
            time.sleep(1)

def main():
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()