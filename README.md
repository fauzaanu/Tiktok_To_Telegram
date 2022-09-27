# TIKTOK TO TELEGRAM
This is a telegram bot that downloads a tiktok video when a link is sent and sends it back to the telegram chat. This is the source code for @tikontgBot
Watermark will be removed now.

# INSTALLATION
```pip install -r requirements.txt```

# USAGE
Replace the value of the string in line 82 to the BOT_TOKEN given by @Botfather

# DEPLOYING THE BOT
@tikontgBot along with 4 other bots are hosted on a small $6 ubuntu server on vultr. To run multiple bots at the same time "screen" is used

### Screen useful commands
Screen : Creates a new screen
Pressing ctrl+A+D : Detaches from the screen (The Bot stays running within that screen)

To later access the detached screen we should be listing all of them and finding the right screen:
Screen -list : Lists all screens

### Access Token Being Visible on Github
Git clone is used to get the code from main pc to the server
Once it is cloned goto @botfather and revoke all tokens
do a nano for the python files and rewrite the tokens


