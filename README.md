# restaurant-inventory-tracker

This is an inventory app built with Django, which allows users to manage ingredients, purchases, and menu items for a restaurant. The app allows users to perform CRUD operations on the ingredients, purchases, and menu items, and provides summary metrics for the restaurant.

## Installation and Setup (For local use)

1. Clone the repository to your local machine
2. Ensure that Python and Django are installed on your system
3. Install the required dependencies by running `pip install -r requirements.txt`
4. Migrate the database by running `python manage.py migrate`
5. Create a superuser account by running `python manage.py createsuperuser`
6. Run the development server by running `python manage.py runserver`
7. Access the app by visiting `http://127.0.0.1:8000/` in your web browser
8. Log in to the app using your superuser account

## Visiting the Heroku hosted website and signing up

- Visit: https://fast-coast-58525.herokuapp.com/
- Click "Sign up" in the top right corner to create an account
- You will be automatically logged in after signing up

## Usage

Once logged in to the app, you can use the following views to manage the inventory:

- **Ingredients**: View a list of all ingredients, add new ingredients, update existing ingredients, and delete ingredients.
- **Purchases**: View a list of all purchases, add new purchases, and delete purchases.
- **Menu**: View a list of all menu items, add new menu items, update existing menu items, and delete menu items.
- **Reports**: View summary metrics for the restaurant, including the total cost of inventory, total revenue, and total profit.
- **Ingredient Chart**: View a bar chart of the ingredients.
- **Purchase Chart**: View a bar chart of purchases.

Note that some views are only accessible to authenticated users, and require you to log in using your superuser account.

## Contributing

Contributions are welcome! If you have an idea for a new feature or want to report a bug, please open an issue on the repository.

## Future Enhancements

Here are some potential future enhancements for the inventory management system:

1. **API:** Create a RESTful API to allow other applications to interact with the inventory management system.
2. **User roles:** Add support for different user roles (e.g. manager, chef, waiter) with different levels of access to the inventory management system.
3. **Order tracking:** Develop a system to track ingredient orders and their delivery status.
4. **Real-time inventory tracking:** Add support for real-time inventory tracking to provide up-to-date information on ingredient availability.
5. **Recipe cost tracking:** Enable recipe cost tracking to help users determine the profitability of menu items.

