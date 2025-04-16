import requests

class Fruit:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_fruits(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur de connexion à l'API: {str(e)}")

    def add_fruit(self, fruit_name: str):
        try:
            response = requests.post(self.api_url, json={"name": fruit_name})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

    def delete_fruit(self, fruit_id: str):
        try:
            response = requests.delete(f"{self.api_url}/{fruit_id}")
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la suppression du fruit: {str(e)}")

    def edit_fruit(self, fruit_id: str, new_name: str):
        try:
            update_fruit_request = {"id": fruit_id, "new_name": new_name}
            response = requests.put(self.api_url, json=update_fruit_request)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la modification du fruit: {str(e)}")