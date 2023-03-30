"""
This file allows you to run the project app.
"""
from multipage import MultiPage
from pages import inventory # import your page modules here
from pages import report
from pages import inventory_unsegmented

app = MultiPage()

# Add all your application here
app.add_page("INVENTAIRE DES ARTICLES", inventory_unsegmented.app)
app.add_page("BILAN DES MODIFICATIONS", report.app)

# The main app
app.run()