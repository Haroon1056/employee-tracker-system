# Employee Tracker System

## Overview
The Employee Tracker System monitors employee activity by detecting keyboard and mouse usage. If an employee becomes inactive, the system initiates countdowns and takes actions based on the duration of inactivity. 

Key features include:
- Detection of employee inactivity through keyboard and mouse inputs.
- A 20-second countdown followed by a notification to focus on work.
- A 10-second countdown, after which a screenshot and picture are taken and saved.
- The process restarts after every inactivity period.
- The countdown is interrupted if the employee becomes active at any point during the countdown.

## Features
1. **Employee Activity Detection**: Tracks keyboard and mouse usage to determine inactivity.
2. **Countdown Timers**: 
   - **20-second Timer**: Notifies the employee to focus on their work.
   - **10-second Timer**: If inactivity persists, captures a screenshot and photo.
3. **Notifications**: Alerts the employee during the countdown periods.
4. **Screenshot and Photo Capture**: Saves the captured data in a specified folder.
5. **Interruptions**: Countdown timers are interrupted if the employee becomes active at any point.

## Setup
To set up the project locally, follow these steps:

## Requirements
- Python 3.x
- PyQt5
- OpenCV (for camera functionality)

## Usage
Start the System: Once the application is running, it will continuously monitor employee activity.
Inactivity Detection: If inactivity is detected, the system will start countdowns and take actions as described above.
Data Storage: Captured screenshots and photos are saved in the specified folder.

## Contributing
Feel free to fork this repository and make contributions. Pull requests are welcome!


## Authors

- [@HaroonRasheed](https://github.com/Haroon1056)
