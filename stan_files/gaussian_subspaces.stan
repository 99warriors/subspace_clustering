data{
	int n_dim;
	int n_clusters;
	int N;
	real d[N, n_dim];

	real prior_cluster_mean_sd;
	real prior_cluster_variance_lambda;
	real prior_background_mean_sd;
	real prior_background_variance_lambda;
	real prior_specificities_alpha;
	real prior_specificities_beta;
	vector<lower=0> [n_clusters] prior_pis_dirichlet_counts;

}

parameters{
	real cluster_means[n_dim, n_clusters];
	real<lower=0> cluster_variances[n_dim, n_clusters];
	real background_mean[n_dim];
	real<lower=0> background_variance[n_dim];
	real<lower=0,upper=1.0> specificities[n_dim, n_clusters];
	simplex[n_clusters] pis;
}

transformed parameters{

}

model{

	real temp;
	real cluster_probs[n_clusters];

	for(i in 1:n_clusters){
	      for(j in 1:n_dim){
	      	    cluster_means[j,i] ~ normal(0, prior_cluster_mean_sd);
		    cluster_variances[j,i] ~ exponential(prior_cluster_variance_lambda);
		    specificities[j,i] ~ beta(prior_specificities_alpha, prior_specificities_beta);
	      }
	}

	for(j in 1:n_dim){
	      background_mean[j] ~ normal(0, prior_background_mean_sd);
	      background_variance[j] ~ exponential(prior_background_variance_lambda);
	}


	pis ~ dirichlet(prior_pis_dirichlet_counts);


	for(k in 1:N){
	      for(i in 1:n_clusters){
	      	    // get the prob conditioned on cluster assignment
		    temp <- 0;
	      	    for(j in 1:n_dim){
		    	  //temp <- log(specificities[j,i]);// + normal_log(d[k,j], cluster_means[j,i], cluster_variances[j,i]);
	      	    	  temp <- temp + log_sum_exp(log(specificities[j,i]) + normal_log(d[k,j], cluster_means[j,i], cluster_variances[j,i]), log(1.0-specificities[j,i]) + normal_log(d[k,j], background_mean[j], background_variance[j]));
		    }
		    temp <- temp + log(pis[i]);
		    cluster_probs[i] <- temp;
	      }
	      increment_log_prob(log_sum_exp(cluster_probs));
	}
     
}