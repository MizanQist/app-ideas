import json,sys
FX=1330
SPEED=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
RAISE=35e6
# use of funds (one-off / prepaid, all funded by the raise)
USE={'equipment':17.2e6,'software6m':4.8e6,'rent2y':10e6,'devs6m':3e6}
# hires after the first 2 devs: (month, monthly salary) paid from revenue; on-cost 15% for later hires
H=[(3,400e3),(4,350e3),(5,300e3),(6,450e3),(7,400e3),(8,350e3),(9,600e3),(10,400e3),(11,350e3),(12,800e3),
   (12,400e3),(13,350e3),(14,450e3),(14,400e3),(15,350e3),(15,600e3),(16,400e3),(16,350e3),(17,450e3),(17,800e3),(18,400e3)]
def pts(m,p):
    for (a,x),(b,y) in zip(p,p[1:]):
        if a<=m<=b: return x+(y-x)*(m-a)/(b-a)
    return p[-1][1]
# client counts (international retainers, Nigerian retainers); month 0 = today
IR=[(0,0.3),(6,6),(12,17),(18,37)]
NR=[(0,1),(6,5),(12,9),(18,12)]
def ipj(m): return 0 if m<=1 else 0.25 if m<=3 else 1.0 if m<=9 else 1.5
rows=[];cash=RAISE-sum(USE.values())  # buffer left after prepaid items? no: salaries/software drawn monthly
cash=RAISE; spent_setup=USE['equipment']
cash-=spent_setup+USE['rent2y']  # paid up front
soft_left=USE['software6m']; dev_left=USE['devs6m']
cum=0
for m in range(1,19):
    mm=m*SPEED if SPEED!=1 else m
    ir=pts(mm,IR); nr=pts(mm,NR)
    rev=(ir*2000*FX + ipj(mm)*6000*FX + nr*600e3)*0.95  # +1m small Nigerian projects, 5% bad debt
    if SPEED!=1: hires=[s for (hm,s) in H if hm/SPEED<=m]
    else: hires=[s for (hm,s) in H if hm<=m]
    devs=2*250e3
    later=sum(hires)*1.15
    founders=0 if m<=6 else (1.0e6 if m<=12 else 2.0e6)
    software=800e3*(1+0.04*len(hires))
    ops=450e3+80e3*len(hires)  # power/diesel, internet, utilities
    mkt=0.12*rev; comm=0.10*rev*0.85; free=0.12*rev; fees=0.03*rev
    office=0 if m<10 else 1.5e6
    cost=devs+later+founders+software+ops+mkt+comm+free+fees+office
    # prepaid items reduce cash only once (already), so for months 1-6 devs and software are covered by the raise allocation
    cash_cost=cost
    cash+=rev-cash_cost
    cum+=rev
    rows.append(dict(m=m,staff=2+len(hires)+2,ir=round(ir),nr=round(nr),rev=rev,cost=cost,net=rev-cost,cash=cash,runrate_usd=rev*12/FX))
for r in rows: print(r['m'],r['staff'],r['ir'],r['nr'],f"rev {r['rev']/1e6:.1f} cost {r['cost']/1e6:.1f} net {r['net']/1e6:.1f} cash {r['cash']/1e6:.1f} runrate ${r['runrate_usd']/1e3:.0f}k")
print("cum rev ₦%.0fm ($%.0fk)"%(cum/1e6,cum/FX/1e3))
m1_6=[r for r in rows if r['m']<=6]; m7_12=[r for r in rows if 6<r['m']<=12]; m13=[r for r in rows if r['m']>12]
for n,g in (('M1-6',m1_6),('M7-12',m7_12),('M13-18',m13)):
    rv=sum(r['rev'] for r in g); c=sum(r['cost'] for r in g); print(n,f"rev ₦{rv/1e6:.0f}m cost ₦{c/1e6:.0f}m profit ₦{(rv-c)/1e6:.0f}m ({(rv-c)/rv:.0%})")
print("min cash ₦%.1fm"%(min(r['cash'] for r in rows)/1e6))
json.dump(rows,open(f'model2_{SPEED}.json','w'))
