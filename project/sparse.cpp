#include <vector>
#include <iostream>

#include "sparse.hpp"
#include "COO2CSR.hpp"

#include "matvecops.hpp"

void SparseMatrix::Resize(int nrows, int ncols)
{
    this->ncols = ncols;
    this->nrows = nrows;
}

/* Method to add entry to matrix in COO format */
void SparseMatrix::AddEntry(int i, int j, double val)
{
    // assuming that we are filling up the matrix and a, i_idx,j_idx are COO format
    this->i_idx.push_back(i);
    this->j_idx.push_back(j);
    this->a.push_back(val);
}

/* Method to convert COO matrix to CSR format using provided function */
void SparseMatrix::ConvertToCSR()
{
    // Get CSR from COO
    COO2CSR(this->a, this->i_idx, this->j_idx); 
}

/* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
std::vector<double> SparseMatrix::MulVec(std::vector<double> &vec)
{
    std::vector<double> Av = matvec_mult(this->a, this->i_idx, this->j_idx, vec);
    return Av;
}
