def format_response(response_text, mode, chat_model=None):
    """
    Format response based on selected mode.
    - Detailed: Return full response
    - Concise: Use LLM to create bullet-point summary
    """
    if mode == "Concise":
        if chat_model:
            summary_prompt = """Summarize the following response into concise bullet points. 
Keep it brief but informative. Preserve any links in markdown format.
Focus on the key actionable items and main points.

Response to summarize:
{response}

Provide a concise summary with:
- Main points as bullet points
- Keep any job links intact
- Maximum 5-7 bullet points
- Be direct and actionable"""
            
            from langchain_core.messages import SystemMessage, HumanMessage
            try:
                messages = [
                    SystemMessage(content="You are an expert at creating concise, actionable summaries."), 
                    HumanMessage(content=summary_prompt.format(response=response_text))
                ]
                summary_response = chat_model.invoke(messages)
                return summary_response.content
            except Exception as e:
                print(f"Summarization error: {e}")
                # Fallback: Extract first few sentences
                sentences = response_text.split('.')[:3]
                return '. '.join(sentences) + ".\n\n[Full response truncated - switch to Detailed mode for complete answer]"
        else:
            # No model available, simple truncation
            return response_text[:400] + "\n\n...[Truncated - switch to Detailed mode for full response]"
    
    # Detailed mode - return as is
    return response_text