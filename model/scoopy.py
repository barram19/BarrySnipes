import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
from .utils import EventHandler, run_function

load_dotenv()


openai = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

class Scoopy:
    def __init__(self):
        self.assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

    def create_thread(self):
        return openai.beta.threads.create().id
    
    def process_function(self, stream, thread_id):
        outputs = []

        required_action = stream.current_run.required_action.submit_tool_outputs.tool_calls[0]
    
        # Get the function name and arguments
        function_name = required_action.function.name
        arguments = list(json.loads(required_action.function.arguments).values())
        
        # Call the function
        output = run_function(function_name, *arguments)

        outputs.append({"tool_call_id" : required_action.id, "output" : output})

        with openai.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=thread_id,
            run_id=stream.current_run.id,
            tool_outputs=outputs,
            event_handler=EventHandler()
        ) as stream2:
            
            stream2.until_done()

            if stream2.current_run.status == "requires_action":
                self.process_function(stream2, thread_id)   

    def query(self, input: str, thread_id = None, sample = False) -> list:

        if sample:
            answer = "Not sure about that, ask me something else!"
            return answer
        
        if not thread_id:
            thread_id = self.create_thread()

        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=input
        )
        
        with openai.beta.threads.runs.create_and_stream(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(),
            ) as stream:
            
            stream.until_done()

            if stream.current_run.status == "requires_action":
                self.process_function(stream, thread_id)

        return None