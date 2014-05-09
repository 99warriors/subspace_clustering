import pandas as pd


def get_gaussian_subspace_model_init(data, n_clusters, n_dim):
    init_d = {\
              'cluster_means':pd.DataFrame({i:[0.0 for x in xrange(n_dim)] for i in xrange(n_clusters)}),\
              'cluster_variances':pd.DataFrame({i:[1.0 for x in xrange(n_dim)] for i in xrange(n_clusters)}),\
              'background_mean':[0.0 for x in xrange(n_dim)],\
              'background_variance':[1.0 for x in xrange(n_dim)],\
              'specificities':pd.DataFrame({i:[0.2 for x in xrange(n_dim)] for i in xrange(n_clusters)}),\
              'pis':[1.0/n_clusters for x in xrange(n_clusters)],\
              }
    return init_d


def get_gaussian_subspace_model_traces(num_iters, num_chains, seed, init_d, n_clusters, data, hypers):
    """
    hypers should be in dictionary form, read to pass to pystan
    parallel version would map this function partialed with only seed undetermined to a list of seeds, then reduce the results
    returns list of dictionary of param_name:traces
    """
    
    import crime_pattern.constants as constants

    stan_file = '%s/%s' % (constants.stan_folder, 'gaussian_subspaces.stan')
    N, n_dim = len(data), len(iter(data).next())
    import pystan
    pystan_data = hypers.copy()
    pystan_data['d'] = data
    pystan_data['N'] = N
    pystan_data['n_dim'] = n_dim
    pystan_data['n_clusters'] = n_clusters

    if init_d == None:
        fit = pystan.stan(file=stan_file, data=pystan_data, seed = seed, iter=num_iters, chains=num_chains, verbose=True)
    else:
        fit = pystan.stan(file=stan_file, data=pystan_data, seed = seed, iter=num_iters, chains=num_chains, verbose=True, init=[init_d for i in xrange(num_chains)])
    return fit.extract()
