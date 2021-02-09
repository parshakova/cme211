#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>
#include <string>

/* Matrix vector multiplication */
std::vector<double> matvec_mult(std::vector<double> &val,
             std::vector<int>    &i_idx,
             std::vector<int>    &j_idx,
             std::vector<double> &x);

double dotprod(std::vector<double> &val1,
				 std::vector<double> &val2);

std::vector <double> sumvec(std::vector<double> &val1,
				 std::vector<double> &val2);

std::vector <double> alphavec(std::vector<double> &val1,
				 double alpha);

double L2norm(std::vector<double> &val);

void v1_alpha_v2(std::vector<double> &v1,
				std::vector<double> &v2,
				 double alpha);

void StoreSolution(int n_iter, std::string soln_prefix, std::vector<double> &u_n);

void StoreSolutionInt(int n_iter, std::string soln_prefix, std::vector<int> &u_n); 


#endif /* MATVECOPS_HPP */
