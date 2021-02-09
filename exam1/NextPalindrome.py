
def NextPalindrome(palindrome):
	# center digit
	mid = palindrome // 100 % 10
	s = str(palindrome)
	if mid < 9:
		# we can simply increment the center digit
		out =  int (s[:2]+str(mid+1)+s[3:])
	else:
		# deal with 0's
		mid2 = int(s[1])
		if mid2 < 9:
			# increase second and 4-th digits
			out = int(s[0] + str(mid2+1)+'0'+ str(mid2+1)+ s[-1])
		else:
			# increase the 1st and 5th digits
			out = int(str(int(s[0])+1) + '000'+ str(int(s[-1])+1))
	return out