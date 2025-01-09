from llama_cpp import Llama
import ollama

def use_llm_to_compare(entity1, entity2, llama_cpp=False):
    query = f"""Are the phrases \"{entity1}\" and \"{entity2}\" the same, similar phrases, or synonyms?
             Allow some deviation in phrasing if necessary. Only answer True or False."""
    if llama_cpp:
        messages = [
            {"role": "user", "content": query}
        ]
        llm = Llama(
            model_path="models/Phi-3.5-mini-instruct-Q5_K_M.gguf",
            chat_format="chatml",
            verbose=False,
            n_ctx=250,
        )
        answer = llm.create_chat_completion(
            messages=messages,
            max_tokens=2,
            temperature=0,
        )
        # print(answer['choices'][0]['message'])
        return "True" in answer['choices'][0]['message']['content']
    else:
        answer = ollama.generate(
            model='gemma2:2b', prompt=query, 
            options={'temperature': 0, 'num_predict': 2}
        )
        return "True" in answer['response']