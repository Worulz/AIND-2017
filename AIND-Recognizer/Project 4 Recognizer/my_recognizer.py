import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    #raise NotImplementedError


    for test_word, (X, lengths) in test_set.get_all_Xlengths().items():

        max_score = float("-inf") # Save max score as recognizer iterates the list
        best_guess = None # Save the best guess as recognizer iterations the list
        logL = {} # Save the log likelihood of a word

        for word, model in models.items():
            try:
              # Score the word using the model
              word_score = model.score(X, lengths)
              logL[word] = word_score

            except:
              # assign -inf if unable to process a word
              logL[word] = float("-inf")

            if word_score > max_score:
                max_score = word_score
                best_guess = word

        probabilities.append(logL)
        guesses.append(best_guess)

    return probabilities, guesses
