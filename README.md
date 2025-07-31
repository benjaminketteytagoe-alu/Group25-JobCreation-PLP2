# Pantry Vault - Group25 Job Creation Project (PLP2)

**Pantry Vault** is a command-line interface (CLI) application designed to help individuals especially beginners, foreigners, or everyday cooks manage, explore, and preserve culinary recipes from selected African countries. This simple and intuitive tool allows users to browse culturally rich dishes, save their favorites, and contribute to the preservation of African food heritage.

---

## Application Goals

1. **Cultural Preservation**
   As food and cooking are integral aspects of culture, Pantry Vault helps preserve traditional recipes that are at risk of fading with time.

2. **Access to Diverse Recipes**
   Users can discover and explore a variety of authentic African recipes from different regions, encouraging cultural exchange and culinary exploration.

3. **Beginner-Friendly Cooking Platform**
   New cooks and kitchen novices can easily find straightforward, guided recipes that reduce the complexity of cooking traditional meals.

---

## Repository Structure

```
.
├── LICENSE                # Project license
├── README.md              # Project overview and instructions
├── config.py              # Configuration settings
├── main.py                # Main entry point of the application
├── pantry/                # Core application package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface logic
│   ├── crud.py            # Create, Read, Update, Delete operations
│   └── db.py              # Database connection and models
└── requirements.txt       # Python dependencies
```

---

## How to Run the Application

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Group25-JobCreation-PLP2.git
cd Group25-JobCreation-PLP2
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application

You can run the application using the following command:

```bash
python3 main.py
```

> `streamlit run app.py` or `flask run` are included only if you later integrate a GUI or web-based interface. The current version is CLI-only.

---

## Features & Menu Options

Upon running the application, users will be prompted to log in or register. First-time users must register using a username and password.

Once logged in, the following menu will appear:

1. **Browse Foods by Country** – View recipes grouped by country.
2. **View All Foods** – List all available recipes.
3. **View Food Details** – Get detailed information about a selected recipe.
4. **Add New Recipe** – Submit your own recipe to the database.
5. **Recipe Menu** – Navigate and interact with your saved/favorite recipes.
6. **Logout** – Sign out of the current session.
7. **Exit** – Terminate the application.

> Simply enter the corresponding number to access each feature.

---

## Notes

* Pantry Vault is in active development. Future versions may include web and mobile interfaces using Flask or Streamlit.
* Contributions, feedback, and feature suggestions are welcome.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---
