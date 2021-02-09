#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <math.h>

#include "heat.hpp"
#include "sparse.hpp"
#include "CGSolver.hpp"


/* Method to setup Ax=b system */
int HeatEquation2D::Setup(std::string inputfile)
{
    int i, j, ki, kj, k, ni, nj;
    int m, n;
    float length, width, h, Tc, Th, val, x;

    // load (length, width, h, Tc, Th)
    std::fstream f;
    try{
        f.open(inputfile);
        if (f.is_open()){
            f >> length >> width >> h;
            f >> Tc >> Th;
        }
        f.close();
    }catch (std::exception e) {
        return -1;
    }

    if ( fabs(round(length/h) - length/h)>1e-5 || fabs(round(width/h) -width/h) >1e-5 ){
        return -1;
    }

    m = (int) round(length/h);
    n = (int) round(width/h);

    ni = m-1; // since u is periodic in x
    nj = n-2; // since top and low values of u are defined by Th and Tc

    // initialize x = 0
    this->x.resize(ni*nj, 0.0f);
    this->b.resize(ni*nj, 0.0f);

    // construct matrix A that approximates heat equation and vector b
    for (k=0; k < ni*nj; k++)
    {
        i = k % ni;
        j = k / ni;
        ki = k; // row in matrix A
        this->A.AddEntry(ki, ki, 4.f);
        val = 0.0f; // b[k]
        if (i == 0){
            // u_i-1,j is computed from u_m-2,j
            kj = (m-2) + j*ni;   
        }else{
            kj = (i-1) + j*ni;
        }
        this->A.AddEntry(ki, kj, -1.f);

        if (i == ni-1){
            // u_i+1,j is computed from u_0,j
            kj = 0 + j*ni;   
        }else{
            kj = (i+1) + j*ni;
        }
        this->A.AddEntry(ki, kj, -1.f);  

        if (j == 0){
            // u_i,j-1 is computed Gaussian temperature
            x = ((float)i)*h;
            val = (float) (-Tc*(exp(-10*pow(( x - length/2), 2)) - 2));   
        }else{
            kj = i + (j-1)*ni;
            this->A.AddEntry(ki, kj, -1.f);
        }

        if (j == nj-1){
            // u_i,j+1 is computed from Th
            val = Th;   
        }else{
            kj = i + (j+1)*ni;
            A.AddEntry(ki, kj, -1.f);
        }
        this->b[k] = val; 
        //std::cout << i << " " << j << " " << val <<"\n";          
    }

    this->A.ConvertToCSR();
    return 0;
}

/* Method to solve system using CGsolver */
int HeatEquation2D::Solve(std::string soln_prefix)
{

    double tol = 1.e-5;

    int niter = CGSolver(this->A, this->b, this->x, tol, soln_prefix);

    if (niter == -1){
        return -1;
    }
    std::cout << "SUCCESS: CG solver converged in "<< niter <<" iterations.\n";
    return 0;
}
