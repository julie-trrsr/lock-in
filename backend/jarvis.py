import json
from system_prompt import *
from openai import OpenAI
from brain_agent import EEGAgent
from typing import Dict, Any, List, Optional
import time
import base64
from vision import AgentCoordinator

class TopLevelAgent:
    """
    The Top-Level Agent orchestrates the conversation with the OpenAI assistant,
    registering the 'process_image' and 'process_eeg' functions as potential calls.
    After gathering the results, it fuses them into a final summary describing the
    surroundings (from camera data) and potential distractions, along with advice to reduce them.
    """

    def __init__(
        self,
        vision_agent = AgentCoordinator,
        eeg_agent = EEGAgent,
        model_name = MODEL_NAME
    ):
        self.model_name = model_name
        
        self.client = OpenAI()
        self.instructions = jarvis_instructions
        self.eeg_agent_tool_description = eeg_agent_summary
        self.vision_agent_tool_descriptions = vision_agent_summary
        self.eeg_agent = eeg_agent
        self.vision_agent = vision_agent


        
        self.assistant = self.client.beta.assistants.create(
          name = "Jarivs",
          instructions = self.instructions,
          tools=[{"type":"function", "function":self.eeg_agent_tool_description}, {"type" : "function", "function":self.vision_agent_tool_descriptions}],
          model = self.model_name
        )

        self.thread  = self.client.beta.threads.create()


    def run_analysis(self, eeg_data: Dict[str, Any], image_urls) -> str:
      image_files = []
      claude_image_files = []

      for url in image_urls :
        image_file = self.client.files.create(file = open(url, "rb"), purpose="vision")
        image_files.append(image_file)

        image_content = {
          "type": "image",
          "source": {
              "type": "base64",
              "media_type": "image/jpeg",
              "data": base64.standard_b64encode(open(url, 'rb').read()).decode("utf-8")
          }
        }
        claude_image_files.append(image_content)

      full_prompt = jarvis_prompt + f" {eeg_data}"
      full_msg = [{"type" : "text", "content": full_prompt}]

      for image in image_files : 
        full_msg.append({
          "type": "image_file",
          "image_file": {"file_id": image.id}
        })


      self.client.beta.threads.messages.create(
         thread_id = self.thread.id,
         role = "user",
         content = jarvis_prompt
      )

      run = self.client.beta.threads.runs.create_and_poll(
         thread_id = self.thread.id,
         assistant_id=self.assistant.id,
         tool_choice = "required",
         tools = [{"type":"function", "function" : self.eeg_agent_tool_description}, {"type":"function", "function" : self.vision_agent_tool_descriptions}]
      )

      response = None
      while True : 
         
        if run.status == "requires_action" :
          for tool in run.required_action.submit_tool_outputs.tool_calls:
            tool_output = []

            if tool.function.name == "process_eeg_data" :
              eeg_response = self.eeg_agent.process_eeg_data(eeg_data)
              tool_output.append({"tool_call_id" : tool.id, "output" : eeg_response})

            elif tool.function.name == "process_images" :
              image_response = self.vision_agent.process_frame(claude_image_files)
              tool_output.append({"tool_call_id" : tool.id, "output" : image_response})

            else : 
              error_msg = {"error": f"Unknown function '{tool.function.name}'."}
              self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="function",
                name=tool.function.name,
                content=json.dumps(error_msg)
              )

          if tool_output : 
            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
              thread_id=self.thread.id,
              run_id = run.id,
              tool_outputs=tool_output
            )

        elif run.status == "completed" :
          response_id = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
          ).first_id

          response = self.client.beta.threads.messages.retrieve(
             thread_id=self.thread.id,
             message_id=response_id
          )

          break

        elif run.status == "failed" :
          print(run.status)
          print(f"[-] ERROR : {run.last_error} ")
          pass

        
        else :
          print(run.status)
          time.sleep(2)
          pass
          

      return response
