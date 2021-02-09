import sys
import time

if len(sys.argv) != 4:
	print('Usage:\n  $ python3 processdata.py <ref_file> <reads_file> <align_file>')
	sys.exit()


reference_file,reads_file,align_file = sys.argv[1:]
# get data from txt files
with open(reference_file, 'r') as f:
	reference = f.read()
with open(reads_file, 'r') as f:
	reads = []
	for line in f:
		reads += [line.strip()]

def find_all_alignments(ref, read):
	# find the first two alignments of reads in reference
	# if one alignment is found at position (i) then search for the next alignment 
	# starting from the position (i+1)
	align_pos = [ref.find(read)]
	if align_pos[0] != -1:
		pos = ref[align_pos[0]+1:].find(read)
		if pos != -1:
			align_pos += [pos + align_pos[0]+1]
	return align_pos

start_time = time.time()


# counts for alignment at 0 position, 1 position, 2 positions
counts = [0, 0, 0]
# list of alignments and reads
reads_alignments = []


# find alignments and keep track of their counts
for i, read in enumerate(reads):
	align = find_all_alignments(reference, read)
	
	if align[0] == -1:
		counts[0] += 1
	elif len(align) == 2:
		counts[2] += 1
	else:
		counts[1] += 1
	read_align = read+' '+' '.join(map(str, align))+'\n'
	if i == len(reads)-1:
		read_align = read_align.strip()
	reads_alignments += [read_align]

for i in range(3):
	print('aligns %d: %f'%(i, counts[i]*1.0/len(reads)))
print('elapsed time: %f'%(time.time()-start_time))

with open(align_file, 'w') as f:
	f.writelines(reads_alignments)

