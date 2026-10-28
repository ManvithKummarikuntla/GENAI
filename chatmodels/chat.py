from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()


model = ChatOpenRouter(model="nvidia/nemotron-3.5-lightning:free",temperature=0.9)

response=model.invoke("write a poem on ai")

print(response.content)
