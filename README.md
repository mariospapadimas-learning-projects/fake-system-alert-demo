# Fake System Alert Demo
A simple Python prank script that simulates a fake "hacker attack" by opening Command Prompt, displaying scary messages in Notepad, and rickrolling the viewer. It ends with a humorous reveal by default. This is a simulation, not a real security incident, made for educational and entertainment purposes only.

<img width="1919" height="1034" alt="Στιγμιότυπο οθόνης 2026-06-08 174549" src="https://github.com/user-attachments/assets/dce714dd-e737-450c-a89e-b63601b9b0e7" />

Repository: [mariospapadimas-learning-projects/fake-system-alert-demo](https://github.com/mariospapadimas-learning-projects/fake-system-alert-demo).

## Features

* Pops up a fake Windows error message for an instant jump-scare
* Opens Command Prompt automatically
* Changes CMD text color to green
* Runs `dir/s` to list real directories recursively for the fake scan effect (it does not modify files)
* Opens a surprise video (Rickroll)
* Creates a scary Notepad message
* Displays a fake countdown with dramatic beeps
* Ends with a typed-out "Just kidding!" reveal — the PC is safe by default
* Optional real shutdown requires both the boolean setting and an explicit confirmation

## Requirements

* Windows with an unlocked interactive desktop, Command Prompt, and Notepad available through Run (`Win+R`)
* Python 3 with pip, and Git for the clone instructions below
* PyAutoGUI, the only third-party dependency
* A default web browser and internet access to play the Rickroll video

Install PyAutoGUI into the Python environment you will use to run the script:

```powershell
python -m pip install pyautogui
```

See the [PyAutoGUI installation guide](https://pyautogui.readthedocs.io/en/latest/install.html). `ctypes` and `winsound` are used for the popup and beeps; they and `time`, `os`, and `webbrowser` are included with Python on Windows. This script uses Windows APIs and commands and is not intended to run on macOS, Linux, or a headless session.

## Usage

Clone the repository:

```powershell
git clone https://github.com/mariospapadimas-learning-projects/fake-system-alert-demo.git
cd fake-system-alert-demo
```

After installing the dependency, run the script:

```powershell
python main.py
```

The script will:

1. Show a fake "Critical System Failure" popup
2. Open Command Prompt
3. Change the terminal text to green and list directories with `dir/s`
4. Open a surprise video
5. Display a fake warning message
6. Count down from 3, with a beep each second
7. Type out a "Just kidding!" message (or ask for confirmation of real shutdown, if enabled)

## Warning

This project is intended for educational and entertainment purposes only.

Do not run this on computers without the owner's permission. PyAutoGUI sends real keystrokes to the active desktop; let the sequence finish without switching windows. The security alert, hacked message, and countdown are theatrical effects, not evidence of an actual hack.

By default the script does **not** actually shut down the PC — it ends with a harmless "Just kidding!" message typed into Notepad. The normal Python boolean near the beginning of `main.py` is:

```python
shutdown_in_the_end = False
```

To request optional real shutdown, save your work first and change this setting to `True`. After the visual sequence and countdown, a separate Windows confirmation warns that this is a **REAL shutdown**, with **Yes**, **No**, and **Cancel** buttons. **No** is the default. Only selecting **Yes** initiates the real `shutdown /s /t 1` command (a one-second delay). Choosing **No**, **Cancel**, pressing **Esc**, or closing the confirmation keeps the computer on and retains the humorous reveal. If the confirmation cannot be displayed, shutdown is not initiated. Restore the setting to `False` to return to the harmless default ending.

## Tests

```powershell
python -B -m unittest discover -v
```

The tests use Python's built-in `unittest` and mock all desktop, popup, browser, sleep, beep, and OS effects, including the shutdown command. They do not execute an interactive prank or a real shutdown, and do not require PyAutoGUI to be installed. Enabling shutdown in a test changes only an in-memory copy of the script.

## Disclaimer

The author is not responsible for any misuse of this project. Use responsibly and only as a harmless prank among friends.

## Preview

```
YOU HAVE BEEN HACKED!!!

Your pc will shut down in

3
2
1

Just kidding! 😄 You have NOT been hacked.
```

Have fun and don't scare your friends too much. 😈
