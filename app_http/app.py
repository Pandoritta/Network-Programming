import api_client as api
import sys

class UtmShopApp:

    def __init__(self):
        self.client = api.APIClient()

        choices = {
                "1": self.client.show_all_categories,
                "3": lambda: self.client.create_category(input("\n\033[95m Enter the title of the new category: \033[0m")),
                "4": lambda: self.client.delete_category(input("\n\033[95m Enter the ID of the category to delete: \033[0m")),
                "5": lambda: self.client.change_category_title(input("\n\033[95m Enter the ID of the category to change: \033[0m"), 
                                                       input("\n\033[95m Enter the new title: \033[0m")),
                "6": lambda: self.client.create_products(input("\n\033[95m Enter the ID of the category to add products: \033[0m"),
                                                    input("\n\033[95m Enter the title of the new product: \033[0m"),
                                                    input("\n\033[95m Enter the price of the new product: \033[0m")), 
                "7": lambda: self.client.show_products_category_by_id(input("\n\033[95m Enter the ID of the category to show products: \033[0m")),
                "8": sys.exit
            }
        choice2 = {
                "1": lambda: self.client.show_category_by_id(input("\n\033[95m Enter the ID of the category: \033[0m")),
                "2": lambda: self.client.show_category_by_title(input("\n\033[95m Enter the title of the category: \033[0m"))
            }
        
        self.choices = choices
        self.choice2 = choice2

    def show_menu(self):
        while True:
            print("\n\033[32m >UtmShop Menu: \033[0m")
            print(" \033[32m >1. Show all Categories \033[0m")
            print(" \033[32m >2. Show Category Details \033[0m")
            print(" \033[32m >3. Create a New Category \033[0m")
            print(" \033[32m >4. Delete a Category \033[0m")
            print(" \033[32m >5. Change the title for a category \033[0m")
            print(" \033[32m >6. Add new Products in Category \033[0m")
            print(" \033[32m >7. Show all Products in Category \033[0m")
            print(" \033[32m >8. Exit \033[0m")

            choice = input("\n\033[95m Enter your choice (1-8): \033[0m")
            self.handle_choice(choice)
        
    def handle_choice(self, choice):
        if choice in self.choices:
            self.choices[choice]()
        elif choice == "2":
            print("\n\033 Please choose the info you have for the category \n 1. ID \n 2. Title \033[0m")
            info = input("\n\033[95m Enter your choice (1-2): \033[0m")
            if info in self.choice2:
                self.choice2[info]()
            else:
                print("\n\033[91m Invalid choice. Please try again. \033[0m")
        else: 
            print("\n\033[91m Invalid choice. Please try again. \033[0m")
            return self.show_menu()

if __name__ == "__main__":
    client = UtmShopApp()
    client.handle_choice(client.show_menu())