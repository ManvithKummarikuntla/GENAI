from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

embedder = HuggingFaceEmbeddings(
    model_name="thenlper/gte-small"
)

vector = embedder.embed_query("""
HF Hub unauthenticated warning: Optional for public models; a Hugging Face token can provide higher rate limits.



Windows symlink warning: Not fatal. The cache works, but may use more disk space.



Missing pytorch_model.bin error: The actual failure. The selected repository doesnt provide the model weights in the format your current loader expects.
""")

print("Embedding dimensions:", len(vector))
print(vector)
