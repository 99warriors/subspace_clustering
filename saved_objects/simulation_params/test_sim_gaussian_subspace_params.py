"""
for each dimension, a background distribution (mu, sigma)
for each cluster:
  for each dimension:
    cluster specific distribution(mu, sigma), mixture scalar between 0,1
"""
import pandas as pd


cluster_means = pd.DataFrame({\
                              0:[-5,-5],\
                              1:[5,5],\
#                              2:[-1,-2],\
#                              3:[-2,-1]\
                          })

cluster_variances = pd.DataFrame({\
                                  0:[0.1,0.1],\
                                  1:[0.1,0.1],\
#                                  2:[2.0,1.5],\
#                                  3:[1.2,5.3]\
                              })

background_mean = pd.Series([25,25])

background_variance = pd.Series([6,6])

specificities = pd.DataFrame({\
                              0:[0.1, 0.1],\
                              1:[0.1, 0.1],\
#                              2:[0.3, 0.3],\
#                              3:[0.6, 0.2],\
                         })

pis = pd.Series([\
                         0.5,\
                         0.5,\
#                         0.3,\
#                         0.4\
                     ])


params = {'cluster_means':cluster_means, 'cluster_variances':cluster_variances, 'background_mean':background_mean, 'background_variance':background_variance, 'specificities':specificities, 'pis':pis}
