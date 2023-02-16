from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from time import sleep

# Firefox version
driver = webdriver.Firefox()

print("process started...")

# open the notepad file and read in the list of urls one line at a time
with open("links.txt") as url_file:
    for line in url_file.readlines():

        # trim the url address in notepad (to remove any leading or trailing spaces )
        url = line.strip()

        # check that the URL is not blank
        if url != "":

            # then navigate to the web page
            driver.get(url)

            # parse out the hostname from the URL to provide the png filename
            host = urlparse(url).hostname

            # wait 3 seconds for website to load fully
            sleep(3)

            # take screenshot and save as png with hostname as filename
            driver.get_screenshot_as_file("{}.png".format(host))            
            
            # inform user that this particular URL has been printed            
            print(url + " printed")

# close driver and message user
driver.quit()
print("process completed")


# What follows is Chrome version
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# with open("links.txt") as url_file:
#     for line in url_file.readlines():
#         url = line.strip()
#         if url != "":        
#             driver.get(url)
#             host = urlparse(url).hostname
#             sleep(3)
#             driver.get_screenshot_as_file("{}.png".format(host))            
#             print(url + " printed")

# driver.quit()
# print("process completed")


