import random
import sys
import time

if len(sys.argv) != 6:
	print('Usage:\n  $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>')
	sys.exit()

#start_time = time.time()
reference_length,nreads,read_length,reference_file,reads_file = sys.argv[1:]
reference_length = int(reference_length)
nreads = int(nreads)
read_length = int(read_length)

vocab = ['T', 'G', 'A', 'C']
copy_percent = 0.25
print("reference length: %d"%reference_length)
print('number reads: %d'%nreads)
print("read length: %d"%read_length)

def generate_sequence(seq_len):
	# generate random sequence of DNA strip
	seq = ""
	for _ in range(seq_len):
		letter = vocab[random.randint(0,len(vocab)-1)]
		seq += letter
	return seq

def make_reference(ref_len, ref_file, copy_percent):
	# make reference randomly for every character in 75% of length
	# into the last 25% copy the last part of the string
	# store ref it in txt
	ref = generate_sequence(ref_len - int(ref_len*copy_percent))
	ref = ref + ref[-int(ref_len*copy_percent):]

	#assert len(ref) == ref_len

	with open(ref_file, 'w') as f:
		f.write(ref)

	return ref

def make_reads_1(nreads, ref, read_len):
	# make reads that align once
	reads = []
	ref_len = len(ref)
	for _ in range(nreads):
		start_pos = random.randint(0, int(ref_len*0.5)-read_len)
		reads += [ref[start_pos:start_pos+read_len]+'\n']
	return reads

def make_reads_2(nreads, ref, read_len, copy_percent):
	# make reads that align twice
	# by randomly picking a starting position in the last 25% of the full reference
	reads = []
	ref_len = len(ref)
	for _ in range(nreads):
		start_pos = random.randint(ref_len - int(ref_len*copy_percent)+1, ref_len - read_len)
		reads += [ref[start_pos:start_pos+read_len]+'\n']
	return reads

def make_reads_0(nreads, ref, read_len):
	# make reads that do not align
	reads = []
	while len(reads) < nreads:
		read = generate_sequence(read_len)
		if ref.find(read) == -1:
			reads += [read+'\n']
	return reads


reference = make_reference(reference_length, reference_file, copy_percent )
reads = []
# counts for alignment at 0 position, 1 position, 2 positions
counts = [0,0,0]

# probs for alignment at: 2 positions, 0 positions, 1 position
probs = [0.1, 0.15, 0.75]

for i in range(nreads):
	numb = random.random()

	if numb < probs[0]:
		# generate reads at 2 positions
		counts[2] += 1
		reads += make_reads_2(1, reference, read_length, copy_percent)
	elif numb < probs[1]+probs[0]:
		# generate reads at 0 positions
		counts[0] += 1
		reads += make_reads_0(1, reference, read_length)
	else:
		# generate reads at 1 positions
		counts[1] += 1
		reads += make_reads_1(1, reference, read_length)

for i in range(3):
	print('aligns %d: %f'%(i, counts[i]*1.0/nreads))

#print('elapsed time: %f'%(time.time()-start_time))

with open(reads_file, 'w') as f:
	for read in reads[:-1]:
		f.write(read)
	f.write(reads[-1].strip())
