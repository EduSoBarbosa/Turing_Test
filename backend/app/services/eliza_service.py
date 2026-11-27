from nltk.chat.eliza import eliza_chatbot

from app.services.base_chatbot import Reply


class Eliza:
    def reply(self, experiment, history, prompt):
        # Match NLTK Chat.converse's handling of trailing punctuation.
        text = history[-1].content.rstrip("!.")
        return Reply(eliza_chatbot.respond(text))
