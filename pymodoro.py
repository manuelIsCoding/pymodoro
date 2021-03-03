# -*- coding: UTF-8 -*-
# author: Manuel Rubio
# date: 03-Mar-21
# description: A simple cli to do pomodoro's study sessions.

# importing the dependencies
import time
import sys
import os
import click


class PomodoroTimer:
    """A pomodoro timer class that can be displayed at the terminal using
    the start method."""
    def __init__(self, pomodoro, short, long_):
        """Initialize the duration of the session and breaks."""
        self.pomodoro = pomodoro
        self.short = short
        self.long = long_

        # variables to check the status of the session
        self._sessions = 0
        self._session_active = True
        self._long_active = False

    @staticmethod
    def _min_to_sec(minutes):
        """Internal static method to convert minutes to seconds."""
        return minutes * 60

    @staticmethod
    def _sec_to_min(seconds):
        """Internal static method to convert seconds to minutes."""
        return seconds / 60

    @staticmethod
    def _zero_pad(number):
        """Internal static method to pad the zeros on a number."""
        number_str = str(number)
        if len(number_str) == 1:
            return '0' + number_str
        else:
            return number

    def _send_message(self, title, message):
        """Displays a notification using the os.method function to
        execute the `notify-send` command if the machine runs on linux
        else it just print the `{title}: {message}`."""
        if os.uname().sysname == 'Linux':
            os.system(f"notify-send '{title}' '{message}'")
        else:
            print(f"{title}: {message}")

    def _display_timer(self, minutes):
        """Displays the timer from the `minutes` parameter starting 
        a while loop end when minutes are smaller than zero."""
        minutes = minutes - 1
        # Variable to count every minute decreasing it every second
        a_minute = 59
        # we converts the minutes to seconds to track easily 
        #  the time.
        timer = self._min_to_sec(minutes)
        try:
            while minutes >= 0:
                if not a_minute:
                    # it the `a_minute` variable is zero we decrease by one
                    #  the minutes and re-assign `a_minute` to 59 seconds.
                    minutes -= 1
                    a_minute = 59
                time.sleep(1)
                os.system('clear')
                print('timer is active, press ctrl + c to stop it.')

                # pretty-printing the timer using the `self._zero_pad` method.
                if not minutes:
                    print(f'00:{self._zero_pad(a_minute)}')
                else:
                    print(f'{self._zero_pad(minutes)}:'
                            f'{self._zero_pad(a_minute)}')
                # we use time.sleep function to decrease the `timer` and `a_minute`
                #  every second.
                timer -= 1
                a_minute -= 1

            # when while loop end we check the status of the session
            #  if the long break variable is true means that we completed all
            #  the study sessions, so we just send a message saying that the 
            #  pomodoro finished and exit.
            if self._long_active:
                self._send_message('long break is up', 'pomodoro finished')
                os.system('clear')
                return sys.exit(0)

            # if the pomodoro sessions count is greater than 3, we set the 
            #  self._long_active variable to True and we start the final break.
            if self._sessions > 2:
                self._send_message('pomodoro is up', 'starting a long break')
                self._long_active = True
                self._display_timer(self.long)

            # if the session was active means that we just end of study, so we 
            #  set self._session_active to false, plus 1 to the counter of sessions 
            #  and we start a short break.
            if self._session_active:
                self._session_active = False
                self._sessions += 1
                self._send_message('pomodoro is up', 'starting a short break')
                self._display_timer(self.short)
            else:
                # if the self._session_active variable was not True means that the 
                #  finished time was a break, so we set self._session_active to True
                #  and start a pomodoro time.
                self._session_active = True
                self._send_message('short break is up', 'starting a pomodoro')
                self._display_timer(self.pomodoro)

        except KeyboardInterrupt:
            # If the user press ctrl + c we exit the program.
            print('session stopped')
            sys.exit(0)
    
    def start(self):
        """Call the self._display_timer internal method with the pomodoro time."""
        return self._display_timer(self.pomodoro)

    def __str__(self):
        """Returns a friendly print of the class."""
        return f'A {self.pomodoro!r}/{self.short!r} pomodoro timer'

    def __repr__(self):
        """Returns a more descriptive print of the class."""
        return (f'{self.__class__.__name__}(pomodoro={self.pomodoro!r}, '
                f'short={self.short!r}, long={self.long!r})')


@click.command()
@click.option('-p', '--pomodoro', default=25, help='Pomodoro session time in minutes.')
@click.option('-s', '--short-break', default=5, help='Short break time in minutes.')
@click.option('-l', '--long-break', default=15, help='Long break timer in minutes.')
def main(pomodoro, short_break, long_break):
    """Main function that handle the cli options and it's no charge of start
    the timer."""
    session = PomodoroTimer(pomodoro, short_break, long_break)
    return session.start()


if __name__ == '__main__':
    # run the main function if the file is executed directly.
    main()
