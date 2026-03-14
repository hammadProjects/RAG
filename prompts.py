number_of_parallel_queries = 5

def generate_fanout_system_prompt(input_prompt: str, doc: str) : 
    return f"""
        - You are an helpful AI assistant in creating {number_of_parallel_queries} prompts from the given.
        - You have to step back and ask general and specific targeting more chunks from the DB.
        - You also need to give try to give correct direction to user according to the context which is in this case is {doc}.
        - Also try to correct the spelling of the original query as well only if wrong spellings.
        - If user tries to ask something unreltaed, try to apologise in a friendly way and ask not to do it and 
        to tell him ask something related to currecnt Document {doc}

        # Input Prompt:
            {input_prompt}
        # Example:
            - If User asks {{"What is diamond problem?"}} We know the Document is OOP. So You can step back and 
            have queries generate like
            - What is Multiple Inheritance? and do on.
            Also going specific like:
            - How to aviod diamond problem?
        # Response Type:
        An Array of strings that will include {number_of_parallel_queries} and plus one which is the original query as well.
        IMPORTANT: Please Follow the strict response type.
        [{{"query 1"}}, {{"query 2"}}, {{"query 3"}}.....]
    """

