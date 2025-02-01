import openai
import json
from system_prompt import *
from openai import OpenAI
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
        vision_agent: VisionAgent,
        model_name: str = "gpt-4-0613"
    ):
        self.vision_agent = vision_agent
        self.eeg_agent = eeg_agent
        self.model_name = model_name

        # Prepare the function schemas for the ChatCompletion call
        self.functions = [
            self.vision_agent.get_function_schema(),
            self.eeg_agent.get_function_schema()
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
        """
        Main entry point:
          1. Provide instructions to the assistant about the context.
          2. Let the assistant decide (via function calling) when to call EEG or Vision analysis.
          3. We intercept function calls, run the actual logic, and feed the results back.
          4. Finally, ask for a fused summary about the person's surroundings, distractions, and how to reduce them.
        """

        # Initial system + user messages to set the stage.
        system_msg = (
            "You are a top-level orchestrator that can analyze EEG data and images "
            "to determine potential distractions. You have two callable functions: "
            "'process_image' for image data, and 'process_eeg' for EEG data. "
            "When you're ready, call these functions to get the information you need."
        )
        user_msg = (
            "Here's the scenario: We have EEG data and some images captured "
            "during a time when a person's focus dropped. Please analyze them."
        )

        self._append_message("system", system_msg)
        self._append_message("user", user_msg)

        # 1) We'll make a single call letting the model know it can call the specialized functions.
        #    But in a realistic scenario, you might loop until the model stops calling functions.
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.messages,
            functions=self.functions,
            function_call="auto"
        )

        first_msg = response["choices"][0]["message"]

        # If the model attempts a function call, we handle it here.
        # We do this for both the EEG and image calls. We'll demonstrate a single iteration,
        # but in a real system, you could loop until no more function calls occur.
        if "function_call" in first_msg:
            fc = first_msg["function_call"]
            func_name = fc["name"]
            args = json.loads(fc["arguments"])

            # If it's the EEG function
            if func_name == "process_eeg":
                # Actually run the EEG agent
                eeg_result = self.eeg_agent.process_eeg(args["eeg_data"])
                # Provide that result back to the conversation
                self._append_message("function", eeg_result, name="process_eeg")

            elif func_name == "process_image":
                # Actually run the vision agent
                image_result = self.vision_agent.process_image(args["image_path"])
                # Provide that result back to the conversation
                self._append_message("function", image_result, name="process_image")

        # In practice, the model may want to call the other function as well, or call multiple times
        # (one for each image). We'll do it manually for demonstration:
        # Let's forcibly provide the image paths by "role=user" so the model might call process_image:

        # Next step: Provide the EEG data and image paths in the conversation. 
        # The model can decide to call the relevant function again.
        self._append_message(
            "user",
            f"EEG data:\n{json.dumps(eeg_data, indent=2)}\n"
            f"Image paths: {image_paths}\n"
            "Use your available functions to analyze them. Then summarize."
        )

        # Another ChatCompletion call. The model might call the functions again if needed.
        response2 = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.messages,
            functions=self.functions,
            function_call="auto"
        )
        second_msg = response2["choices"][0]["message"]

        if "function_call" in second_msg:
            fc2 = second_msg["function_call"]
            func_name2 = fc2["name"]
            args2 = json.loads(fc2["arguments"])

            if func_name2 == "process_eeg":
                result = self.eeg_agent.process_eeg(args2["eeg_data"])
                self._append_message("function", result, name="process_eeg")
            elif func_name2 == "process_image":
                result = self.vision_agent.process_image(args2["image_path"])
                self._append_message("function", result, name="process_image")
                
            # ... potentially more calls if the model tries to analyze each image separately.

        # After all function calls are done, we ask for the fused final summary:
        self._append_message(
            "user",
            "Now that you have the EEG analysis and image analysis, "
            "please provide a final summary of the person's surroundings, "
            "what might be distracting them, and how to reduce those distractions."
        )

        final_response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.messages
        )

        final_text = final_response["choices"][0]["message"]["content"]
        return final_text