from src.state.state import Blog,BlogState
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_community.document_loaders import YoutubeLoader
import os
from src.llm.groqllm import GroqLm

llm=GroqLm()



class BlogNode:
    def __init__(self):
        llm=GroqLm()
        self.llm=llm.get_llm()
        
    def transcript_extractor(self,state: BlogState):
        "Extract the transcript from the youtube links"
        try:
            url=state["url"]
            loader=YoutubeLoader.from_youtube_url(youtube_url=url,add_video_info=False,language=["hi"],translation="en")
        
            documents=loader.load()
            return {"blog":{"transcript":documents[0].page_content}}
        except Exception as e:
            raise ValueError(f"Error occur with the exception :{e}")
        
        
    def title_creation(self,state: BlogState):
        "Crate the title for the blog post"
        
        if "url" in state and state["url"]:
            prompt=f"""you a professional blog writter use markdownformat.
            Generate a suitable title based on the transcript: {state["blog"]["transcript"]}"""
            llm_with_structured=self.llm.with_structured_output(Blog)
            response=llm_with_structured.invoke(SystemMessage(content=prompt))
            return {"blog":{"title":response}}
        elif "topic" in state and state["topic"]:
            prompt=f"""you a professional blog writter use markdownformat.
            Generate a suitable title based on the topic: {state["topic"]}"""
            response=llm_with_structured.invoke(SystemMessage(content=prompt))
            return {"blog":{"title":response}}
        
        
        else:
            raise ValueError("Both Url and topic is not present in the state.")
            
    def content_generator(self,state: BlogState):
        "Generate the content for the blog post"    
        if "url" in state and state["url"]:
            prompt=f"""You are a professional blog writter .Use markdown formatting.
            Generate a blog content for the transcript: {state["blog"]["transcript"]}"""
            llm_with_structured=self.llm.with_structured_output(Blog)
            response=llm_with_structured.invoke(SystemMessage(content=prompt))
            return {"blog":{"content":response.content}}
            
        elif "topic" in state and state["topic"]:
            prompt=f"""You are a professional blog writter .Use markdown formatting.
            Generate a blog content for the transcript: {state["topic"]}"""
            llm_with_structured=self.llm.with_structured_output(Blog)
            response=llm_with_structured.invoke(SystemMessage(content=prompt))
            return {"blog":{"content":response.content}}
        
        else:
            raise ValueError("Both Url and topic is not present in the state.")
        
    def route(self,state: BlogState):
        return {"current_language":state["current_language"]}
    
    def route_decision(self,state: BlogState):
        "Route the content to respective translation function."
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            raise ValueError("Invalid language")
            
    def translation(self,state: BlogState):
        "translate the content to the specified language."
        sys_mes="You are a very good translator .you translate very wisely with specific accent to the required language"
        prompt=f"""
        translate the following content into {state["current_language"]} language.
        -maintain the original tone style and formatting.
        -adapt the cultural references and idoms to be apppropriate for {state["current_language"]}
        
        -use the following content as the source text.
        {state["blog"]["content"]}
        """
        messages=[(SystemMessage(content=sys_mes)),(HumanMessage(content=prompt))]
        response=self.llm.with_structured_output(Blog).invoke(messages)
        
        return {"blog":{"content":response.content}}
    