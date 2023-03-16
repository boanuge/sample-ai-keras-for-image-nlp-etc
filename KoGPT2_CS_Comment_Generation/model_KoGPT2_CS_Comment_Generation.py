from transformers import TFGPT2LMHeadModel, AutoTokenizer
from timeit import default_timer

loaded_tokenizer = None
loaded_model = None

def create_model_instance(model_path):
    print("create_model_instance()...")

    start = default_timer()

    global loaded_tokenizer, loaded_model

    loaded_model = TFGPT2LMHeadModel.from_pretrained(model_path)
    loaded_tokenizer = AutoTokenizer.from_pretrained(model_path)

    end = default_timer()
    print("Time duration(in seconds):", end - start)
    return

def get_text(input_str):
    print("get_text()...")

    start = default_timer()

    input_ids = loaded_tokenizer.encode(input_str, return_tensors="tf")
    output_ids = loaded_model.generate(input_ids=input_ids, max_length=280, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    generated_text = loaded_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    end = default_timer()
    print("Time duration(in seconds):", end - start)
    return generated_text
