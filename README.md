# Python Clock Application

A versatile desktop clock application built with Python and Tkinter that combines an alarm clock, stopwatch, and countdown timer in one convenient interface.

## Features

### 1. Alarm Clock
- Set multiple alarms with specific times
- Choose days of the week for each alarm
- Enable/disable alarms without deleting them
- Visual list of all set alarms with their status
- Customizable alarm sound
- 24-hour time format

### 2. Stopwatch
- Precision timing with centisecond accuracy
- Start, stop, and reset functionality
- Lap time recording
- Scrollable lap time history
- Clear, easy-to-read display

### 3. Timer
- Set hours (0-99), minutes (0-59), and seconds (0-59)
- Start, pause/resume, and reset functionality
- Visual countdown display
- Alert sound on completion
- Input validation for time values

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Windows OS (for sound functionality - winsound module)

## Installation

1. Clone this repository or download the source code:
```bash
git clone https://github.com/KalyanRajSahu-Snap/Alarm-clock.git
```

2. Navigate to the project directory:
```bash
cd Alarm-clock
```

3. Run the application:
```bash
python alarm.py
```

## Usage

### Alarm Clock
1. Select the "Alarm" tab
2. Enter the desired hour (00-23) and minute (00-59)
3. Select the days of the week for the alarm
4. Click "Set New Alarm"
5. Use the "Toggle Alarm" button to enable/disable alarms
6. Use the "Delete Alarm" button to remove alarms

### Stopwatch
1. Select the "Stopwatch" tab
2. Click "Start" to begin timing
3. Use "Lap" to record split times
4. Click "Stop" to pause the stopwatch
5. Use "Reset" to clear all times and start over

### Timer
1. Select the "Timer" tab
2. Enter the desired hours, minutes, and seconds
3. Click "Start" to begin countdown
4. Use "Pause/Resume" to control the timer
5. Click "Reset" to clear the timer
6. An alert will sound when the timer reaches zero

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using Python's Tkinter library for the GUI
- Uses threading for non-blocking alarm and timer functionality
- Implements standard Windows sound for notifications
