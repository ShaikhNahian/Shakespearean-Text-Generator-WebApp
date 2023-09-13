from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import keras
import tensorflow as tf
import numpy as np

app = FastAPI()

# Define a Pydantic model for the request data
class InputText(BaseModel):
    inputText: str

model = keras.models.load_model('E:\Projects\Shakespearean\shakespearean\shakespeare_text_gen_model.h5')
path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
vocab = sorted(set(text))
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)


# Define a route to generate Shakespearean text
@app.post("/api/generate")
async def generate_text(input_data: InputText):
    try:
        start_string = input_data.inputText

        # Generate text using your model (replace this with your actual text generation logic)
        generated_text = generate_shakespearean_text(start_string)

        return {"generatedText": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_shakespearean_text(start_string):
 num_generate = 1000

  # Converting our start string to numbers (vectorizing)
 input_eval = [char2idx[s] for s in start_string]
 input_eval = tf.expand_dims(input_eval, 0)

  # Empty string to store our results
 text_generated = []

  # Low temperatures results in more predictable text.
  # Higher temperatures results in more surprising text.
  # Experiment to find the best setting.
 temperature = 1.0

  # Here batch size == 1
 model.reset_states()
 for i in range(num_generate):
    predictions = model(input_eval)
      # remove the batch dimension
    predictions = tf.squeeze(predictions, 0)

      # using a categorical distribution to predict the character returned by the model
    predictions = predictions / temperature
    predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      # We pass the predicted character as the next input to the model
      # along with the previous hidden state
    input_eval = tf.expand_dims([predicted_id], 0)

    text_generated.append(idx2char[predicted_id])

 return (start_string + ''.join(text_generated))