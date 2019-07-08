#!/bin/python3

import os
import re
import glob

currdir = os.getcwd() + "/"

def generate(params):
    fir = []
    sec = []
    st = open(currdir + "dft-rhf-param.inp", "r")
    beg = st.readlines()
    st.close()
    start = beg[:beg.index(" $mndft\n")+1]
    f_part = "".join(start)
    f = open(currdir + "tmp_input", "r")
    text = f.readlines()
    f.close()
    part = text[text.index("$mndft\n")+1:text.index("$end\n")-1]
    part2 = text[text.index("$end\n")-1:-1]
    for i in range(len(params)):
        result = re.sub("%\w+%", str(params[i]), part[i])
        sec.append("  " + result)
    s_part = "".join(sec)
    fin_part = "".join(part2)
    for f in glob.glob(currdir + "MGAE109" + "/*.g09"):
        print(f) 
    alls = f_part + s_part + fin_part
    
        
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