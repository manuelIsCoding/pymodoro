# -*- coding: UTF-8 -*-
# author: Manuel Rubio
# date: 03-Mar-21
# description: A simple cli to do pomodoro's study sessions.
import time
import sys
import os
import click


class PomodoroTimer:
    def __init__(self, pomodoro, short, long_):
        self.pomodoro = pomodoro
        self.short = short
        self.long = long_

        self._sessions = 0
        self._session_active = True
        self._long_active = False

    @staticmethod
    def _min_to_sec(minutes):
        return minutes * 60

    @staticmethod
    def _sec_to_min(seconds):
        return seconds / 60

    @staticmethod
    def _zero_pad(number):
        number_str = str(number)
        if len(number_str) == 1:
            return '0' + number_str
        else:
            return number

    def _send_message(self, title, message):
        if os.uname().sysname == 'Linux':
            os.system(f"notify-send '{title}' '{message}'")

    def _display_timer(self, minutes):
        minutes = minutes - 1
        a_minute = 59
        timer = self._min_to_sec(minutes)
        try:
            while minutes >= 0:
                if not a_minute:
                    minutes -= 1
                    a_minute = 59
                time.sleep(0.01)
                os.system('clear')
                print('timer is active, press ctrl + c to stop it.')
                if not minutes:
                    print(f'00:{self._zero_pad(a_minute)}')
                else:
                    print(f'{self._zero_pad(minutes)}:'
                            f'{self._zero_pad(a_minute)}')
                timer -= 1
                a_minute -= 1

            if self._long_active:
                self._send_message('long break is up', 'pomodoro finished')
                os.system('clear')
                return sys.exit(0)

            if self._sessions > 2:
                self._send_message('pomodoro is up', 'starting a long break')
                self._long_active = True
                self._display_timer(self.long)

            if self._session_active:
                self._session_active = False
                self._sessions += 1
                self._send_message('pomodoro is up', 'starting a short break')
                self._display_timer(self.short)
            else:
                self._session_active = True
                self._send_message('short break is up', 'starting a pomodoro')
                self._display_timer(self.pomodoro)

        except KeyboardInterrupt:
            print('session stopped')
            sys.exit(0)
    
    def start(self):
        return self._display_timer(self.pomodoro)

    def __str__(self):
        return f'A {self.pomodoro!r}/{self.short!r} pomodoro timer'

    def __repr__(self):
        return (f'{self.__class__.__name__}(pomodoro={self.pomodoro!r}, '
                f'short={self.short!r}, long={self.long!r})')


@click.command()
@click.option('-p', '--pomodoro', default=25, help='Pomodoro session time in minutes.')
@click.option('-s', '--short-break', default=5, help='Short break time in minutes.')
@click.option('-l', '--long-break', default=15, help='Long break timer in minutes.')
def main(pomodoro, short_break, long_break):
    session = PomodoroTimer(pomodoro, short_break, long_break)
    return session.start()

if __name__ == '__main__':
    main()
