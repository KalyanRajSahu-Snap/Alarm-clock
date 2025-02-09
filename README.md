# Python Alarm Clock

A simple, user-friendly alarm clock application built with Python and Tkinter. This desktop application features a clean graphical interface that displays the current time and allows users to set alarms with ease.

## Features

- Real-time digital clock display
- 24-hour format time input
- User-friendly graphical interface
- Input validation for time entries
- Visual feedback through message boxes
- Ability to stop alarm at any time
- Non-blocking alarm functionality using threading

## Prerequisites

Before running this application, make sure you have:

- Python 3.x installed
- Tkinter library (usually comes with Python)
- Windows OS (for current sound implementation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/KalyanRajSahu-Snap/Alarm-clock.git
```

2. Navigate to the project directory:
```bash
cd py-ala
```

3. Run the application:
```bash
python alarm.py
```

## Usage

1. Launch the application
2. Enter the alarm time:
   - Hour (00-23)
   - Minute (00-59)
3. Click "Set Alarm"
4. When the alarm time is reached, the system will beep 10 times
5. Use the "Stop Alarm" button to stop the alarm at any time

## GUI Components

- Current time display (updates every second)
- Hour input field (24-hour format)
- Minute input field
- Set Alarm button
- Stop Alarm button
- Status messages for user feedback

## Code Structure

- `AlarmClock` class: Main application class
  - `__init__`: Initializes the application window and variables
  - `create_widgets`: Sets up the GUI elements
  - `update_time`: Updates the current time display
  - `validate_time`: Validates user input
  - `set_alarm`: Initiates the alarm thread
  - `start_alarm`: Handles the alarm functionality
  - `stop_alarm`: Stops the active alarm

## Customization

You can modify the following aspects of the alarm:
- Alarm sound duration and frequency in the `start_alarm` method
- Number of beeps by changing the range in the beep loop
- GUI colors by modifying the background (`bg`) and foreground (`fg`) parameters
- Window size by adjusting the `geometry` setting

## Notes for Non-Windows Users

The current implementation uses the `winsound` module, which is Windows-specific. For other operating systems, you'll need to modify the sound implementation. Some alternatives include:

- Linux: Use the `beepy` module
- MacOS: Use `os.system('afplay /System/Library/Sounds/Ping.aiff')`
- Cross-platform: Consider using the `playsound` module

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with Python and Tkinter
- Inspired by the need for a simple, customizable alarm clock
- Thanks to all contributors who help improve this project

## Support

For support, issues, or contributions, please:
1. Check existing issues or create a new one
2. Submit pull requests with improvements
3. Contact the maintainer through GitHub

---
Created with ❤️ by Kalyan Raj Sahu
