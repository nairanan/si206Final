import beautifulsoup4
import sqlite3
import requests
import json
import re
import os
import unittest



def howMuchAura(name):
    if name == "Savin":
        return 0
    elif name == "Ananthu":
        return 10000