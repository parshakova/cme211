import sys
import time

def cos_similarity(all_movies, a, b, user_thresh):
	users_a = set(all_movies[a].keys())
	users_b = set(all_movies[b].keys())
	# get set of users that ranked both movies
	users_ab = users_a.intersection(users_b)

	if len(users_ab) < user_thresh:
		return None, None
	ra = []; rb = []
	for user in users_ab:
		ra = ra + [all_movies[a][user]]
		rb = rb + [all_movies[b][user]]
	mean_ra = (sum(ra)*1.0)/len(ra)
	mean_rb = (sum(rb)*1.0)/len(rb)
	numer, denom1, denom2 = cossim_extra(ra, rb, mean_ra, mean_rb)
	
	cos_sim = numer / ((denom1 * denom2*1.0)**0.5+1e-06)
	return cos_sim, len(users_ab)

def cossim_extra(ra, rb, mean_ra, mean_rb):
	numer = sum([ (ra[i] - mean_ra)*(rb[i] - mean_rb) for i in range(len(ra))])
	denom1 = sum([ (ra[i] - mean_ra)**2 for i in range(len(ra))])
	denom2 = sum([ (rb[i] - mean_rb)**2 for i in range(len(rb))])
	return numer, denom1, denom2

def add_entry_cossim(cossim_movies, a, b, cos_sim, n_us):
	if a in cossim_movies:
		if cossim_movies[a][1] < cos_sim:
			cossim_movies[a] = (b, cos_sim, n_us)
	else:
		cossim_movies[a] = (b, cos_sim, n_us)


# print instruction when not enough arguments given
if len(sys.argv) not in [3, 4]:
	print("Usage:\n$ python3 similarity.py <data_file> <output_file> [user_thresh (default = 5)]")
	sys.exit()

# parse the command line arguments
user_thresh = 5
if len(sys.argv)== 4:
	data_file, output_file, user_thresh = sys.argv[1:]
	user_thresh = int(user_thresh)
else:
	data_file,output_file = sys.argv[1:]

print("Input MovieLens file: %s"%data_file)
print("Output file for similarity data: %s"%output_file)
print("Minimum number of common users: %d"%user_thresh)


f = open(data_file, "r")
# a dictionary containing the mapping
# {..., movie_i : {..., user_j:review_j, ...}, ...}
movie_dict = dict()
all_users = set()
for i, line in enumerate(f):
	iuser, imovie, irating, _ = list(map(int,line.split()))
	all_users.add(iuser)
	if imovie in movie_dict:
		# since every user can give a single review to a movie
		movie_dict[imovie][iuser] = irating
	else:
		movie_dict[imovie] = {iuser:irating}

f.close()
total_lines = i+1
all_movies = list(movie_dict.keys())
all_movies.sort()
nmovies = len(all_movies)
print("Read %d lines with total of %d movies and %d users"%(total_lines, nmovies, len(all_users)))

start_time = time.time()

# {..., movie a: (movie b, cos sim, number of common users), ...}
cossim_movies = dict()
# consider unique pairs of movies (a,b)
for i in range(nmovies):
	for j in range(i+1, nmovies):
		a = all_movies[i]
		b = all_movies[j]
		cos_sim, n_us = cos_similarity(movie_dict, a, b, user_thresh)
		if cos_sim == None:
			continue
		add_entry_cossim(cossim_movies, a, b, cos_sim, n_us)
		add_entry_cossim(cossim_movies, b, a, cos_sim, n_us)


print("Computed similarities in %.3f seconds"%(time.time() - start_time))


# movie a: (movie b, cos sim, number of common users)
with open(output_file, "w") as f:
	for i in range(nmovies):
		a = all_movies[i]
		if a in cossim_movies:
			line = str(a) + " "+str(cossim_movies[a])
		else:
			line = str(a)
		f.write("%s\n"%line)




