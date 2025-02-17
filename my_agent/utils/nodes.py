from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode
from langchain.chat_models.fake import FakeListChatModel

responses = [
    "Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
llm = FakeListChatModel(responses=responses)


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    print(f"Creating model: {model_name}")
    if model_name == "openai":
        # model = ChatOpenAI(temperature=0, model_name="Qwen2.5-14B",
        #                    base_url="http://192.168.4.128:4000/v1", api_key="sk-1234")
        model = llm
    elif model_name == "anthropic":
        # model = ChatOpenAI(temperature=0, model_name="Qwen2.5-14B",
        #                    base_url="http://192.168.4.128:4000/v1", api_key="sk-1234")
        model = llm
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    # model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


system_prompt = """Be a helpful assistant"""

# Define the function that calls the model


def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "anthropic")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
tool_node = ToolNode(tools)
