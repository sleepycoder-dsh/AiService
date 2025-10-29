from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
# Try the canonical langchain import first, then fall back to the separate package
try:
    from langchain.sql_database import SQLDatabase
except Exception:
    try:
        from langchain_sql_database import SQLDatabase
    except Exception:
        # If neither import is available, set a placeholder to avoid import-time crashes;
        # attempting to use SQLDatabase later will raise a clearer error.
        SQLDatabase = None
from langchain.chains import SQLDatabaseChain
import os

app = FastAPI()

# ✅ Set your OpenAI API key (best to use environment variables in real projects)
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"

# ✅ Connect to PostgreSQL
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/bookreviewdb")

# ✅ Create chatbot using LangChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
def chat_with_ai(msg: ChatMessage):
    response = db_chain.run(msg.message)
    return {"reply": response}
