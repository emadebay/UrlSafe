import tensorflow as tf
from transformers import DistilBertTokenizerFast

# Load the TensorFlow model (using the saved directory)
model = tf.keras.models.load_model('malicious_phish_model')

# Initialize the tokenizer (same tokenizer used during training)
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

# Map for URL labels
url_label_categorical_to_numerical_dictionary = {
    'phishing': 0,
    'defacement': 1,
    'benign': 2,
    'malware': 3
}

# Function to predict a URL
def predict_url(url):
    encodings = tokenizer([url], truncation=True, padding=True, max_length=2)
    dataset = tf.data.Dataset.from_tensor_slices((dict(encodings),)).batch(1)
    predictions = model.predict(dataset)
    predicted_class_index = tf.argmax(predictions.logits, axis=-1).numpy()[0]

    predicted_label = [
        label for label, index in url_label_categorical_to_numerical_dictionary.items()
        if index == predicted_class_index
    ][0]

    return predicted_label
