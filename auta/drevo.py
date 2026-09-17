# -*- coding: utf-8 -*-
"""Prida WOOD (slot 0x24) do always_refittable_cargos u 0x0083 TAZ 1203 valnik drevo."""
import io, re
p="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad/krok5/sprites/VWT1.yagl"
L=io.open(p,encoding="utf-8").read().split("\n")
# najdi blok vozidla 0x0083
zac=None
for i,l in enumerate(L):
    if re.match(r'properties<RoadVehicles, 0x0083>', l): zac=i; break
assert zac is not None, "vozidlo 0x0083 nenalezeno"
konec=next(i for i in range(zac+1,len(L)) if L[i]=="}")
# v tom bloku uprav seznam nakladu
cil=[i for i in range(zac,konec) if "always_refittable_cargos:" in L[i]]
assert len(cil)==1, cil
i=cil[0]
m=re.search(r'always_refittable_cargos: \[([^\]]*)\]', L[i])
sloty=[int(x,16) for x in m.group(1).split()]
print("pred:  %d slotu, WOOD(0x24) %s" % (len(sloty), "je" if 0x24 in sloty else "chybi"))
assert 0x24 not in sloty
# vloz 0x24 na spravne misto (seznam je vzestupny), zbytek necham presne jak je
poz=next(k for k,s in enumerate(sloty) if s>0x24)
novy=sloty[:poz]+[0x24]+sloty[poz:]
L[i]=re.sub(r'always_refittable_cargos: \[[^\]]*\]',
            "always_refittable_cargos: [ %s ]" % " ".join("0x%02X"%s for s in novy), L[i])
print("po:    %d slotu, WOOD(0x24) vlozen za 0x%02X pred 0x%02X" % (len(novy), novy[poz-1], novy[poz+1]))
io.open(p,"w",encoding="utf-8").write("\n".join(L))
