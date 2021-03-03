# Pymodoro
![pymodoro gif](./pymodoro.gif)

### Description
A simple pomodoro timer using a simple CLI with python.

_note: notifications only works on linux's that supports the `notify-send` command._

### Installation
- Clone the repository
    ```
    git clone https://github.com/manuelIsCoding/pymodoro.git
    ```
- Start the virtual environment
    ```
    cd pymodoro
    source ./venv/bin/activate
    ```
- Install the requirements
    ```
    pip install -r requirements.txt
    ```
- Run the `pymodoro.py` file
    ```
    python pymodoro.py
    ```

### Usage
The duration of the sessions and breaks are set by default
to 25 minutes pomodoro, 5 minutes short break and 10 minutes long break.

You can change it's values using the following cli options:

- Setting a 50/10 pomodoro session.
    ```
    python pymodoro.py --pomodoro 50 --short-break 10 --long-break 30
    ```
- or you can use `-p`, `-s` and `-l` instead:
    ```
    python pymodoro.py -p 50 -s 10 -l 30
    ```

Use the _--help_ option to see all options.

![CLI Help](./cli-help.png)

___
Feel free to clone this repository and improve or modify the code
as you want.