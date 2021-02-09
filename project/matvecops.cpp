#include <vector>
#include <iostream>
#include <math.h>
#include <fstream>
#include <string>

#include "matvecops.hpp"


/* 
	Matrix vector multiplication
	Matrix in CSR format 
*/
std::vector<double> matvec_mult(std::vector<double> &val,
             std::vector<int>    &i_idx,
             std::vector<int>    &j_idx,
             std::vector<double> &x){

	unsigned int m = (unsigned int)i_idx.size() - 1;
	unsigned int i, k, cur_col;
	std::vector<double> res(m, 0.0);

	for ( i=0; i < i_idx.size()-1; i++){
		// go over the rows of matrix A
		for (k=(unsigned int)i_idx[i]; k < (unsigned int)i_idx[i+1]; k++){
			cur_col = (unsigned int)j_idx[k];
			res[i]  +=  val[k] * x[cur_col];
		}
	}
	return res;
}


/* 
	Dot product of two vectors
*/
double dotprod(std::vector<double> &val1,
				 std::vector<double> &val2){

	double res = 0.;

	for ( unsigned int i=0; i < val1.size(); i++){
		res  += val1[i] * val2[i] ;
	}
	return res;
}


/* 
	sum of two vectors
*/
std::vector <double> sumvec(std::vector<double> &val1,
				 std::vector<double> &val2){

	std::vector <double> res(val1.size(), 0.);

	for ( unsigned int i=0; i < val1.size(); i++){
		res[i]  = val1[i] + val2[i] ;
	}
	return res;
}


/* 
	v1 <- v1 + v2 
*/
void sumvec_in(std::vector<double> &val1,
				 std::vector<double> &val2){

	for ( unsigned int i=0; i < val1.size(); i++){
		val1[i]  = val1[i] + val2[i] ;
	}
}


/* 
	Modify v1 
	v1 <- v1 + alpha*v2
*/
void v1_alpha_v2(std::vector<double> &v1,
				std::vector<double> &v2,
				 double alpha){

	std::vector <double> alpha_v2 = alphavec(v2, alpha);
	sumvec_in(v1, alpha_v2);
}


/* 
	v1 <- alpha * v1 
*/
void alphavec_in(std::vector<double> &val1,
				 double alpha){

	for ( unsigned int i=0; i < val1.size(); i++){
		val1[i]  = val1[i] *  alpha ;
	}
}


/* 
	Dot product of two vectors
*/
std::vector <double> alphavec(std::vector<double> &val1,
				 double alpha){

	std::vector <double> res(val1.size(), 0.);

	for ( unsigned int i=0; i < val1.size(); i++){
		res[i]  = val1[i] *  alpha ;
	}
	return res;
}


/* 
	L2 norm of a vector
*/
double L2norm(std::vector<double> &val){

	double res = dotprod(val, val);
	res = sqrt(res);
	return  res;
}

void StoreSolution(int n_iter, std::string soln_prefix, std::vector<double> &u_n)
{
	std::string store_file, cur_iter;
	std::ofstream f;
	unsigned int i;
	
	cur_iter = std::to_string(n_iter);
	cur_iter.insert(cur_iter.begin(), 3-cur_iter.length(), '0');
	store_file = soln_prefix + cur_iter + ".txt";

    f.open(store_file);
    for ( i=0; i < u_n.size(); i++)
    {
    	f << u_n[i] << std::endl ;
    }
    f.close();
}
