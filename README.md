# Automated regulatory monitoring application

⭐️  Welcome to this framework for regulatory monitoring. The purpose of this framework is to allow the creation of inventories of legal texts appearing on the national online database legifrance.gouv.fr
It allows you to generate an encapsulated website thanks to Streamlit Cloud, which includes the developed functionalities.

📝  This framework is based on web scraping methods using the Selenium library, the inventories of legal texts are generated thanks to an automaton based on Google Chrome which browses the Légrifrance website.
The application consists of 2 pages:
  - The page called "INVENTAIRE DES ARTICLES" allows you to make inventories of the articles of law present in the database at the time the button is triggered.
  - The page called "BILAN DES MODIFICATIONS" allows you to carry out, from two inventories saved at different dates and loaded on the platform, the report of changes relating to the articles (addition, deletion, modification, repeal).

⚠️  [Inventory Functionality Interruption] 
As the data is temporarily stored in the cloud, if the program is interrupted, simply press the inventory button again to resume the calculation where the program left off. 

⚠️ [App Hibernation]
Community Cloud apps without traffic for 7 consecutive days will automatically go to sleep. 
<img src="https://docs.streamlit.io/images/spin_down.png" width="500">
![alt text](https://docs.streamlit.io/images/spin_down.png)
To wake the app up, press the "Yes, get this app back up!" button. This can be done by anyone who wants to view the app, not just the app developer!


