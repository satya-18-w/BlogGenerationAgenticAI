from langgraph.graph import StateGraph,START,END
from llm.groqllm import GroqLm
from node.blog_node import BlogNode
from state.state import BlogState,Blog

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)
        
    def build_url_graph(self):
        "Buld url graph"
        self.blog_node=BlogNode()
        self.graph.add_node("transcript_extractor",self.blog_node.transcript_extractor)
        self.graph.add_node("Title_creation",self.blog_node.title_creation)
        self.graph.add_node("content_generator",self.blog_node.content_generator)
        
        self.graph.add_edge(START,"transcript_extractor")
        self.graph.add_edge("transcript_extractor","Title_creation")
        self.graph.add_edge("Title_creation","content_generator")
        self.graph.add_edge("content_generator",END)
        return self.graph
        
    def build_topic_graph(self):
        "build the graph from given llm"
        self.blog_node=BlogNode()
        #self.graph.add_node("transcript_extractor",self.blog_node.transcript_extractor)
        self.graph.add_node("title_creator",self.blog_node.title_creation)
        self.graph.add_node("content_generator",self.blog_node.content_generator)
        
        # Edges
        self.graph.add_edge(START, "title_creator")
        self.graph.add_edge("title_creator", "content_generator")
        self.graph.add_edge("content_generator", END)

        return self.graph
        
        
    def build_multi_language_graph(self):
        "Build a graph that convert blog content to multiple languages"
        self.blog_node=BlogNode()
        self.graph.add_node("title_generator",self.blog_node.title_creation)
        self.graph.add_node("content_generator",self.blog_node.content_generator)
        self.graph.add_node("hindi_translation",lambda state: self.blog_node.translation({**state,"current_language":"hindi"}))
        self.graph.add_node("french_translation",lambda state: self.blog_node.translation({**state,"current_language":"french"}))
        self.graph.add_node("route",self.blog_node.route)
        
        # Edges
        self.graph.add_edge(START,"title_generator")
        self.graph.add_edge("title_generator","content_generator")
        self.graph.add_edge("content_generator","route")
        
        self.graph.add_conditional_edges("route",self.blog_node.route_decision,{"hindi":"hindi_translation","french":"frenech_translation"})
        self.graph.add_edge("hindi_translation",END)
        self.graph.add_edge("french_translation",END)
        
        return self.graph
    
    
    def set_up_graph(self,usecase):
        if "usecase" == "url":
            return self.build_url_graph().compile()
        if "usecase" == "topic":
            return self.build_topic_graph().compile()
        if "usecase" == "language":
            return self.build_multi_language_graph().compile()
        
        
        