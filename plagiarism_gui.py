import tkinter as tk
from tkinter import scrolledtext, filedialog
import tensorflow as tf
import string

app = tk.Tk()
app.title("Plagiarism Detector")
app.geometry("500x500")

# Load the pre-trained Keras model
model = tf.keras.models.load_model('model_cnn/NLP_cnn_model.h5')

# Tokenize and preprocess the input text
def tokenize_and_preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    # Your additional tokenization logic here if needed
    return tokens

def detect_plagiarism():
    try:
        file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt")])

        with open(file_path, 'r') as file:
            input_text = file.read()

        # Tokenize and preprocess the input text
        input_tokenized = tokenize_and_preprocess(input_text)

        # Convert tokens to a sequence (numeric representation)
        word_index = {word: idx for idx, word in enumerate(set(input_tokenized))}
        sequences = [word_index[word] for word in input_tokenized]

        # Pad the sequence
        max_sequence_length = 100  # Adjust this based on your model's input shape
        padded_sequence = tf.keras.preprocessing.sequence.pad_sequences([sequences], maxlen=max_sequence_length)

        # Make predictions with the loaded model
        predictions = model.predict(padded_sequence)

        # Assuming binary classification (1 for plagiarism, 0 for no plagiarism)
        is_plagiarized = predictions[0, 0] > 0.5

        # Display the result
        result_text.set('Plagiarism Detected!' if is_plagiarized else 'No Plagiarism Detected')

    except Exception as e:
        result_text.set('Error detecting plagiarism. Please try again.')

# GUI components
upload_button = tk.Button(app, text="Upload Text File", command=detect_plagiarism)
upload_button.pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(app, textvariable=result_text, font=('Helvetica', 12))
result_label.pack(pady=10)

app.mainloop()
