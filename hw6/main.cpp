#include <iostream>
#include <string>

#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "hw6.hpp"
#include "image.hpp"

int main(){
	/*

	1) Loads the original image stanford.jpg and computes and outputs the sharpness.
    2) For kernel sizes of 3, 7, . . . , 23, 27 reload the original image by instantiating 
    a new instance of yourimage class, 
        - blur the image
        - compute and output the sharpness of the resulting image.
        - store each blurred version of the image 	

	*/

	std::string orig_file = "stanford.jpg";
    std::string img_file;


    image img =  image(orig_file);

    unsigned int sharpness = img.Sharpness();
    int kernel_size = 3;

    std::cout << "Original image: " << sharpness << std::endl;
	
    while (kernel_size <= 27){
        img = image(orig_file);

        img.BoxBlur(kernel_size);
        if (kernel_size < 10){
            img_file = "BoxBlur0" + std::to_string(kernel_size) + ".jpg";
        }else{
            img_file = "BoxBlur" + std::to_string(kernel_size) + ".jpg";
        }

        img.Save(img_file);

        sharpness = img.Sharpness();

        if (kernel_size < 10){
            std::cout << "BoxBlur( " << kernel_size << "): "<< sharpness << std::endl;
        }else{
            std::cout << "BoxBlur(" << kernel_size << "): "<< sharpness << std::endl;
        }
        

        kernel_size += 4;
    }

    return 0;
}