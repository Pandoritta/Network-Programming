import requests


class APIClient:

    #methods

    def __init__(self):
        self.base_url = "http://localhost:5000/api"


    def create_category(self, category_title):
        url = f"{self.base_url}/Category/categories"
        data = {
            "title": category_title
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result

    def get_all_categories(self):
        url = f"{self.base_url}/Category/categories"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        return result
    
    def show_all_categories(self):
        categories = self.get_all_categories()
        Categories = "\n".join(f" ID: {cat['id']}, Title: {cat['name']}" 
                                for cat in categories)
        print(f"\033[95m {Categories} \033[0m")

    def category_by_id(self, id):
        url = f"{self.base_url}/Category/categories/{id}"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()

        return result
    
    def category_by_title(self, title):
        url = f"{self.base_url}/Category/categories/search?categoryName={title}"
        response = requests.get(url)
        response.raise_for_status()
        id = response.json()
        result = self.category_by_id(id)
        return result
    
    def show_category_by_id(self, id):
        id = int(id)
        category  = self.category_by_id(id)
        for cat in category:
            if cat['id'] == id:
                print(f"\033[95m ID: {cat['id']}, Title: {cat['name']}, Products: {cat['itemsCount']} \033[0m")
            else:
                print(f"\033[95m Category not found \033[0m")
        

    def show_category_by_title(self, name):
        category = self.category_by_title(name)
        for cat in category:
            if cat['name'] == name:
                print(f"\033[95m ID: {cat['id']}, Title: {cat['name']}, Products: {cat['itemsCount']} \033[0m")
            else:
                print(f"\033[95m Category not found \033[0m")

    def delete_category(self, id):
        url = f"{self.base_url}/Category/categories/{id}"
        response = requests.delete(url)
        response.raise_for_status()
        print(f"\033[95m Category with ID {id} deleted successfully \033[0m")
        return None


if __name__ == "__main__":
    client = APIClient()
    client.delete_category(3)
