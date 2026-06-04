# AI Approach & Strategy

This document details the strategies and architecture used to integrate the Large Language Model (LLM) for transcript analysis, ensuring accuracy, strict formatting, and traceability.

---

## 1. Prompt Design
The prompt is engineered using LangChain's `ChatPromptTemplate` with a clear separation of instructions and data:
* **System Message:** Establishes the persona ("expert AI meeting assistant") and sets rigid, unbending rules. It directly injects the JSON formatting requirements so the LLM knows exactly how to structure its output.
* **User Message:** Contains the raw transcript. Before being injected, the transcript is programmatically formatted into a highly readable string structure: `[{timestamp}] {speaker}: {text}`. This makes it effortless for the LLM to comprehend the chronological flow of the conversation.

---

## 2. Citation Strategy
Citations are treated as a mandatory data type, not an optional feature. 
* The Pydantic output schemas (`Insight` and `ActionItemAI`) strictly require a `citations: List[str]` field for every single generated point. 
* The prompt's "CRITICAL RULES" explicitly instruct the model to map the exact timestamps from the provided text to these arrays. 
* By structuring the input text with explicit `[timestamp]` brackets, the model is primed to extract those exact strings as its source of truth.

---

## 3. Hallucination Prevention Approach
Hallucinations are mitigated through a three-layered defense:
1. **Deterministic Execution:** The Hugging Face endpoint (`meta-llama/Meta-Llama-3-8B-Instruct`) is configured with an extremely low temperature (`temperature=0.1`). This forces the model to act analytically and predictably, drastically reducing creative deviations.
2. **Explicit Negative Prompting:** The prompt specifically forbids the model from inventing attendees, action items, or outcomes.
3. **Forced Grounding:** Because the schema demands an array of timestamps for every summary point and decision, the model is forced to logically tie its output to a specific line in the transcript before generating the response.

---

## 4. Output Validation Strategy
Validation is handled programmatically using LangChain's `PydanticOutputParser`. 
* The LLM's output is not treated as raw text; it is strictly parsed against the `MeetingAnalysis` Pydantic model. 
* If the LLM returns malformed JSON, hallucinates incorrect keys, or misses the required citation arrays, the parser rejects it. 
* This failure is safely caught by a `try/except` block in the API router, which prevents server crashes and returns a graceful, formatted `GENERATION_FAILED` error to the client.

---

## 5. Known Limitations
* **Context Window Constraints:** The current implementation processes the entire transcript in a single prompt. For extremely long, multi-hour meetings, the transcript may exceed the token limit of the `Meta-Llama-3-8B-Instruct` model, requiring future implementation of text chunking or MapReduce summarization techniques.
* **Speaker Ambiguity:** If the transcript contains highly fragmented, rapid-fire dialogue or overlapping speech at identical timestamps, the LLM may occasionally misattribute an action item to the wrong participant.