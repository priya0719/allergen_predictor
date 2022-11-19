from django.shortcuts import render
from django.http import HttpResponse
from .LSTM_backend_code import *

from tensorflow.keras.models import load_model
import numpy as np


# Create your views here.
def home(request):
    return render(request, "home.html")

def predict(request):
    protein_sequence = request.POST['sequence']

    if protein_sequence == "":
        return render(request, "result.html", {'prediction': 'Please enter the sequence'})

    converted_sequence = main(protein_sequence, j_list, k_list, lag)

    if converted_sequence == 'Entered sequence has undefined character':
        return render(request, "result.html", {'prediction': 'Entered sequence has undefined character'})

    if len(converted_sequence) < 125:
        converted_sequence.extend([0] * (125 - len(converted_sequence)))
    elif len(converted_sequence) > 125:
        converted_sequence = converted_sequence[0:125]
    converted_sequence = np.array(converted_sequence)
    converted_sequence = np.reshape(converted_sequence, (1, 125))
    loaded_model = load_model('network.h5')
    prediction = loaded_model.predict(converted_sequence)
    prediction = np.argmax(prediction, axis=1)[0]
    if prediction == 0:
        result = "Non Allergenic"
    elif prediction == 1:
        result = "Allergenic"

    return render(request, "result.html", {'prediction':result})


def data_sets(request):
    return render(request, 'data_sets.html')


def method_description(request):
    method = "Here we have considered five E-descriptors which were used to describe features of protein sequences. " \
             "They were computed by Venkatarajan using principal component analysis from a data matrix including 237 " \
             "physicochemical parameters\cite{venkatarajan2001new}. The first primary component (E1) indicates hydrophobicity " \
             "of amino acid ; the second (E2) their size; the third (E3) their helix-forming propensity; the fourth (E4) " \
             "indicates the relative abundance of amino acid; and the fifth (E5) the propensity for  β strand formation. \n" \
             "Proteins are composed of amino acid sequences, each of which is distinct and varies in length. " \
             "So, in order to convert the variable-length string to equal length, we have considered the ACC transformation. " \
             "Auto Cross Covariance includes Auto Covariance and Cross Covariance. \nAuto covariance is calculated between the " \
             "same E Descriptors, that is between E1 and E1, along with lag value and Cross covariance is calculated between " \
             "the different E Descriptors. \nFor classification, we have considered a few machine learning, ensemble learning, " \
             "and deep learning algorithms, which include: The Gaussian Naive Bayes, Radius Neighbour's Classifier, Bagging " \
             "Classifier, ADA Boost, Linear Discriminant Analysis, Quadratic Discriminant Analysis, Extra Tree Classifier " \
             "and LSTM, which have been implemented in Python.\nAmong these LSTM delivered highly defined classification " \
             "performance that is substantially quicker than other algorithms with comparable classification performance. " \
             "LSTM is five times larger than marginally faster classification algorithms.\nUsing performance evaluation " \
             "measures, all of the implemented methods were tested and compared. The top performing model was LSTM, which " \
             "had an accuracy of 91.51 percent . LSTM is a more sophisticated variant of the RNN (recurrent neural network). " \
             "We considered LSTM for our problem because of its application to robustness against long-term dependency problems. " \
             "Since the protein sequences are also correlated with each other, LSTM would be a likely method for solving long-term " \
             "dependencies and would overcome the drawbacks of the alignment method."

    return render(request, 'method_description.html', {'method':method})

def allergen_dataset(request):
    fr = open('new_allergens.fasta','r')
    data = fr.read()
    fr.close()
    return HttpResponse(data)

def non_allergen_dataset(request):
    fr = open('new_Nonallergens.fasta','r')
    data = fr.read()
    fr.close()
    return HttpResponse(data)

