from collections import deque
from threading import Lock
from time import monotonic

import httpx
from google import genai
from google.genai import errors, types

from app.services.base_chatbot import ChatbotError, Reply


class Gemini:
    def __init__(self, settings):
        self.client = None
        self.settings = settings
        self.requests = deque()
        self.lock = Lock()

    def close(self):
        if self.client is not None:
            self.client.close()

    def _reserve_request(self):
        with self.lock:
            now = monotonic()
            while self.requests and self.requests[0] <= now - 60:
                self.requests.popleft()
            if len(self.requests) >= self.settings.gemini_requests_per_minute:
                raise ChatbotError(429, "The conversation service is busy. Try again later.")
            if self.client is None:
                self.client = genai.Client(
                    api_key=self.settings.gemini_api_key.get_secret_value(),
                    vertexai=False,
                    http_options=types.HttpOptions(
                        timeout=int(self.settings.gemini_timeout_seconds * 1000),
                        retry_options=types.HttpRetryOptions(attempts=1),
                    ),
                )
            self.requests.append(now)

    def reply(self, experiment, history, prompt):
        if not self.settings.gemini_enabled:
            raise ChatbotError(503, "The conversation service is temporarily unavailable.")
        contents = [
            types.Content(
                role="user" if item.role == "user" else "model",
                parts=[types.Part(text=item.content)],
            )
            for item in history
        ]
        try:
            self._reserve_request()
            response = self.client.models.generate_content(
                model=experiment.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=prompt,
                    temperature=experiment.temperature,
                    top_p=experiment.top_p,
                    max_output_tokens=experiment.max_output_tokens,
                    candidate_count=1,
                ),
            )
        except (httpx.TimeoutException, TimeoutError):
            raise ChatbotError(504, "The conversation service timed out. Try again.") from None
        except (errors.APIError, httpx.HTTPError):
            raise ChatbotError(502, "The conversation service could not respond. Try again.") from None

        content = (response.text or "").strip()
        if not content:
            raise ChatbotError(502, "The conversation service returned no text. Try again.")
        usage = response.usage_metadata
        return Reply(
            content,
            usage.prompt_token_count if usage else None,
            usage.candidates_token_count if usage else None,
        )
