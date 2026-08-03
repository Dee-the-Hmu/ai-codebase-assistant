from pydantic import BaseModel, HttpUrl, ConfigDict

class QuestionRequest(BaseModel):
    question : str

class CitationResponse(BaseModel):
    file_path : str
    start_line : int | None 
    end_line : int | None 
    similarity_score : float
    
class QuestionResponse(BaseModel):
    answer : str
    citations : list[CitationResponse]

