# RedditWallpaperBot
A Bot for Reddit that gets top Hot sorted picture from a given Subreddit and sets it as background. (Windows only currently)

## Prerequisite
* Must have python3.6+ installed.

## Installation:
  * Download the repository by clicking the green "Clone or download" button on the top-right of the repository's main page, then click on "Download ZIP"<br>
  
  * Extract folder to desired location
  
  * With the Reddit account that the bot will use go to Preferences -> Apps and create an app. Pick any name, choose script, and set the redirect url to http://localhost. Description and about url can be blank.

  * In etc/config.ini add your client id and client secret from the app you just created. Client id is the id underneath the name of the app. Client secret is labeled.

<i>(Installing in closed environment)</i>:
  * Install pipenv through pip. <br>
  ` pip install pipenv`
  
  * Open the extracted folder in terminal and run pipenv install. <br>
  ` cd RedditWallpaperBot-master && pipenv install `

 #### Or:
  
 <i>(Installing globally)</i>:
  * Open the extracted folder in terminal and run: <br>
  ` pip install -r requirements.txt `

## Usage:
  ![Usage Demo](https://media.giphy.com/media/Tk0hzmccJ2rLlbRZxT/giphy.gif)
  
  <i>Skip this step if you installed globally </i>
  * Open extracted folder and run: <br>
  ` pipenv shell `
  
  * Run main.py. <br>
  ` python main.py `

  #### Or:

  * Open extracted folder and run main.py script directly by double clicking.
  
