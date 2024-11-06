from pydantic import BaseModel


class Document(BaseModel):
    title: str
    text: str
    metadata: dict = {}
    model: str = "mxbai-embed-large"
