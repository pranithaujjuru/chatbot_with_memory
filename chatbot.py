import os
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"]="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"
os.environ["LANGSMITH_PROJECT"]="pr-charming-pegboard-92"
os.environ["GOOGLE_API_KEY"]="AIzaSyD_-adCvC_JQNPtWXo8BR_Ftnu6aKbKXh4"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
import warnings
warnings.filterwarnings("ignore")

model=ChatGoogleGenerativeAI(model="gemini-1.5-pro-001",convert_system_message_to_human=True)
parser=StrOutputParser()

store={}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]

config={"configurable":{"session_id":"first_chats"}}

prompt=ChatPromptTemplate(
    [
        ("system","you are an helpful assistant. give answers as best as you can",),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
trimmer=trim_messages(
    max_tokens=400,
    strategy='last',
    token_counter=model,
    allow_partial=False,
    include_system=True,
    start_on="human",

)
chain=(
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
    | prompt
    | model
        )
messages = []
def get_bot_response(user_input: str) -> str:
    global messages
    response = chain.invoke({
        "messages": messages + [HumanMessage(content=user_input)],
        "language": "english"
    },
    config=config)
    messages.append(HumanMessage(content=user_input))
    messages.append(AIMessage(content=response.content))

    return response.content
print(messages)


