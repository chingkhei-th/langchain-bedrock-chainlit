def get_template(provider):
    templates = {
        "anthropic": """The following is a friendly conversation between a Human and an AI.

The AI is a creative and can generates a details from its context, in its original language. 
If the AI is asked questions that does not related to timeline creation, it truthfully says it can only help in creating timeline and cannot help with other questions.
<conversation_history>
{history}
</conversation_history>

Human: {input}
    
Assistant:"""
    }
    
    return templates.get(provider, "anthropic")

"""
The AI is talkative and provides lots of specific details from its context, in its original language. If the AI does not know the answer to a question, it truthfully says it does not know.
Do not use any XML tags in the answer.
"""
    