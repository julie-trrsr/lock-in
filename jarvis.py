import openai
import json
from system_prompt import *
from openai import OpenAI
MODEL_NAME = "claude-3-sonnet-20240229"
from brain_agent import EEGAgent
from typing import Dict, Any, List, Optional

class TopLevelAgent:
    """
    The Top-Level Agent orchestrates the conversation with the OpenAI assistant,
    registering the 'process_image' and 'process_eeg' functions as potential calls.
    After gathering the results, it fuses them into a final summary describing the
    surroundings (from camera data) and potential distractions, along with advice to reduce them.
    """

    def __init__(
        self,
        eeg_agent = EEGAgent,
    ):
        self.client = OpenAI()
        self.assistant = self.client.
        self.model_name = MODEL_NAME
        self.eeg_agent = eeg_agent

        # Prepare the function schemas for the ChatCompletion call
        self.tool_descriptions = [
            self.eeg_agent.get_function_schema(),
        ]

        # We'll maintain a running conversation log:
        self.messages: List[Dict[str, Any]] = []

    def _append_message(self, role: str, content: str, name: Optional[str] = None):
        """
        Helper to append messages to the conversation log.
        """
        if name:
            self.messages.append({"role": role, "name": name, "content": content})
        else:
            self.messages.append({"role": role, "content": content})

    def run_analysis(self, eeg_data: Dict[str, Any], image_paths: List[str]) -> str:
