import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
import os
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


async def download(url, name, watermark=False, original=True, music=False):

    try:
        os.remove("tok.mp4")
    except:
        pass

    tok_link = url
    url = "https://tikwm.com/api/"

    if "tiktok" in tok_link:
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n{tok_link}\r\n-----011000010111000001101001--\r\n"
        headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001",
                   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', }

        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            main_data = response.json()
            water_mark = main_data["data"]["wmplay"]
            no_wm = main_data["data"]["play"]
            music_file = main_data["data"]["music"]

            if watermark:
                download_file = requests.get(water_mark, headers={
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
                with open(f"watermark/{name}.mp4", "wb") as file:
                    file.write(download_file.content)

            if original:
                download_file = requests.get(no_wm, headers={
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
                with open(f"{name}.mp4", "wb") as file:
                    file.write(download_file.content)

            if music:
                download_file = requests.get(music_file, headers={
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
                with open(f"music/{name}.mp3", "wb") as file:
                    file.write(download_file.content)
        else:
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            }
            video_url = url

            page_html = requests.get(video_url, headers=headers)
            main = page_html.content.decode('utf-8')

            startx = main.find('{"url":"')
            # print(startx)
            end = main.find('&mime_type')
            # print(end)

            link = f'{str(main)[startx:end]}'
            link_m = link.replace("u002F", "")
            link_m = link_m.replace('{"url":"', "")
            x = link_m.find("?")
            link_m = link_m[:x]
            link_m = link_m.replace('\\', "/")
            # print(str(link_m))

            link = link.replace('{"url":"', "")

            url = link_m
            downloaded_obj = requests.get(url, headers=headers)

            with open(f"{name}.mp4", "wb") as file:
                file.write(downloaded_obj.content)






logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


# working
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    linkx = update.message.text
    # linkx = update.channel_post.text
    if "tiktok" in linkx:
        #print("before  the async")

        await download(linkx,name="tok")

        # BAD CODE TODO
        try:
            #print("MAIN SEND")
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open("tok.mp4", 'rb'),
                                         supports_streaming=True, caption="", read_timeout=100, write_timeout=100,
                                         connect_timeout=100)
        except Exception as e:
            pass
            # print(f"MAIN SEND E{e}")

        
        os.remove("tok.mp4")
        # os.remove("tok_admin.mp4")


# working part
async def commd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Add me in any group. Make me an Admin & I Will send you viewable tiktoks")


if __name__ == '__main__':
    token = ""
    application = ApplicationBuilder().token(token).build()

    commands = CommandHandler('start', commd)
    links = MessageHandler(filters.TEXT, start)
    # on different commands - answer in Telegram
    application.add_handler(commands)
    application.add_handler(links)

    application.run_polling()
