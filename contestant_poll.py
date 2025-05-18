#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author  : Wleach
Date    : May 2025
Purpose : 

'''

import argparse
import hashlib
import logging
import json
import os
from pprint import pprint
import re
from typing import Text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time


version = "0.3"

class ContestantAutomation(object):
    '''
    An object to represent the invoice collector bot itself
    '''

    def __init__(self) -> None:
        '''
        Initializes the Invoice Collector Object with pre-populated
        values
        '''
        super().__init__()
        self.site = "https://wealth-vibe.mn.co/sign_in?from=https%3A%2F%2Fwealth-vibe.mn.co%2F"
        self.options = Options()
        self.driver = webdriver.Firefox(options=self.options)
        self.username = self._load_env_variable("TWV_USERNAME")
        self.password = self._load_env_variable("TWV_PASSWORD")
        self.output_file = "/home/wonk/contestant_results.json"
        # Checks if the state file exists. Otherwise it uses an empty dictionary
        logging.debug("Collection BOT Initialized")

    def _load_env_variable(self, env_var_name) -> str:
        '''
        Helper function to test if environment variables are set.
        '''
        try:
            logging.debug("Pulling in env variable: %s",env_var_name)
            return os.environ[env_var_name]
        except KeyError as err:
            raise KeyError(f"Set environment variable: {env_var_name}") from err


    def _login(self):
        '''
        Logs into the builder's site with pre-set credentials
        '''
        time.sleep(2)
        logging.debug(f"Attemping to connect to {self.site}")
        self.driver.get(self.site)
        # This will search for the HTML form with the id "userid" in its field name
        time.sleep(2)
        logging.debug("Sending credential material")
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/input').send_keys(
            self.username
        )
        password_field = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[1]/form/div[2]/div/div/div/div[1]/input')
        password_field.send_keys(
            self.password
        )
        time.sleep(1)
        password_field.send_keys(Keys.ENTER)
        time.sleep(10)
        logging.debug(f"Login Successful: {self.site}, user: {self.username}")

    def _gather_posts(self):
        '''
        Navigates to Monthly Challenge
        '''
        self.driver.find_element(
            By.XPATH,
            '/html/body/div[6]/div[1]/div[1]/div[2]/div[4]/div[4]/div/div/a/div[2]'
        ).click()
        time.sleep(5)
        posts = self.driver.find_elements(By.CLASS_NAME,'feed-card')
        pprint(posts[0].text)

def main(args):
    '''
    Main Driver if called alone.
    :param args: an argparse object containing command line arguements.
    '''
    logging.basicConfig(level=args.logging)
    #Instantiates (Creates) an object of type Invoice Collector
    automation_bot = ContestantAutomation()
    automation_bot._login()
    automation_bot._gather_posts()
    # Telling our new invoice collector object to run a function
    exit(0)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-l',
        '--logging',
        action='store',
        required=False,
        default="INFO",
        choices= [
            "DEBUG",
            "WARN",
            "INFO",
            "CRITICAL",
            "ERROR"
        ]
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=args.logging,
        datefmt='%H:%M:%S'
    )
    main(args)
