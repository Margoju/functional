#!/bin/python3

import os
import re
import shutil
import glob
import subprocess
import math

currdir = os.getcwd() + "/"

def gener_params():
    with open(currdir + "gamess.wft/source/dftxcc.src") as f:
        alls = []
        params = []
        src_str = f.read()
        st = src_str.split("C     PARAMETERS FOR M06-2X")[1:]
        for s in st:
            s = s.split("\n")[:15]
            for i in s:
                if len(re.findall("C     PARAMETERS FOR REVM06-L", i)) > 0:
                    break
                else:
                    if "=" in i:
                        alls.append(i.replace(" ", ""))
        del(alls[-1])
        for n in alls:
            ind = n.find("=")
            n = n[ind+1:]
            params.append(float(n.replace("D", "E")))
        return(params)

def gener_inp(params):
    fir = []
    sec = []
    ats = []
    st = open(currdir + "tmp_input", "r")
    beg = st.readlines()
    st.close()
    for x in range(0, len(beg)):
        if x == 3:
            beg[x] = " $basis extfil=.TRUE. $end\n"
    start = beg[:beg.index(" $mndft\n")+1]
    for i in start:
        if len(re.findall("%\w+%", i)) > 0:
            i = re.sub("%\w+%", "{}", i)
        fir.append(i)
    f_part = "".join(fir)
    part = beg[beg.index(" $mndft\n")+1:beg.index(" $end\n")-1]
    search = beg[beg.index(" $end\n")-1]
    if search == "  ASMX=.T.\n":
        del part[:7]
    for i in range(len(params)):
        result = re.sub("%\w+%", str(params[i]), part[i])
        sec.append(result)
    s_part = "  HFEX=0.54000000000000E+00\n" + "".join(sec) 
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
    path = currdir + "Databases/xyz"
    tmp_list = []
    pr = os.walk(path)
    for adress, dirs, files in pr:
        for fil in files:
            f = adress + "/" + fil
            dirname = f.split('/')[-2] + "/" + f.split('/')[-1].split(".")[0]
            path_dir = f.split('/')[-2]
            name = f.split('/')[-1].split(".")[0]
            mc = open(currdir + "Databases/g09inp/" + dirname + ".g09", "r")
            multch = mc.readlines()
            mc.close()
            ind = [x for x in multch if len(re.findall("\d \d\n", x)) > 0][0].split()
            if ind[1] == '1':
                scftyp = "RHF"
            else:
                scftyp = "UHF"
            paras = pars.format(scftyp, ind[1], ind[0], "HUCKEL")
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
            alls = (paras + name + "\nC1\n" + geom + "\n $end")
            if currdir + "calc/" + path_dir not in glob.glob(currdir + "calc/*"):
                os.mkdir(currdir + "calc/" + path_dir)
            fil = open(currdir + "calc/" + dirname + ".inp", "w")
            fil.write(alls)
            fil.close()
            scratch = currdir + "calc/" + path_dir + "/scratch"
            if scratch not in glob.glob(currdir + "calc/*/*"):
                os.mkdir(scratch)

def start_gamess():
    rast = []
    for i in glob.glob(currdir + "calc/IP13/*.inp"):
        i = i.split(".")[0]
        d = i.split("/")[5]
        genstr = "sbatch --job-name={0} /home/margoju/functional/gamess.wft/rungms {0} 00 4".format(i)
        out, err = subprocess.Popen("sgms {0} 00 4".format(i), shell=True, stdout=subprocess.PIPE).communicate()
        out = out.decode("utf-8").split()[-1]
        rast.append(out)
    rast = ":".join(rast)
    P = subprocess.Popen("srun --dependency=afterany:" + rast + " echo", shell = True)
    P.wait()

#def RMSEPB_MGAE109():
    

def RMSE_IP13():
    mols = {}
    ions = {}
    neus = {}
    out = []
    for i in glob.glob(currdir + "calc/IP13/*.log"):
        print(i)
        #dirname = i.split('/')[-2] + ";" + i.split('/')[-1].split(".")[0]

        """if dirname[-1] != "+":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                neus[dirname] = found
        if dirname[-1] == "+":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                ions[dirname] = found
    for i in neus.keys():
        z = i + "+"
        if z not in ions:
            continue
        else:
            num = (float(neus[i]) - float(ions[z]))**2
            rmse = (math.sqrt(num))*627.5095
            out.append(i + ";" + str(rmse))
    tmp_out = "\n".join(out)
    return tmp_out"""

def RMSE_EA13():
    mols = {}
    ions = {}
    neus = {}
    out = []
    for i in glob.glob(currdir + "calc/EA13/*.log"):
        dirname = i.split('/')[-2] + ";" + i.split('/')[-1].split(".")[0]
        if dirname[-1] != "-":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                neus[dirname] = found
        if dirname[-1] == "-":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                ions[dirname] = found
    for i in neus.keys():
        z = i + "-"
        if z not in ions:
            continue
        else:
            num = (float(neus[i]) - float(ions[z]))**2
            rmse = (math.sqrt(num))*627.5095
            out.append(i + ";" + str(rmse))
    tmp_out = "\n".join(out)
    return tmp_out

def RMSE_PA8():
    mols = {}
    ions = {}
    neus = {}
    out = []
    for i in glob.glob(currdir + "calc/PA8/*.log"):
        dirname = i.split('/')[-2] + ";" + i.split('/')[-1].split(".")[0]
        if dirname[-1] != "+":
            with open(i, "r") as f:
                text = f.readlines()
                print(text)
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0]
                #[1].split()[-1]
                neus[dirname] = found
                #print(neus)
        if dirname[-1] == "-":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                ions[dirname] = found
    for i in neus.keys():
        z = i + "-"
        if z not in ions:
            continue
        else:
            num = (float(neus[i]) - float(ions[z]))**2
            rmse = (math.sqrt(num))*627.5095
            out.append(i + ";" + str(rmse))
    tmp_out = "\n".join(out)
    return tmp_out

def RMSE_DBH76():
    mols = {}
    ions = {}
    neus = {}
    out = []
    dict_HTBH = dict(TS1 = 'H;HCl', TS2 = 'OH;H2', TS3 = 'CH3;H2', TS4 = 'OH;CH4', TS5 = 'H;H2', TS6 = 'OH;NH3',
     TS7 = 'HCl;CH3', TS8 = 'OH;C2H6', TS9 = 'F;H2', TS10 = 'O;CH4',
     TS11 = 'H;PH3', TS12 = 'H;OH', TS13 = 'H;H2S', TS14 = 'O;HCl',
     TS15 = 'CH3;NH2', TS16 = 'C2H5;NH2', TS17 = 'NH2;C2H6', TS18 = 'NH2;CH4')
    #TS19 don't forget!
    for i in dict_HTBH:
        with open(currdir + "calc/HTBH38/" + i + ".log", "r") as f:
            text_ts = f.readlines()
            found_ts = [x for x in text_ts if len(re.findall("TOTAL ENERGY", x)) > 0][-1].split()[-1]
        mat1 = dict_HTBH.get(i).split(";")[0]
        mat2 = dict_HTBH.get(i).split(";")[1]
        with open(currdir + "calc/HTBH38/" + mat1 + ".log", "r") as f:
            text_inp = f.readlines()
            found_inp1 = [x for x in text_inp if len(re.findall("TOTAL ENERGY", x)) > 0] [-1].split()[-1]
        with open(currdir + "calc/HTBH38/" + mat2 + ".log", "r") as f:
            text_inp = f.readlines()
            found_inp2 = [x for x in text_inp if len(re.findall("TOTAL ENERGY", x)) > 0][-1].split()[-1]
        num = (float(found_ts) - float(found_inp1) - float(found_inp2))**2
        rmse = (math.sqrt(num))*627.5095
        print(i, num)





#    for i in glob.glob(currdir + "calc/HTBH38/*.log"):
#        dirname = i.split('/')[-2] + ";" + i.split('/')[-1].split(".")[0]
#        name_db = i.split('/')[-1].split(".")[0]
        



def te():
        if dirname[-1] != "+":
            with open(i, "r") as f:
                text = f.readlines()
                print(text)
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0]
                #[1].split()[-1]
                neus[dirname] = found
                #print(neus)
        if dirname[-1] == "-":
            with open(i, "r") as f:
                text = f.readlines()
                found = [x for x in text if len(re.findall("TOTAL ENERGY", x)) > 0][1].split()[-1]
                ions[dirname] = found

def test():
    for i in neus.keys():
        z = i + "-"
        if z not in ions:
            continue
        else:
            num = (float(neus[i]) - float(ions[z]))**2
            rmse = (math.sqrt(num))*627.5095
            out.append(i + ";" + str(rmse))
    tmp_out = "\n".join(out)
    return tmp_out

def unite_st():
    for f in glob.glob(currdir + "Databases/xyz/*"):
        newdir = currdir + "calc/" + f.split('/')[-1]
        if os.path.exists(newdir):
            print(f, "YEsss")
            if len(glob.glob(newdir + "/*.inp")) == len(glob.glob(newdir + "/*.log")):
                print(f, "Y")
            else:
                print(f, "N")
        else:
            print(f, "NOoo")

#unite_st()
#params = gener_params()
#gener_inp(params)
#start_gamess()
IP13 = RMSE_IP13()
print(IP13)
#EA13 = RMSE_EA13()
#PA8 = RMSE_PA8()
#DBH76 = RMSE_DBH76()

par = """[
  0.54000000000000E+00,
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
  0.28450440000000E+02 ]"""


