#include <string>
#include <iostream>

#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "hw6.hpp"
#include "image.hpp"


image::image(std::string filename){
		this->input_file = filename;
		ReadGrayscaleJPEG(filename, img);
}

void image::Save(std::string filename)
{
	if (!filename.empty()){
		WriteGrayscaleJPEG(filename, this->img);
	}else{
		WriteGrayscaleJPEG(this->input_file, this->img);
	}
}

void image::Convolution(boost::multi_array<unsigned char,2>& input,
				boost::multi_array<unsigned char,2>& output,
				boost::multi_array<float,2>& kernel)
{
	// check initial conditions
	if (input.shape()[0] != output.shape()[0] || input.shape()[1] != output.shape()[1] 
		|| kernel.shape()[0] != kernel.shape()[1] || kernel.shape()[0] < 3 || kernel.shape()[0]%2 == 0){
		std::cerr << "ERROR: heck the input data for correctness";
		exit(1);
	}
	int k_size = (int) kernel.shape()[0];
	float val;
	int i_broad, j_broad;
	int m = (int)input.shape()[0];
	int n = (int)input.shape()[1];
	float max_char_val = 255;
	float min_char_val = 0;

	// matrix of size m x n
	for (int i=0; i < m; i++){
		for (int j=0; j < n; j++){
			val = 0;
			// slide a kernel and compute the inner product for k x k window

			for (int ki=0; ki < k_size; ki++){
				for (int kj=0; kj < k_size; kj++){
					// truncate the values that exceed the original matrix size

					i_broad = std::max(0, std::min(m-1, i - (k_size-1)/2 + ki));
					j_broad = std::max(0, std::min(n-1, j - (k_size-1)/2 + kj));
					val += kernel[ki][kj] * (float)input[i_broad][j_broad];
				}
			}

			output[i][j] = (unsigned char) std::max(min_char_val, std::min(val, max_char_val));
		}
	}

}

void image::BoxBlur(int kernel_size)
{
	// blurs the original image with given filter size
	float val = 1.0f/((float) (kernel_size * kernel_size));

	// populate kernel
	boost::multi_array<float,2> kernel(boost::extents[kernel_size][kernel_size]);
	for (int ki=0; ki < kernel_size; ki++){
		for (int kj=0; kj < kernel_size; kj++){
			kernel[ki][kj] = val;
		}
	}

	boost::multi_array<unsigned char,2> img2 = img;
	// use convolution for smooth out the img
	this->Convolution(img2, img, kernel);
}

unsigned int image::Sharpness()
{
	// create Laplacian kernel
	boost::multi_array<float,2> kernel(boost::extents[3][3]);
	for (int ki=0; ki < 3; ki++){
		for (int kj=0; kj < 3; kj++){
			if ((ki + kj) % 2 == 1){
				kernel[ki][kj] = 1;
			}else{
				kernel[ki][kj] = 0;
			}
		}
	}
	kernel[1][1] = -4;

	boost::multi_array<unsigned char,2> img2 = img;
	// use convolution to compute sharpness of the img
	this->Convolution(img2, img, kernel);

	unsigned int sharpness = (unsigned char) *std::max_element( img.origin(), img.origin() + img.num_elements());

	return sharpness;
}

	