# SupBot


A buy bot made for the supereme website. Made back in 2019 probably doe snot work anyone. Adding it to my gihub for archival reasons.

Made By: lejara

## How to Compile

Version 1.1+ : pyinstaller --onefile SupBot.py

	To folder dist:

		1. Transfer PoxyBypass Folder

		2. Transfer mitmproxy-ca-cert.p12

		3. chromedriver.exe

## 3rd Party Projects Used

### Python Libs

- beautifulsoup4

- requests

- selenium

- pillow

- tkinter

- html5lib

- lxml

- cryptography

### External Libs

- mitmproxy

## Initial Setup

0. Install https://mitmproxy.org/ if not done so

1. Run SupBot.exe and select no to options

2. Close SupBot.exe

3. Fill out CategoriesFilter.json

4. Fill out InstaBuyKeywords.json

5. Fill out Info.json with your info

6. Run Bot and Encrypt Info.json (enter 'y'). (Key will be stored in en.json. When rerunning the bot will load the key of whats in en.json)

## Running

1. Install mitmproxy-ca-cert cert (make sure to remove this cert when you are finish)

	- current user

	- leave password empty

	- Place certificate in store Trusted Root certification Authorities

2. Run the run.bat

3. Select options

4. Cross fingers / When done REMOVE the mitmproxy-ca-cert.p12 certificate!

## Encryption Notice!

Make sure you store the key in 'en.json' somewhere safe

## Options

InstaBuy = Will skip the forum selection, and go straight to buying if item name matches a keyword in InstaBuyKeywords.json.

		Note: Only the defualt options will be selected when buying

## Decision Flow Order

This is the order of checks the item go through, before checking out

1. Check Category

-- When Category passes --

2. Spawn new process for that item

-- Populate Additional Info Is loaded To Item Object --

3. Check if not sold out

4. Check if can InstaBuy ---> Goes straight to the buying phase, if not sold out

-- If sold out and can InstaBuy ---

5. Loop check if item is no longer sold out ---> go straight to the buying phase
