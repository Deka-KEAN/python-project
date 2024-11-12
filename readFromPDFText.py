import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from groq import Groq

# Set up the API key
os.environ["GROQ_API_KEY"] = ""

# Initialize the Groq client
client = Groq()

# Read PDF
pdf_path = "C:/Users/anupd/OneDrive/Desktop/Itinerary.pdf"
pdf_reader = PdfReader(pdf_path)

# Extract text from PDF
raw_text = ''
for page in pdf_reader.pages:
    content = page.extract_text()
    if content:
        raw_text += content

# Split text into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

print(f"Number of text chunks: {len(texts)}")

def ask_question(text, question):
    prompt = f"""
    Answer the following question based ONLY on the information in the given text. 
    If the answer is not in the text, say "The answer is not in the given text."

    Text:
    {text}

    Question: {question}

    Answer:
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a Q&A system. Only use the given text to answer questions.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.2,
        max_tokens=200,
        top_p=1,
        stream=False,
    )
    
    return chat_completion.choices[0].message.content

# Example usage
query = "What is the traveller's name? And From where is the traveller boarding and arriving?"
answers = []

for chunk in texts:
    answer = ask_question(chunk, query)
    if "not in the given text" not in answer.lower():
        answers.append(answer)

if answers:
    print("Answer:", " ".join(answers))
else:
    print("Answer: The information is not found in the document.")