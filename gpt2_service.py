from typing import Optional
from fastapi import FastAPI
import tensorflow as tf
import time
import gpt_2_simple as gpt2
import os
import requests
import uvicorn

app = FastAPI()

class GPT2:
    """
    This class serves as a wrapper to the OpenAI's gpt2 model. Have chosen to use gpt2_simple wrapper,
    because it provides a way to easily finetune the model with your own dataset.
    I have chosen to use 124M version of the model, as the footprint is small.

    Provides a predict method, which takes an input string and comes up with the next 5 most probable words
    given the input.
    """
    def __init__(self):
        model_name = "124M"
        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)

    def predict(self, prefix=''):
        start = time.time()
        
        #This is needed if you want to predict more than once for the same
        #session run
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, model_name="124M")

        result = gpt2.generate(sess, 
                                prefix=prefix, 
                                checkpoint_dir='models', 
                                run_name='124M', 
                                return_as_list=True, 
                                length=5)

        print(f'Time taken for the prediction is {time.time() - start}')

        return result

model = GPT2()

@app.get("/")
def read_root():
    return {"Welcome to GPT"}


@app.get("/predict/{prefix}")
def predict(prefix: str):
    "Predict method that takes the input token and returns the 5 next probable words"
    return {"result": model.predict(prefix)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)