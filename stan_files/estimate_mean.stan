data{
	int N;
	real vals[N,N];
}
parameters{
	real mu[N];
}
model{
	#mu ~ normal(0, 2);
	for(i in 1:N){
	      vals[i] ~ normal(mu, 1);
	}
}