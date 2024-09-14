import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

dimension = 384  
index = faiss.IndexFlatL2(dimension)

document = "Jio AI-Cloud Welcome Offer: Reliance has announced the Jio AI-Cloud Welcome Offer to be launched this Diwali, providing up to 100 GB of free cloud storage for Jio users. The initiative aligns with the vision of 'AI Everywhere For Everyone' and includes features like Jio TvOS, Jio Home IoT, Jio TV+, and Jio Phonecall AI."

embedding = model.encode([document])

embedding = np.array(embedding).astype('float32')
index.add(embedding)

print("Document added to FAISS.")

def get_faiss_index():
    return index

def get_model():
    return model

def add_document_to_index(document: str):
    embedding = model.encode([document])
    embedding = np.array(embedding).astype('float32')
    
    index.add(embedding)
    print("Document added to FAISS.")

    print(f"Number of documents in FAISS index: {index.ntotal}")