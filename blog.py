import uvicorn
from fastapi import FastAPI
from src.graph.graph_builder import GraphBuilder
from src.state.state import BlogState

app=FastAPI()

