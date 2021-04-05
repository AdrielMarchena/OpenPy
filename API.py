from ctypes import *
import pathlib
import struct;

class API:
    def __init__(self):
        self.API = 0
        arquitecture = struct.calcsize("P") * 8

        if arquitecture == 64:
            self.API = CDLL(str(pathlib.Path().absolute() / "APIx64.dll"))
        if arquitecture == 32:
            self.API = CDLL(str(pathlib.Path().absolute() / "APIWin32.dll"))

    def cmult(self,x: float,y: float) -> float:
        self.API.cmult.restype = c_float
        return self.API.cmult(c_float(x),c_float(y))

    def cadd(self,x: float,y: float) -> float:
        self.API.cadd.restype = c_float
        return self.API.cadd(c_float(x),c_float(y))

    def cdiv(self,x: float,y: float) -> float:
        self.API.cdiv.restype = c_float
        return self.API.cdiv(c_float(x),c_float(y))

    def csub(self,x: float,y: float) -> float:
        self.API.csub.restype = c_float
        return self.API.csub(c_float(x),c_float(y))

    def cfat(self,x: float) -> float:
        self.API.cfat.restype = c_double
        return self.API.cfat(x)

    def point_vs_rect(self,px: float,py: float,rx: float,ry: float,rw: float,rh: float) -> bool:
        self.API.point_vs_rect.restype = c_bool
        return self.API.point_vs_rect(c_float(px),c_float(py),c_float(rx),c_float(ry),c_float(rw),c_float(rh))

    def rect_vs_rect(self,px: float,py: float,pw: float,ph: float,rx: float,ry: float,rw: float,rh: float) -> bool:
        self.API.rect_vs_rect.restype = c_bool
        return self.API.rect_vs_rect(c_float(px),c_float(py),c_float(pw),c_float(ph),c_float(rx),c_float(ry),c_float(rw),c_float(rh))

#TESTAPI float cmult(float a, float b);
#TESTAPI float cadd(float a, float b)
#TESTAPI float cdiv(float a, float b);
#TESTAPI float csub(float a, float b);
#TESTAPI double cfat(int n);
#TESTAPI bool point_vs_rect(float px, float py, float rx, float ry, float rw, float rh);
#TESTAPI bool rect_vs_rect(float px, float py, float pw, float ph, float rx, float ry, float rw, float rh);