
# coding: utf-8

# Github for imbalance learning:
# https://github.com/scikit-learn-contrib/imbalanced-learn
# 
# Useful articles:
# 强推： https://www.analyticsvidhya.com/blog/2017/03/imbalanced-classification-problem/
# http://contrib.scikit-learn.org/imbalanced-learn/stable/over_sampling.html#smote-variants
# https://quantdare.com/what-is-the-difference-between-bagging-and-boosting/
# 
# 处理数据平衡问题的两个大方向：
# 1. 通过采样方法来平衡数据
#     a. over-sampling  (这是我们以下会用到的方法)
#     b. under-sampling
# 2. 通过混合不同的模型来减少数据不平衡带来的影响

# In[2]:

#1. read data   
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from decimal import *
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.datasets import make_classification


ads = pd.read_csv('./round1_ijcai_18_train_20180301.txt', sep=" ")


# In[ ]:




# In[ ]:

#采样前删除掉干扰的列，例如ID
# 原始数据列数：27
ads.columns


# ['instance_id', 'item_id', 'item_category_list', 'item_property_list', 'item_brand_id', 'item_city_id', 'item_price_level', 'item_sales_level', 'item_collected_level', 'item_pv_level', 'user_id', 'user_gender_id', 'user_age_level', 'user_occupation_id', 'user_star_level', 'context_id', 'context_timestamp', 'context_page_id', 'predict_category_property', 'shop_id', 'shop_review_num_level', 'shop_review_positive_rate', 'shop_star_level', 'shop_score_service', 'shop_score_delivery', 'shop_score_description', 'is_trade']

# In[7]:

#先随机采样减小计算复杂度
chosen_idx = np.random.choice(len(ads), replace=False, size=1000)
sample_raw = ads.iloc[chosen_idx]

rm_col = ['instance_id', 'item_id','user_id','context_id',"item_category_list","item_property_list","predict_category_property"]
sample_raw = sample_raw.drop(rm_col, axis=1)

# sample_raw.item_category_list = sample_raw.item_category_list.str.split(";")
# sample_raw.item_property_list = sample_raw.item_property_list.str.split(";")
# sample_raw.predict_category_property  = sample_raw.predict_category_property.str.split(";")


# In[7]:




# In[ ]:




# 尝试不同的采样方法:
# @Over-sampling
#     Random minority over-sampling with replacement
# 
#     SMOTE - Synthetic Minority Over-sampling Technique 
#         SMOTE_KIND = ('regular', 'borderline1', 'borderline2', 'svm')
# 
#     SVM SMOTE - Support Vectors SMOTE
# 
#     ADASYN - Adaptive synthetic sampling approach for imbalanced learning

# In[4]:

X_reg, y_reg = sample_raw.drop(['is_trade'], axis=1),sample_raw['is_trade']

print('Original dataset shape {}'.format(Counter(y_reg)))

# 使用SMOTE采样方法平衡数据集：
sm = SMOTE(kind='regular',random_state=42)
X_res_reg, y_res_reg = sm.fit_sample(X_reg, y_reg)
print('Resampled dataset shape {}'.format(Counter(y_res_reg)))


# In[ ]:




# In[13]:

X_b1, y_b1 = sample_raw.drop(['is_trade'], axis=1),sample_raw['is_trade']

print('Original dataset shape {}'.format(Counter(y_b1)))

# 使用SMOTE采样方法平衡数据集：
sm = SMOTE(kind='borderline1',random_state=42)
X_res_b1, y_res_b1 = sm.fit_sample(X_b1, y_b1)
print('Resampled dataset shape {}'.format(Counter(y_res)))


# In[ ]:




# In[14]:

X_svm, y_svm = sample_raw.drop(['is_trade'], axis=1),sample_raw['is_trade']

print('Original dataset shape {}'.format(Counter(y_svm)))

# 使用SMOTE采样方法平衡数据集：
sm = SMOTE(kind='svm',random_state=42)
X_res_svm, y_res_svm = sm.fit_sample(X, y)
print('Resampled dataset shape {}'.format(Counter(y_res_svm)))


# Adaptive Synthetic (ADASYN) sampling method
# 针对小众数据，通过类似特征人工生成类似的数据点插入到样本中，以增大小众数据的样本数量，平衡数据。

# In[ ]:

X_ADASYN, y_ADASYN = sample_raw.drop(['is_trade'], axis=1),sample_raw['is_trade']
print('Original dataset shape {}'.format(Counter(y_ADASYN)))
X_res_ADASYN, y_res_ADASYN = ADASYN().fit_sample(X_ADASYN, y_ADASYN)
print('Resampled dataset shape {}'.format(Counter(y_res_ADASYN)))


# In[ ]:




# In[ ]:



