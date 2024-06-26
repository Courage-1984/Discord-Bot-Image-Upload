# Discord-Bot-Image-Upload
A Script/Bot to upload local files (like images, gifs and videos) to a Discord server channel.

**This bot/script recursively looks for files in a directory, adds them all to a list, sorts that list in `chronological order` based on `Date modified` and then sends the files in that order and then the sent file's name gets added to a log file. It also checks a log file (if it already exists) for if a file to be sent has already been sent on the channel and then skips that file if it has already been sent and sends files that have not been sent.**

See 'lol.py' for script.

Steps:

1. Download the [lol.py](https://github.com/Courage-1984/Discord-Bot-Image-Upload/blob/main/lol.py) script in the repo above.
2. Create a folder to put the `lol.py` script in.
3. Open a terminal in that folder location.
4. In that terminal run the following:
```sh
  pip install discord.py
```

4. Now edit the `lol.py` script and add the needed values being `Discord bot token`, `server ID`, `channel ID` and `folder location of files`.

**See the following:**

- [How to Get Your Discord Bot Token](https://www.youtube.com/watch?v=aI4OmIbkJH8)

OR:

![dc bot token](https://github.com/Courage-1984/Discord-Bot-Image-Upload/assets/18268669/c095f6ef-5c1c-42fb-be68-5b1221d24c8d)


- [How to Get Server ID, Channel ID, User ID in Discord - Copy ID's](https://www.youtube.com/watch?v=NLWtSHWKbAI)

6. Navigate to [https://discord.com/developers/applications](https://discord.com/developers/applications) and click on your application.
7. Click on the `Bot` option in the left navbar and make sure to enable the following: `Presence Intent`, `Server Members Intent` and `Message Content Intent`.
8. Now click on the `OAuth2` option in the left navbar and copy the `Client ID`.
9. Now open [https://discordapi.com/permissions.html](https://discordapi.com/permissions.html) in a new browser tab.
10. Tick the boxes next to: `Administrator`, `Manage Messages`, `Manage Channels`, `Manage Events`, `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Manage Server`, `View Channels` and `Manage Server`.
11. Now paste your `Client ID` that you copied in the `Client ID:` field at the bottom of the page.
12. Now click on the link provided at the way bottom of the page.
13. Add your bot/application to your chosen server.
14. Click Continue.
15. Now in the terminal that's in the directory which has your `lol.py` script run the following to excecute the script/bot:
```sh
  python lol.py
```

16. Wait a min for bot to start up and connect.

17. In your chosen channel send the following command:
 
```sh
  !send_files
```

18. Now your script/bot should run smoothly and send all the files in the directory you provided while skipping files that was already sent in the channel.

**PS:**

`Discord bot token`, `server ID` and `folder location of files` should all be enclosed in single qoutations while:

`channel ID` should not be enclosed in qoutations at all.

***

SOURCES:

[Make Your Own Discord Bot | Basics (2019)](https://youtu.be/X_qg0Ut9nU8?si=oq4HbnQi2ZFmS0Lx)
