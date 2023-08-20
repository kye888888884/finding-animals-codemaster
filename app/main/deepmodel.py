from tensorflow import keras
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import urllib.request as request
from PIL import Image
from io import BytesIO
import numpy as np

class DeepModel():
    def __init__(self) -> None:
        self.cat_model = None
        self.dog_model = None
        self.load_models()

        self.pred2labelCat = {}
        self.pred2labelDog = {}
        self.load_labels()
        pass
    
    def load_models(self):
        self.cat_model = keras.models.load_model('./main/model/fin_cat.h5')
        self.cat_model.load_weights('./main/model/cat_inceptionResnet_V2_best')

        self.dog_model = keras.models.load_model('./main/model/fin_dog.h5')
        self.dog_model.load_weights('./main/model/dog_inceptionResnet_V2_best')
    
    def load_labels(self):
        self.pred2labelCat = {
            0: 'abyssinian',
            1: 'americanShorthair',
            2: 'bengal',
            3: 'britishShorthair',
            4: 'koreanShorthair',
            5: 'maineCoon',
            6: 'norwegianForest',
            7: 'persian',
            8: 'ragdoll',
            9: 'russianBlue',
            10: 'siamese',
            11: 'sphynx',
            12: 'turkishAngora'
        }
        self.pred2labelDog = {
            0: 'americanBully',
            1: 'beagle',
            2: 'bichonFrize',
            3: 'borderCollie',
            4: 'bostonTerrier',
            5: 'boxer',
            6: 'bullTerrier',
            7: 'bulldog',
            8: 'chihuahua',
            9: 'cockerSpaniel',
            10: 'corgi',
            11: 'dachshund',
            12: 'doberman',
            13: 'dosa',
            14: 'frenchBulldog',
            15: 'germanShorthairedPointer',
            16: 'greatDane',
            17: 'husky',
            18: 'italianGreyhound',
            19: 'jindo',
            20: 'maltese',
            21: 'miniaturePinscher',
            22: 'mix',
            23: 'pekingese',
            24: 'pomeranian',
            25: 'poodle',
            26: 'poongSan',
            27: 'pug',
            28: 'retriever',
            29: 'samoyed',
            30: 'sapsaree',
            31: 'schnauzer',
            32: 'shepherd',
            33: 'shiba',
            34: 'shihTzu',
            35: 'spitz',
            36: 'yorkshireTerrier'
        }

    def predict(self, img, is_cat=False):
        img_tensor = img
        img_tensor /= 255
        img_tensor = np.expand_dims(img_tensor, axis=0)
        test_image = img_tensor
        
        if is_cat:
            ## predict
            predictBreed = self.cat_model.predict(test_image)
            
        else:
            predictBreed = self.dog_model.predict(test_image)
        
        return predictBreed

    def get_rank(self, pred, is_cat=False):
        if is_cat:
            tmp = 12
        else:
            tmp = 36

        array = pred[0][0]
        temp = array.argsort()
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(array))
        ranks = list(ranks)
    
        result = []

        if is_cat:
            for i in range(len(self.pred2labelCat)):
                result.append(self.pred2labelCat[ranks.index(tmp)])
                tmp -=1
        else:
            for i in range(len(self.pred2labelDog)):
                result.append(self.pred2labelDog[ranks.index(tmp)])
                tmp -=1
        
        return result
    
    def get_similarity(self, ranks, is_cat=False):
        result = []
        return result