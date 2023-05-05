import tensorflow as tf
import glob


class Model:
    def __init__( self ):
        self.model = tf.keras.models.load_model( './agent/model/file/beefprince_model.h5', compile=False)
        self.y_predict = None
        
    def predict(self, preprocessed_img):
        self.y_predict = self.model.predict( preprocessed_img )
        return self.y_predict
        
