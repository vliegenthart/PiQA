from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model='gpt-3.5-turbo')
# conversation = ConversationChain(
#     llm=llm,
#     verbose=True,
#     memory=ConversationBufferMemory()
# )


# TODO: Add chat interactions + history
def get_chat_completion(df: pd.DataFrame) -> str:
    print("Generating completion...")
    pdf_content = ' '.join(df['Text'])

    instruction_template="{instruction}"

    # TODO: Remove linebreaks.
    task_template=  """TASK:
        Extract key information from the content below. The content is the text of a pitch deck. Only use the content provided and be as precise (include important numbers) and concise as possible.  Structure your answer into the following sections:
        Name of the product, Team (in this format: <NAME>: <TITLE> - <OTHER INFO>), Traction, Problem, Solution, Market, Market Size, Product-Market Fit, Go-to-market (GTM) Strategy, Target Customers, Competition, Business Model, and Revenue Model, a concise summary of the content below (maximum of 80 words), A longer summary of the content below (maximum of 200 words) and a critical, step by step, guide on how to assess the risks of investing in this startup, and a recommendation on whether to invest in the startup or not.
        Only include the sections if the relevant information is present in the content. Use structure for each section if relevant, like a list or table.
        Include a header for each section. Format the output in Markdown.

        CONTENT: {pdf_content}

        ANSWER:
        """

    instruction = "You are a venture capitalist looking to invest in a startup. You have been given a startup's pitch deck. You are asked to extract key information from the document and provide a recommendation on whether to invest in the startup or not."

    instruction_human_prompt = HumanMessagePromptTemplate.from_template(instruction_template)
    task_human_prompt = HumanMessagePromptTemplate.from_template(task_template)

    chat_prompt = ChatPromptTemplate.from_messages([instruction_human_prompt, task_human_prompt])

    print("PROMPT", chat_prompt.format_prompt(instruction=instruction, pdf_content=pdf_content).to_string())
    resp = chat(chat_prompt.format_prompt(instruction=instruction, pdf_content=pdf_content).to_messages())
    return resp.dict()["content"]

