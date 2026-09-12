#!/usr/bin/env python3
"""Procedural EP01 teen performance layer.

The cast is intentionally more developed than stick figures: each performer
has a readable head shape, torso/clothing silhouette, shoes, and distinct
acting language while remaining cheap to animate as cutout-style SVG parts.
"""
from __future__ import annotations
import math

W, H = 1920, 1080
TEENS = [
    {"x":560,"y":430,"head":45,"body":160,"leg":92,"offset":0.0,"head_shape":"hair","stance":1.00,"arm_bias":1.0,"delay":0.0,"tempo":1.06,"skin":"#c9c1b5","shirt":"#4a5664","accent":"#8e98a3","style":"hoodie"},
    {"x":760,"y":455,"head":43,"body":165,"leg":88,"offset":1.7,"head_shape":"cap","stance":0.92,"arm_bias":0.82,"delay":3.0,"tempo":0.94,"skin":"#d3cabe","shirt":"#8a6f58","accent":"#c8a88d","style":"jacket"},
    {"x":950,"y":450,"head":44,"body":158,"leg":96,"offset":3.1,"head_shape":"hairflat","stance":1.08,"arm_bias":0.68,"delay":6.0,"tempo":0.88,"skin":"#bfae9e","shirt":"#566c63","accent":"#91a59c","style":"tee"},
]

def esc(v): return f"{v:.2f}"
def clamp(t): return max(0.0,min(1.0,t))
def ease(t): t=clamp(t); return t*t*(3-2*t)
def lerp(a,b,t): return a+(b-a)*t

def _pose_values(name):
    return {
      "hang":(0,-115,88,-25,25,0,0,0,""),
      "talk":(1,-112,72,-23,24,2,0,0,"<path d='M-16 8 Q0 20 16 8' fill='none'/>") ,
      "turn":(-5,-115,92,-25,25,-8,0,0,""), "stare":(-7,-100,105,-22,30,-12,0,0,""),
      "panic":(-10,-145,125,-42,42,-4,0,0,"<circle cx='0' cy='14' r='8' fill='#0b0d12' stroke='none'/>") ,
      "freeze":(-4,-130,115,-25,25,0,0,0,""), "grab":(-10,-40,35,-28,32,4,0,0,""),
      "turn_exit":(-14,-55,35,-38,42,10,0,0,""), "run":(-16,-125,110,-38,38,12,0,0,""),
      "duck":(-8,-90,105,-30,30,0,4,58,""), "hide":(-4,-65,75,-25,25,-8,24,70,""),
      "peek":(-12,-70,80,-28,28,-20,0,62,""), "crouch":(2,-75,70,-24,24,0,0,62,""),
      "breathe":(0,-78,74,-24,24,0,0,58,""), "look_pack":(1,-55,55,-24,24,8,18,54,""),
      "look_bush":(0,-75,90,-22,28,28,0,50,""), "ask":(0,-120,45,-22,24,-4,0,50,"<path d='M-14 10 Q0 2 14 10' fill='none'/>") ,
      "glance_bush":(0,-75,88,-22,28,26,0,48,""), "neutral":(0,-105,88,-25,25,0,0,0,""),
      "point":(0,-90,25,-25,25,18,0,0,""), "commit":(-8,-115,18,-38,42,24,0,0,""),
      "throw":(-20,-150,12,-45,48,18,0,0,""), "flee":(-20,-145,125,-45,45,18,0,0,""),
      "flee_fast":(-24,-155,135,-52,52,22,0,0,""),
    }[name]

def _sequence(frame,start,end,poses):
    t=clamp((frame-start)/max(1,end-start))
    if len(poses)==1: return _pose_values(poses[0])
    u=ease(t)*(len(poses)-1); i=min(len(poses)-2,int(u)); lt=u-i
    a,b=_pose_values(poses[i]),_pose_values(poses[i+1])
    return tuple(lerp(a[j],b[j],lt) if isinstance(a[j],(int,float)) and isinstance(b[j],(int,float)) else (a[j] if lt<.5 else b[j]) for j in range(len(a)))

def pose_at(frame:int,shot_id:str,performer:int=0):
    ranges={
      "S01":(0,83,["hang","talk","hang"]),"S02":(108,143,["hang","turn","stare","panic"]),
      "S03":(144,215,["freeze","grab","turn_exit","run"]),"S04":(216,299,["run","duck","hide","peek"]),
      "S05":(300,371,["crouch","breathe","look_pack","look_bush"]),"S06":(372,419,["ask","glance_bush"]),
      "S07":(420,455,["neutral","point","commit"]),"S08":(456,539,["run","throw","flee"]),"S09":(520,610,["flee","flee_fast"]),
    }
    if shot_id not in ranges:return _pose_values("hang")
    start,end,poses=ranges[shot_id]; performer=max(0,min(len(TEENS)-1,performer)); p=TEENS[performer]
    effective=start+(frame-start-p["delay"])*p["tempo"]+p["offset"]
    return _sequence(effective,start,end,poses)

def _limb(x,y,angle_deg,length):
    r=math.radians(angle_deg-90); return x+math.cos(r)*length,y+math.sin(r)*length

def _head(shape,r,skin):
    if shape=="hair": return f"<circle cx='0' cy='0' r='{r}' fill='{skin}'/><path d='M{-r} -2 Q{-r*.65} {-r*1.15} 0 {-r*1.2} Q{r*.65} {-r*1.1} {r} -2' fill='#272d35'/><path d='M{-r*.7} {-r*.65} Q0 {-r*1.05} {r*.65} {-r*.65}' fill='none' stroke='#272d35' stroke-width='9'/><path d='M{-r*.45} {r*.82} Q0 {r*.95} {r*.45} {r*.82}' fill='none' stroke='#b8a99a' stroke-width='5'/>"
    if shape=="cap": return f"<circle cx='0' cy='0' r='{r}' fill='{skin}'/><path d='M{-r} -5 Q0 {-r*1.05} {r} -5 L{r*.75} {-r*.65} L{-r*.75} {-r*.65} Z' fill='#303944'/><path d='M{-r*.9} {-2} Q0 {-r*.28} {r*.95} -2' fill='none' stroke='#20262d' stroke-width='8'/><path d='M{-r*.75} {r*.85} Q0 {r*.95} {r*.75} {r*.85}' fill='none' stroke='#b7a99a' stroke-width='5'/>"
    return f"<circle cx='0' cy='0' r='{r}' fill='{skin}'/><path d='M{-r} {-r*.35} Q0 {-r*1.05} {r} {-r*.35}' fill='#1f242a'/><path d='M{-r*.7} {r*.85} L{r*.7} {r*.85}' stroke='#9f8d7d' stroke-width='5'/>"

def _clothes(style,body,accent):
    if style=="hoodie":
        return f"<path d='M-74 -5 Q0 -40 74 -5 L92 {body-25} Q0 {body+8} -92 {body-25} Z' fill='#4a5664'/><path d='M-38 -10 Q0 20 38 -10' fill='none' stroke='#8e98a3' stroke-width='7'/><path d='M-10 12 L-10 {body-15} M10 12 L10 {body-15}' stroke='{accent}' stroke-width='4'/><path d='M-22 55 L22 55 L28 85 L-28 85 Z' fill='#394451'/><path d='M-8 55 L8 55' stroke='#8e98a3' stroke-width='4'/></g>"
    if style=="jacket":
        return f"<path d='M-78 -5 Q0 -35 78 -5 L70 {body} Q0 {body+12} -70 {body} Z' fill='#8a6f58'/><path d='M0 -10 L0 {body}' stroke='#c8a88d' stroke-width='7'/><path d='M-65 10 L-82 82 M65 10 L82 82' stroke='#6e5949' stroke-width='10'/></g>"
    return f"<path d='M-72 -5 Q0 -28 72 -5 L78 {body} Q0 {body+8} -78 {body} Z' fill='#566c63'/><path d='M-25 20 L25 20' stroke='{accent}' stroke-width='6'/><path d='M-20 45 L20 45 M-20 70 L20 70' stroke='#40534d' stroke-width='4'/></g>"

def teen_svg(frame:int,shot_id:str)->str:
    groups=[]
    for idx,t in enumerate(TEENS):
        phase=frame*(.35+idx*.035)+t["offset"]*35
        lean,arm_l,arm_r,leg_l,leg_r,head_dx,head_dy,crouch,mouth=pose_at(frame,shot_id,idx)
        sway=math.sin(math.radians(phase))*(2.5 if shot_id in {"S01","S05"} else 1.2)
        if idx==0: lean*=1.12; arm_r+=5; head_dx+=3
        elif idx==1: lean*=.78; arm_l*=.90; arm_r*=.90; head_dx-=3; head_dy+=2
        else: lean*=.62; arm_l*=.78; arm_r*=.78; head_dx-=6
        if shot_id=="S08" and 480<=frame<=520:
            arm_r,lean=((5,-24) if idx==0 else (22,-17) if idx==1 else (34,-10))
        if shot_id in {"S04","S08","S09"}:
            stride=math.sin(math.radians(phase*(1 if shot_id!="S09" else 1.25)))*(18+idx*3)
            leg_l-=stride; leg_r+=stride; arm_l-=stride*.65*t["arm_bias"]; arm_r+=stride*.65*t["arm_bias"]
        lean+=sway; by=t["body"]+crouch; hx,hy=head_dx,head_dy-crouch*.10
        body_bottom=(lean*.35,by); shoulder_y=55+crouch*.22
        hand_l=_limb(-lean*.25-4,shoulder_y,arm_l,92*t["stance"]); hand_r=_limb(-lean*.25+5,shoulder_y,arm_r,92*t["stance"])
        foot_l=_limb(body_bottom[0],body_bottom[1],leg_l,t["leg"]+crouch*.25); foot_r=_limb(body_bottom[0],body_bottom[1],leg_r,t["leg"]+crouch*.25)
        eye_dir=1 if head_dx>=0 else -1; eye_shift=5 if idx==0 else 2 if idx==1 else 0
        eyes=f"<circle cx='{esc(-10+eye_shift*eye_dir)}' cy='-5' r='4' fill='#0b0d12' stroke='none'/><circle cx='{esc(10+eye_shift*eye_dir)}' cy='-5' r='4' fill='#0b0d12' stroke='none'/>{mouth}"
        # Each teen is a compact character rig: head, torso/clothing, hands, legs and shoes.
        g=f"<g transform='translate({esc(t['x'])} {esc(t['y'])}) rotate({esc(lean)} 0 {esc(t['body']/2)})' stroke='#0b0d12' stroke-width='11' stroke-linecap='round' stroke-linejoin='round'>"
        g+=f"<g transform='translate({esc(hx)} {esc(hy)})'>{_head(t['head_shape'],t['head'],t['skin'])}{eyes}</g>"
        g+=_clothes(t['style'],by,t['accent'])
        g+=f"<path d='M0 {esc(shoulder_y)} L{esc(hand_l[0])} {esc(hand_l[1])}' fill='none'/><circle cx='{esc(hand_l[0])}' cy='{esc(hand_l[1])}' r='9' fill='{t['skin']}'/><path d='M0 {esc(shoulder_y)} L{esc(hand_r[0])} {esc(hand_r[1])}' fill='none'/><circle cx='{esc(hand_r[0])}' cy='{esc(hand_r[1])}' r='9' fill='{t['skin']}'/>"
        g+=f"<path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_l[0])} {esc(foot_l[1])}' fill='none' stroke-width='24'/><path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_r[0])} {esc(foot_r[1])}' fill='none' stroke-width='24'/><path d='M{esc(foot_l[0]-18)} {esc(foot_l[1])} L{esc(foot_l[0]+25)} {esc(foot_l[1])}' stroke='#20252b' stroke-width='20'/><path d='M{esc(foot_r[0]-18)} {esc(foot_r[1])} L{esc(foot_r[0]+25)} {esc(foot_r[1])}' stroke='#20252b' stroke-width='20'/></g>"
        groups.append(g)
    return "<g fill='none'>"+"".join(groups)+"</g>"

def performance_layer(frame:int,shot_id:str)->str:
    return teen_svg(frame,shot_id)
