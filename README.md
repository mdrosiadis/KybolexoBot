# KybolexoBot

A bot for dod.gr game "Κυβόλεξο"

## Requirments

The bot better plays on Chromium-based broswers. You will need the following plugins:

- [Disable CSP](https://chrome.google.com/webstore/detail/disable-content-security/ieelmcmcagommplceebfedjlakkhpden) (to allow foreign JS)
- A Javascript Injection plugin like [Scripy](https://chrome.google.com/webstore/detail/scripty-javascript-inject/milkbiaeapddfnpenedfgbfdacpbcbam)

## Installing

- Download the bot using git.
	```sh
	$ git clone https://github.com/mdrosiadis/KybolexoBot
	$ cd KybolexoBot
	```

- Install dependencies using pip.
	```sh
	$ pip3 install -r requirments.txt
	```

- Set your Javascript injector to run ``game_parser.js``

## Using the bot

You need to let the bot source the wordlist and create
the internal data structure before attempting a connection from
the client.

Follow these steps.

1. Run the bot worker: 
	```sh
	$ python3 main.py
	```
2. Wait for a response from the bot. It should look like this:
	```
	Playing with 655635 words (1104573 nodes)
	```
3. Login to [Dod Games](https://www.dod.gr/).
4. Run the client code using your Javascript injector.
5. Enjoy!

## Controls

While playing, click on **Εύρεση λύσεων** to find the best words for the current board.
The bot will highlight the letters required to play the best word.
You can change the word being displayed by clicking the word you want to use from the list of
recomended ones.

Use **Q** to step through the letters of the selected word.

Use **Ctrl-Space** to toggle the bot display.

## Notes

The bot (for the time being) will not account for scores, or potentially allowing the opponent
a winning word, by revealling letters.

The bot may recommend words not supported by Dod Games. Use an other word in that case.

## Disclaimer

This is just a toy, made for entertainment purposes.

**DO NOT** use this bot to bully online players.


