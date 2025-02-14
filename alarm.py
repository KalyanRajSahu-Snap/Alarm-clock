import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import winsound
from threading import Thread
import math

class Alarm:
    def __init__(self, hour, minute, days):
        self.hour = hour
        self.minute = minute
        self.days = days
        self.is_active = True
        self.thread = None

class AlarmClockStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock, Stopwatch & Timer")
        self.root.geometry("650x650")
        self.root.configure(bg="#f0f0f0")
        
        # Alarm Variables
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.alarms = []
        self.days_vars = []
        self.days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Stopwatch Variables
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed_time = 0
        self.lap_times = []
        
        # Timer Variables
        self.timer_running = False
        self.timer_paused = False
        self.timer_remaining = 0
        self.timer_hours = tk.StringVar(value="00")
        self.timer_minutes = tk.StringVar(value="00")
        self.timer_seconds = tk.StringVar(value="00")
        
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Frames for Different Functions
        self.alarm_frame = ttk.Frame(self.notebook)
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.timer_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.alarm_frame, text="Alarm")
        self.notebook.add(self.stopwatch_frame, text="Stopwatch")
        self.notebook.add(self.timer_frame, text="Timer")
        
        # Initialize Frames
        self.create_alarm_widgets()
        self.create_stopwatch_widgets()
        self.create_timer_widgets()
        
        # Update current time
        self.update_time()

    def create_timer_widgets(self):
        # Timer display frame
        timer_display_frame = tk.Frame(self.timer_frame, bg="#f0f0f0")
        timer_display_frame.pack(pady=20)

        # Timer input fields
        tk.Label(timer_display_frame, text="Hours:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        tk.Entry(timer_display_frame, textvariable=self.timer_hours, width=3).grid(row=0, column=1)
        
        tk.Label(timer_display_frame, text="Minutes:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        tk.Entry(timer_display_frame, textvariable=self.timer_minutes, width=3).grid(row=0, column=3)
        
        tk.Label(timer_display_frame, text="Seconds:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
        tk.Entry(timer_display_frame, textvariable=self.timer_seconds, width=3).grid(row=0, column=5)

        # Timer display
        self.timer_label = tk.Label(
            self.timer_frame,
            text="00:00:00",
            font=("Helvetica", 36),
            bg="#f0f0f0"
        )
        self.timer_label.pack(pady=20)

        # Timer buttons frame
        timer_btn_frame = tk.Frame(self.timer_frame, bg="#f0f0f0")
        timer_btn_frame.pack(pady=10)

        # Start button
        self.timer_start_btn = tk.Button(
            timer_btn_frame,
            text="Start",
            command=self.start_timer,
            width=10,
            bg="#4CAF50",
            fg="white"
        )
        self.timer_start_btn.pack(side=tk.LEFT, padx=5)

        # Pause button
        self.timer_pause_btn = tk.Button(
            timer_btn_frame,
            text="Pause",
            command=self.pause_timer,
            width=10,
            state=tk.DISABLED,
            bg="#FFA500",
            fg="white"
        )
        self.timer_pause_btn.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.timer_reset_btn = tk.Button(
            timer_btn_frame,
            text="Reset",
            command=self.reset_timer,
            width=10,
            bg="#f44336",
            fg="white"
        )
        self.timer_reset_btn.pack(side=tk.LEFT, padx=5)

    def start_timer(self):
        try:
            hours = int(self.timer_hours.get())
            minutes = int(self.timer_minutes.get())
            seconds = int(self.timer_seconds.get())
            
            if not (0 <= hours <= 99 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ValueError
                
            if not self.timer_running:
                total_seconds = hours * 3600 + minutes * 60 + seconds
                if total_seconds > 0:
                    self.timer_remaining = total_seconds
                    self.timer_running = True
                    self.timer_paused = False
                    self.timer_start_btn.config(state=tk.DISABLED)
                    self.timer_pause_btn.config(state=tk.NORMAL)
                    Thread(target=self.run_timer, daemon=True).start()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid time values!")

    def pause_timer(self):
        if self.timer_running:
            if not self.timer_paused:
                self.timer_paused = True
                self.timer_pause_btn.config(text="Resume")
            else:
                self.timer_paused = False
                self.timer_pause_btn.config(text="Pause")

    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.timer_remaining = 0
        self.timer_start_btn.config(state=tk.NORMAL)
        self.timer_pause_btn.config(state=tk.DISABLED, text="Pause")
        self.timer_label.config(text="00:00:00")
        self.timer_hours.set("00")
        self.timer_minutes.set("00")
        self.timer_seconds.set("00")

    def run_timer(self):
        while self.timer_running and self.timer_remaining > 0:
            if not self.timer_paused:
                hours = self.timer_remaining // 3600
                minutes = (self.timer_remaining % 3600) // 60
                seconds = self.timer_remaining % 60
                
                self.timer_label.config(
                    text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                )
                
                self.timer_remaining -= 1
                time.sleep(1)
                
                if self.timer_remaining == 0:
                    self.timer_running = False
                    self.timer_start_btn.config(state=tk.NORMAL)
                    self.timer_pause_btn.config(state=tk.DISABLED)
                    winsound.Beep(1000, 1000)  # Timer completion sound
                    messagebox.showinfo("Timer", "Time's up!")
        
        if not self.timer_remaining:
            self.reset_timer()

    # [Previous methods remain the same]
    def create_alarm_widgets(self):
        # Current time display
        self.time_label = tk.Label(
            self.alarm_frame,
            text="",
            font=("Helvetica", 24),
            bg="#f0f0f0"
        )
        self.time_label.pack(pady=10)
        
        # Alarm Settings Frame
        settings_frame = tk.Frame(self.alarm_frame, bg="#f0f0f0")
        settings_frame.pack(pady=10)
        
        # Hour input
        tk.Label(settings_frame, text="Hour (00-23):", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        hour_entry = tk.Entry(settings_frame, textvariable=self.hour, width=5)
        hour_entry.grid(row=0, column=1, padx=5)
        
        # Minute input
        tk.Label(settings_frame, text="Minute (00-59):", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        minute_entry = tk.Entry(settings_frame, textvariable=self.minute, width=5)
        minute_entry.grid(row=0, column=3, padx=5)

        # Days selection frame
        days_frame = tk.Frame(self.alarm_frame, bg="#f0f0f0")
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
            self.alarm_frame,
            text="Set New Alarm",
            command=self.set_alarm,
            bg="#4CAF50",
            fg="white",
            width=15
        )
        set_button.pack(pady=10)

        # Alarm List Frame
        list_frame = tk.Frame(self.alarm_frame)
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
        actions_frame = tk.Frame(self.alarm_frame, bg="#f0f0f0")
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

    def create_stopwatch_widgets(self):
        # Stopwatch Display
        self.stopwatch_label = tk.Label(
            self.stopwatch_frame, 
            text="00:00:00.00", 
            font=("Helvetica", 36)
        )
        self.stopwatch_label.pack(pady=20)

        # Stopwatch Buttons Frame
        btn_frame = tk.Frame(self.stopwatch_frame)
        btn_frame.pack(pady=10)

        # Start/Stop Button
        self.start_stop_btn = tk.Button(
            btn_frame, 
            text="Start", 
            command=self.toggle_stopwatch,
            width=10
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)

        # Reset Button
        reset_btn = tk.Button(
            btn_frame, 
            text="Reset", 
            command=self.reset_stopwatch,
            width=10
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Lap Button
        lap_btn = tk.Button(
            btn_frame, 
            text="Lap", 
            command=self.record_lap,
            width=10
        )
        lap_btn.pack(side=tk.LEFT, padx=5)

        # Lap Times Listbox
        self.lap_listbox = tk.Listbox(
            self.stopwatch_frame, 
            width=40, 
            height=10
        )
        self.lap_listbox.pack(pady=10)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        
        # Update stopwatch if running
        if self.stopwatch_running:
            self.update_stopwatch()
        
        self.root.after(50, self.update_time)

    def toggle_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
            self.stopwatch_running = True
            self.start_stop_btn.config(text="Stop")
        else:
            self.stopwatch_running = False
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
            self.start_stop_btn.config(text="Start")

    def update_stopwatch(self):
        elapsed = time.time() - self.stopwatch_start_time
        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)
        centiseconds = int((elapsed - int(elapsed)) * 100)
        self.stopwatch_label.config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        )

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed_time = 0
        self.start_stop_btn.config(text="Start")
        self.stopwatch_label.config(text="00:00:00.00")
        self.lap_times.clear()
        self.lap_listbox.delete(0, tk.END)

    def record_lap(self):
        if self.stopwatch_running:
            lap_time = time.time() - self.stopwatch_start_time
            minutes, seconds = divmod(int(lap_time), 60)
            hours, minutes = divmod(minutes, 60)
            centiseconds = int((lap_time - int(lap_time)) * 100)
            lap_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            self.lap_times.append(lap_time)
            self.lap_listbox.insert(tk.END, lap_str)
            self.lap_listbox.see(tk.END)

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
        alarm.thread = Thread(target=self.start_alarm, args=(alarm,), daemon=True)
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
    app = AlarmClockStopwatch(root)
    root.mainloop()

if __name__ == "__main__":
    main()