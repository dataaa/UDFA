from glob import glob
from os.path import join

ratranPath = '/Users/pmw/Work/RATRAN/Ratran/'

# A dictionary to convert LAMDA filenames to UDFA species names
fileToMol = {
'13co.dat': '',
'29sio.dat': '',
'a-ch3oh.dat': 'CH3OH',
'c+.dat': 'C+',
'c+@uv.dat': '',
'c17o.dat': '',
'c18o.dat': '',
'c2h_h2_e.dat': 'C2H',
'catom.dat': 'C',
'ch3cn.dat': 'CH3CN',
'cn.dat': 'CN',
'co.dat': 'CO',
'co@neufeld.dat': '',
'co@old.dat': '',
'cs@lique.dat': 'CS',
'dco+@xpol.dat': '',
'e-ch3oh.dat': 'CH3OH',
'h13cn@xpol.dat': '',
'h13co+@xpol.dat': '',
'hc15n@xpol.dat': '',
'hc17o+@xpol.dat': '',
'hc18o+@xpol.dat': '',
'hc3n.dat': 'HC3N',
'hcl.dat': 'HCl',
'hcl@hfs.dat': '',
'hcn.dat': 'HCN',
'hcn@hfs.dat': '',
'hcn@xpol.dat': '',
'hco+.dat': 'HCO+',
'hco+@xpol.dat': '',
'hcs+@xpol.dat': 'HCS+',
'hdo.dat': '',
'hf.dat': 'HF',
'hnc.dat': 'HNC',
'hnco.dat': 'HNCO',
'n2h+@xpol.dat': 'N2H+',
'n2h+_hfs.dat': '',
'no.dat': 'NO',
'o-c3h2.dat': 'C3H2',
'o-h3o+.dat': 'H3O+',
'o-nh2d.dat': '',
'o-nh3.dat': 'NH3',
'o-sic2.dat': 'SiC2',
'o2.dat': 'O2',
'oatom.dat': 'O',
'ocs@xpol.dat': 'OCS',
'oh+.dat': 'OH+',
'oh.dat': 'OH',
'oh2co-h2.dat': 'H2CO',
'oh2cs.dat': 'H2CS',
'oh2o@daniel.dat': 'H2O',
'oh2o@rovib.dat': '',
'oh2s.dat': 'H2S',
'oh@hfs.dat': '',
'p-c3h2.dat': '',
'p-h3o+.dat': '',
'p-nh2d.dat': '',
'p-nh3.dat': '',
'ph2co-h2.dat': '',
'ph2cs.dat': '',
'ph2o@daniel.dat': '',
'ph2o@rovib.dat': '',
'ph2s.dat': '',
'sio.dat': 'SiO',
'sis@.dat': 'SiS',
'so2.dat': 'SO2',
'so@lique.dat': 'SO'
}

def getALMABand(mu):
	almaBands = [84.0,116.0, 125.0,163.0, 211.0,275.0, 275.0,373.0, 385.0,500.0, 602.0,720.0, 787.0,950.0]
	for i in range(0,len(almaBands)-1,2):
		if mu > almaBands[i] and mu < almaBands[i+1]:
			return True

molFilePaths = glob(join(ratranPath,'molec','*.dat'))

for x in molFilePaths:
	currentFile = open(x,'rb')
	availableTx = []
	freqFlag = 0
	for line in currentFile:
		if re.search('PARTNERS', line):
			freqFlag = 0
		if freqFlag == 1:
			if getALMABand(float(line.split()[freqIndex])):
#				print "Freq:",line.split()[freqIndex],"Tx:",line.split()[0]
				availableTx.append(line.split()[0])
		if re.search('FREQ', line):
			freqFlag = 1
			try:
				freqIndex = "".join(line.split()).split("+").index('FREQ(GHz)')
			except ValueError:
				try:
					freqIndex = "".join(line.split()).split("+").index('FREQ[GHz]')
				except ValueError:
					print "Frequency information not found in "+re.search(r'([^/]+$)',x).group(1)
	currentFile.close()
	print re.search(r'([^/]+$)',x).group(1), ",".join(availableTx)
#	if fileToMol[re.search(r'([^/]+$)',x).group(1)] != "":
#		print fileToMol[re.search(r'([^/]+$)',x).group(1)], ",".join(availableTx)