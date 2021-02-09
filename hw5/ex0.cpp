#include <iostream>
#include <string>
#include <iostream>
#include <fstream>



//int main(int argc, char *argv[]){
int main(int argc, char *argv[]){
	int a = 2, b = -3, c = -7;

	int* d = &c;
	int& e = a;
	int f   = b*c;
	int g   = *&a;
	int* h = a;	

	std::cout << "d" << d << "\ne" << e << "\nf" << f << "\ng" << g << "\nh" << h << std::endl;



	return 0;
}