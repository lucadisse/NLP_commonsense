import os
import pandas as pd
import numpy as np

# BLEU Score
from Scoring.BLEUScore import own_bleu_score, challenge_score

# Mover Score
from moverscore_v2 import get_idf_dict, word_mover_score, plot_example
from collections import defaultdict

# Rouge Score
#from rouge_score import rouge_scorer


class Scorer:
    def __init__(self, prediction_path, reference_path):
        self.prediction_path = prediction_path
        self.reference_path = reference_path
        self._references = []
        self._predictions = []
        self._scores = []
        self.predictions_df = pd.DataFrame()
        self.references_df = pd.DataFrame()
        self.load_data(prediction_path, reference_path)


    def load_data(self, prediction_path, reference_path):
        if  not os.path.isfile(prediction_path):
            raise ImportError ('File '+ prediction_path +' does not exist.')
        elif not os.path.isfile(reference_path):
            raise ImportError ('File '+ reference_path +' does not exist.')

        self.predictions_df = pd.read_csv(prediction_path, index_col = 0)
        self.references_df = pd.read_csv(reference_path, index_col = 0)

        if len(self.predictions_df) != len(self.references_df):
            raise ValueError("Number of reference and generated reasons do not match.")

        if any(self.predictions_df.index.to_numpy() != self.references_df.index.to_numpy()):
            raise ValueError("Indices of provided predictions and reference reasons do not match.")

    def compute_scores(self):
        pass

    def preprocess(self):
        pass

    def print_bad_results(self):
        pass

    @property
    def scores(self):
        return self._scores 


    
class BLEUScore(Scorer):
    def __init__(self, prediction_path, reference_path):
        super().__init__(prediction_path, reference_path)
        self.compute_scores()

    def compute_scores(self):
        self.preprocess()

        for prediction, reference_triplet in zip(self._predictions, self._references):
            self._scores.append(own_bleu_score(predictions=prediction, references=reference_triplet))

    def preprocess(self):
        self._predictions = self.predictions_df.values
        self._references = self.references_df.values

    def print_bad_results(self, shown_elems=3):
        idx = np.argpartition(self._scores, shown_elems)
        for i in idx[:shown_elems]:
            print("BLEU References:     ", self._references[i], "\n")
            print("BLEU Answer:     : ", self._predictions[i], "\n")
            print("BLEU Row Index:     : ", self.references_df.index[int(i/3.)], "\n")
            print("------------------------------------\n")



class MoverScore(Scorer):

    def __init__(self, prediction_path, reference_path):
        super().__init__(prediction_path, reference_path)
        self.compute_scores()

    def compute_scores(self):
        # only import these module if object instantiated
        # demands GPU 

        # Beispiel Sätze
        # predictions = ["A rabbit can not fly because he has no wings.", "The rabbit is running over the moon.","Having breakfast is genious since cheese is delicous."]
        # references = ["The rabbit is not a bird.","Showing mercy is not an option.", "The dinner was very good because the meat was very tender."]
        self.preprocess()

        idf_dict_hyp = get_idf_dict(self._predictions)
        idf_dict_ref = get_idf_dict(self._references)
        self._scores = word_mover_score(self._references, self._predictions, idf_dict_ref, idf_dict_hyp, stop_words=["."], n_gram=4, remove_subwords=True)

    def preprocess(self):
        predictions_array = pd.concat([self.predictions_df, self.predictions_df, self.predictions_df], axis=1).to_numpy()
        references_array = self.references_df.to_numpy()
        self._predictions = predictions_array.reshape((np.prod(predictions_array.shape),)).tolist()
        self._references = references_array.reshape((np.prod(predictions_array.shape),)).tolist()

    def print_bad_results(self, shown_elems=3):
        idx = np.argpartition(self._scores, shown_elems)
        for i in idx[:shown_elems]:
            print("Mover Reference:     ", self._references[i], "\n")
            print("Mover Answer:     : ", self._predictions[i], "\n")
            print("Mover Row Index:     : ", self.references_df.index[int(i/3.)], "\n")
            print("------------------------------------\n") 
        
class RougeScore(Scorer):
    def __init__(self, prediction_path, reference_path):
        super().__init__(prediction_path, reference_path)
        self.compute_scores()
        
    def compute_scores(self):
        self.preprocess()
        
        scorer = rouge_scorer.RougeScorer(["rouge2"], use_stemmer=True)
        self._scores = self.data_converted.apply(lambda x: scorer.score(x['reference'], x['prediction'])["rouge2"], axis = 1, result_type = 'expand')
        self._scores.rename(columns={0: 'precision', 1: 'recall', 2: 'fmeasure'})

    def preprocess(self):
        
        self.data_converted = pd.concat([self.predictions_df, self.reference_df.iloc[:,0]], axis=1, join='inner')
        self.data_converted = self.data_converted.append([pd.concat([prediction_df, reference_df.iloc[:,1]], axis=1, join='inner'),
                                                          pd.concat([prediction_df, reference_df.iloc[:,2]], axis=1, join='inner')])
        self.data_converted.columns = ['prediction', 'reference']
