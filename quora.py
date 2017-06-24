import pandas as pd
import math

#create vocabulary from data assigning unique index to each word

def create_vocab(all_questions):
    data = all_questions.split(" ")
    vocab_index = {}
    for word in data:
        if word not in vocab_index:
            vocab_index[word] = len(vocab_index) + 1
    #print (vocab_index, len(vocab_index))
    return vocab_index

#counts all the occurences of words
def count_words(all_questions):
    counter = {}
    for word in all_questions:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    print (counter, len(counter))
    return counter


def convert_to_vector(question, vocab_index):
    #create a fixed size vector equal to the size of the vocabulary
    vector = [0.0]* (len(vocab_index) + 1)
    for word in question:
        word_index = vocab_index[word]
        #print(word_index, len(vocab_index))
        vector[word_index] += 1
    return vector


def compare_questions(question_1, question_2, gold_answer, vocab_index):
    # convert the questions to vectors
    vector_1 = convert_to_vector(question_1.split(" "), vocab_index)
    vector_2 = convert_to_vector(question_2.split(" "), vocab_index)

    vector_size = len(vector_1)

    sum_ = 0.0 # dot product
    norm_1 = 0.0 # the sum of squares of the components of vector_1
    norm_2 = 0.0 # the sum of squares of the components of vector_2

    for i in range(0, vector_size):
        a = vector_1[i]
        b = vector_2[i]
        sum_ += a*b
        norm_1 += a*a
        norm_2 += b*b

    normalization = (math.sqrt(norm_1))*(math.sqrt(norm_2))
    cosine_similarity = sum_/normalization

    print (cosine_similarity, gold_answer)

def main():
    df = pd.read_csv("train.csv")
    question_1 = list(df.question1.values)
    question_2 = list(df.question2.values)
    answer = list(df.is_duplicate.values)

    total_questions = " ".join(question_1 + question_2)
    total_questions = total_questions.replace("?", "")
    total_questions = total_questions.lower()

    vocab_index = create_vocab(total_questions)
    for i in range(len(question_1)):
        question_1[i] = question_1[i].replace("?", "")
        question_1[i] = question_1[i].lower()
        question_2[i] = question_2[i].replace("?", "")
        question_2[i] = question_2[i].lower()
        result = compare_questions(question_1[i], question_2[i], answer[i], vocab_index)
main()
