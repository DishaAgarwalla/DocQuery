# 📄 DocQuery - Intelligent Document QA System


**DocQuery** is an intelligent document question-answering system that allows users to upload PDF documents and ask questions in natural language. The system uses advanced NLP techniques to provide accurate answers with page citations.

## ✨ Features

- 📚 **PDF Upload & Processing** - Upload multiple PDF documents
- 🤖 **AI-Powered Answers** - Uses FLAN-T5 for accurate responses
- 📍 **Page Citations** - Answers include exact page numbers
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📋 **Copy Answers** - One-click copy to clipboard
- 📥 **Export Q&A** - Save conversations as text files
- 💡 **Question Suggestions** - AI-generated follow-up questions
- 📊 **Document Comparison** - Compare answers across documents

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyPDF
- **Text Chunking**: LangChain
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **LLM**: FLAN-T5-small


## 📦 Installation (Local)

```bash
git clone https://github.com/DishaAgarwalla/DocQuery.git
cd DocQuery
pip install -r requirements.txt
streamlit run streamlit_app.py
