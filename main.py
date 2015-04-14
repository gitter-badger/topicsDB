DIR = '../'
PATH =  DIR 
DADOS = PATH + '/DADOS'
#dado retirado da tabela de refencia do dados aberto para docente

TS_DOCENTES_REF = [5, 13, 3, 3, 5, 4, 1, 1, 1, 4, 3, 2, 9, 3, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 6, 2, 2, 5, 5, 2, 
100, 9, 1, 4, 6, 2, 2, 5, 5, 2, 100, 9, 1, 4, 6, 2, 2, 5, 5, 2, 100, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 3, 3, 4,
9, 9, 3, 2, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

TS_ESCOLA = [5,9,100,10,15,1,20,20,3,2,9,9,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,1,1,1]

DCO = DADOS + '/Docentes Centro-Oeste'
DND = DADOS + '/Docentes Nordeste'
DNR = DADOS + '/Docentes Norte'
DSD = DADOS + '/Docentes Sudeste'
DSU = DADOS + '/Docentes Sul'
ESC = DADOS + '/ESCOLAS'
repositorio = { 
	'PATH' : PATH,
	'DADOS' : DADOS,
	'DOCENTES': [DCO, DND, DNR, DSD, DSU],
	'ESCOLAS' :	[ESC],
	'REFERENCIA' : [TS_DOCENTES_REF,TS_ESCOLA]
}

# def miner(arq, ref):
# 	# for txt in arq.readlines() :
# 	txt = arq.readline()
# #	txt = txt.replace(" ","_")
# 	a = 0
# 	campos = []
# 	while a < len(ref) :
# 		campos.append(txt[:ref[a]])
# 		txt = txt[ref[a]:]
# 		a += 1
# 	print campos
def miner(line, ref):
	# for txt in arq.readlines() :
	txt = line
#	txt = txt.replace(" ","_")
	a = 0
	campos = []
	while a < len(ref) :
		campos.append(txt[:ref[a]])
		txt = txt[ref[a]:]
		a += 1
	print campos[2]
from os import listdir
from os.path import isfile, join, exists

def main():

	# for mypath in repositorio['DOCENTES'] :
	# 	if exists(mypath) :
	# 		for f in listdir(mypath) :
	# 			if isfile(join(mypath,f)) :
	# 				print "#FILE: " + f; 
	# 				miner(open(mypath + "/" + f,'r'), repositorio["REFERENCIA"][0])
	for mypath in repositorio['ESCOLAS'] :
		if exists(mypath) :
			for f in listdir(mypath) :
				if isfile(join(mypath,f)) :
					print "#FILE: " + f; 
					arq = open(mypath + "/" + f,'r')
					lines = arq.readlines()
					for ln in lines:
						miner(ln, repositorio["REFERENCIA"][1])


main()
