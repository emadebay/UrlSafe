import zipfile
import os
import shutil
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification

# Define paths
model_zip_path = 'malicious_phish_model.zip'  # Path to the zipped model file
model_dir = 'malicious_phish_model'  # Directory where the model will be unzipped

# Unzip the model if it's not already unzipped
if not os.path.exists(model_dir):
    with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
        zip_ref.extractall(model_dir)

# Load the unzipped model and tokenizer
model = TFDistilBertForSequenceClassification.from_pretrained(model_dir)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)

# Remove the unzipped model directory to free up space
shutil.rmtree(model_dir)

# Define the dictionary for mapping predicted indices back to labels
url_label_categorical_to_numerical_dictionary = {
    0: 'phishing', 
    1: 'defacement',
    2: 'benign', 
    3: 'malware'
}

# Function for predicting the label of a new URL
def predict_url_label(url):
    # Tokenize the new URL
    new_url_encodings = tokenizer([url], truncation=True, padding=True, max_length=16)
    
    # Convert to TensorFlow dataset format
    new_url_dataset = tf.data.Dataset.from_tensor_slices(
        dict(new_url_encodings)
    ).batch(1)  # Batch size of 1 for single prediction
    
    # Make the prediction
    new_url_predictions = model.predict(new_url_dataset)
    
    # Get the predicted class index
    predicted_class_index = tf.argmax(new_url_predictions.logits, axis=-1).numpy()[0]
    
    # Map the predicted class index to the corresponding label
    predicted_label = url_label_categorical_to_numerical_dictionary[predicted_class_index]
    
    return predicted_label
