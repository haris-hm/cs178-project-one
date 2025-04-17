# ShopSmart - A Simple Online Store Emulator
## Project Overview
ShopSmart is a simple web application which emulates the experience of an online store. Users can create accounts, log in, browse products from various categories, add products to their cart, and update quantities and delete products from their cart.

### Key Features
1. Simple User Authentication:
    - Users can register accounts and log in.
    - Authentication validates the user's credentials from their URL request arguments whenever they try to access any route which requires the user to be logged in.
2. Inventory Display:
    - Products are displayed by querying the SQL database for the `Inventory` table.
    - The user can filter the products based on their category.
3. Shopping Cart:
    - The user can add products into their cart from the inventory display page.
    - In the cart, the user can add or remove product quantities, as well as remove the product from the cart.
    - The user can also clear their entire cart.

## Technologies Used
This project uses a wide variety of cloud and database tools which we learned about over the course of the semester, so far.
### Backend
- **Flask**: A Python web framework which was used to build and run the entire application.
- **PyMySQL**: A Python library for connecting to SQL databases and making queries to them.
- **Boto3**: The AWS SDK for Python, which is used for interacting with AWS services. In this case, it's used to connect to a DynamoDB database and make queries.
### Frontend
- **Bootstrap**: A CSS framework which allows people to build fast and responsive sites without having to worry about complicated CSS.
- **HTML**: Markup language for websites.
- **CSS**: Custom styles for the project.
- **Jinja2**: A templating engine used by Flask for rendering HTML templates.
### Database
- **MySQL (Hosted on AmazonRDS)**: Used for storage of relational data (*e.g.,* user accounts, inventory, and product categories).
- **AWS DynamoDB**: A NoSQL database used for managing non-relational and high demand data (*e.g.,* user's shopping carts).
### Development Tools
- **[uv](https://docs.astral.sh/uv/)**: A Python package manager which simplifies dealing with virtual environments and dependencies. We use it in CS-188 (Software Engineering), and I really like it, so I used it here, as well.
- **Git/Github**: Code version control
 

## Setup & Run Instructions
### Using uv (Recommended)
To set up uv, run the following commands:

1. Install uv:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Instruct uv to use Python 3.13 as default:
```sh
echo export UV_PYTHON=$(which python3.13) >> $HOME/.local/bin/env
```
3. Source the file:
```sh
source $HOME/.local/bin/env
```

After installing, it's as simple as going into the project directory, and running the command `uv run start`, which runs a project script that calls the `serve()` function in app.py.

### Using Python and pip
Using Python and pip is a bit more involved, but possible. Ensure you have Python3.13 and pip installed, then follow these steps:

1. `cd` into the project directory
2. Create and activate the virtual environment
```sh
python3 -m venv .venv
source .venv/bin/activate
```
3. Install all required packages in the virtual environment
```sh
pip install -r requirements.txt
```
4. Finally, you can start the Flask application
```sh
python3 -m src.cs178_project_one.app
```
5. Once you're done running, deactivate the virtual environment
```sh
deactivate
```
