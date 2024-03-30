# https://platform.openai.com/docs/assistants/overview?context=with-streaming

from typing_extensions import override
from openai import AssistantEventHandler
from openai import OpenAI
from . import tools

dispatcher = {
    'get_menu': tools.get_menu,
    'place_order': tools.place_order,
    'get_feedback': tools.get_feedback,
    'submit_feedback': tools.submit_feedback,
    'get_inventory': tools.get_inventory,
    'restock_item': tools.restock_item,
    'submit_report': tools.submit_report
}

def run_function(name, *args):
	"""
	Runs a function based on the provided name with the given arguments.

	Parameters:
		name (str): The name of the function to be executed.
		*args: Variable length argument list.

	Returns:
		The result of the executed function.

	Raises:
		ValueError: If the provided name is not a valid function name.
	"""

	try:

		function = dispatcher[name]
		return function(*args)
	
	except KeyError:

		raise ValueError('Invalid input')

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.


class EventHandler(AssistantEventHandler):   

  output = None

  @override
  def on_text_created(self, text) -> None:
    print(f"\nScoopy: ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
 