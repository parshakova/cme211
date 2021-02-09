#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <string>
#include <iostream>

#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "hw6.hpp"


class image
{
	std::string input_file;
	boost::multi_array<unsigned char, 2> img;
public:
	image(std::string filename);

	void Save(std::string filename);

	void Convolution(boost::multi_array<unsigned char,2>& input,
					boost::multi_array<unsigned char,2>& output,
					boost::multi_array<float,2>& kernel);

	void BoxBlur(int kernel_size);

	unsigned int Sharpness();

	
};

#endif /* IMAGE_HPP */