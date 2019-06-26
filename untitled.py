from locust import HttpLocust, TaskSet


def login(e):
    e.client.post("/login", {"username": "user", "password": "pass"})


def logout(e):
    e.client.post("/logout", {"username": "user", "password": "pass"})


def index(e):
    e.client.get("/index")


def profile(e):
    e.client.get("/profile")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 2}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
