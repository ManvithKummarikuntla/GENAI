from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

model=ChatGroq(model="openai/gpt-oss-20b")

#single line prompt we cannot do this way for all the problems so 
#we comment the response 
###response=model.invoke("Set against the gritty backdrop of a Godavari coal-mining village named Veerlapally, Dasara is a raw and explosive tale of friendship, loyalty, and fierce retribution. The story follows Dharani—a local youth living in the dust and sweat of the coal fields—whose life is upended when a violent political and social conflict shatters his world. Driven by raw Telangana dialect, unfiltered local culture, and deep-seated rage against caste and power imbalances, a small personal clash among friends spirals rapidly into a massive, blood-soaked battle for survival and justice. Can you please extract the summary and information of the movie")


prompt=ChatPromptTemplate.from_messages(([
    ("system",
     """You are an information-extraction assistant for a movie database.
Read the paragraph the user gives and extract useful details about the movie.

Rules:
- Use ONLY information present in the paragraph. Do not add outside knowledge.
- If a detail is not mentioned, write "Not mentioned". Do not guess.
- Ignore any links or markdown; use the plain movie title.
- Keep proper nouns spelled exactly as written.

Return the answer in this format:

Movie Name:
Genre(s):
Tone / Mood:
Language / Dialect:
Setting (place & time):
Cast (actor - character):
Main Characters:
Director / Writer / Producer / Music:
Release Year:
Themes:
Central Conflict:
Key Plot Points:
Quick Summary (max 2 sentences):"""),
    ("human", "Paragraph:\n{paragraph}"),
]))

para = input("Give your paragraph")

final_prompt=prompt.invoke(
    {"paragraph":para }
)

response= model.invoke(final_prompt)

print(response.content)