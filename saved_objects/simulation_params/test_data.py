"""
for each dimension, a background distribution (mu, sigma)
for each cluster:
  for each dimension:
    cluster specific distribution(mu, sigma), mixture scalar between 0,1
"""
import functools
import numpy as np
import numpy.random
import python_utils.utils as utils
import itertools
import pandas as pd


cluster_means = pd.DataFrame({\
                              0:[-5,-5],\
                              1:[2,3],\
                              2:[-1,-2],\
                              3:[-2,-1]\
                          })

cluster_variances = pd.DataFrame({\
                                  0:[0.1,.4],\
                                  1:[6.3,1.0],\
                                  2:[2.0,1.5],\
                                  3:[1.2,5.3]\
                              })

background_mean = pd.Series([5,5])

background_variance = pd.Series([.8,.7])

specificitys = pd.DataFrame({\
                             0:[0.8, 0.4],\
                             1:[0.3, 0.7],\
                             2:[0.1, 0.1],\
                             3:[0.3, 0.3],\
                             })

cluster_pis = pd.Series([\
                         0.1,\
                         0.2,\
                         0.3,\
                         0.4\
                     ])




background_dist = [functools.partial(np.random.normal, loc=mean, scale=variance) for mean, variance in itertools.izip(background_mean, background_variance)]

cluster_specific_dists = [\
                          [functools.partial(np.random.normal, loc=mean_coord, scale=variance_coord) for mean_coord, variance_coord in itertools.izip(cluster_mean, cluster_variance)]\
                          for (k1,cluster_mean), (k2,cluster_variance) in itertools.izip(cluster_means.iteritems(), cluster_variances.iteritems())\
                      ]

cluster_dists = [\
                          utils.tuple_f(*\
                                        [utils.mixture_dist(coord_specificity, [coord_cluster_specific_dist, coord_background_dist])\
                                         for coord_cluster_specific_dist, coord_background_dist, coord_specificity in itertools.izip(cluster_specific_dist, background_dist, specificity)]\
                                        )\
                          for cluster_specific_dist, (k,specificity) in itertools.izip(cluster_specific_dists, specificitys.iteritems())\
                      ]

sim_f = utils.mixture_dist(cluster_pis, cluster_dists)


"""

cluster_specific_dists = [\
                          [functools.partial(np.random.normal, loc = 3, scale = 0.1), functools.partial(np.random.normal, loc = 1, scale = 0.1)],\
                          [functools.partial(np.random.normal, loc = -1, scale = 1.5), functools.partial(np.random.normal, loc = 2, scale = 0.3)],\
                          [functools.partial(np.random.normal, loc = 2, scale = 0.4), functools.partial(np.random.normal, loc = -1, scale = 0.5)],\
                          [functools.partial(np.random.normal, loc = -0.5, scale = 0.5), functools.partial(np.random.normal, loc = -2, scale = 1.5)],\
                          ]





cluster_dists = [utils.tuple_f(*[utils.mixture_dist(proportion, [cluster_specific_coord_dist, background_dist]) for background_dist, cluster_specific_coord_dist, proportion in itertools.izip(background_dists, cluster_specific_dist, specificity)]) for cluster_specific_dist, specificity in itertools.izip(cluster_specific_dists, specificitys)]
    
sim_f = utils.mixture_dist(cluster_pis, cluster_dists)

"""
