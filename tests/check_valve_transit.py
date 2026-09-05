import sys,json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'src'))
from render_scene import reset,make_asset
from geometry import palette
from cardiac_motion import cardiac_cycle
m=json.loads((root/'storyboards/heart.json').read_text());results=[]
for index in [5,10,13]:
 reset();st=make_asset(m['shots'][index],palette());markers=set(st['valve_markers']);plane=0 if index==13 else .36;events=0;lowest=1.;worst=None
 for f in range(2400):
  sec=f/240;cycle=cardiac_cycle(sec);opening=cycle[2 if index==13 else 1]
  for ob,pts,phase,period in st['movers']:
   if ob not in markers:continue
   t=(sec/period+phase)%1;q=t*(len(pts)-1);j=min(int(q),len(pts)-2);z=pts[j].lerp(pts[j+1],q-j).z
   half=max(abs(v.co.z) for v in ob.data.vertices)*ob.scale.z
   if abs(z-plane)<half:
    events+=1
    if opening<lowest:lowest=opening;worst=dict(seconds=sec,z=z,half=half)
 assert events>0 and lowest>.98,(index,lowest,worst)
 results.append(dict(shot=index,transit_checks=events,minimum_valve_opening=lowest,passed=True))
(root/'tests/valve-transit-check.json').write_text(json.dumps(results,indent=2));print('VALVE_TRANSIT_CHECK',results)
