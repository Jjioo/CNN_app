from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import string

app = Flask(__name__)

# Load the pre-trained Keras model
model = tf.keras.models.load_model('model_cnn/NLP_cnn_model.h5')

# Tokenize and preprocess the input text
def tokenize_and_preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    # Your additional tokenization logic here if needed
    return tokens

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_plagiarism', methods=['POST'])
def detect_plagiarism():
    try:
        file = request.files['file']
        if file:
            input_text = file.read().decode('utf-8')

            # Tokenize and preprocess the input text
            input_tokenized = tokenize_and_preprocess(input_text)

            # Convert tokens to a sequence (replace with your actual tokenization logic)
            sequences = [hash(word) for word in input_tokenized]

            # Pad the sequence
            max_sequence_length = 100  # Adjust this based on your model's input shape
            padded_sequence = tf.keras.preprocessing.sequence.pad_sequences([sequences], maxlen=max_sequence_length)

            # Make predictions with the loaded model
            predictions = model.predict(padded_sequence)

            # Assuming binary classification (1 for plagiarism, 0 for no plagiarism)
            is_plagiarized = predictions[0, 0] > 0.5

            # Return the result as JSON
            return jsonify({'isPlagiarized': bool(is_plagiarized)})

        else:
            return jsonify({'error': 'No file uploaded'}), 400

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
