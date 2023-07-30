# Import required modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from info import username,username2,password,key

# Define the twitter class
class twitter:
    # Constructor to initialize the class
    def __init__(self, username, password):
        # Create a Chrome WebDriver instance
        self.browser = webdriver.Chrome()
        self.password = password
        self.username = username
    
    # Method to sign in to Twitter
    def signIn(self):
        # Open Twitter login page
        self.browser.get("https://twitter.com/login")
        time.sleep(3)

        # Find the username input element and enter the username
        usernameinp = self.browser.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
        usernameinp.send_keys(self.username)
        time.sleep(3)

        # Click on the "Next" button
        self.browser.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span").click()
        time.sleep(3)

        # Find the password input element and enter the password
        passinp = self.browser.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
        passinp.send_keys(self.password)
        time.sleep(3)

        # Click on the "Log in" button
        self.browser.find_element(by=By.XPATH, value="//span[contains(text(),'Giriş yap')]").click()
        time.sleep(10)
    
    # Method to search for a hashtag and scrape tweets
    def search(self, hashtagKey):
        # Find the search input element, enter the hashtag, and press ENTER
        searchInp = self.browser.find_element(by=By.XPATH, value="//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
        searchInp.send_keys(hashtagKey)
        searchInp.send_keys(Keys.ENTER)
        time.sleep(3)

        # Initialize an empty list to store the tweet texts
        results = []

        # Find all tweet elements and extract their texts
        tweet_elements = self.browser.find_elements(by=By.XPATH, value="//article[@data-testid='tweet']//div[@data-testid='tweetText']")
        time.sleep(3)
        print("Count of initial tweets: " + str(len(tweet_elements)))

        # Loop to scroll and load more tweets until all tweets are scraped
        last_height = self.browser.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            time.sleep(2)
            new_height = self.browser.execute_script("return document.documentElement.scrollHeight")
            if last_height == new_height:
                break
            last_height = new_height

            # Find the updated tweet elements after scrolling and extract their texts
            tweet_elements = self.browser.find_elements(by=By.XPATH, value="//article[@data-testid='tweet']//div[@data-testid='tweetText']")
            time.sleep(1)
            print("Updated count of tweets: " + str(len(tweet_elements)))

            # Append the extracted tweet texts to the results list
            for i in tweet_elements:
                results.append(i.text)

        # Print and write the tweets to a file
        i = 0
        for textt in results:
            print(str(i) + textt)
            i += 1

        count = 1
        with open("tweets.txt", "w", encoding="UTF-8") as file:
            for item in results:
                file.write(f"{count}-{item}\n")
                count += 1

# Usage of the twitter class
# Replace 'username', 'password', and 'username2' with appropriate credentials before running the code
tw = twitter(username, password)
tw.signIn()
tw.search(key)
