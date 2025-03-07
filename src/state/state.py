from typing import TypedDict,Dict,Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel,Field

class Blog(BaseModel):
    title: str=Field(description="The title of the blog")
    transcript: str=Field(description="The transcript extracted from the youtube video.")
    content: str=Field(description="The main content of the blog post")
    
    
    
    
class BlogState(TypedDict):
    topic: str
    url: str
    blog: Blog
    current_language: str