#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import os
import subprocess
"""
    Utilities
"""

VERSION_MAJOR = 0
VERSION_MINOR = 11
VERSION_PATCH = 0
VERSION_IDENTIFIER = "beta"

VERSION_SHORT = '{}.{}'.format(VERSION_MAJOR, VERSION_MINOR)
VERSION = "{}.{}.{}-{}".format(VERSION_MAJOR,
                               VERSION_MINOR, VERSION_PATCH, VERSION_IDENTIFIER)

HUMIDITY_NORMAL = 0
HUMIDITY_COMFORTABLE = 1
HUMIDITY_DRY = 2
HUMIDITY_WET = 3

_MS_KMH = 60 * 60 / 1000


def machine():
    return platform.machine()


def node():
    return platform.node()


def os_command(command):
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    data, errors = p.communicate()
    if p.returncode != 0:
        r = None
    else:
        r = data.decode("utf-8", "ignore")
    return r


def os_release():
    return platform.release()


def os_version():
    return platform.version()


def processor():
    return platform.processor()


def python_version():
    return platform.python_version()


def system():
    return platform.system()


def version():
    return VERSION


def version_identifier():
    return VERSION_IDENTIFIER


def version_major():
    return VERSION_MAJOR


def version_minor():
    return VERSION_MINOR


def version_patch():
    return VERSION_PATCH


def version_short():
    return VERSION_SHORT


def c_2_f(value):
    """Temperature conversion from Celsius to Fahrenheit

    Args:
        value (float): temperature in Celsius

    Returns:
        temperature in Fahrenheit
    """
    return (value * 1.8) + 32


def f_2_c(value):
    """Temperature conversion from Fahrenheit to Celsius

    Args:
        value (float): temperature in Fahrenheit

    Returns:
        temperature in Celsius
    """
    return (value - 32) / 1.8


def bearing_2_status(d):
    """ Converts wind direction in degrees to a winddirection in letters
    Used in wind devices

    Args:
        d (float): winddirection in degrees, 0 - 360

    Returns:
        description of the wind direction, eg. "NNE", WNW", etc.

    Ref:
        Based on https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    """
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    count = len(dirs)  # Number of entries in list
    step = 360 / count  # Wind direction is in steps of 22.5 degrees (360/16)
    ix = int((d + (step / 2)) / step)  # Calculate index in the list
    return dirs[ix % count]


def bool_2_int(value):
    """Convert boolean to 0 or 1
    Required for eg. /json.htm?type=command&param=makefavorite&idx=IDX&isfavorite=FAVORITE

    Args:
        value (bool)

    Returns:
        1 if True, else 0
    """
    if isinstance(value, bool):
        return int(value)
    else:
        return 0


def bool_2_str(value):
    """Convert boolean to a string "true" or "false"
    Required for eg. /json.htm?type=setused&idx=IDX&used=true|false

    Args:
        value (bool)

    Returns:
        "true" if True, else "false"
    """
    if isinstance(value, bool):
        return str(value).lower()
    else:
        return "false"


def humidity_2_status(hlevel):
    """Converts humidity in % to a humidity level
    Used in weather stations

    Args:
        hlevel (float): humidity in %

    Returns:
        1, 2, 3 depending on hlevel
    """
    if hlevel < 25:
        return HUMIDITY_DRY
    if 25 <= hlevel <= 60:
        return HUMIDITY_COMFORTABLE
    if hlevel > 60:
        return HUMIDITY_WET
    # Useless, but this is how Get_Humidity_Level works in Domoticz!
    return HUMIDITY_NORMAL


def int_2_bool(value):
    """Converts an integer, eg. 0, 1, 11, 123 to boolean

    Args:
        value (int)

    Returns:
        False for value: 0
        True otherwise
    """
    if isinstance(value, int):
        return (bool(value))
    else:
        return False


def str_2_bool(value):
    """ Converts 'something' to boolean.

    Args:
        value (str)

    Returns:
        True for values : 1, True, "1", "TRue", "yes", "y", "t"
        False otherwise
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"):
        return True
    else:
        return False


def wind_chill(t, v):
    """
    Windchill temperature is defined only for temperatures at or below 10 °C 
    and wind speeds above 4.8 kilometres per hour.

    Args:
        t: temperature in celsius
        v: wind speed in m/s

    Returns:
        calculated windchill temperature

    Ref: 
        https://en.wikipedia.org/wiki/Wind_chill
    """
    # Calculation expects km/h instead of m/s, so
    v = ms_2_kmh(v)
    if t < 10 and v > 4.8:
        v = v ** 0.16
        return round(13.12 + 0.6215 * t - 11.37 * v + 0.3965 * t * v, 1)
    else:
        return t


def kmh_2_ms(value):
    """Convert speed from km/h to m/s

    Args:
        value (float): speed in km/h

    Returns:
        speed in m/s
    """
    return value / _MS_KMH


def ms_2_kmh(value):
    """Convert speed m/s to from km/h

    Args:
        value (float): speed in m/s

    Returns:
        speed in km/h
    """
    return value * _MS_KMH
