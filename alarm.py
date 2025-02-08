import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import winsound
from threading import Thread

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Alarm Clock")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        # Variables for hour, minute
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.alarm_thread = None
        self.alarm_running = False
        
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
        self.time_label.pack(pady=20)
        
        # Frame for alarm settings
        settings_frame = tk.Frame(self.root, bg="#f0f0f0")
        settings_frame.pack(pady=20)
        
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
        
        # Set alarm button
        set_button = tk.Button(
            self.root,
            text="Set Alarm",
            command=self.set_alarm,
            bg="#4CAF50",
            fg="white",
            width=15
        )
        set_button.pack(pady=10)
        
        # Stop alarm button
        stop_button = tk.Button(
            self.root,
            text="Stop Alarm",
            command=self.stop_alarm,
            bg="#f44336",
            fg="white",
            width=15
        )
        stop_button.pack(pady=5)
    
    def update_time(self):
        # Update current time display
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
    
    def set_alarm(self):
        if not self.validate_time(self.hour.get(), self.minute.get()):
            messagebox.showerror("Error", "Please enter valid time!")
            return
        
        if self.alarm_thread and self.alarm_running:
            messagebox.showinfo("Info", "Alarm is already set!")
            return
        
        self.alarm_running = True
        self.alarm_thread = Thread(target=self.start_alarm)
        self.alarm_thread.start()
        messagebox.showinfo("Success", "Alarm has been set!")
    
    def start_alarm(self):
        while self.alarm_running:
            current_time = datetime.now()
            alarm_hour = int(self.hour.get())
            alarm_minute = int(self.minute.get())
            
            if (current_time.hour == alarm_hour and 
                current_time.minute == alarm_minute):
                for _ in range(10):  # Beep 10 times
                    if not self.alarm_running:
                        break
                    winsound.Beep(1000, 1000)  # Frequency: 1000Hz, Duration: 1s
                self.alarm_running = False
                break
            time.sleep(1)
    
    def stop_alarm(self):
        self.alarm_running = False
        if self.alarm_thread:
            self.alarm_thread.join(timeout=1)
        messagebox.showinfo("Info", "Alarm stopped!")

def main():
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()