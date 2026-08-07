# AI Codebase Assistant

## Authors
Dee Aein

## 1. Overview

AI Codebase Assistant is a Retrieval-Augmented Generation (RAG) application designed to help developers understand public GitHub repositories.

Users provide the URL of a public GitHub repository, and the system ingests its source code and documentation, divides supported files like .py, .java, .json, etc. into searchable chunks, generates vector embeddings, and stores the resulting data in PostgreSQL with pgvector.

When a user asks a question about an ingested repository, the system performs semantic similarity search to retrieve the most relevant 10 code chunks. These chunks are provided to an LLM as grounded repository context, along with the user's question, allowing the system to generate answers based on the actual codebase rather than unsupported model knowledge.

Each retrieved chunk preserves source metadata such as its file path and line range, allowing generated answers to include verifiable citations.

---

## 2. Features

- Ingest public GitHub repositories from a repository URL
- Retrieve repository information and the latest commit SHA
- Download repository source code as a ZIP archive
- Extract repositories into temporary storage for processing
- Recursively discover repository files
- Filter unsupported, generated, secret, oversized, and dependency files
- Read supported source files as text
- Split each file into searchable chunks
- Preserve metadata for each chunk, including:
  - File path
  - Start line number
  - End line number
  - Function name
  - Class name
  - Chunk type
  - Chunk code context 
- Generate vector embeddings using Sentence Transformers
- Store embeddings using PostgreSQL and pgvector
- Perform semantic similarity search using cosine distance
- Restrict searches to the selected repository
- Generate grounded answers using an LLM
- Return file paths and exact line-number citations
- Browse previously ingested repositories
- Ask repository-specific questions through a web interface
- Display structured answers and retrieved sources
- Preserve both Flask and FastAPI backend implementations

---

## 3. How It Works

1. The user submits the URL of a public GitHub repository.
2. The backend validates and parses the repository URL.
3. The system verifies that the repository exists and is publicly accessible.
4. Repository metadata and the latest commit SHA are retrieved.
5. The repository archive is downloaded from GitHub.
6. The archive is extracted into a temporary directory.
7. The system recursively discovers repository files.
8. Unsupported or unnecessary files are filtered out.
9. Supported files are read as UTF-8 text.
10. Each file is divided into searchable chunks.
11. Metadata is attached to each chunk.
12. Searchable chunk text is converted into a vector embedding.
13. Repository, file, chunk, metadata, and embedding information is stored in PostgreSQL.
14. The user selects an ingested repository and submits a question.
15. The question is converted into an embedding using the same embedding model.
16. pgvector performs semantic similarity search against chunks belonging to the selected repository.
17. The most relevant chunks are retrieved.
18. Retrieved chunks are formatted into structured context.
19. The context and question are sent to the LLM.
20. The LLM generates an answer using only the supplied repository context.
21. The system returns the answer along with source file paths and exact stored line ranges.

---

## 4. Tech Stack

### Backend

The backend and RAG system were implemented end-to-end using: 

- Python
- Flask
- FastAPI (currently not used)
- SQLAlchemy
- Pydantic
- Alembic

Flask is currently used as the primary backend for the project demo and grading environment.

FastAPI is preserved as an alternative API layer while sharing the same underlying application logic. (I wanted to learn how to use FastAPI)

### Database

- PostgreSQL
- pgvector

PostgreSQL stores repository metadata, file metadata, chunks, and vector embeddings.

pgvector provides vector similarity search directly inside PostgreSQL.

### AI / Machine Learning

- Sentence Transformers
- OpenAI Responses API
- Retrieval-Augmented Generation (RAG)
- Vector embeddings
- Semantic similarity search
- Cosine-distance retrieval

### Data Visualization

- Matplotlib

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Motion

**Note:** The frontend was integrated with the backend but was not part of my primary implementation work except the data visualization part.
---

## 5. Architecture / RAG Pipeline

The application contains two major pipelines:

1. Repository ingestion
2. Repository question answering

### Repository Ingestion Pipeline

```text
GitHub Repository URL
        |
        v
Repository Validation
        |
        v
Latest Commit SHA
        |
        v
Download Repository ZIP
        |
        v
Extract Repository
        |
        v
Discover Files
        |
        v
Filter Unsupported Files
        |
        v
Read Source Files
        |
        v
Create File Records
        |
        v
Chunk File Content
        |
        v
Build Searchable Text
        |
        v
Generate Embeddings
        |
        v
PostgreSQL + pgvector
````

### Question Answering Pipeline

```text
User Question
      |
      v
Question Embedding
      |
      v
pgvector Semantic Search
      |
      v
Top 10 Relevant Repository Chunks
      |
      v
Structured LLM Context
      |
      v
OpenAI LLM
      |
      v
Grounded Answer
      |
      v
File + Line Citations
```

Semantic retrieval is repository-specific, preventing chunks from unrelated repositories from being included in the search.

Retrieved chunks are ordered using pgvector cosine distance, where a smaller distance represents greater semantic similarity.

---

## 6. Project Structure

```text
project-root/
|
├── alembic/
|   └── Alembic database migrations
|
├── crud/
|   └── Database CRUD and semantic-search operations
|
├── frontend/
|   └── React + TypeScript frontend
|
├── models/
|   └── SQLAlchemy ORM models
|
├── routers/
|   ├── fastapi/
|   |   ├── repositories.py
|   |   └── questions.py
|   |
|   └── flask/
|       ├── repositories.py
|       └── questions.py
|
├── schemas/
|   └── Pydantic request and response schemas
|
├── services/
|   ├── file_processing/
|   |   └── File discovery, filtering, and reading logic
|   |
|   ├── github/
|   |   ├── archive.py
|   |   ├── client.py
|   |   └── url_validation.py
|   |
|   ├── answer_question.py
|   ├── chunk_service.py
|   ├── embedding.py
|   ├── repo_ingestion.py
|   └── searchable_text.py
|
|
├── database.py
├── fastapi_main.py (currently not used)
├── flask_main.py
├── requirements.txt
└── README.md
```

Both Flask and FastAPI use the same:

* Database models
* CRUD functions
* Schemas
* Repository ingestion services
* File-processing logic
* Chunking logic
* Embedding logic
* Semantic retrieval logic
* LLM answer-generation logic

This keeps the web framework separate from the core application behavior.

---

## 7. Setup and Installation

### Prerequisites

Install the following before running the project:

* Python
* PostgreSQL
* pgvector
* Node.js
* npm
* Git

An OpenAI API key is also required for question answering.

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Create a Python Virtual Environment

```bash
python -m venv .venv
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install Backend Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## 8. Environment Variables

Create a `.env` file in the backend project directory.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
OPENAI_API_KEY=your_openai_api_key
```

Replace:

- `username` with your PostgreSQL username
- `password` with your PostgreSQL password
- `your_openai_api_key` with your OpenAI API key

Do not commit the `.env` file or API keys to source control.

---

## 9. Database Setup

The application uses PostgreSQL with the pgvector extension.

### Create the Database

```sql
CREATE DATABASE ai_codebase_assistant;
```

Connect to the database and enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Add the PostgreSQL connection string to the `.env` file.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_codebase_assistant
```

### Run Database Migrations

The project uses Alembic to create and manage the database schema.

```bash
alembic upgrade head
```
The migrations create the required tables, relationships, and pgvector-compatible columns.

### Database Structure 

The database 3 primary database entities:

### Repository

Stores information about an ingested GitHub repository.

### File

Stores metadata about files belonging to a repository.

The full source-file content is not stored directly in the `File` table.

### Chunk

Stores searchable portions of repository content.

Each chunk contains:

* Text content
* Vector embedding
* Start line
* End line
* Function name
* Class name
* Chunk type
* File relationship

The vector embedding is stored using pgvector and is used for semantic similarity search.

### Database Relationships

```text
Repository
    |
    | one-to-many
    v
File
    |
    | one-to-many
    v
Chunk
```
---

## 10. Running the Application

The current demo configuration uses:

* Flask backend: `http://localhost:5001`
* React frontend: `http://localhost:5173`

### Start the Flask Backend

From the project root:

```bash
python flask_main.py
```

The Flask API runs at:

```text
http://localhost:5001
```

### Start the React Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

### Optional: Run the FastAPI Backend

The FastAPI application is defined in:

```text
fastapi_main.py
```

It is typically available at:

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

The frontend is currently configured to communicate with Flask on port `5001`.

---

## 11. Usage

### Ingest a Repository

1. Start PostgreSQL.
2. Start the Flask backend.
3. Start the React frontend.
4. Open the frontend in a browser.
5. Enter the URL of a public GitHub repository.
6. Submit the repository for ingestion.
7. Wait while the backend downloads and processes the repository.
8. The repository becomes available for question answering after ingestion completes.

Example:

```text
https://github.com/owner/repository
```

### Select an Existing Repository

Previously ingested repositories are retrieved from the backend and displayed in the frontend.

Select a repository before asking a question.

### Ask a Question

Example:

```text
How does repository ingestion work?
```
---

## 12. API Endpoints

### Health Check

```http
GET /health
```

Checks whether the Flask server is running.

### Get Repositories

```http
GET /repositories
```

Returns previously ingested repositories.

### Ingest Repository

```http
POST /repositories
```

Example request:

```json
{
  "github_url": "https://github.com/owner/repository"
}
```

### Ask Repository Question

```http
POST /repositories/<repo_id>/questions
```

Example:

```http
POST /repositories/1/questions
```

Request:

```json
{
  "question": "How does repository ingestion work?"
}
```

---

## 13. Citation / Grounding Behavior

The application is designed to reduce hallucination by restricting the LLM to repository context retrieved through semantic search.

Each retrieved chunk is provided to the model as a structured source containing information such as:

```text
SOURCE 1

File: services/repo_ingestion.py
Lines: 30-70
Class: ...
Function: ...
Chunk Type: ...
Content:
...
```

The LLM is instructed to:

* Answer only from supplied repository context
* Avoid inventing files
* Avoid inventing functions or classes
* Avoid inventing program behavior
* Avoid inventing line numbers
* Use complete source file paths
* Use exact stored line ranges
* Avoid estimating narrower citation ranges
* State when the retrieved context is insufficient

Generated citations follow the format:

```text
[file_path:start_line-end_line]
```

Example:

```text
[services/repo_ingestion.py:30-70]
```

The API also returns structured citation objects generated directly from retrieved database chunks.

---

## 14. Current Limitations

* Only public GitHub repositories are currently supported.
* Private repository authentication is not implemented.
* Repository ingestion is synchronous.
* Large repositories may require significant processing time and memory.
* Running multiple backend processes may load multiple copies of the embedding model.
* Chunking works best for Python files currently. 
* Ingestion status tracking is not yet implemented.
* Have yet to include testing.
* Repository updates are not automatically re-ingested.
* Semantic retrieval currently uses a fixed top-10 limit. (top-k)

---

## 15. Project Goals

The goal of AI Codebase Assistant is to demonstrate how modern AI systems can combine software engineering, semantic search, relational databases, vector databases, REST APIs, and Retrieval-Augmented Generation to improve codebase understanding.

Rather than allowing an LLM to answer repository questions from general model knowledge, the system retrieves relevant source code from the actual repository and provides that code as grounded context.


