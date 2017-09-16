
import	glob
#import	pathlib
import	os.path
import	re

mlfile_ns	=	[]
for ml in glob.glob ("./includes/*.ml", recursive = True):
	mlfile_ns.append (ml)

#print (mlfile_ns)
mlfiles	=	{}
for ml in mlfile_ns:
	#print	(ml)
	f	=	open(ml, "r", encoding="utf-8")
	#parts	=	pathlib.Path(ml).name
	key	=	os.path.splitext(os.path.basename(ml))[0]
	text	=	f.read()
	mlfiles[key]	=	text
	f.close()
#for k in mlfiles.keys():
#	print (k, "=>", mlfiles[k], "\n------------------")

for ht in glob.glob ("./ht/**", recursive = True):
	if not ht.endswith(".ht"):
		continue
	print	("Processing: ", ht)
	f	=	open(ht, "r", encoding="utf-8")
	ftext	=	f.read().split("\n")
	n_ht	=	ht[4:]
	print (n_ht)
	ndx	=	0
	#collect the macros from the head of the file
	macros	=	{"!htmlroot!" : "./", "!htmlpath!" : "./html/"}
	while (ftext[ndx] and ftext[ndx][0] == "!"):
		lin	=	ftext[ndx].split("\t", 1)
		if len(lin) != 2 or lin[0][-1] != "!":
			print	("Macro replace error in: ", ht, "\n\t", lin)
			exit (93)
		macros[lin[0]]	=	lin[1]
#		print	(macros)
		ndx	=	ndx + 1
#	if ftext[ndx].rfind("\n") >= 0:
#		print	("ftext [", ndx, "] contains a carriage return\n\t", ftext[ndx])
#	print	("mlfiles.keys() = ", mlfiles.keys(),)
#	for k in mlfiles.keys():
#		print	("key = ", k, ", mlfiles[key] = ", repr(mlfiles[k]), "\n")
	
	##	Note:  This doesn't allow include files to be recursive.  Good?  Bad?
	ftext	=	"\n".join(ftext[ndx : -1])
	for k in mlfiles.keys():
		ftext	=	ftext.replace ("!!" + k + "!", mlfiles[k])
	for k in mlfiles.keys():
		if ftext.find ("!!" + k + "!") >= 0:
			print	('ftext.find ("!!" + k + "!") = ', ftext.find ("!!" + k + "!"))
			print	("Recursive include file detected for !!" + k + "!, aborting")
			print	(ftext)
			exit	(94)
	
	print	("macros = ", repr(macros) )
	#	replace the macros
	for k in macros.keys():
		ftext	=	ftext.replace(k, macros[k])
	print	(macros["!htmlpath!"])
	print	(n_ht)
#	n_html	=	"./html/" + macros["!htmlpath!"]+n_ht + "ml"
	n_html	=	"./html" + n_ht + "ml"
	print	("now writing: ", n_html)
	fhtml	=	open(n_html, "w")
	fhtml.write(ftext)
#	print	(ftext)
#	print	(macros)
#	print ("\n-----------------\n")

		
	
