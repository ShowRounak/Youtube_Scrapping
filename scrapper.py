from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import logging

logging.basicConfig(filename="scrapper.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

#load_dotenv()
API_KEY = "AIzaSyCWjOqPt0_sxoErum-BegpDwViqhRFh5u0"
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=API_KEY)


class YouTube():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def total_videos(self, c_url):
        """This Method Scraps total number of videos uploaded by a channel"""
        try:
            self.driver.get(c_url)
            content = self.driver.page_source.encode('utf-8').strip()
            self.soup = BeautifulSoup(content, 'html.parser')
            logging.info("Scrapping successful")
            print("Scrapping successful")
            self.driver.quit()
            number = self.soup.find('span', class_='style-scope yt-formatted-string')
            num = number.text
            logging.info("Returning total no. of videos")
            return num
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred", e)

    def comment_threads(self, video_id):
        """This method scraps all comments from a YouTube video"""
        try:
            reply = []
            comments_list = []
            request = youtube.commentThreads().list(part="id, snippet", videoId=video_id)
            response = request.execute()
            comments_list.append(response)
            total_comments = len(comments_list[0]['items'])
            logging.info("Comments fetched")
            print(f"A total {total_comments} comments has been fetched")
            for i in range(len(comments_list[0]['items'])):
                person = comments_list[0]['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment = comments_list[0]['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
                temp_dict = {"Person":person,"Comment":comment}
                reply.append(temp_dict)
            return reply
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred", e)

    def video_description(self, v_url):
        """This Method returns all details of a YouTube video"""
        try:
            self.driver.get(v_url)
            showmore = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-button[id='expand']")))
            showmore.click()
            content = self.driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, 'html.parser')
            self.driver.quit()
            titles_views = soup.findAll('yt-formatted-string', class_='style-scope ytd-watch-metadata')
            title = titles_views[1].text
            view = titles_views[2].text
            view = view.split(" ")[0:2]
            view = ' '.join(view)
            likes = soup.findAll('span', class_='yt-core-attributed-string yt-core-attributed-string--white-space-no-wrap')
            like = likes[4].text
            description = soup.findAll('div', class_='item style-scope ytd-watch-metadata')
            text = description[2].text
            text = text.split('\n')[9:]
            text = '\n'.join(text)

            mydict = {"TITLE": title, "VIEWS": view, "LIKES": like, "DESCRIPTION": text}
            logging.info("Returning dictionary of video details")
            return mydict
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred", e)


