import requests
import xlsxwriter
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Font, Alignment, PatternFill, numbers
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

SPORT = 'upcoming'  # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us'  # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h'  # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal'  # decimal | american

DATE_FORMAT = 'iso'  # iso | unix

BET_SIZE = 100

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
).json()

# print(odds_response)

formatted_data = json.dumps(odds_response, indent=4)  # Formats json into a much more readable response

print(formatted_data)

BOOKMAKER_INDEX = 0
NAME_INDEX = 1
ODDS_INDEX = 2
FIRST = 0

class Event:
    def __init__(self, data):
        self.data = data
        self.sport_key = data['sport_key']
        self.id = data['id']

    def find_best_odds(self):
        # number of possible outcomes for a sporting event
        num_outcomes = len(self.data['bookmakers'][FIRST]['markets'][FIRST]['outcomes'])  
        self.num_outcomes = num_outcomes  # assigns count

        # finding the best odds for each outcome in each event
        best_odds = [[None, None, float('-inf')] for _ in range(num_outcomes)]
        # [Bookmaker, Name, Price]

        bookmakers = self.data['bookmakers']
        print(bookmakers)
        for index, bookmaker in enumerate(bookmakers):

            # determining the odds offered by each bookmaker
            for outcome in range(num_outcomes):

                # determining if any of the bookmaker odds are better than the current best odds
                bookmaker_odds = float(bookmaker['markets'][FIRST]['outcomes'][outcome]['price'])
                current_best_odds = best_odds[outcome][ODDS_INDEX]

                if bookmaker_odds > current_best_odds:
                    best_odds[outcome][BOOKMAKER_INDEX] = bookmaker['title']
                    best_odds[outcome][NAME_INDEX] = bookmaker['markets'][FIRST]['outcomes'][outcome]['name']
                    best_odds[outcome][ODDS_INDEX] = bookmaker_odds

        self.best_odds = best_odds
        return best_odds


event = Event(odds_response)  # placeholder event instance

event.find_best_odds()
