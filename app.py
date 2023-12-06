import boto3
from langchain.prompts import PromptTemplate 
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.bedrock import Bedrock
import chainlit as cl
from prompt_template import get_template


@cl.on_chat_start
async def main():
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    inference_modifier = {
        "max_tokens_to_sample": 1000,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": [
          "\n\nHuman:"
        ],
        "anthropic_version": "bedrock-2023-05-31"
    }

    llm = Bedrock(
        model_id = 'anthropic.claude-v2:1',
        client = bedrock,
        model_kwargs = inference_modifier
    )

    provider = 'anthropic'
    if provider == "anthropic":
        human_prefix="H"
        ai_prefix="A"

    prompt = PromptTemplate(
        template=get_template(provider),
        input_variables=["history", "input"],
    )

    conversation = ConversationChain(
        prompt=prompt, 
        llm=llm, 
        memory=ConversationBufferMemory(
            human_prefix=human_prefix,
            ai_prefix=ai_prefix
        ),
        verbose=True
    )
    # Store the chain in the user session
    cl.user_session.set("llm_chain", conversation)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chain from the user session
    conversation = cl.user_session.get("llm_chain") 

    # Call the chain asynchronously
    res = await conversation.acall(
        message.content, 
        callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    
    await cl.Message(content=res["response"]).send()