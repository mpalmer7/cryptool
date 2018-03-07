#fuzzer
#the idea of this script is to automatically generate test cases to test the tool
#and eventually implement machine learning

import sys

if (len(sys.argv) != 4):
	print("Usage: python fuzzer <input> <num characters> <output>\n")
	sys.exit()
	
print("Arguments: ", end='')
for arg in sys.argv:
	print("%s, " % arg, end='')
print("")




#c code I wrote to port and change to fit this program's needs
'''
int main(int argc, char** argv) {
	if (argc != 5) {
		printf("Usage is: ./fuzzer <input> <num characters> <output>\n");
		return 0;
	}
	
	//read input data, get size of file
	FILE* input = fopen(argv[1], "rb");
	fseek(input, 0, SEEK_END);
	long file_size = ftell(f);
	fseek(input, 0, SEEK_SET);
	
	char* data = malloc(file_size); //allocate memory with filesize
	
	//need to check if valid pointer and not null data
	if (data == NULL) {
		printf("Failed to allocate memory\n");
		return 0;
	}
	
	//read the data
	fread(data, 1, filesize, input);
	fclose(input);
	
	unsigned int num_characters = atoi(argv[2]);
	srand(time(0) ^ getpid());	
	/*time seeded and increments by seconds, include pid so we can call this function faster
	otherwise would return same number
	*/
	
	for (int i = 0; i < num_characters; i++) {
		unsigned int idx = rand() % file_size;	//modulus, restrict to length of file
		unsigned char value = rand();	//want any char
			
		data[idx] = value;	
	}

	//output
	FILE* f = fopen(argv[3], "wb");
	fwrite(data, 1, file_size, f);
	fclose(f);
	return(0);
}
'''