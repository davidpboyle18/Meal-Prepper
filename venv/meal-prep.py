import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Sample recipe database
recipes = [
    {
        "name": "Grilled Chicken Salad",
        "ingredients": ["chicken", "lettuce", "tomato", "olive oil"],
        "cuisine": "Healthy",
        "healthiness": 5,
        "instructions": "Grill the chicken and mix with other ingredients."
    },
    {
        "name": "Pasta Alfredo",
        "ingredients": ["pasta", "cream", "parmesan"],
        "cuisine": "Italian",
        "healthiness": 2,
        "instructions": "Cook pasta, mix with cream and parmesan."
    },
    {
        "name": "Vegan Tacos",
        "ingredients": ["tortilla", "black beans", "avocado", "lettuce"],
        "cuisine": "Vegan",
        "healthiness": 4,
        "instructions": "Fill tortillas with beans, avocado, and lettuce."
    }
]

# Available options
ingredient_options = [
    "chicken", "lettuce", "tomato", "olive oil",
    "pasta", "cream", "parmesan", "tortilla",
    "black beans", "avocado", "cheese", "onion",
    "spinach", "bread", "rice", "milk", "eggs",
    "potato", "carrot", "peanut butter", "jam"
]
cuisine_options = ["Healthy", "Italian", "Vegan"]

# Pagination logic for ingredients
PAGE_SIZE = 10
current_page = 0

def paginate_ingredients(page):
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    return ingredient_options[start_index:end_index]

def update_ingredient_display():
    for widget in ingredient_frame.winfo_children():
        widget.destroy()

    ingredients = paginate_ingredients(current_page)
    for i, ingredient in enumerate(ingredients):
        row, col = divmod(i, 2)
        ttk.Checkbutton(ingredient_frame, text=ingredient, variable=ingredient_vars[ingredient]).grid(row=row, column=col, padx=10, pady=5)

def next_page():
    global current_page
    if (current_page + 1) * PAGE_SIZE < len(ingredient_options):
        current_page += 1
        update_ingredient_display()

def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        update_ingredient_display()

# Custom range slider
def on_slider_change(event):
    min_val = int(min_health_var.get())
    max_val = int(max_health_var.get())
    if event.widget == min_slider and min_val > max_val:
        min_health_var.set(max_val)
    elif event.widget == max_slider and max_val < min_val:
        max_health_var.set(min_val)

def find_recipes(ingredients, cuisine, min_health, max_health):
    matching_recipes = []
    for recipe in recipes:
        if (
            any(ingredient in ingredients for ingredient in recipe["ingredients"]) and
            recipe["cuisine"].lower() == cuisine.lower() and
            min_health <= recipe["healthiness"] <= max_health
        ):
            matching_recipes.append(recipe)
    return matching_recipes

def search_recipes():
    selected_ingredients = [ingredient for ingredient, var in ingredient_vars.items() if var.get()]
    selected_cuisine = cuisine_var.get()
    min_health = int(min_health_var.get())
    max_health = int(max_health_var.get())

    if not selected_ingredients:
        messagebox.showwarning("No Ingredients", "Please select at least one ingredient!")
        return

    if not selected_cuisine:
        messagebox.showwarning("No Cuisine", "Please select a type of cuisine!")
        return

    matches = find_recipes(selected_ingredients, selected_cuisine, min_health, max_health)
    result_text.delete(1.0, "end")

    if matches:
        for recipe in matches:
            result_text.insert("end", f"Name: {recipe['name']}\n")
            result_text.insert("end", f"Ingredients: {', '.join(recipe['ingredients'])}\n")
            result_text.insert("end", f"Instructions: {recipe['instructions']}\n\n")
    else:
        result_text.insert("end", "No matching recipes found.")

# Main window
app = ttk.Window(themename="flatly")
app.title("Recipe Finder")
app.geometry("800x600")

# Ingredient selection
ingredient_vars = {ingredient: ttk.BooleanVar() for ingredient in ingredient_options}
ttk.Label(app, text="Select Ingredients:", font=("Arial", 14, "bold")).pack(anchor="center", pady=10)

ingredient_frame = ttk.Frame(app)
ingredient_frame.pack(anchor="center", pady=5)

pagination_frame = ttk.Frame(app)
pagination_frame.pack(anchor="center", pady=5)
ttk.Button(pagination_frame, text="Previous", bootstyle="secondary", command=previous_page).pack(side="left", padx=5)
ttk.Button(pagination_frame, text="Next", bootstyle="secondary", command=next_page).pack(side="left", padx=5)

update_ingredient_display()

# Cuisine selection
ttk.Label(app, text="Select Cuisine:", font=("Arial", 14, "bold")).pack(anchor="center", pady=10)
cuisine_var = ttk.StringVar()
cuisine_dropdown = ttk.Combobox(app, textvariable=cuisine_var, values=cuisine_options, state="readonly", width=20)
cuisine_dropdown.pack(anchor="center", pady=5)

# Healthiness range slider
ttk.Label(app, text="Select Healthiness Range:", font=("Arial", 14, "bold")).pack(anchor="center", pady=10)
healthiness_frame = ttk.Frame(app)
healthiness_frame.pack(anchor="center", pady=5)
min_health_var = ttk.IntVar(value=1)
max_health_var = ttk.IntVar(value=5)
min_slider = ttk.Scale(healthiness_frame, from_=1, to=5, variable=min_health_var, orient=HORIZONTAL, length=300)
max_slider = ttk.Scale(healthiness_frame, from_=1, to=5, variable=max_health_var, orient=HORIZONTAL, length=300)
min_slider.bind("<Motion>", on_slider_change)
max_slider.bind("<Motion>", on_slider_change)
min_slider.pack(side="left")
ttk.Label(healthiness_frame, text="to").pack(side="left")
max_slider.pack(side="left")

# Search button
ttk.Button(app, text="Find Recipes", bootstyle="success", command=search_recipes).pack(anchor="center", pady=15)

# Results display
ttk.Label(app, text="Matching Recipes:", font=("Arial", 14, "bold")).pack(anchor="center", pady=10)
result_text = ttk.Text(app, height=10, width=80, wrap="word")
result_text.pack(anchor="center", pady=5)

# Run the application
app.mainloop()

