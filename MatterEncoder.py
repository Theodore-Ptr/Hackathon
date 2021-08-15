class MatterEncoder(BaseEstimator, TransformerMixin):
    '''
    This class encodes the matters with goldsilver separation and respect to platemark
    '''
    def __init__(self, drop=True):
        BaseEstimator.__init__(self)
        TransformerMixin.__init__(self)
        self.drop = drop
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X['matter'] += X['platemark']
        X = pd.get_dummies(X,columns=['matter'])
        if self.drop == True
            return X.drop('platemark', axis=1)
        return X
