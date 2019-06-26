from locust import HttpLocust, TaskSet
from bs4 import BeautifulSoup
import random

auth_token = ""


def login(self):
    response = self.client.get("/login")
    pq = BeautifulSoup(response.text)
    text = pq.find('input', attrs={'name': 'authenticity_token'}).get('value')
    global auth_token
    auth_token = text


def login_post(self):
    global auth_token
    self.client.post("/session", {"commit": "Sign in",
                                  "utf8": "✓",
                                  "authenticity_token": auth_token,
                                  "login": "",
                                  "password": ""})


def logout(self):
    response = self.client.get("/logout")
    pq = BeautifulSoup(response.text)
    text = pq.find('input', attrs={'name': 'authenticity_token'}).get('value')
    global auth_token
    auth_token = text


def logout_post(self):
    global auth_token
    self.client.post("/logout", {"utf8": "✓",
                                 "authenticity_token": auth_token})


def profile(self):
    text = ['/erfdf', '/arifekubrahos']
    url = random.choice(text)
    print(url)
    response = self.client.get(url, catch_response=True)
    if not response.ok:
        response.failure("Get user fail")


def search(self):
    text = ['et', 'te']
    variables = {'q': random.choice(text)}
    response = self.client.get("/search?", params=variables)


class UserBehavior(TaskSet):
    tasks = {profile: 1, search: 1}


class LoginBehavior(TaskSet):
    tasks = {UserBehavior: 1}

    def on_start(self):
        login(self)
        login_post(self)

    def on_stop(self):
        logout(self)
        logout_post(self)


class GithubUser(HttpLocust):
    task_set = LoginBehavior
    min_wait = 5000
    max_wait = 10000
