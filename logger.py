import json
import structlog

from config.paths import REPO_DIR

logger = structlog.get_logger()

# Anchored to the repo rather than the CWD so sibling apps append to the same
# log instead of scattering `logs/agent.log` next to whatever directory they
# happened to be started from.
AGENT_LOG_PATH = REPO_DIR / "logs" / "agent.log"

class StreamingAgentLogger:
    def __init__(self):
        self.token_buffer = []
        self.tool_buffer = []
# Testing the commit to github
    def __call__(self, **kwargs):
        """Shared event processor for both async iterators and callback handlers"""
        messages = []
        event = kwargs.get("event", {})

        if event.get("contentBlockStart", False):

            messages.append(f"\n{"".join(self.token_buffer)}")
            self.token_buffer.clear()

            start = event["contentBlockStart"]["start"]
            if "toolUse" in start:
                messages.append(f"\nTool use: {start["toolUse"]["name"]}")

        if event.get("contentBlockStop", False):
            raw = ""
            try:
                raw = "".join(self.tool_buffer)
                parameters = json.loads(raw)
            except Exception as e:
                logger.error(e)
                parameters = raw
            messages.append("\n")
            messages.append(parameters)
            self.tool_buffer.clear()

        if event.get("contentBlockDelta", False):
            delta = event["contentBlockDelta"]["delta"]
            if delta and "text" in delta:
                self.token_buffer.append(delta.get("text"))
            elif delta and "toolUse" in delta:
                if "input" in delta.get("toolUse", {}):
                    self.tool_buffer.append(delta["toolUse"]["input"])

        if messages:
            self.append_to_file(messages)

    def append_to_file(self, messages: list[str]):
        AGENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(AGENT_LOG_PATH, mode="a", encoding="utf-8") as file:
            try:
                for message in messages:
                    file.write(f"{message}")
            except Exception as e:
                logger.error(e)
                file.write(str(e))


streaming_agent_logger = StreamingAgentLogger()
