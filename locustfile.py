from locust import HttpUser, task, between

class ProductApiUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/token", data={"username": "user", "password": "password"})
        print("Login response:", response.text)  # Ajoutez cette ligne pour imprimer la réponse
        try:
            self.token = response.json()["access_token"]
        except KeyError:
            print("Login failed, no access_token in response:", response.json())
            self.token = None

    @task
    def get_clients(self):
        if self.token:
            self.client.get("/products/", headers={"Authorization": f"Bearer {self.token}"})
        else:
            print("Skipping get_products task because login failed")
