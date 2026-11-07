"""Ejemplo de grupos y pares de kerning UFO para un proyecto latino. Adapta los valores a tu diseño: no los copies.

Los valores se decidieron mirando las pruebas de este proyecto, no se midieron en ninguna
fuente ajena. Los grupos son iguales en todos los másteres; los pares también, para que no
aparezcan jorobas al interpolar.
"""
A = "A Agrave Aacute Acircumflex Atilde Adieresis Aring".split()
E = "E Egrave Eacute Ecircumflex Edieresis AE OE".split()
O = "O Ograve Oacute Ocircumflex Otilde Odieresis Oslash".split()
U = "U Ugrave Uacute Ucircumflex Udieresis".split()
Y = "Y Yacute Ydieresis".split()
a = "a agrave aacute acircumflex atilde adieresis aring".split()
o = "o ograve oacute ocircumflex otilde odieresis oslash".split()
e = "e egrave eacute ecircumflex edieresis".split()
u = "u ugrave uacute ucircumflex udieresis".split()
y = "y yacute ydieresis".split()

IZQ = {  # kern1: el glifo va primero; cuenta su lado derecho
    "A": A, "D": ["D", "Eth"] + O + ["Q"], "C": ["C", "Ccedilla"], "E": E, "F": ["F"], "J": ["J"] + U,
    "K": ["K", "X"], "L": ["L"], "P": ["P", "Thorn"], "R": ["R"], "S": ["S"], "T": ["T"], "V": ["V", "W"],
    "Y": Y, "Z": ["Z"],
    "n": ["a", "d", "h", "i", "l", "m", "n", "q", "u"] + a[1:] + u[1:] + ["ntilde", "dotlessi", "iacute"],
    "o": ["b", "p", "thorn"] + o + e + ["ae", "oe"], "c": ["c", "ccedilla"], "f": ["f"], "k": ["k", "x"], "r": ["r"],
    "s": ["s"], "t": ["t"], "v": ["v", "w"] + y, "z": ["z"],
    "punto": ["period", "comma", "ellipsis", "quotesinglbase", "quotedblbase"],
    "guion": ["hyphen", "endash", "emdash", "uni00AD", "uni2010"],
    "cierra": ["quoteright", "quotedblright", "quotesingle", "quotedbl"], "abre": ["quoteleft", "quotedblleft"],
    "gder": ["guillemotright", "guilsinglright"], "gizq": ["guillemotleft", "guilsinglleft"],
    "apertura": ["exclamdown", "questiondown"], "paren": ["parenleft", "bracketleft", "braceleft"],
}
DER = {  # kern2: el glifo va segundo; cuenta su lado izquierdo
    "A": A + ["AE"], "O": ["C", "Ccedilla", "G", "Q", "OE"] + O, "S": ["S"], "T": ["T"], "U": U, "V": ["V", "W"], "Y": Y,
    "J": ["J"], "X": ["X"], "Z": ["Z"],
    "o": ["c", "ccedilla", "d", "g", "q", "oe", "ae"] + a + o + e, "n": ["m", "n", "p", "r", "ntilde"], "u": u, "s": ["s"], "t": ["t"], "f": ["f"],
    "v": ["v", "w"] + y, "x": ["x"], "z": ["z"], "j": ["j", "uni0237"],
    "punto": ["period", "comma", "ellipsis", "quotesinglbase", "quotedblbase"],
    "guion": ["hyphen", "endash", "emdash", "uni00AD", "uni2010"],
    "cierra": ["quoteright", "quotedblright", "quotesingle", "quotedbl"], "abre": ["quoteleft", "quotedblleft"],
    "gizq": ["guillemotleft", "guilsinglleft"], "gder": ["guillemotright", "guilsinglright"],
    "pcierra": ["parenright", "bracketright", "braceright"], "preg": ["question", "exclam"],
}
PARES = """
T: o-92 n-56 u-56 s-82 v-46 x-46 z-60 punto-92 guion-72 gizq-60 A-72 J-64 O-20 preg10
F: o-32 n-14 A-64 punto-96 J-46 s-18
P: A-72 punto-112 o-22 J-52 s-10 guion-20
V: A-62 o-48 n-22 u-20 s-36 punto-82 guion-36 gizq-30 O-14 J-30 preg14
Y: A-62 o-72 n-38 u-34 s-52 punto-92 guion-62 gizq-52 O-22 J-44 preg14
A: T-72 V-62 Y-66 U-14 O-18 v-30 t-16 cierra-62 abre-40 preg-20 gder-10
L: T-84 V-82 Y-84 O-26 U-20 v-42 cierra-96 abre-70 guion-52 gizq-20
K: O-34 o-24 u-16 v-34 guion-44 gizq-26 s-12
R: T-20 V-16 Y-24 O-8 o-8
D: A-26 T-20 V-18 Y-30 X-26 Z-12 J-16 punto-42 cierra-12
C: O-10 guion-16
S: V-10 Y-14 T-10
E: guion-14 o-6
J: A-14 punto-16
Z: O-14 o-8 guion-36
n: T-60 V-30 Y-50 cierra-14 v-6
o: T-82 V-42 Y-68 v-10 x-16 z-6 cierra-20 punto-16
c: T-44 V-16 Y-34
f: o-12 punto-40 cierra34 abre26 guion-20 pcierra30 preg30 s-6
k: o-20 s-8 guion-28
r: punto-74 o-14 guion-34 v10 x8 z-6 s-6 T-20
s: T-54 V-20 Y-44
t: o-6 guion-16 T-16
v: o-12 s-6 punto-54 guion-14 T-40 V-10 Y-20
z: o-8 T-30
punto: cierra-64 abre-40 T-82 V-74 Y-84 v-42 O-14 guion-20
guion: T-72 V-36 Y-62 A-16 X-28 Z-30 J-30
gder: T-58 V-30 Y-52 A-12
gizq: Y-10
cierra: A-64 o-44 s-30 n-12 punto-84 J-50
abre: A-52 o-22 J-40 V10 Y10 T10
apertura: T-44 V-38 Y-46 A6 J-10 v-14
paren: j34 J20 O-8
"""


def aplica(u, escala):
    u.groups.clear(); u.kerning.clear()
    presentes = set(u.keys())
    for nom, lista in IZQ.items():
        u.groups[f"public.kern1.{nom}"] = [g for g in lista if g in presentes]
    for nom, lista in DER.items():
        u.groups[f"public.kern2.{nom}"] = [g for g in lista if g in presentes]
    for linea in PARES.strip().splitlines():
        izq, resto = linea.split(":")
        for t in resto.split():
            i = next(k for k, ch in enumerate(t) if ch in "-0123456789")
            der, v = t[:i], int(t[i:])
            u.kerning[(f"public.kern1.{izq}", f"public.kern2.{der}")] = round(v * escala)
