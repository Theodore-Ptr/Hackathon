#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class PlatemarkTransformer(BaseEstimator, TransformerMixin):
    """
    The class provides functionality for converting matter
    with respect to platemark
    """
    
    def __init__(self, drop=False):
        """
        Initializes class instance by setting convert options. 
        
        Parameters
        ----------
        drop: bool, 
            if True, removes the original columns from the dataset.
        """
        BaseEstimator.__init__(self)
        TransformerMixin.__init__(self)
        self.drop = drop
    
    def fit(self, X, y=None):
        """
        Fit DateTransformer to X, but really do nothing.
        Return self.
        """
        return self
    
    def transform(self, X, y=None):
        """
        Transfor X using the parameters set in the constructor.
        Return transformed dataframe.
        """
        X['matter'] = X['matter'].add(str(X['platemark']))
        X = pd.get_dummies(X, columns=['matter'])
        if self.drop:
            X.drop('platemark', axis=1, inplace=True)
        return X


# In[ ]:


class NoiseCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, rate=5):
        """
        cleans instances and columns that do not have significant impact
        """
        BaseEstimator.__init__(self)
        TransformerMixin.__init__(self)
        self.rate= rate
        
    def fit(self, X, y=None):
        """
        Fit NoiseCleaner to X, but really do nothing.
        Return self.
        """
        return self
    
    
    def transform(self, X, y=None):
        clean_up_mask = X.count() >  self.rate
        for row, flag in zip(clean_up_mask.index, clean_up_mask):
            if flag == False:
                X.drop(row, axis = 1, inplace=True)
        return X


# In[ ]:


class ParseInjection(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        BaseEstimator.__init__(self)
        TransformerMixin.__init__(self)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        i = 0
        for inj in X.injection_params:
            if inj == "None":
                i += 1
                continue
            stones = dict()
            inj_strs = (inj.replace(', ', '|').replace('. ', '|')
                        .replace(';', '|').split('|'))
            for inj_substr in inj_strs:
                str_split = inj_substr.split()
                if len(str_split) < 3: 
                  continue
                if str_split[0].isdigit() and (str_split[1].isalpha() or 
                                               str_split[1] in ["Кер.кольцо", "Гор.хр"]):
                    stones.setdefault(str_split[1].lower(), 0)
                    stones[str_split[1].lower()] += int(str_split[0])
                elif any([True if "БРКр" in x else False for x in str_split]):
                    for sub in str_split:
                        if "БРКр" in sub:
                            stones.setdefault("бриллиант", 0)
                            br_num = sub.split("БРКр")[0]
                            stones["бриллиант"] += (int(br_num) if "Родий" not in sub 
                                                    else int(br_num.split("Родий")[1]))
                elif str_split[0][1:] in ["Сапфир", "Изумруд"]:
                    stones.setdefault(str_split[0][1:].lower(), 0)
                    stones[str_split[0][1:].lower()] += int(str_split[0][0])
                elif str_split[0].isdigit() and str_split[2] in ["Сапфир", "Изумруд"]:
                    stones.setdefault(str_split[2].lower(), 0)
                    stones[str_split[2].lower()] += int(str_split[0])
                elif len(str_split) > 2 and str_split[2] == "Эмаль":
                    stones.setdefault(str_split[2].lower(), 0)
                    stones[str_split[2].lower()] += int(str_split[0])
            for name, num in stones.items():
                name = name if name not in ["бр", "брилл"] else "бриллиант"
                X.loc[X.index[i], name] = num
            i += 1
        return X.drop(["injection_params"], axis=1)


# In[ ]:


class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    The class provides basic functionality for retrieving
    a subset of columns from the dataset.
    """
    
    def __init__(self, feature_names):
        """
        Initialize class instance by setting
        a list of columns to retrieve from the dataset.
        """
        BaseEstimator.__init__(self)
        TransformerMixin.__init__(self)
        self.feature_names = feature_names
        
    def fit(self, X, y=None):
        """
        Fit FeatureSelector to X, but really do nothing.
        Return self.
        """
        return self
    
    def transform(self, X, y=None):
        """
        Transform X using feature selection. 
        Return column-subset of X.
        """
        return X[self.feature_names]

