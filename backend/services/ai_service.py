from core.config import config
from pydantic import BaseModel, Field
from typing import List
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

## Define the output json structure for the AI response
class Insight(BaseModel):
    text: str = Field(description="The generated insight or summary point")
    citations: List[str] = Field(description="Array of timestamps from the transcript")

class ActionItemAI(BaseModel):
    task: str = Field(description="The required action item")
    assignee: str = Field(description="The name of the person assigned to the task")
    citations: List[str] = Field(description="Array of timestamps from the transcript")

class MeetingAnalysis(BaseModel):
    summary: List[Insight]
    actionItems: List[ActionItemAI]
    decisions: List[Insight]
    followUps: List[Insight] 
    

## Meeting analysis class
class MeetingAnalyzer:
    def __init__(self):
        self.HF_TOKEN = config.HF_TOKEN
        
        self.llm = HuggingFaceEndpoint(
            repo_id = "meta-llama/Meta-Llama-3-8B-Instruct",
            temperature=0.1,
            max_new_tokens=1500,
            huggingfacehub_api_token=self.HF_TOKEN
        )
        
        self.model = ChatHuggingFace(llm = self.llm)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert AI meeting assistant. Analyze the meeting transcript.
            
            CRITICAL RULES:
            1. Do not invent attendees, action items, or outcomes.
            2. Every generated insight MUST include at least one citation referencing the exact timestamp from the transcript.
            
            {format_instructions}"""),
            ("user", "Here is the transcript to analyze:\n\n{transcript}")
        ])
        
        self.output_parser = PydanticOutputParser(pydantic_object=MeetingAnalysis)
        
        ## Excution chain
        self.chain = self.prompt | self.model | self.output_parser

    def analyze_transcript(self, transcript) -> dict:
        try:
            formatted_transcript = "\n".join(
                [f"[{segment['timestamp']}] {segment['speaker']}: {segment['text']}" for segment in transcript]
            )
            
            result = self.chain.invoke({
                "transcript": formatted_transcript,
                "format_instructions": self.output_parser.get_format_instructions()
            })
            
            return result.model_dump()
        
        except Exception as e:
            raise ValueError(f"Error during transcript analysis: {str(e)}")
        

analysis_service = MeetingAnalyzer()