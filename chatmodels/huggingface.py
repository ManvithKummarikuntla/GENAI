from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.3-70B-Instruct"
)

model=ChatHuggingFace(llm=llm)
response = model.invoke("Who are you?")
print(response.content)