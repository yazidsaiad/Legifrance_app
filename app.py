"""
This file allows you to run the project app.
"""
from multipage import MultiPage
from pages import page_acceuil # import your page modules here

app = MultiPage()

# Add all your application here
app.add_page("Page d'accueil", page_acceuil.app)


# The main app
app.run()