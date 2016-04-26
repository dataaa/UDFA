from glob import glob
from os.path import join
import re

################################################################################
##### dc2rad.py, v1.1                                                      #####
##### Originally written in 2015 by Paul M. Woods.                         #####
##### This script automatically generates input files for RADEX, from      #####
##### the public dark interstellar cloud code available at http://udfa.net #####
##### This code is distributed under the terms of the MIT License (MIT)    #####
#####                                                                          #
##### Copyright (c) 2015 Dr. Paul M. Woods                                     #
#####                                                                          #
#Permission is hereby granted, free of charge, to any person obtaining a copy  #
#of this software and associated documentation files (the "Software"), to deal #
#in the Software without restriction, including without limitation the rights  #
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
#copies of the Software, and to permit persons to whom the Software is         #
#furnished to do so, subject to the following conditions:                      #
#                                                                              #
#The above copyright notice and this permission notice shall be included in all#
#copies or substantial portions of the Software.                               #
#                                                                              #
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
#SOFTWARE.                                                                     #
#####                                                                      #####
################################################################################

# Turn on (1) or off (0) user interaction
interaction = 0

### User must set the following variables
# Molecule of interest or 'ALL' for all molecules for which there is collisional data
specString = 'SiS'

radexPath = '/Users/abc/Work/RATRAN/Radex/'
molecPath = '/Users/abc/Work/RATRAN/Ratran/molec/'

### User may adjust the following defaults

# Line width (km/s), cloud size (pc) and output time (yrs)
db = 1.0
cloudDiam = 1.0
outputTime = '1.000E+06'

# Convert to cm
cloudDiam = cloudDiam * 3.08567758e18

# Input file from UDFA DC code
dataFilename = 'dc.out'
ssDataFilename = 'rate13steady.state'

# Format of collision partners
elecString = 'e-'
h2String = 'H2'
hString = 'H'
heString = 'He'
hpString = 'H+'

# Get input parameters directly from user
if interaction ==1:
	specString = raw_input("Please enter species name, exactly as in Rate12: ")
	db = raw_input("Give the line width in the cloud, in km/s: ")
	db = float(db)
	cloudDiam = raw_input("Give the diameter of your cloud, in parsecs (Default is 1 pc): ")
	cloudDiam = float(cloudDiam) * 3.08567758e18
	radexPath = raw_input("Provide the absolute path to the RADEX directory, including a trailing slash: ")
	molecPath = raw_input("Provide the absolute path to the collisional data files, including a trailing slash: ")
	dataFilename = raw_input("Please enter the name of the dark cloud model datafile you would like to use: ")
	ssDataFilename = raw_input("Please enter the name of the dark cloud model steady state file you would like to use: ")
	outputTime = raw_input("Please enter the age at which you would like abundances (Default is 1.000E+06; use this format): ")

# A dictionary to convert LAMDA filenames to UDFA species names; 
# second element of the tuple is the transitions within ALMA windows. Use getTrans.py to generate these.
fileToMol = {
'13co.dat': ('','1,2,3,4,6,8'),
'29sio.dat': ('','2,3,5,6,7,8,9,10,11,15,16,19,20,21,22'),
'a-ch3oh.dat': ('CH3OH','49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691'),
'c+.dat': ('C+',''),
'c+@uv.dat': ('','1,2'),
'c17o.dat': ('','1,2,3,4,6,8'),
'c18o.dat': ('','1,2,3,4,6,8'),
'c2h_h2_e.dat': ('C2H','1,2,3,4,5,6,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,95,96,97,98,99,100,101,102,103,104,105'),
'catom.dat': ('C','1,2'),
'ch3cn.dat': ('CH3CN',''),
'cn.dat': ('CN','1,2,3,4,5,6,7,8,9,10,11,15,16,17,18,19,20,21,22,23'),
'co.dat': ('CO','1,2,3,4,6,7,8'),
'co@neufeld.dat': ('','1,2,3,4,6,7,8'),
'co@old.dat': ('','1,2,3,4,6,7,8'),
'cs@lique.dat': ('CS','2,3,5,6,7,8,9,10,13,14,17,18,19'),
'dco+@xpol.dat': ('','2,3,4,5,6,9,11,12,13'),
'e-ch3oh.dat': ('CH3OH','79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059'),
'h13cn@xpol.dat': ('','1,3,4,5,7,8,10,11'),
'h13co+@xpol.dat': ('','1,3,4,5,7,8,10'),
'hc15n@xpol.dat': ('','1,3,4,5,7,8,10,11'),
'hc17o+@xpol.dat': ('','1,3,4,5,7,8,10'),
'hc18o+@xpol.dat': ('','1,3,4,5,8,10,11'),
'hc3n.dat': ('HC3N','10,11,12,14,15,16,17'),
'hcl.dat': ('HCl','1'),
'hcl@hfs.dat': ('','1,2,3'),
'hcn.dat': ('HCN','1,3,4,5,7,8,9,10'),
'hcn@hfs.dat': ('','1,2,3,7,8,9,11,12,13,14'),
'hcn@xpol.dat': ('','1,3,4,5,7,8,9,10'),
'hco+.dat': ('HCO+','1,3,4,5,7,8,9,10'),
'hco+@xpol.dat': ('','1,3,4,5,7,8,9,10'),
'hcs+@xpol.dat': ('HCS+','2,3,5,6,7,8,10,11,15,16,19,20,21,22'),
'hdo.dat': ('','1,2,5,6,7,9,20,25,26,44,45,52,63,72,97,104,105,113'),
'hf.dat': ('HF',''),
'hnc.dat': ('HNC','1,3,4,5,7,9,10'),
'hnco.dat': ('HNCO','34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,86,87,88,93,94,95,96,97,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123'),
'n2h+@xpol.dat': ('N2H+','1,3,4,5,7,9,10'),
'n2h+_hfs.dat': ('','1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129'),
'no.dat': ('NO','253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694'),
'o-c3h2.dat': ('C3H2','20,21,22,23,24,25,26,27,28,29,30,38,39,40,41,42,43,44,45,46,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,134,135,136,137,138,139,140,141,142,143,148,149,150,151,152,153,154'),
'o-h3o+.dat': ('H3O+','3'),
'o-nh2d.dat': ('',''),
'o-nh3.dat': ('NH3',''),
'o-sic2.dat': ('SiC2','17,18,19,20,25,26,27,28,29,30,31,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78'),
'o2.dat': ('O2','33,34,35,36,38'),
'oatom.dat': ('O',''),
'ocs@xpol.dat': ('OCS','7,8,9,11,12,13,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,50,51,52,53,54,55,56,57,58,59,65,66,67,68,69,70,71,72,73,74,75,76,77,78'),
'oh+.dat': ('OH+',''),
'oh.dat': ('OH',''),
'oh2co-h2.dat': ('H2CO','2,4,5,7,8,10,11,14,15,16,17,18,28,33,39,44,48,49,50,51,56,60,70,82,83,84,89,93,94,95'),
'oh2cs.dat': ('H2CS','4,6,7,9,16,18,19,20,21,23,26,28,31,32,33,35,36,38,40,43,45,48,50,51,54'),
'oh2o@daniel.dat': ('H2O','17,32,57,90,144'),
'oh2o@rovib.dat': ('','17,38,67,112,148,218,235,254,278,410,474,527,550,635,834,850,886,1066,1164,1206,1281,1324,1458,1575,1738,1761,1846,1904,2064,2262,2369,2477,2519,2566,2686,2707,2758,2836,2880,2957,3027,3053,3212,3214,3294,3409,3440,3514,3604,3643,3749,3762,3876,4220,4347,4415,4966,4998,5031,5082,5083,5183,5224,5341,5342,5359,5401,5443,5615,5822,6193,6396,6435,6436,6481,6586,6587,6699,6857,6858,6908,7188,7317,7503'),
'oh2s.dat': ('H2S','7,9,14,17,21,35,37,42,63,66,89,95,98,103,118'),
'oh@hfs.dat': ('','51,60'),
'p-c3h2.dat': ('','19,20,21,22,23,24,25,26,27,34,35,36,37,38,39,40,41,42,43,44,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,134,135,136,137,138,139,140,148,149,150,151,152'),
'p-h3o+.dat': ('','1,5,12'),
'p-nh2d.dat': ('',''),
'p-nh3.dat': ('',''),
'ph2co-h2.dat': ('','2,3,4,5,10,13,14,16,17,20,21,24,27,30,33,34,40,43,47,50,51,54,55,67,70,75,79,84,90,91,94,95'),
'ph2cs.dat': ('','3,4,6,7,9,10,11,18,19,21,22,24,25,27,28,30,31,34,37,40,46,49,52,53'),
'ph2o@daniel.dat': ('','17,29,34,58,70,94,113'),
'ph2o@rovib.dat': ('','19,21,38,45,71,115,118,192,227,231,282,350,449,502,545,558,760,899,928,990,1060,1208,1471,1688,1705,1773,1971,1989,1990,2121,2186,2258,2386,2455,2509,2526,2551,2653,2668,2755,2756,2775,2802,2860,3120,3121,3196,3382,3453,3508,3532,3587,3752,3964,3965,4189,4224,4349,4655,4775,4805,4838,4893,5045,5257,5352,5458,5684,5901,6162,6244,6288,6289,6427,6628,6710,6848,7176,7223,7295'),
'ph2s.dat': ('','1,2,4,5,7,19,24,26,27,30,42,45,60,65,67,93,102,115'),
'sio.dat': ('SiO','2,3,5,6,7,8,9,10,11,14,15,16,19,20,21'),
'sis.dat': ('SiS','5,6,7,8,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,34,35,36,37,38,39'),
'so2.dat': ('SO2','48,49,50,51,52,53,54,55,56,57,58,59,60,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562'),
'so@lique.dat': ('SO','3,4,5,6,7,8,10,11,12,14,15,16,17,18,21,22,24,26,27,28,34,35,36,37,39,41,42,44,47,48,49,50,51,52,55,56,57,58,59,62,63,65,66,68,70,71,72,73,75,77,78,82,84,85,87,89,90,92,93,94,95,96,98,99,101,102,104,107,108,110,111,113,117,122,125,129,132,137,138,142,144,147,149,150,154,155,158,159,161,162,166,167,170,171,173,182,185,190,192,194,197,198,202,203,204,207,209,210,213,214,215,218,220,221,224,225,229,231,232,236,237,239,241,246,250,255,259,264')
}

# Set up list to hold the required species
requiredSpec = []

if specString == 'ALL':
	availableSpec = []
	molFilePaths = glob(join(molecPath,'*.dat'))
	for i, x in enumerate(molFilePaths):
		availableSpec.append(re.search(r'([^/]+$)',x).group(1))
	for x in availableSpec:
		requiredSpec.append(fileToMol[x][0])
else:
	requiredSpec.append(specString)

# Open the DC output file with 'steady state' information to retrieve some physical parameters
with open(ssDataFilename,'rb') as dataFile:
	for line in dataFile:
		if line.split()[0] == "Temperature..":
			temp = float(line.split()[1])
		if line.split()[0] == "Density..":
			dens = float(line.split()[1])
			cd = dens * cloudDiam
		if line.split()[0] == "H2":
			h2frac = float(line.split()[1])
		if line.split()[0] == "e-":
			efrac = float(line.split()[1])

# Open the DC output file with fractional abundances
dataFile = open(dataFilename, 'rb')
# Generate a list of non-empty entries (generator object)
gen = (x for x in requiredSpec if x)
for x in gen:
		specString = x

		specLoc = []
		specAbund = []

		time = []

		# Collision partners
		elecLoc = []
		elecAbund = []

		h2Loc = []
		h2Abund = []

		hLoc = []
		hAbund = []

		heLoc = []
		heAbund = []

		hpLoc = []
		hpAbund = []

		collParts = []

		# Output files (for RADEX)
		outFile = open(radexPath+specString+'.inp','w')

		# Get the location of key lines in the data file
		for num, line in enumerate(dataFile, 0):
		# Find our species of interest, and store its abundance
			if ' '+specString+' ' in line:
				specLoc.append(num)
			if len(specLoc) == 1:
				if num == specLoc[0]:
					specIndex = line.split().index(specString)
				specAbund.append(line.split()[specIndex])
		# Find the electron abundance, store it		
			if ' '+elecString+' ' in line:
				elecLoc.append(num)
			if len(elecLoc) == 1:
				if num == elecLoc[0]:
					elecIndex = line.split().index(elecString)
				elecAbund.append(line.split()[elecIndex])
		# Find the H2 number density, store it		
			if ' '+h2String+' ' in line:
				h2Loc.append(num)
			if len(h2Loc) == 1:
				if num == h2Loc[0]:
					h2Index = line.split().index(h2String)
				h2Abund.append(line.split()[h2Index])
				time.append(line.split()[0])
		# Find the H abundance, store it		
			if ' '+hString+' ' in line:
				hLoc.append(num)
			if len(hLoc) == 1:
				if num == hLoc[0]:
					hIndex = line.split().index(hString)
				hAbund.append(line.split()[hIndex])
		# Find the He abundance, store it		
			if ' '+heString+' ' in line:
				heLoc.append(num)
			if len(heLoc) == 1:
				if num == heLoc[0]:
					heIndex = line.split().index(heString)
				heAbund.append(line.split()[heIndex])
		# Find the H+ abundance, store it		
			if ' '+hpString+' ' in line:
				hpLoc.append(num)
			if len(hpLoc) == 1:
				if num == hpLoc[0]:
					hpIndex = line.split().index(hpString)
				hpAbund.append(line.split()[hpIndex])
		dataFile.seek(0)

		if len(specAbund) == 0:
			print "Species",specString,"not found."
		if len(elecAbund) == 0:
			print "Electrons",elecString,"not found."
		if len(h2Abund) == 0:
			print "Molecular hydrogen (",h2String,") not found."
			
		# Print the output .inp file in RADEX format
		# Get name of LAMDA molecular data file 
		for k, v in fileToMol.iteritems():
			if v[0] == specString:
				molFile = k
				break
		outFile.write(molFile+'\n')
		# RADEX output filename
		outFile.write(specString+'.out\n')
		# Frequency range (ALMA bands 3-10 range by default)
		outFile.write('84 950\n')
		# Kinetic temperature (K)
		outFile.write(repr(temp)+'\n')
		# Open LAMDA molecular data file, find all collision partners
		with open(molecPath+molFile,'rb') as molecFile:
			for line in molecFile:
				if ('NUMBER OF COLL' in line.upper()) and ('PARTNERS' in line.upper()):
					# Strip carriage return
					nCollPart = molecFile.next()[:-1]
				# Unfortunately LAMDA files are not standardised, and have different wording. The last 'Partner' is solely for the hf.dat file.
				if ('COLLISIONS BETWEEN' in line.upper()) or (len(re.findall(r'(COLLISION PARTNER\s+$)',line.upper())) > 0) or ('Partner' in line): #('COLLISION PARTNER' in line.upper()):
					# Get number at start of line
					collParts.append(molecFile.next().split()[0])
					print line
		outFile.write(nCollPart+'\n')
		outputIndex = time.index(outputTime)
		for i in range(0,len(collParts)):
			if collParts[i] == '1':
				outFile.write('H2\n{0:8.3e}\n'.format(float(h2Abund[outputIndex])))
			if collParts[i] == '2':
				outFile.write('p-H2\n{0:8.3e}\n'.format(0.25*float(h2Abund[outputIndex])))
			if collParts[i] == '3':
				outFile.write('o-H2\n{0:8.3e}\n'.format(0.75*float(h2Abund[outputIndex])))
			if collParts[i] == '4':
				outFile.write('e\n{0:8.3e}\n'.format(max(2.0*float(h2Abund[outputIndex])*float(elecAbund[outputIndex]),1.001e-3)))
			if collParts[i] == '5':
				outFile.write('H\n{0:8.3e}\n'.format(max(2.0*float(h2Abund[outputIndex])*float(hAbund[outputIndex]),1.001e-3)))
			if collParts[i] == '6':
				outFile.write('He\n{0:8.3e}\n'.format(max(2.0*float(h2Abund[outputIndex])*float(heAbund[outputIndex]),1.001e-3)))
			if collParts[i] == '7':
				outFile.write('H+\n{0:8.3e}\n'.format(max(2.0*float(h2Abund[outputIndex])*float(hpAbund[outputIndex]),1.001e-3)))
		# Background temperature (K)
		outFile.write('2.728\n')
		# Molecular column density (cm-3)
		outFile.write('{0:8.3e}\n'.format(2.0*float(h2Abund[outputIndex])*float(specAbund[outputIndex])*cloudDiam))
		# Line width (km/s)
		outFile.write(repr(db)+'\n')
		outFile.write('0')
		outFile.close()
dataFile.close()
print "DONE!"
