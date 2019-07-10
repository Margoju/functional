#!/bin/python3

import os
import re
import glob

currdir = os.getcwd() + "/"

def generate(params):
    fir = []
    sec = []
    ats = []
    st = open(currdir + "tmp_input", "r")
    beg = st.readlines()
    st.close()
    start = beg[:beg.index(" $mndft\n")+1]
    for i in start:
        if len(re.findall("%\w+%", i)) > 0:
            i = re.sub("%\w+%", "{}", i)
        fir.append(i)
    f_part = "".join(fir)
    part = beg[beg.index(" $mndft\n")+1:beg.index(" $end\n")-1]
    search = beg[beg.index(" $end\n")-1]
    if search == "  ASMX=.T.\n":
        del part[1:7]
        del params[1:7]
    for i in range(len(params)):
        result = re.sub("%\w+%", str(params[i]), part[i])
        sec.append(result)
    s_part = "".join(sec)    
    pars = (f_part + s_part + search + " $end\n $data\n")

    at = open(currdir + "mg3s.gbs", "r")
    all_text = at.readlines()
    at.close()
    for l in all_text:
        res = re.match("-\w.", l)
        if res != None:
            ats.append(res.group(0).replace("-", "").replace(" ", ""))
    nums = [str(float(i)) for i in range(1,19)]
    nums.append("40.0")
    dic = dict(zip(ats, nums))

    for f in glob.glob(currdir + "MGAE109" + "/*.xyz"):
        name = f.split('/')[-1].split(".")[0]
        mc = open(f[:-3] + "g09", "r")
        multch = mc.readlines()
        ind = [x for x in multch if len(re.findall("\d \d", x)) > 0][0].split()
        mc.close()
        if ind[1] == '1':
            scftyp = "RHF"
        else:
            scftyp = "UHF"
        pars = pars.format(scftyp, ind[1], ind[0], "HUCKEL")
        fin = open(f, "r")
        xyz = fin.readlines()[2:]
        fin.close()
        stroc = [s for s in xyz if len(re.findall("\w.", s)) > 0]
        nach = []
        for k in stroc:
            k = k.split()
            number = dic.get(k[0])
            k.insert(1, number)
            pak = " ".join(k)
            nach.append(pak)
        geom = "\n".join(nach)
        alls = (pars + name + "\nC1\n" + geom + "\n $end")
        fil = open(currdir + "calc/" + name + ".inp", "w")
        fil.write(alls)
        fil.close()
        
        


params = [
  0.27000000000000E+00,
   .13232606370554E+00,
  -.68582715146028E-03,
  0.14901187899946E-01,
  0.00000000000000E+00,
  0.00000000000000E+00,
  0.00000000000000E+00,
  -.27415390000000E+01,
  -.67201130000000E+00,
  -.79326880000000E-01,
  0.19186810000000E-02,
  -.20329020000000E-02,
  0.00000000000000E+00,
  0.49059450000000E+00,
  -.14373480000000E+00,
  0.23578240000000E+00,
  0.18710150000000E-02,
  -.37889630000000E-02,
  0.00000000000000E+00,
  0.58779430000000E+00,
  -.13717760000000E+00,
  0.26823670000000E+00,
  -.25158980000000E+01,
  -.29788920000000E+01,
  0.87106790000000E+01,
  0.16881950000000E+02,
  -.44897240000000E+01,
  -.32999830000000E+02,
  -.14490500000000E+02,
  0.20437470000000E+02,
  0.12565040000000E+02,
  0.37415390000000E+01,
  0.21870980000000E+03,
  -.45312520000000E+03,
  0.29364790000000E+03,
  -.62874700000000E+02,
  0.50940550000000E+00,
  -.14910850000000E+01,
  0.17239220000000E+02,
  -.38590180000000E+02,
  0.28450440000000E+02 ]


generate(params)