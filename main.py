# Vigenere decipher using AI
# LordShadowT 2023
# CC-BY-NC


import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv
import random as rnd

# Creates a keras AI model using tensorflow
try:
    model = keras.models.load_model('/saved_model')
    print('prev model loaded')
except:
    model = keras.Sequential([
        keras.layers.LSTM(128, input_shape=(None, 26), return_sequences=True),
        keras.layers.Dense(26, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print('new model generated')


# Encrypt Text with Vigenère cipher
def vigenere_encrypt(text, key: str):
    result = ""
    key = key.lower()
    j = 0
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text
        if char.isupper():
            result += chr((ord(char) + ord(key[j % len(key)]) - ord('a') - 65) % 26 + 65)
            j += 1
        # Encrypt lowercase characters in plain text
        elif char.islower():
            result += chr((ord(char) + ord(key[j % len(key)]) - ord('a') - 97) % 26 + 97)
            j += 1
        else:
            result += char
    return result


# Pads the Sequence to have the same length
def pad_sequences(sequences, max_length):
    padded_sequences = []
    for seq in sequences:
        if len(seq) < max_length:
            padded_seq = seq + " " * (max_length - len(seq))
        else:
            padded_seq = seq
        padded_sequences.append(padded_seq)
    return padded_sequences


def pad_single(sequence, max_length):
    padded_sequence = ""
    if len(sequence) < max_length:
        padded_sequence = sequence + " " * (max_length - len(sequence))
    return padded_sequence


# Converts characters to one-hot encoding
def char_to_onehot(char):
    if char.islower():
        return [1 if char == chr(i) else 0 for i in range(ord('a'), ord('z') + 1)]
    elif char.isupper():
        return [1 if char == chr(i) else 0 for i in range(ord('A'), ord('Z') + 1)]
    else:
        return [0] * 26


def generate_text(amount: int):
    training_data = []
    with open('/wordlists/training_data.txt', encoding='Windows-1252') as f:
        lines = f.readlines()
        for i in range(amount):
            text = lines[rnd.randint(0, len(lines) - 1)]
            training_data.append(text)
    return training_data


def encrypt_text(text: str, is_sample: bool):
    encrypted_text = []
    with open('/wordlists/wordlist_keys.txt', encoding='Windows-1252') as g:
        for i in text:
            g.seek(rnd.randrange(22415) + 1)
            g.readline()
            key = g.readline().replace('\n', '')
            if is_sample:
                print(key)
            encrypted_text.append(vigenere_encrypt(i, key))
    return encrypted_text


# Trains the AI
def train_ai(generated_data: int, epochs: int):
    print('Training started')
    training_text = generate_text(generated_data)
    while max(len(seq) for seq in training_text) > 2100:
        print('Max line length is too long, length is: ' + str(max(len(seq) for seq in training_text)) + '\n Generating new data...')
        training_text = generate_text(generated_data)
    enc_training_text = encrypt_text(training_text, False)
    print('Training data generated')
    input_data = pad_sequences(enc_training_text, 2100)
    input_data = [list(map(char_to_onehot, text)) for text in input_data]
    input_data = np.array(input_data, dtype=np.float32)
    target_data = pad_sequences(training_text, 2100)
    target_data = [list(map(char_to_onehot, text)) for text in target_data]
    target_data = np.array(target_data, dtype=np.float32)
    print('Training data is in the right format')
    model.fit(input_data, target_data, epochs=epochs, batch_size=64, callbacks=[keras.callbacks.ModelCheckpoint(filepath='/saved_model')])
    print('Training complete')
    input_data = []
    target_data = []


def sample(amount: int, one_hot: int):
    print('Starting Generation')
    training_text = generate_text(amount)
    while max(len(seq) for seq in training_text) > 2100: training_text = generate_text(amount)
    enc_training_text = encrypt_text(training_text, True)
    print('Training data generated')
    input_data = pad_sequences(enc_training_text, 2100)
    target_data = pad_sequences(training_text, 2100)
    if one_hot != 0:
        input_data = [list(map(char_to_onehot, text)) for text in input_data]
        input_data = np.array(input_data, dtype=np.float32)
        target_data = [list(map(char_to_onehot, text)) for text in target_data]
        target_data = np.array(target_data, dtype=np.float32)
    print('\n Encrypted Data: \n \n')
    print(input_data)
    print('\n Unencrypted Data: \n \n')
    print(target_data)


# Uses the trained AI to decrypt a given encrypted input
def vigenere_decrypt_ai(ciphertext: str):
    ciphertext = pad_single(ciphertext, 2100)
    #print(ciphertext)
    input_data = np.array([list(map(char_to_onehot, ciphertext))], dtype=np.float32)
    predicted_keys = model.predict(input_data)[0]
    predicted_text = ""
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            predicted_key = predicted_keys[i]
            shift = np.argmax(predicted_key)
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            predicted_text += decrypted_char
        else:
            predicted_text += char
    return predicted_text



s = ''
#main loop
while s != 'stop':
    s = input('> ')
    if s == 'help':
        print('\n \n -----\n')
        print('stop: stops the program')
        print('train: trains the AI with a set number of datasets and epochs')
        print('new: creates a new AI model and deletes every training progress (NOT REVERSABLE)')
        print('sample: generates a set amount of unencrypted and encrypted text')
        print('decrypt: uses the AI to decrypt a vigenere-encrypted message (currently only supports german)')
        print('\n ----- \n')
    if s == 'train':
        data_amount = int(input('Number of datasets: '))
        epochs = int(input('Number of epochs: '))
        train_ai(data_amount, epochs)
    elif s == 'new':
        if input('You sure? (y/n): ') == 'y':
            model = keras.Sequential([
                keras.layers.LSTM(128, input_shape=(None, 26), return_sequences=True),
                keras.layers.Dense(26, activation='softmax')
            ])
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            print('new model generated')
    elif s == 'sample':
        sample(int(input('Amount of Data: ')), int(input('One-Hot?: ')))
    elif s == 'encrypt':
        print('Encrypted: ' + vigenere_encrypt(input('Message: '), input('Key: ')))
    elif s == 'decrypt':
        print('\n' + vigenere_decrypt_ai(input('Encrypted Text: ')) + '\n')
print('\n--------------')
print('System stopped')
print('--------------\n')
