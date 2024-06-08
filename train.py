from model.model import CodeSwitchingModel
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Dữ liệu mẫu
sentences = [
    "Hello bạn, how are you?",
    "Tôi đang học machine learning and it's really interesting.",
    "Let's đi ăn tối.",
]

labels = [
    ["en", "vi", "en", "en", "en"],
    ["vi", "vi", "en", "en", "en", "en", "en", "en"],
    ["en", "vi", "vi", "vi"],
]

# Tạo danh sách các ký tự duy nhất
chars = set(''.join(sentences))
char2idx = {c: i + 1 for i, c in enumerate(chars)}  # Bắt đầu từ 1 để 0 dành cho padding
char2idx['PAD'] = 0
idx2char = {i: c for c, i in char2idx.items()}

# Mã hóa nhãn
label_tokenizer = tf.keras.preprocessing.text.Tokenizer()
label_tokenizer.fit_on_texts(labels)
label2idx = label_tokenizer.word_index
num_classes = len(label2idx) + 1

# Chuyển đổi câu và nhãn
X = []
y = []

for sentence, label_list in zip(sentences, labels):
    x_sentence = []
    y_sentence = []
    for word, label in zip(sentence.split(), label_list):
        for char in word:
            x_sentence.append(char2idx[char])
            y_sentence.append(label2idx[label])
        x_sentence.append(char2idx[' '])  # Thêm khoảng trắng vào danh sách ký tự
        y_sentence.append(0)  # Thêm nhãn 0 (không xác định) cho khoảng trắng
    
    # Loại bỏ khoảng trắng cuối cùng
    x_sentence = x_sentence[:-1]
    y_sentence = y_sentence[:-1]

    X.append(x_sentence)
    y.append(y_sentence)

# Pad sequences để các câu có độ dài bằng nhau
X = pad_sequences(X, padding='post')
y = pad_sequences(y, padding='post')

# One-hot encode các nhãn
y = [to_categorical(i, num_classes=num_classes) for i in y]
y = np.array(y)


# Khởi tạo mô hình
vocab_size = len(char2idx)
embedding_dim = 64
lstm_units = 64

model = CodeSwitchingModel(vocab_size, num_classes, embedding_dim, lstm_units)

# Định nghĩa hàm mất mát và optimizer
loss_fn = tf.keras.losses.CategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

# Huấn luyện mô hình
epochs = 10
batch_size = 1
num_batches = len(X) // batch_size

for epoch in range(epochs):
    print(f"Epoch {epoch + 1}/{epochs}")
    epoch_loss = 0
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        x_batch = X[start:end]
        y_batch = y[start:end]
        batch_loss = model.train_step(x_batch, y_batch, loss_fn, optimizer)
        epoch_loss += batch_loss
    print(f"Loss: {epoch_loss / num_batches}")