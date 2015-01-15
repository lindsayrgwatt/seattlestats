from selenium import webdriver

browser = webdriver.Firefox()

# Visit homepage
browser.get('http://localhost:8000')

# Confirm that it is a Django project
assert 'Django' in browser.title

browser.quit()
