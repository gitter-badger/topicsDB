from os import listdir
from os.path import isfile, join, exists

DIR = './'
PATH =  DIR 
DADOS = PATH + '/DADOS'
INPUT = PATH + 'INPUTS/'
campos = []
#dado retirado da tabela de refencia do dados aberto para docente
TS_DOCENTES_REF = [5, 13, 3, 3, 5, 4, 1, 1, 1, 4, 3, 2, 9, 3, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 6, 2, 2, 5, 5, 2, 
100, 9, 1, 4, 6, 2, 2, 5, 5, 2, 100, 9, 1, 4, 6, 2, 2, 5, 5, 2, 100, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 3, 3, 4,
9, 9, 3, 2, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

TS_ESCOLA = [5,9,100,10,15,1,20,20,3,2,9,9,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,1,1,1]

DCO = DADOS + '/Docentes Centro-Oeste'
DND = DADOS + '/Docentes Nordeste'
DNR = DADOS + '/Docentes Norte'
DSD = DADOS + '/Docentes Sudeste'
DSU = DADOS + '/Docentes Sul'
ESC = DADOS + '/TURMA'

repositorio = { 
	'PATH' : PATH,
	'DADOS' : DADOS,
	'INPUT' : INPUT,
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
	# print valores
	# for txt in arq.readlines() :
	txt = line
	# txt = txt.replace(" ","_")
	ind = 0
	campos = '('
	for a in ref[1]:
		# print a[1]
		if ind != 0 :
			campos += ','
		# print int(a[1])
		if ref[0][ind] == 3:
			campos += "'"+txt[:int(a[1])].strip()+"'"
		else:
			campos += txt[:int(a[1])].strip()
		ind += 1
		txt = txt[int(a[1]):]
		
	print campos + '),'

def extractNum(str):
	num = '';
	for x in str : 
		if x.isdigit() :
			num += x
	return num

def generatorDDL(path, f):
	arq = open(path + "/" + f,'r')

	txt = ''.join(arq.readlines())

	#txt = txt[txt.startswith('INPUT') + 7 : ]

	ddl = []
	ddl.append("--")
	ddl.append("-- " + f)
	ddl.append("--")
	ddl.append("CREATE TABLE " + f[:-4].lower() + "(")

	FKS = []
	PKS = [] # Nao eh possivel reestabelecer a chave estrangeira

	field = []
	nome = []

	# gerando as colunas 
	for line in txt.split("\n") :
		campos = line.split("\t")
		if len(campos) == 4 and campos[0].strip() != "FORMAT":

			n_campo = campos[1].lower().strip()

			nome.append([n_campo, extractNum(campos[2])])

			if n_campo.startswith('fk_') :
				FKS.append(n_campo)
		
			if n_campo.startswith('pk_') :
				PKS.append(n_campo)

			info_c = n_campo.strip()

			if campos[2][0].isdigit() : 
				info_c += ' numeric'
				field.append(1)
			else :
				info_c += ' varchar(256)'
				field.append(3)
			info_c += ' NOT NULL,'

			ddl.append(info_c)

	# gerando a lista de chaves primarias
	pk_nome = "pk"
	pk_campos = ""
	i = 0
	for pk in PKS :
		if i != 0 :
			pk_campos += ", "
		pk_nome += pk.replace("pk","")
		pk_campos += pk
		i += 1

	ddl.append("CONSTRAINT " + pk_nome + " PRIMARY KEY(" + pk_campos.strip() + ")")

	ddl.append(");")
	# print ddl
	# print FKS

	return {'DDL' : ddl, 'CAMPO' : [field, nome]}

def inputs():
	ddls = []
	for f in listdir(repositorio['INPUT']) :
		if  f[-4:] == ".sas" and isfile(join(repositorio['INPUT'],f)) :
			ddls.append(generatorDDL(repositorio['INPUT'], f))
	return ddls
	# for element in ddls:
	# 	k = 0
	# 	t = len(element['DDL'])
	# 	for ddl in element['DDL']:
	# 		imp = ""
	# 		if k > 3 and k != t - 1:
	# 			imp += '\t'
	# 		imp += ddl
	# 		print imp
	# 		k += 1
	# 	print ''

def main():
	global campos 
	campos = inputs()[3]['CAMPO']	
	# Printando informacoes
	# for element in ddls:
	# 	k = 0
	# 	t = len(element['DDL'])
	# 	for ddl in element['DDL']:
	# 		imp = ""
	# 		if k > 3 and k != t - 1:
	# 			imp += '\t'
	# 		imp += ddl
	# 		print imp
	# 		k += 1
		# print ''


	# for mypath in repositorio['ESCOLAS'] :
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
					# lines = arq.readlines()
					# for ln in lines:
					# miner(lines[0], repositorio["REFERENCIA"][1])
					# arq = open(mypath + "/" + f,'r')
					lines = arq.readlines()
					# for ln in lines:
					miner(lines[0], campos)


main()
