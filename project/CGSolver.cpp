#include <vector>
#include <math.h>
#include <iostream>
#include <string>

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

/*

Ax = b

where A is in CSR format.  The starting guess for the solution
is provided in x, and the solver runs a maximum number of iterations
equal to the size of the linear system.  

Return the number of iterations to converge the solution to the specified
tolerance, or -1 if the solver did not converge.

*/
int CGSolver(SparseMatrix &A,
             std::vector<double> &b,
             std::vector<double> &u_n,
             double              tol,
             std::string soln_prefix){
	
	// number of equations = number of rows
	int niter_max = (int)b.size(); 
	int n_iter = 0;
	int stop_n = -1;
	double alpha, norm_r0, norm_r_np1, pAp, beta, norm_rn_2;
	std::vector<double> r_n, p_n, Ap, p_np1;
	bool flag = false;

	norm_r_np1 = 0;

	StoreSolution(n_iter, soln_prefix, u_n);

	r_n = b;
	Ap = A.MulVec(u_n);
	//modify r_n = b - Au_0 
	alpha = -1.0;
	v1_alpha_v2(r_n, Ap, alpha); // modify r_n inplace
	norm_r0 = L2norm(r_n);

	p_n = r_n; // deep copy of r_n

	int freq_store = 10;

	while (n_iter < niter_max && flag == false)
	{

		Ap = A.MulVec(p_n);
		pAp =  dotprod(p_n, Ap);
		norm_rn_2 = dotprod(r_n, r_n);
		alpha = norm_rn_2 / pAp; 

		// u_np1 = u_n + alpha * p_n
		v1_alpha_v2(u_n, p_n, alpha); // modify u_n inplace

		if ((n_iter+1) % freq_store == 0){
			// store current solution
			StoreSolution(n_iter+1, soln_prefix, u_n);
		}


		// r_np1 = r_n - aplpha * Ap
		alpha = (-1.0) * alpha;
		v1_alpha_v2(r_n, Ap, alpha); // modify r_n inplace

		norm_r_np1 = L2norm(r_n);

		if ( norm_r_np1 / norm_r0 < tol) {
        	// terminate the loop
        	stop_n = n_iter+1;
        	flag = true;
        	continue;
		}

		beta = pow(norm_r_np1, 2.0) / norm_rn_2;
		p_np1 = r_n;
		v1_alpha_v2(p_np1, p_n, beta); // modify p_np1 inplace

		p_n = p_np1;

		n_iter += 1;	

	}
	// store current solution
	StoreSolution(n_iter+1, soln_prefix, u_n);

	return stop_n;

}
