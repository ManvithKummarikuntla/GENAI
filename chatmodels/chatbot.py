from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

llm=ChatGroq(model="openai/gpt-oss-20b")

print("choose your AI model")
print("press 1 for teacher mode")
print("press 2 for funny mode")

choice=int(input(" tell me your response :- "))

if choice==1:
    mode = "You are a teaching agent and you need to reply responsiblily"
elif choice == 2:
    mode = "You are a funny agent can give reply in funny way"

messages=[
    SystemMessage(content=mode)

]

print("-------------Welcome type 0 to exit--------------")
while True:
    
    prompt=input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))

    print("BOT: ",response.content)

print(messages)