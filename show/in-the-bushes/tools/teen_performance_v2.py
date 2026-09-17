#!/usr/bin/env python3
"""Clean procedural teen performance backend for In the Bushes EP01.

The rig deliberately separates large travel from small acting: gaze, breath,
head response, hand beats, anticipation and recovery are layered on top of the
same economical cutout poses.
"""
from __future__ import annotations
import math
TEENS=[dict(x=560,y=430,skin="#c9c1b5",shirt="#4a5664",accent="#8e98a3",style="hoodie",delay=0,tempo=1.06,lean=1.15),dict(x=760,y=455,skin="#d3cabe",shirt="#8a6f58",accent="#c8a88d",style="jacket",delay=3,tempo=.94,lean=.82),dict(x=950,y=450,skin="#bfae9e",shirt="#566c63",accent="#91a59c",style="tee",delay=6,tempo=.88,lean=.65)]
POSES={"hang":(0,-110,-25,25,0),"talk":(1,-108,-22,20,2),"turn":(-7,-112,-28,30,-8),"stare":(-10,-100,-22,34,-12),"panic":(-12,-140,-45,45,-5),"grab":(-10,-48,-28,34,5),"run":(-18,-125,-42,42,14),"duck":(-8,-90,-30,30,0),"hide":(-4,-65,-25,25,-8),"peek":(-12,-70,-30,28,-20),"crouch":(2,-75,-24,24,0),"breathe":(0,-78,-24,24,0),"look_pack":(1,-55,-24,28,8),"look_bush":(0,-75,-22,30,26),"ask":(0,-118,-22,24,-4),"glance_bush":(0,-75,-22,28,26),"neutral":(0,-105,-25,25,0),"point":(0,-90,-25,20,18),"commit":(-8,-115,-38,42,24),"throw":(-20,-150,-45,48,18),"flee":(-20,-145,-45,45,18),"flee_fast":(-24,-155,-52,52,22)}
SEQUENCES={"S01":(0,83,["hang","talk","hang"]),"S02":(108,143,["hang","turn","stare","panic"]),"S03":(144,215,["panic","grab","turn","run"]),"S04":(216,299,["run","duck","hide","peek"]),"S05":(300,371,["crouch","breathe","look_pack","look_bush"]),"S06":(372,419,["ask","glance_bush"]),"S07":(420,455,["neutral","point","commit"]),"S08":(456,539,["run","throw","flee"]),"S09":(520,610,["flee","flee_fast"])}
def ease(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def pose(frame,shot,idx):
 if shot not in SEQUENCES:return POSES["hang"]
 start,end,names=SEQUENCES[shot];p=TEENS[idx];local=(frame-start-p["delay"])*p["tempo"];t=max(0,min(1,local/max(1,end-start)));u=ease(t)*(len(names)-1);i=min(len(names)-2,int(u)) if len(names)>1 else 0;q=u-i if len(names)>1 else 0;a=POSES[names[i]];b=POSES[names[i+1]] if len(names)>1 else a;return tuple(a[j]+(b[j]-a[j])*q for j in range(5))
def point(x,y,angle,length):
 r=math.radians(angle-90);return x+math.cos(r)*length,y+math.sin(r)*length
def clamp(v,a,b):return max(a,min(b,v))
def character(frame,idx,shot):
 p=TEENS[idx];lean,head_y,left_a,right_a,head_x=pose(frame,shot,idx);phase=frame*(.35+idx*.035)+idx*55;active=shot in {"S01","S05","S06","S07"};travel=shot in {"S04","S08","S09"}
 breath=math.sin(math.radians(phase*1.7))*(3.0 if active else 1.2);lean=lean*p["lean"]+breath
 stride=math.sin(math.radians(phase))*(18+idx*3) if travel else 0
 if shot=="S02":
  response=max(0,min(1,(frame-(108+idx*5))/18));head_x+=math.sin(response*math.pi)*(-10-idx*2);head_y+=math.sin(response*math.pi)*(-3)
 elif shot=="S03":
  response=max(0,min(1,(frame-(144+idx*4))/22));head_x+=math.sin(response*math.pi)*(-5)
 elif shot=="S05":head_y+=breath*.45
 elif shot=="S06":head_x+=math.sin(math.radians(phase*1.25))*3
 elif shot=="S07":head_x+=math.sin(math.radians(phase*.9))*2
 if idx==0:right_a+=5;head_x+=3
 elif idx==1:left_a*=.9;right_a*=.9;head_x-=3
 else:left_a*=.78;right_a*=.78;head_x-=6
 left_a-=stride*.55;right_a+=stride*.55
 if shot=="S06":right_a+=math.sin(math.radians((frame-372)*12+idx*30))*4
 if shot=="S07":right_a-=clamp((frame-(420+idx*3))/18,0,1)*10
 if shot=="S08":
  wind=clamp((frame-(456+idx*2))/24,0,1)
  if frame<500:right_a-=wind*16
  else:right_a+=clamp((frame-500)/18,0,1)*18
 body_h=155;hand_l=point(-4,55,left_a,92);hand_r=point(4,55,right_a,92);foot_l=point(lean*.3,body_h,-38-stride,92);foot_r=point(lean*.3,body_h,38+stride,92)
 gaze_x=0;gaze_y=0
 if shot in {"S02","S03"}:gaze_x=-6+idx*2;gaze_y=-2
 elif shot in {"S05","S06"}:gaze_x=6;gaze_y=4
 elif shot=="S07":gaze_x=10;gaze_y=5
 elif shot in {"S08","S09"}:gaze_x=7
 blink_phase=(frame+idx*17)%53;blink=blink_phase in {51,52};eye_r=1.2 if blink else 5
 mouth=""
 if shot in {"S01","S06"}:mouth="<path d='M-14 9 Q0 17 14 9' fill='none'/>"
 elif shot in {"S02","S03"}:mouth="<path d='M-11 12 Q0 4 11 12' fill='none' stroke-width='8'/>"
 elif shot=="S07":mouth="<path d='M-9 8 Q0 14 9 8' fill='none' stroke-width='7'/>"
 head=f"<circle cx='{head_x:.2f}' cy='{head_y:.2f}' r='44' fill='{p['skin']}'/>"
 if idx==0:head+="<path d='M-44 -8 Q0 -56 44 -8 Q20 -28 0 -24 Q-22 -30 -44 -8' fill='#272d35'/>"
 elif idx==1:head+="<path d='M-44 -12 Q0 -52 44 -12 L35 -35 L-35 -35 Z' fill='#303944'/><path d='M-42 -6 Q0 -20 42 -6' fill='none' stroke='#20262d' stroke-width='8'/>"
 else:head+="<path d='M-44 -8 Q0 -55 44 -8 Q0 -25 -44 -8' fill='#1f242a'/>"
 eyes=f"<circle cx='{-10+gaze_x:.2f}' cy='{-5+gaze_y:.2f}' r='{eye_r}' fill='#0b0d12' stroke='none'/><circle cx='{10+gaze_x:.2f}' cy='{-5+gaze_y:.2f}' r='{eye_r}' fill='#0b0d12' stroke='none'/>"
 clothes=f"<path d='M-74 -4 Q0 -32 74 -4 L82 155 Q0 174 -82 155 Z' fill='{p['shirt']}'/>"
 if p['style']=='hoodie':clothes+="<path d='M-36 -8 Q0 18 36 -8' fill='none' stroke='#8e98a3' stroke-width='7'/><path d='M-10 15 L-10 135 M10 15 L10 135' stroke='#8e98a3' stroke-width='4'/><path d='M-22 52 L22 52' stroke='#394451' stroke-width='10'/>"
 elif p['style']=='jacket':clothes+="<path d='M0 -8 L0 155' stroke='#c8a88d' stroke-width='7'/><path d='M-62 15 L-78 82 M62 15 L78 82' stroke='#6e5949' stroke-width='10'/>"
 else:clothes+="<path d='M-25 22 L25 22 M-20 48 L20 48 M-20 74 L20 74' stroke='#91a59c' stroke-width='5'/>"
 return (f"<g transform='translate({p['x']} {p['y']}) rotate({lean:.2f} 0 78)' fill='none' stroke='#0b0d12' stroke-width='11' stroke-linecap='round' stroke-linejoin='round'>{head}{eyes}{mouth}{clothes}"
         f"<path d='M0 55 L{hand_l[0]:.2f} {hand_l[1]:.2f}'/><circle cx='{hand_l[0]:.2f}' cy='{hand_l[1]:.2f}' r='9' fill='{p['skin']}'/>"
         f"<path d='M0 55 L{hand_r[0]:.2f} {hand_r[1]:.2f}'/><circle cx='{hand_r[0]:.2f}' cy='{hand_r[1]:.2f}' r='9' fill='{p['skin']}'/>"
         f"<path d='M0 {body_h} L{foot_l[0]:.2f} {foot_l[1]:.2f}' stroke-width='24'/><path d='M0 {body_h} L{foot_r[0]:.2f} {foot_r[1]:.2f}' stroke-width='24'/>"
         f"<path d='M{foot_l[0]-18:.2f} {foot_l[1]:.2f} L{foot_l[0]+25:.2f} {foot_l[1]:.2f}' stroke='#20252b' stroke-width='20'/><path d='M{foot_r[0]-18:.2f} {foot_r[1]:.2f} L{foot_r[0]+25:.2f} {foot_r[1]:.2f}' stroke='#20252b' stroke-width='20'/></g>")
def performance_layer(frame,shot):return "<g>"+"".join(character(frame,i,shot) for i in range(3))+"</g>"
