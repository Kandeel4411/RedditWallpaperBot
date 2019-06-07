# :sparkler: RedditWallpaperBot :crystal_ball:
A Bot for Reddit that gets top Hot sorted picture from a given Subreddit and sets it as background.


## Supported OS & Environments
 Windows, Mac and Linux(Ubuntu, Linux Mint)
 
 
## Prerequisite
* Must have python3.6+ installed.


## Installation: :hammer:

  * Download the repository by clicking the green "Clone or download" button on the top-right of the repository's main page, then click on "Download ZIP"<br>
  
  * Extract folder to desired location
  
  * With the Reddit account that the bot will use go to Preferences -> Apps and create an app. Pick any name, choose script, and set the redirect url to http://localhost. Description and about url can be blank.
  
  i.e: ![Reddit App preferences](assets/redditClientCredentials.png)
  
  * In etc/config.ini add your client id and client secret from the app you just created. Client id is the id underneath the name of the app. Client secret is labeled.
  
  * Choose one of the following methods:
    - *Installing in closed environment (Recommended)*:
      - Install pipenv through pip. <br>
      ` pip install pipenv`
      
      - Open the extracted folder in terminal and run pipenv install. <br>
      ` cd RedditWallpaperBot-master && pipenv install `
    - *Installing globally*:
        - Open the extracted folder in terminal and run: <br>
        ` pip install -r requirements.txt `



## Usage:
  ![Usage Demo](assets/giphy.gif)
  
  <i>Skip this step if you installed globally </i>
  * Open extracted folder and run: <br>
  ` pipenv shell `
  
  * Run main.py. <br>
  ` python main.py `

  #### Or:

  * Open extracted folder and run main.py script directly by double clicking.
  <br>
  
## Running the tests: :wrench:


Tests are written using the [pytest](https://github.com/pytest-dev/pytest) framework. <br>

Open terminal and navigate to the project directory
* If you installed globally run:<br>
`pytest`

* If you installed using the pipenv method:<br>
    - Run the following command to install pytest:<br>
     ` pipenv install --dev` 
    - Close and re-open the terminal to the project directory and run:<br>
     `pytest`


## Importing: :package:

*  *Notes:*
If you want to import the bot functions, it by default uses sys.exit() to exit program once an error has been caught. You may want to use bot.raise_bot_exception(option=True) to raise BotExceptions instead that you can catch.



### Acknowledgement:
   * [Wallie](https://github.com/Dextroz/Wallie) for Mac support.

### License:
   * [MIT](https://github.com/Kandeel4411/RedditWallpaperBot/LICENSE)
