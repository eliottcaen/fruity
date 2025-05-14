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

    def add_fruit(self, fruit_name: str, price: float, supermarket: str):
        try:
            # Sending the name, price, and supermarket along with the request
            response = requests.post(self.api_url, json={
                "name": fruit_name,
                "price": price,
                "supermarket": supermarket
            })
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

    def delete_fruit(self, fruit_id: str):
        try:
            response = requests.delete(f"{self.api_url}/{fruit_id}")
            response.raise_for_status()
            # Assuming the API returns a JSON with a status key
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la suppression du fruit: {str(e)}")

    def edit_fruit(self, fruit_id: str, updated_fields: dict):
        try:
            payload = {"id": fruit_id}
            payload.update(updated_fields)  # Include only the fields to update
            print("Payload:", payload)
            response = requests.patch(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la modification du fruit: {str(e)}")