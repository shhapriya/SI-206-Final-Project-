import requests
import json
import unittest
import os

def read_api_key (file):
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.readline().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: {'api_key.txt'} not found.")
        return None
API_KEY = read_api_key("api_key_lastfm.txt")