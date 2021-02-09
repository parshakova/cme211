CXX := g++
CXXFLAGS := -O3 -std=c++11 -Wall -Wconversion -Wextra -pedantic

CPPFLAGS := -DDEBUG

TARGET := main
OBJS := main.o hw6.o image.o 
INCS := hw6.hpp image.hpp 

LDFLAGS := -ljpeg

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)

# this is a make pattern rule
%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)