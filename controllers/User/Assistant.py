import datetime
import wikipedia
from fastapi import Request
import urllib.parse

wikipedia.set_lang("en")


class AssistantController:

    WAKE_WORDS = ["hey sonu", "hi sonu", "hello sonu"]

    @staticmethod
    async def assistant_page(request: Request):

        from helpers.views import user
        import time

        return user("assistant", {
            "request": request,
            "title": "AI Assistant",
            "time": int(time.time())
        })

    @staticmethod
    async def process_command(command: str):

        if not command:
            return {"type": "text", "message": ""}

        command = command.lower().strip()

        wake = None
        for w in AssistantController.WAKE_WORDS:
            if command.startswith(w):
                wake = w
                break

        if not wake:
            return {"type": "text", "message": ""}

        command = command.replace(wake, "", 1).strip()

        if command == "":
            return {"type": "text", "message": "Yes, I am listening."}

        # logout
        if "logout" in command:
            return {"type": "redirect", "url": "/logout"}

        # dashboard
        if "dashboard" in command:
            return {"type": "redirect", "url": "/dashboard"}

        # time
        if "time" in command:

            now = datetime.datetime.now().strftime("%I:%M %p")

            return {
                "type": "text",
                "message": f"The time is {now}"
            }

        # date
        if "date" in command:

            today = datetime.date.today().strftime("%B %d %Y")

            return {
                "type": "text",
                "message": f"Today is {today}"
            }

        # play youtube
        if "play" in command:

            song = command.replace("play", "").strip()

            if song:

                query = urllib.parse.quote(song)

                url = f"https://www.youtube.com/results?search_query={query}"

                return {
                    "type": "youtube",
                    "url": url,
                    "message": f"Playing {song} on YouTube"
                }

            return {
                "type": "text",
                "message": "Please tell the song name"
            }

        # wikipedia
        if "who is" in command or "what is" in command:

            query = command.replace("who is","").replace("what is","").strip()

            try:

                info = wikipedia.summary(query, sentences=1)

                return {
                    "type": "text",
                    "message": info
                }

            except:

                return {
                    "type": "text",
                    "message": "I could not find information"
                }

        return {
            "type": "text",
            "message": "Sorry I did not understand"
        }