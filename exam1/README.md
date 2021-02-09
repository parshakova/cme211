Language choice
1. low level - since the response rate is fast, high perfomance needed
2. high level - because the computation is done slowly and speeding up the code by seconds or miliseconds does not make a difference 
3. high level - easy to debug and check functionality
4. high level is ok, since there is not many views, so speed optimized implementation is not necessary
5. low level - high perfomance is necessary and fast response rate


Data types
1. integer
2. floating point
3. floating 
4. integer
5. floating


Loops
1. for
2. for
3. while
4. for
5. for


Sequence types
1. tuple
2. dictionary
3. tuple
4. list
5. dictionary


Conditionals
since we compute random number twice, i.e. the random number in the first bin is not the same as in the second bin
the fist bin gets 35% of data, and the second bin gets 65% * 85%=55%, and the third bin get the resulting 65% - 55% = 10%

for the method to work, we need to fix random number,i.e.

nvalues = 10000
histogram = [0, 0, 0]
for n in range(nvalues):
	u = random.random()
	if u < 0.35:
		histogram[0] += 1
	elif u < 0.85:
		histogram[1] += 1
	else:
		histogram[2] += 1



Mutable or immutable
it is a partly mutable type, since we can change the value in a[1] & a[2]
b = a creates a new alias for the container a, namely a and b reference same object
since we can change the value of the last item, i.e. b[-1]
however, we do not  know if a[0] can be muted
