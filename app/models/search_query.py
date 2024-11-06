from pydantic import BaseModel


class SearchQuery(BaseModel):
    query: str
    top_k: int = 10
    model: str = "mxbai-embed-large"
