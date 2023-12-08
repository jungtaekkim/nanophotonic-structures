# Materials Library
import numpy as np

import meep as mp

from nanophotonic_structures import constants


# default unit length is 1 μm
um_scale = 1.0
um_scale = 0.001 * um_scale # it changes um_scale as 1 nm.
um_scale = constants.unit_length * um_scale # it changes um_scale as unit_length nm.

# conversion factor for eV to 1/μm [=1/hc]
eV_um_scale = um_scale / 1.23984193

# ------------------------------------------------------------------
# TiO2
# https://refractiveindex.info/?shelf=main&book=TiO2&page=Siefke

TiO2_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

TiO2_frq1 = 3.403962681155004 * um_scale
TiO2_gam1 = 0.2676646628577047 * um_scale
TiO2_sig1 = 0.3146993202049315
TiO2_frq2 = 4.729440690256998 * um_scale
TiO2_gam2 = 0.0 * um_scale
TiO2_sig2 = 2.9229032712845155
TiO2_frq3 = 3.2042794875952514 * um_scale
TiO2_gam3 = 0.25066245967954254 * um_scale
TiO2_sig3 = 0.18881024699605675
TiO2_frq4 = 3.6091661345945165 * um_scale
TiO2_gam4 = 0.2669709542039742 * um_scale
TiO2_sig4 = 0.5457833514991891

TiO2_susc = [
    mp.LorentzianSusceptibility(frequency=TiO2_frq1, gamma=TiO2_gam1, sigma=TiO2_sig1),
    mp.LorentzianSusceptibility(frequency=TiO2_frq2, gamma=TiO2_gam2, sigma=TiO2_sig2),
    mp.LorentzianSusceptibility(frequency=TiO2_frq3, gamma=TiO2_gam3, sigma=TiO2_sig3),
    mp.LorentzianSusceptibility(frequency=TiO2_frq4, gamma=TiO2_gam4, sigma=TiO2_sig4),
]

TiO2 = mp.Medium(epsilon=1.1, E_susceptibilities=TiO2_susc, valid_freq_range=TiO2_range)

# ------------------------------------------------------------------
# cSi
# https://refractiveindex.info/?shelf=main&book=Si&page=Schinke

cSi_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

cSi_frq1 = 2.9049378046646845 * um_scale
cSi_gam1 = 0.22354682828454184 * um_scale
cSi_sig1 = 1.4446589949396824
cSi_frq2 = 2.744487817739379 * um_scale
cSi_gam2 = 0.13895484344423764 * um_scale
cSi_sig2 = 1.3324582737601078
cSi_frq3 = 3.133193531536882 * um_scale
cSi_gam3 = 0.3070912576977342 * um_scale
cSi_sig3 = 2.0101051542886985
cSi_frq4 = 3.8033689256371654 * um_scale
cSi_gam4 = 0.0 * um_scale
cSi_sig4 = 1.9195723483890088
cSi_frq5 = 3.4066069612082 * um_scale
cSi_gam5 = 0.3185416670394807 * um_scale
cSi_sig5 = 3.8868818083642678

cSi_susc = [
    mp.LorentzianSusceptibility(frequency=cSi_frq1, gamma=cSi_gam1, sigma=cSi_sig1),
    mp.LorentzianSusceptibility(frequency=cSi_frq2, gamma=cSi_gam2, sigma=cSi_sig2),
    mp.LorentzianSusceptibility(frequency=cSi_frq3, gamma=cSi_gam3, sigma=cSi_sig3),
    mp.LorentzianSusceptibility(frequency=cSi_frq4, gamma=cSi_gam4, sigma=cSi_sig4),
    mp.LorentzianSusceptibility(frequency=cSi_frq5, gamma=cSi_gam5, sigma=cSi_sig5),
]

cSi = mp.Medium(epsilon=1.1, E_susceptibilities=cSi_susc, valid_freq_range=cSi_range)

# ------------------------------------------------------------------
# aSi
# https://refractiveindex.info/?shelf=main&book=Si&page=Pierce

aSi_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

aSi_frq1 = 3.5149827222777117 * um_scale
aSi_gam1 = 0.6821859794779671 * um_scale
aSi_sig1 = 1.740520746778338
aSi_frq2 = 4.318242049485203 * um_scale
aSi_gam2 = 0.0 * um_scale
aSi_sig2 = 1.619813402084383
aSi_frq3 = 3.0722412165827193 * um_scale
aSi_gam3 = 0.6336703233481144 * um_scale
aSi_sig3 = 2.247863207836874
aSi_frq4 = 2.7105978016731 * um_scale
aSi_gam4 = 0.5618595876879876 * um_scale
aSi_sig4 = 2.3627605994933543
aSi_frq5 = 1.9918024886447987 * um_scale
aSi_gam5 = 0.46568946931538735 * um_scale
aSi_sig5 = 1.006241451760267
aSi_frq6 = 2.367142904873401 * um_scale
aSi_gam6 = 0.5131089334123214 * um_scale
aSi_sig6 = 1.8982481952457901

aSi_susc = [
    mp.LorentzianSusceptibility(frequency=aSi_frq1, gamma=aSi_gam1, sigma=aSi_sig1),
    mp.LorentzianSusceptibility(frequency=aSi_frq2, gamma=aSi_gam2, sigma=aSi_sig2),
    mp.LorentzianSusceptibility(frequency=aSi_frq3, gamma=aSi_gam3, sigma=aSi_sig3),
    mp.LorentzianSusceptibility(frequency=aSi_frq4, gamma=aSi_gam4, sigma=aSi_sig4),
    mp.LorentzianSusceptibility(frequency=aSi_frq5, gamma=aSi_gam5, sigma=aSi_sig5),
    mp.LorentzianSusceptibility(frequency=aSi_frq6, gamma=aSi_gam6, sigma=aSi_sig6),
]

aSi = mp.Medium(epsilon=1.1, E_susceptibilities=aSi_susc, valid_freq_range=aSi_range)

# ------------------------------------------------------------------
# ZnO
# https://refractiveindex.info/?shelf=main&book=ZnO&page=Aguilar

ZnO_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

ZnO_frq1 = 4.792479519443894 * um_scale
ZnO_gam1 = 1.89400656066627 * um_scale
ZnO_sig1 = 0.51753371720332
ZnO_frq2 = 2.8820196187335547 * um_scale
ZnO_gam2 = 0.4534435882879744 * um_scale
ZnO_sig2 = 0.09024863392652145
ZnO_frq3 = 6.390390997677161 * um_scale
ZnO_gam3 = 3.6431490712818597 * um_scale
ZnO_sig3 = 0.3370311390715335
ZnO_frq4 = 6.417481265234065 * um_scale
ZnO_gam4 = 0.0 * um_scale
ZnO_sig4 = 0.9387460611257881

ZnO_susc = [
    mp.LorentzianSusceptibility(frequency=ZnO_frq1, gamma=ZnO_gam1, sigma=ZnO_sig1),
    mp.LorentzianSusceptibility(frequency=ZnO_frq2, gamma=ZnO_gam2, sigma=ZnO_sig2),
    mp.LorentzianSusceptibility(frequency=ZnO_frq3, gamma=ZnO_gam3, sigma=ZnO_sig3),
    mp.LorentzianSusceptibility(frequency=ZnO_frq4, gamma=ZnO_gam4, sigma=ZnO_sig4),
]

ZnO = mp.Medium(epsilon=1.1, E_susceptibilities=ZnO_susc, valid_freq_range=ZnO_range)

# ------------------------------------------------------------------
# AZO
# https://refractiveindex.info/?shelf=other&book=Al-ZnO&page=Treharne (300 nm - 900 nm)
# https://refractiveindex.info/?shelf=other&book=Al-ZnO&page=Shkondin (2000 nm - 20000 nm)

AZO_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

AZO_frq0 = 1.0 * um_scale
AZO_gam0 = 0.13718868148713007 * um_scale
AZO_sig0 = 1.0494120013404664
AZO_frq1 = 4.959451345573931 * um_scale
AZO_gam1 = 0.0 * um_scale
AZO_sig1 = 0.6326883076059766
AZO_frq2 = 4.958452461092521 * um_scale
AZO_gam2 = 0.0 * um_scale
AZO_sig2 = 0.6172353978504751
AZO_frq3 = 4.959469675570231 * um_scale
AZO_gam3 = 0.0 * um_scale
AZO_sig3 = 0.37821115810450057
AZO_frq4 = 3.1809831165604514 * um_scale
AZO_gam4 = 0.44623994942384954 * um_scale
AZO_sig4 = 0.10767517516788606
AZO_frq5 = 4.955152661999414 * um_scale
AZO_gam5 = 0.0 * um_scale
AZO_sig5 = 0.5257836653155247

AZO_susc = [
    mp.DrudeSusceptibility(frequency=AZO_frq0, gamma=AZO_gam0, sigma=AZO_sig0),
    mp.LorentzianSusceptibility(frequency=AZO_frq1, gamma=AZO_gam1, sigma=AZO_sig1),
    mp.LorentzianSusceptibility(frequency=AZO_frq2, gamma=AZO_gam2, sigma=AZO_sig2),
    mp.LorentzianSusceptibility(frequency=AZO_frq3, gamma=AZO_gam3, sigma=AZO_sig3),
    mp.LorentzianSusceptibility(frequency=AZO_frq4, gamma=AZO_gam4, sigma=AZO_sig4),
    mp.LorentzianSusceptibility(frequency=AZO_frq5, gamma=AZO_gam5, sigma=AZO_sig5),
]

AZO = mp.Medium(epsilon=1.1, E_susceptibilities=AZO_susc, valid_freq_range=AZO_range)

# ------------------------------------------------------------------
# ITO
# https://refractiveindex.info/?shelf=other&book=In2O3-SnO2&page=Konig

ITO_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

ITO_frq0 = 1.0 * um_scale
ITO_gam0 = 0.00740939088475533 * um_scale
ITO_sig0 = 2.232057795017662
ITO_frq1 = 4.389462324641558 * um_scale
ITO_gam1 = 0.0 * um_scale
ITO_sig1 = 0.531824572553752
ITO_frq2 = 5.250376782483699 * um_scale
ITO_gam2 = 0.0 * um_scale
ITO_sig2 = 0.31931457570121946
ITO_frq3 = 6.339353681021138 * um_scale
ITO_gam3 = 0.0 * um_scale
ITO_sig3 = 0.12631750307952902
ITO_frq4 = 10.311475001958657 * um_scale
ITO_gam4 = 0.0 * um_scale
ITO_sig4 = 1.5819418789374073
ITO_frq5 = 3.68183547898561 * um_scale
ITO_gam5 = 0.43914396431231845 * um_scale
ITO_sig5 = 0.20642108313393856

ITO_susc = [
    mp.DrudeSusceptibility(frequency=ITO_frq0, gamma=ITO_gam0, sigma=ITO_sig0),
    mp.LorentzianSusceptibility(frequency=ITO_frq1, gamma=ITO_gam1, sigma=ITO_sig1),
    mp.LorentzianSusceptibility(frequency=ITO_frq2, gamma=ITO_gam2, sigma=ITO_sig2),
    mp.LorentzianSusceptibility(frequency=ITO_frq3, gamma=ITO_gam3, sigma=ITO_sig3),
    mp.LorentzianSusceptibility(frequency=ITO_frq4, gamma=ITO_gam4, sigma=ITO_sig4),
    mp.LorentzianSusceptibility(frequency=ITO_frq5, gamma=ITO_gam5, sigma=ITO_sig5),
]

ITO = mp.Medium(epsilon=1.1, E_susceptibilities=ITO_susc, valid_freq_range=ITO_range)

# ------------------------------------------------------------------
# GaAs
# https://refractiveindex.info/?shelf=main&book=GaAs&page=Rakic

GaAs_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

GaAs_frq1 = 4.612147114837906 * um_scale
GaAs_gam1 = 0.0 * um_scale
GaAs_sig1 = 1.4819608112369491
GaAs_frq2 = 2.575947604986498 * um_scale
GaAs_gam2 = 0.37398901410686 * um_scale
GaAs_sig2 = 1.5909776128517523
GaAs_frq3 = 2.9690110147467776 * um_scale
GaAs_gam3 = 0.7194944334495252 * um_scale
GaAs_sig3 = 1.8206736419683736
GaAs_frq4 = 2.3702596888558176 * um_scale
GaAs_gam4 = 0.20887618263022947 * um_scale
GaAs_sig4 = 0.8906711753603344
GaAs_frq5 = 3.7195975123809424 * um_scale
GaAs_gam5 = 0.7237123927253203 * um_scale
GaAs_sig5 = 4.162419732091599

GaAs_susc = [
    mp.LorentzianSusceptibility(frequency=GaAs_frq1, gamma=GaAs_gam1, sigma=GaAs_sig1),
    mp.LorentzianSusceptibility(frequency=GaAs_frq2, gamma=GaAs_gam2, sigma=GaAs_sig2),
    mp.LorentzianSusceptibility(frequency=GaAs_frq3, gamma=GaAs_gam3, sigma=GaAs_sig3),
    mp.LorentzianSusceptibility(frequency=GaAs_frq4, gamma=GaAs_gam4, sigma=GaAs_sig4),
    mp.LorentzianSusceptibility(frequency=GaAs_frq5, gamma=GaAs_gam5, sigma=GaAs_sig5),
]

GaAs = mp.Medium(epsilon=1.1, E_susceptibilities=GaAs_susc, valid_freq_range=GaAs_range)

# ------------------------------------------------------------------
# CH3NH3PbI3
# https://refractiveindex.info/?shelf=other&book=CH3NH3PbI3&page=Phillips

CH3NH3PbI3_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

CH3NH3PbI3_frq1 = 1.5987050730555856 * um_scale
CH3NH3PbI3_gam1 = 0.2929631542188442 * um_scale
CH3NH3PbI3_sig1 = 0.16605241105999183
CH3NH3PbI3_frq2 = 5.8487559687442605 * um_scale
CH3NH3PbI3_gam2 = 0.0 * um_scale
CH3NH3PbI3_sig2 = 0.6750081953170926
CH3NH3PbI3_frq3 = 2.9046596361554458 * um_scale
CH3NH3PbI3_gam3 = 0.6525767013296309 * um_scale
CH3NH3PbI3_sig3 = 0.4623436688187648
CH3NH3PbI3_frq4 = 1.887332642512735 * um_scale
CH3NH3PbI3_gam4 = 0.4199078790695697 * um_scale
CH3NH3PbI3_sig4 = 0.2402683079268417
CH3NH3PbI3_frq5 = 4.005841133877313 * um_scale
CH3NH3PbI3_gam5 = 0.5131919178893565 * um_scale
CH3NH3PbI3_sig5 = 0.8486278536950237
CH3NH3PbI3_frq6 = 2.569052087148723 * um_scale
CH3NH3PbI3_gam6 = 0.7184005029729414 * um_scale
CH3NH3PbI3_sig6 = 0.6070355247082725
CH3NH3PbI3_frq7 = 9.128486989154181 * um_scale
CH3NH3PbI3_gam7 = 0.0 * um_scale
CH3NH3PbI3_sig7 = 0.8010707136339789
CH3NH3PbI3_frq8 = 7.099751466574845 * um_scale
CH3NH3PbI3_gam8 = 0.0 * um_scale
CH3NH3PbI3_sig8 = 0.11003249593278348

CH3NH3PbI3_susc = [
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq1, gamma=CH3NH3PbI3_gam1, sigma=CH3NH3PbI3_sig1),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq2, gamma=CH3NH3PbI3_gam2, sigma=CH3NH3PbI3_sig2),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq3, gamma=CH3NH3PbI3_gam3, sigma=CH3NH3PbI3_sig3),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq4, gamma=CH3NH3PbI3_gam4, sigma=CH3NH3PbI3_sig4),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq5, gamma=CH3NH3PbI3_gam5, sigma=CH3NH3PbI3_sig5),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq6, gamma=CH3NH3PbI3_gam6, sigma=CH3NH3PbI3_sig6),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq7, gamma=CH3NH3PbI3_gam7, sigma=CH3NH3PbI3_sig7),
    mp.LorentzianSusceptibility(frequency=CH3NH3PbI3_frq8, gamma=CH3NH3PbI3_gam8, sigma=CH3NH3PbI3_sig8),
]

CH3NH3PbI3 = mp.Medium(epsilon=1.1, E_susceptibilities=CH3NH3PbI3_susc, valid_freq_range=CH3NH3PbI3_range)

# ------------------------------------------------------------------
# fused silica
# https://refractiveindex.info/?shelf=glass&book=fused_silica&page=Malitson

fusedsilica_range = mp.FreqRange(min=um_scale / constants.wavelength_solar[1] * 1000, max=um_scale / constants.wavelength_solar[0] * 1000)

fusedsilica_frq0 = 1.0 * um_scale
fusedsilica_gam0 = 23.41164202963599 * um_scale
fusedsilica_sig0 = 1.2299394250786793
fusedsilica_frq1 = 6.843099809302946 * um_scale
fusedsilica_gam1 = 0.0 * um_scale
fusedsilica_sig1 = 0.862697275980768
fusedsilica_frq2 = 3.329518916200986 * um_scale
fusedsilica_gam2 = 3.8871099922202483 * um_scale
fusedsilica_sig2 = 0.12104749555323233

fusedsilica_susc = [
    mp.DrudeSusceptibility(frequency=fusedsilica_frq0, gamma=fusedsilica_gam0, sigma=fusedsilica_sig0),
    mp.LorentzianSusceptibility(frequency=fusedsilica_frq1, gamma=fusedsilica_gam1, sigma=fusedsilica_sig1),
    mp.LorentzianSusceptibility(frequency=fusedsilica_frq2, gamma=fusedsilica_gam2, sigma=fusedsilica_sig2),
]

fusedsilica = mp.Medium(epsilon=1.1, E_susceptibilities=fusedsilica_susc, valid_freq_range=fusedsilica_range)
