#!/usr/bin/env python
import os
import sys

filename = "password.x.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p"

while filename!="password":
	os.system("unzip "+filename)
	#os.system("rm "+filename)
	filename = filename[:-2]
	print(filename)