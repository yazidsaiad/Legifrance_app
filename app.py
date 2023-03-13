"""
This file allows you to run the project app.
"""
from multipage import MultiPage
from pages import inventory # import your page modules here
from pages import report

app = MultiPage()

# Add all your application here
app.add_page("INVENTAIRE DES ARTICLES", inventory.app)
app.add_page("BILAN DES MODIFICATIONS", report.app)

# The main app
app.run()