import numpy as np
from transformers import BertTokenizerFast
from transformers import TFBertForSequenceClassification
from transformers import TextClassificationPipeline
from timeit import default_timer

loaded_tokenizer = None
loaded_model = None
text_classifier = None

def create_model_instance(model_path):
    print("create_model_instance()...")

    #start = default_timer()

    global loaded_tokenizer, loaded_model, text_classifier

    loaded_model = TFBertForSequenceClassification.from_pretrained(model_path)
    loaded_tokenizer = BertTokenizerFast.from_pretrained(model_path)
    text_classifier = TextClassificationPipeline(
        tokenizer=loaded_tokenizer, 
        model=loaded_model, 
        framework='tf',
        return_all_scores=True
    )

    #end = default_timer()
    #print("Time duration(in seconds):", end - start)
    return

def get_label(input_str):
    print("get_label()...")

    #start = default_timer()

    predicted_result = text_classifier(input_str)

    # Get the predicted label name
    label_map = {0: "Neutral", 1: "Positive", 2: "Negative"}

    predicted_label_scores = []
    for prediction_item in predicted_result:
        for prediction_dict in prediction_item:
            predicted_label_scores.append(prediction_dict['score'])
        predicted_label_id = np.argmax(predicted_label_scores)
        predicted_label_name = label_map[predicted_label_id]

    #end = default_timer()
    #print("Time duration(in seconds):", end - start)
    return predicted_label_name
