import requests


class APIClient:

    def __init__(self):
        self.base_url = "http://localhost:5000/api/Category"


    def create_category(self, category_title):
        url = f"{self.base_url}/categories"
        data = {
            "title": category_title
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result

    def get_all_categories(self):
        url = f"{self.base_url}/categories"
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
        url = f"{self.base_url}/categories/{id}"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()

        return result
    
    def category_by_title(self, title):
        url = f"{self.base_url}/categories/search?categoryName={title}"
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
        url = f"{self.base_url}/categories/{id}"
        response = requests.delete(url)
        response.raise_for_status()
        print(f"\033[95m Category with ID {id} deleted successfully \033[0m")
        return None
    
    def get_products_category_by_id(self, id):
        url = f"{self.base_url}/categories/{id}/products"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        return result
    
    def get_products_category_by_title(self, title):
        url = f"{self.base_url}/categories/search?categoryName={title}"
        response = requests.get(url)
        response.raise_for_status()
        id = response.json()
        result = self.get_products_category_by_id(id)
        return result
    
    def show_products_category_by_id(self, id):
        id = int(id)
        products = self.get_products_category_by_id(id)
        Products = "\n".join(f" ID: {prod['id']}, Title: {prod['title']}, Price: {prod['price']}" 
                                for prod in products)
        print(f"\033[95m {Products} \033[0m")

    def show_products_category_by_title(self, title):
        products = self.get_products_category_by_title(title)
        Products = "\n".join(f" ID: {prod['id']}, Title: {prod['title']}, Price: {prod['price']}" 
                                for prod in products)
        print(f"\033[95m {Products} \033[0m")

    def change_category_title(self, id, new_title):
        url = f"{self.base_url}/{id}"
        data = {
            "title": new_title
        }
        response = requests.put(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result
    
    def create_products(self, id, title, price):
        url = f"{self.base_url}/categories/{id}/products"
        data = {
            "title": title,
            "price": price,
            "categoryId": id
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result
    