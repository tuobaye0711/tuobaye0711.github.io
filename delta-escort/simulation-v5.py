#!/usr/bin/env python3
"""Conditional scenario experiment. No fitted or hand-entered expected returns.
All loot and costs are in 万哈夫币; prices are CNY. Capped paths stay in means.
"""
from pathlib import Path
import json,re,math,hashlib,os,csv
import numpy as np
ROOT=Path(__file__).resolve().parent
VERSION='2026-09-24-r5';N=int(os.getenv('ESCORT_REPS','6000'));H=200;SEED=240924
DOC=json.loads((ROOT/'rules.json').read_text())
SCENARIOS=[
 dict(id='pressure',name='高压装备局',p=.25,bag=.05,x=[600,950,1450,2200],w=[.15,.35,.30,.20],red=[.10,.30,.55,.85],gold=[3,4,5,6],kills=[2,4,6,9],loot=.65,aw=1.1,gear=1.5),
 dict(id='base',name='基准混合局',p=.45,bag=.04,x=[450,800,1150,1800],w=[.15,.35,.35,.15],red=[.2,.5,1.,1.6],gold=[4,6,8,10],kills=[2,4,6,9],loot=1.,aw=.55,gear=1.),
 dict(id='search',name='顺畅搜资局',p=.65,bag=.03,x=[400,700,1050,1500],w=[.15,.30,.40,.15],red=[.4,.9,1.5,2.3],gold=[6,8,10,12],kills=[1,3,5,7],loot=1.4,aw=.25,gear=.7)
]
PARAMS={
 'kind':'主观参数驱动的条件蒙特卡洛，不是游戏/商家统计','repetitions_per_tier_scenario':N,'horizon_rounds':H,'seed':SEED,
 'net_defaults':{'cash_conversion':.90,'success_cost_w':8,'failure_cost_w':55,'bag_cost_w':35},
 'net_note':'毛收益是模型生成的新增带出，不重复计算原有战备。净收益=新增毛收益×兑现比例−成功/失败/丢包成本；0.90不是官方税率。失败安全箱残值已包含在毛收益，成本为丢失入场战备及消耗。',
 'environment':SCENARIOS,
 'round_generation':'先生成完整成功/失败/丢包和共享质量档；X=档位值×Uniform(0.9,1.1)。红数、金数、击杀按该档Poisson生成，保留与收益的相关性。红最多6、金最多20、击杀最多15。心泪事件另按0.1%×搜资系数/局假设并增加1000W，不采用巨额传闻报价。',
 'item_assumptions':{'synthetic_red_identities':12,'red_cells':[2,4,6,9],'red_cell_probabilities':[.25,.25,.25,.25],'medical_share':.12,'gold_cells_per_item':1.5,'helper_gold_multiplier':1.5,'team_small_gold_fraction':.55,'small_gold_identity_probabilities':[.25,.2,.15,.12,.1,.08,.06,.04],'million_card_chance':.10,'failed_safe_red_chance':.025,'failed_safe_value_w':[0,15,80,130],'failed_safe_value_weights':[.55,.30,.10,.05]},
 'task_assumptions':{'specific_gold_share':.10,'source_eligibility_base_advanced_hard':[1,.60,.35],'legend_per_success':[.10,.035,.025],'card_uses_per_full_card_ASSUMED':10,'card_visit_probability':.45,'safe_count_proxy':'floor(gold_count*0.45)','sand_safe_pair_chance':.35,'boss_chance_per_attempt':.10,'questions_candidate_set_base':128,'questions_candidate_set_advanced':256},
 'blackhole_note':'q为收益免计分覆盖的等效参数，不是出生率统计。此模型假设免计分事件与X独立，故q也等于该模型成功事件覆盖；不以K/总出生点作真实概率。选点组合只是待验证策略。',
 'blackhole_base_q':{'航天':[.52,.67,.78,.88],'巴克什':[.54,.71,.79,.91],'监狱':[.55,.64,.78,.91]},'blackhole_sensitivity_q_shift':[-.10,0,.08],
 'simplifications':'普通成功X采用新增毛价值且用于计分的简化。未建立精确游戏物品目录：金身份8类、红身份12类为合成类别，任务真实推进率未知。小金来源按比例稀释，地图任务部分子目标使用事件代理。所有同档比较默认同队伍/待遇；低价档不保证同产出。',
 'fulfillment':'假设规则完整履约，无退款弃单、无主动送死。触发200局上限仍只统计到上限，不删除样本、不声称已结单；大长尾不等于保本或无限收益。',
 'status':'原图2026-09-22归档，核图2026-09-24；不是商家实时接单价格确认。'
}
FAMILIES={
 'fixed':'累计有效计分达到保底；失败只增加应补目标，补齐前不当已到账。末局全部实际带出保留。',
 'thousand':'成功计分=max(X−1000,0)；失败目标+10；丢包流局。388/888的基础目标分别488/1288。',
 'hand':'有效成功计分=X/2^合格红数；无红局按X；须3保险。首次成功即结单另开2888W普通补单阶段。',
 'white':'有合格红成功局免计分，>600W才消耗次数；无红局计分，基础目标先满即结单，不承诺用满上限。',
 'miner':'累计108格；G=10×金格+100×红格。588收集收益抵G；988基线为收集后额外补G。帮带任务金不全部当老板收入。',
 'bigred':'同时满足红格任务和币量；25/50格允许失败保险红推进，66/368只计成功。',
 'nine':'同时满足币量与9个指定小金；来源比例/赖子资格按档区分。千万撤离并非每档能抵。',
 'gold':'同时满足币量与20个同种小金。按8类显式假设物品累计，最先凑齐种类加赖子；不把20个当20格。',
 'legend':'同时满足币量与任选/指定/集齐目标。使用明示假设成功局事件率，不声称官方掉率。',
 'billion':'有效成功总计分=(红数+1)×X−金增加目标；流局只计X，不重复扣一次普通收益。',
 'twohundred':'有效成功进度=X+300×金格−500×红格；失败只改变下次少算金，不加普通炸补；低门槛成功只计X。',
 'blackhole':'黑洞成功X归老板、不计基础目标；低价值失败另记补偿，基础结束后另补；丢包>500W例外计分。',
 'giant':'12/30/40起始血，首档封顶25；最高满足金额档扣血，医疗回血与心泪在同局净额结算。无上限档可能长期未吸收。',
 'tower':'成功>700W掷1至3骰上楼；失败退2层，有负层封底；每个6加288W目标；层数/币量同时满足。',
 'challenge':'四图逐关，金额达标才过；三档分别原地/退一关/重头。四关后补总保底，不将时长直接当收益。',
 'dog':'区分单局15牌、累计高价牌、狗牌价值保卫战；任务牌值不直接当老板收入。',
 'war':'金弹批量生成，AW枪/弹分开；三枪必须同局；失败可推进AW弹，不当整包带出。同个红不同时抵两类弹药。',
 'sand':'成功+≥788W+同局2沙色才计1次，累计1/2/5次；许愿及炸补另建补单。',
 'maptask':'任务计数向量并行；开卡/看点可失败推进，保险/大红单独处理。房卡耐久和访问率是明示假设。',
 'turtle':'候选集合与问题数近似猜物，属于策略代理模型，不是复刻真实双方问答。',
 'ancestor':'只成功收菜一次，默认首次成功立即收；三倍仅作用于该阶段；另测等待两次连续成功的策略。',
 'parity':'基线单双为最终结单门槛、收益先计；另测未命中整局不计分解释，不默认翻倍。',
 'pairs':'同格与同种分开；有限类别重复碰撞，2对需两种物品，4个同物不重复算2对。',
 'dice':'由三人物资尾数、金数、两打手击杀及总击杀、红数得到不同有效骰子点数；不是条件条数÷6。',
 'hourly':'计时按假设胜率、每小时3局和收益结构；未复刻补时退款，不将半小时价格误当半小时800W保底。',
 'unmodeled':'不凭空编造结单率；保留完整价格与原文，并说明缺什么。'
}
def number(s):
 m=re.search(r'\d+(?:\.\d+)?',s);return float(m.group()) if m else None
def target(s):
 if '1亿3888' in s:return 13888.
 if s=='1亿':return 10000.
 if s.startswith('2亿'):return 20000.
 return number(s) or 0.
def spec_for(name,i,t):
 z=dict(family='unmodeled',price=number(t[1]),target=target(t[2]),mode='绝密',extra='',certainty='条件模型',failure_bonus=60,excluded=False)
 if name in ['VIP预存','七夕限定预存'] or '附加' in t[0]:
  z.update(extra='储值/附加权益不是独立产币订单，不能用相同分母排名。',excluded=True);return z
 if name in ['bingo','五子棋','法外狂徒','婚礼进行时']:
  z['extra']={'bingo':'已核3–10连；棋盘类别映射与赖子放置策略未建模，旧6.2作废。','五子棋':'棋力、落子策略、多步顺序未定，不能设一个任意胜率冒充完整模型。','法外狂徒':'加人头的方向未明确，暂不输出单一EV。','婚礼进行时':'并行/串行和部分头甲阶段逻辑未核，不能用任意通关局数替代。'}[name];return z
 if name in ['新用户专属','体验单','机密专区','秋日限定保底','限时活动']:
  z['family']='fixed'
  if name=='新用户专属':z.update(excluded=True,extra='新客资格未确认，不参加默认可购排序。')
  if ('机密' in t[0] and '绝密' not in t[0]) or name=='机密专区':z.update(mode='机密',failure_bonus=25)
  if name=='体验单' and i==3:z['single_goal']=800
  if name=='机密专区' and i in [4,5]:z.update(certainty='未计作战加成',extra='当前只算原保底部分，不猜老板击杀/救人和额外战损。')
  if name=='秋日限定保底' and i>=7:z.update(certainty='未计尊享赠送',extra='双倒/开卡/清图赠送未设虚构发生率；仅计算常规保底部分，是保守机制下界。')
  if name=='秋日限定保底' and i>=12:z['failure_bonus']=100
  if name=='限时活动':z['extra']='海报9.18–10.20，仍在售未确认；皮肤/消费券不计哈夫币。'
 if '小时' in t[1] or '/H' in t[1]:
  z.update(family='hourly',price=z['price']*(2 if '半小时' in t[1] else 1),target=0,excluded=True,extra='统一1小时分母、每小时3局、含整备平均20分钟/局仅是假设。')
  if any(w in t[0] for w in ['物资','顶级双陪']):z['extra']+='未完整计补物资/补时退款，仅给计时收益参考。'
 if name=='千万才是开始':z.update(family='thousand',failure_bonus=10)
 if name=='骰子大王':z.update(family='dice',failure_bonus=80)
 if name=='小香手':z.update(family='hand',target=1388)
 if name=='白嫖单':z.update(family='white',limit=[4,7,9,99999][i])
 if name=='黄金大矿工':z.update(family='miner',target=0,extra_pay=i==1,certainty='988含解释分支',extra='基线988另补；同时计算按补差额解释。')
 if name=='大红爆仓':z.update(family='bigred',cells=[25,50,66,368][i],failed_progress=i<2,certainty='368格含解释分支',extra='368格枪计入冲突：基线不计，另给计枪解释。')
 if name=='九九归一':z.update(family='nine',source=[1,.60,.35][i],thousand_wild=i<2)
 if name=='淘金大作战':z.update(family='gold',level=i,failure_bonus=70)
 if name=='三幻神专区':z.update(family='legend',level=i,extra='三目标成功局概率为明示假设，非官方掉率；默认目标须成功带出。')
 if name=='我要亿万哈夫币':z.update(family='billion',hard=i>=2,target=13888 if i<2 else 20000,map='航天' if '航天' in t[0] else '巴克什',failure_bonus=0)
 if name=='爽吃两亿':z.update(family='twohundred',target=20000,map=['巴克什','航天','监狱'][i],gold_credit=1 if i==1 else 2,failure_bonus=0)
 if name=='超级黑洞':
  mp=(['航天']*4+['监狱']*4+['巴克什']*4)[i]
  z.update(family='blackhole',map=mp,q=PARAMS['blackhole_base_q'][mp][i%4],failure_bonus=80 if mp=='监狱' else 60,certainty='覆盖率敏感',extra='q为收益覆盖率假设，非平均出生率；另计算q变化情景。')
 if name=='小小巨人':z.update(family='giant',hp=[12,30,40][i],hp_cap=25 if i==0 else None,level=i,failure_bonus=0,target=0)
 if name=='永恒之塔':z.update(family='tower',height=[10,20,30,50][i],floor=[-5,-10,-15,-25][i])
 if name=='一命通关':z.update(family='challenge',level=i,extra='跨地图价值倍率大坝.48/巴克什.9/航天1/监狱.9和胜率偏移均为假设，不套用个人26局。')
 if name=='狗牌收集计划':z.update(family='dog',level=i,extra='任务牌值不等于老板实际带出；价值门槛档只计队内击杀。')
 if name=='战争贩子':z.update(family='war',level=i)
 if name=='沙色保险':z.update(family='sand',target=0,needed=[1,2,5][i],extra='1/2/5局已核；同局2沙色概率与许愿率均为假设。')
 if name in ['巴克什大王','典狱长阁下','监狱管理者']:z.update(family='maptask',task=name,certainty='任务速率代理',extra='访问/开卡/保险/BOSS概率和满卡次数为明示假设，不是实测地图数据。')
 if name=='海龟汤':z.update(family='turtle',level=i,certainty='问答策略代理')
 if name=='收手吧，阿祖':z.update(family='ancestor',level=i,wait=1,certainty='策略敏感',extra='默认首次成功立即收；另模拟等连续2次成功。')
 if name=='单双对弈':z.update(family='parity',free_miss=False,certainty='解释分支',extra='基线只延迟结单；另测未命中整局免费解释。')
 if name=='保底出红单':
  z.update(family='pairs',level=i,excluded=True,extra='海报8.19–9.20已过期、续期未知；同种配对使用有限类别模型。')
  if i==4:z.update(family='unmodeled',extra='7777档基础币量未核且旧活动过期，不猜目标。')
 return z

def bank(s):
 rng=np.random.default_rng(SEED);sh=(H,N);q=rng.choice(4,sh,p=s['w']);u=rng.random(sh)
 x=np.asarray(s['x'])[q]*rng.uniform(.9,1.1,sh)
 rc=np.minimum(rng.poisson(np.asarray(s['red'])[q]),6).astype(float)
 gn=np.minimum(rng.poisson(np.asarray(s['gold'])[q]),20).astype(float)
 redids=rng.multinomial(rc.astype(int),[1/12]*12).astype('int16')
 cells=(redids*np.asarray([2,2,2,4,4,4,6,6,6,9,9,9])).sum(axis=-1)
 goldids=rng.multinomial(np.floor(gn*1.5*.55).astype(int),PARAMS['item_assumptions']['small_gold_identity_probabilities']).astype('int16')
 kills=np.minimum(rng.poisson(np.asarray(s['kills'])[q]),15).astype(float)
 return dict(u=u,x=x,red=rc,gold=gn,redcells=cells,goldcells=gn*1.5,kills=kills,
  card=(rng.random(sh)<.10*s['loot']).astype(float),rare=rng.random(sh)<.001*s['loot'],
  med=rng.binomial(rc.astype(int),.12)*rng.choice([4,6,9,10],sh,p=[.4,.3,.25,.05]),
  fsafe=rng.choice([0.,15.,80.,130.],sh,p=[.55,.30,.10,.05]),fred=(rng.random(sh)<.025*s['loot']).astype(float),
  gun=rng.poisson(s['aw'],sh).astype(float),ammo=rng.poisson(3,sh)*80.,awammo=rng.poisson(1.5*s['aw'],sh),dice=rng.integers(1,7,sh+(3,)),
  a=rng.random(sh),b=rng.random(sh),c=rng.random(sh),d=rng.random(sh),goldids=goldids,redids=redids)

def simulate(z,s,B):
 price=z['price'];family=z['family'];target0=z['target']
 if family=='unmodeled' or price is None:return None
 arr=lambda v=0:np.full(N,v,dtype=float)
 gross=arr();paidscore=arr();goals=arr(target0);wins=arr();fails=arr();bags=arr();rounds=arr();done=np.zeros(N,bool)
 state=arr();pending=arr();comp=arr();phase=arr();aux=arr();aux2=arr();hp=arr(z.get('hp',0));stage=arr();info=arr()
 goldhist=np.zeros((N,8));redhist=np.zeros((N,12));mapstate=np.zeros((N,6));leg=np.zeros((N,3),bool)
 for t in range(H):
  active=~done
  if not active.any():break
  if family=='hourly' and t>=3:break
  x=B['x'][t].copy();p=np.full(N,s['p']);fb=np.full(N,z['failure_bonus'])
  if z['mode']=='机密':x*=.48;p=np.minimum(.95,p+.12);fb[:]=25
  if family=='challenge':
   k=np.minimum(stage.astype(int),3);x*=np.asarray([.48,.90,1.,.90])[k];p=np.minimum(.95,p+np.asarray([.12,.02,0.,-.02])[k]);fb=np.asarray([25.,60.,60.,80.])[k]
  success=(B['u'][t]<p)&active;bag=(B['u'][t]>=p)&(B['u'][t]<p+s['bag'])&active;fail=active&~success&~bag
  x+=B['rare'][t]*1000
  sg=success.astype(float);ff=fail.astype(float);bb=bag.astype(float)
  rv=sg*x+ff*B['fsafe'][t]+bb*x*.25
  gross+=rv;rounds+=active;wins+=sg;fails+=ff;bags+=bb
  red=B['red'][t];gold=B['gold'][t];kill=B['kills'][t];card=B['card'][t];rare=B['rare'][t]
  topping=active&(phase==2)
  paidscore[topping]+=rv[topping];goals[topping]+=ff[topping]*fb[topping]
  base=active&~topping;w=success&base;f=fail&base;b=bag&base;count_failure=(f|b).astype(float)
  credit=w*x+f*np.maximum(B['fsafe'][t]-100,0)+b*x*.25
  if family not in ['thousand','giant','twohundred','blackhole','billion','hourly']:goals+=base*count_failure*fb
  paidscore+=np.where(base,credit,0)
  if family=='fixed':
   ok=w&(x>=z['single_goal']) if 'single_goal' in z else paidscore>=goals
  elif family=='thousand':
   paidscore-=np.where(base,credit,0);paidscore+=w*np.maximum(x-1000,0);goals+=f*10;ok=paidscore>=goals
  elif family=='hand':
   paidscore-=np.where(base,credit,0);valid=w&(B['a'][t]<min(.95,.7*s['loot']));paidscore+=valid*x/(2**red)
   hit=base&(paidscore>=goals);special=hit&(wins==1);phase[special]=2;paidscore[special]=0;goals[special]=2888;ok=hit&~special
  elif family=='dice':
   paidscore-=np.where(base,credit,0)
   money=(np.floor(x*10000)+np.floor(x*B['b'][t]*10000)+np.floor(x*B['c'][t]*10000)).astype(int)%10
   k1=np.floor(kill*B['d'][t]).astype(int);k2=kill.astype(int)-k1
   values=np.column_stack([money,gold.astype(int)%10,k1%10,k2%10,kill.astype(int)%10,red.astype(int)%10])
   free=w&(values==B['dice'][t,:,0,None]).any(axis=1);aux+=free
   paidscore+=w*~free*x+f*np.maximum(B['fsafe'][t]-100,0)+b*x*.25
   hit=paidscore>=goals;first=base&hit&(wins==1)&(state==0);state[first]=1
   ok=hit&~first&((state==0)|(wins>=2))
  elif family=='white':
   paidscore-=np.where(base,credit,0);free=w&((red+card)>0)&(state<z['limit']);state+=free&(x>600)
   goals+=500*(w&(wins==1)&((red+card)==0));paidscore+=w*~free*x+f*np.maximum(B['fsafe'][t]-100,0)+b*x*.25;ok=paidscore>=goals
  elif family=='miner':
   collect=base&(phase==0);remain=np.maximum(108-state,0)
   radd=np.minimum(B['redcells'][t],remain)*w*collect;gadd=np.minimum(B['goldcells'][t]*1.5,np.maximum(remain-radd,0))*w*collect
   state+=radd+gadd;aux+=radd*100+gadd*10;comp+=count_failure*fb*collect;hit=collect&(state>=108)
   goals[hit]=aux[hit]+comp[hit]+(paidscore[hit] if z['extra_pay'] else 0);phase[hit]=1;ok=(phase>=1)&(paidscore>=goals)
  elif family=='bigred':
   inc=B['redcells'][t]+card*2
   if z.get('count_guns'):inc+=B['gun'][t]*10
   state+=w*inc
   if z['failed_progress']:state+=f*B['fred'][t]*4
   ok=(state>=z['cells'])&(paidscore>=goals)
  elif family in ['nine','gold']:
   valid=w&(x>=(800 if family=='nine' else 600))
   if family=='nine':
    qty=gold*1.5*.10*z['source'];wild=red+card+rare
    if z['thousand_wild']:wild+=x>=1000
    if z['source']<1:wild*=z['source']
    state+=valid*(qty+wild);ok=(state>=9)&(paidscore>=goals)
   else:
    goldhist+=B['goldids'][t]*valid[:,None]*np.where(kill<4,.5,1.)[:,None]
    level=z['level'];wild=red*(3 if level==0 else 2)+card*(2 if level<2 else 0)+rare*(8 if level==0 else 4)
    if level==0:wild+=2*(x>=1000)
    if level==2:wild[:]=0
    aux+=valid*wild*np.where(kill<4,.5,1.);ok=(goldhist.max(axis=1)+aux>=20)&(paidscore>=goals)
  elif family=='legend':
   for j,rate in enumerate([.10,.035,.025]):leg[:,j]|=w&(B[['a','b','c'][j]][t]<rate*s['loot'])
   enough=[leg.any(axis=1),leg[:,1:].any(axis=1),leg[:,2],leg.all(axis=1)][z['level']];ok=enough&(paidscore>=goals)
  elif family=='billion':
   paidscore-=np.where(base,credit,0);valid=w&(x>=(750 if z['map']=='航天' else 600))
   goldinc=B['goldcells'][t]*50 if z['hard'] else gold*30
   paidscore+=w*x+valid*(red*x-goldinc);goals+=(f|b)*(100 if z['hard'] else 60);ok=paidscore>=goals
  elif family=='twohundred':
   paidscore-=np.where(base,credit,0);threshold={'航天':800,'巴克什':700,'监狱':600}[z['map']]
   valid=(w&(x>=threshold))|(b&(x*.25>=threshold));pending+=(f|b)*z['gold_credit'];kg=np.maximum(B['goldcells'][t]*1.5-pending,0)
   paidscore+=w*x+b*x*.25+f*(B['fsafe'][t]>100)*B['fsafe'][t];paidscore+=valid*(300*kg-500*B['redcells'][t]-6000*rare)
   pending[valid]=0;ok=paidscore>=goals
  elif family=='blackhole':
   paidscore-=np.where(base,credit,0);q=np.clip(z['q']+z.get('q_shift',0),0,.98);free=w&(B['a'][t]<q)
   paidscore+=w*~free*x+b*(x*.25>500)*x*.25;comp+=(f|b)*(B['fsafe'][t]<100)*fb;hit=base&(paidscore>=goals)
   phase[hit]=2;goals[hit]=comp[hit];paidscore[hit]=0;ok=hit&(comp<=0)
  elif family=='giant':
   lv=z['level'];cuts=([700,800,900,1000],[800,1200,1300,1500],[800,1200,1300,1500,2000])[lv];dmg=([7,8,9,10],[5,6,8,12],[5,6,8,9,12])[lv];damage=np.zeros(N)
   for cut,val in zip(cuts,dmg):damage=np.where(x>=cut,val,damage)
   med=B['med'][t]*(w+((f|b)&(B['b'][t]<.15)));hp+=base*((f|b)*(3 if lv==2 else 2)+med-w*damage-w*rare*10)
   if z['hp_cap']:hp=np.minimum(hp,z['hp_cap'])
   ok=hp<=0
  elif family=='tower':
   valid=w&(x>700);nd=1+np.minimum(2,red+card+(x>=1000)).astype(int);dice=B['dice'][t]
   steps=np.sum(dice*(np.arange(3)[None,:]<nd[:,None]),axis=1);six=np.sum((dice==6)*(np.arange(3)[None,:]<nd[:,None]),axis=1)
   state+=valid*steps-f*2;state=np.maximum(state,z['floor']);goals+=valid*six*288;ok=(state>=z['height'])&(paidscore>=goals)
  elif family=='challenge':
   idx=np.minimum(stage.astype(int),3);need=np.asarray([288,688,888,788])[idx]
   good=w&(x>=need)&(stage<4);bad=base&~good&(stage<4);stage[good]+=1
   if z['level']==1:stage[bad]=np.maximum(0,stage[bad]-1)
   if z['level']==2:stage[bad]=0
   ok=(stage>=4)&(paidscore>=goals)
  elif family=='dog':
   lv=z['level'];dogs=np.minimum(17,kill+np.floor(B['a'][t]*7))
   if lv==0:state=np.maximum(state,w*dogs);enough=state>=15
   elif lv==1:state+=w*dogs*160*s['gear'];enough=state>2088
   elif lv<=4:
    threshold=[0,0,80,200,300][lv];prob=np.exp(-threshold/(190*s['gear']));state+=w*np.floor(kill*prob+B['b'][t]);enough=state>=[0,0,12,12,15][lv]
   else:state+=w*kill*160*s['gear'];enough=state>=target0;paidscore=state.copy()
   ok=enough&(paidscore>=goals)
  elif family=='war':
   lv=z['level'];aw_need=20 if lv==2 else 5 if lv==1 else 0;aw_raw=base*B['awammo'][t]
   allocated=np.minimum(red,np.maximum(aw_need-aux-aw_raw,0))*w;aux+=aw_raw+allocated
   state+=w*(B['ammo'][t]+(red-allocated)*100+card*50);aux2=np.maximum(aux2,w*B['gun'][t])
   enough=state>=1000 if lv==0 else ((state>=1000)&(aux>=5) if lv==1 else (aux>=20)&(aux2>=3));ok=enough&(paidscore>=goals)
  elif family=='sand':
   valid=w&(x>=788)&(B['a'][t]<min(.9,.35*s['loot']));state+=valid;comp+=(f|b)*fb
   wish=w&(B['b'][t]<.03*s['loot'])&(aux==0);aux+=wish;comp+=wish*1088
   hit=base&(state>=z['needed']);phase[hit]=2;goals[hit]=comp[hit];paidscore[hit]=0;ok=hit&(comp<=0)
  elif family=='maptask':
   access=base&(B['a'][t]<min(.9,.45*s['loot']));maps=z['task'];mapstate[:,0]+=access;mapstate[:,1]+=w*np.floor(gold*.45)
   mapstate[:,2]+=access*3;mapstate[:,3]+=base&(B['b'][t]<.10*s['loot']);mapstate[:,4]+=w&(B['c'][t]<.35*s['loot']);mapstate[:,5]+=w*red
   need={'巴克什大王':[10,9,30,1,1,0],'典狱长阁下':[10,40,30,2,5,0],'监狱管理者':[10,60,50,2,5,3]}[maps]
   ok=(mapstate>=np.asarray(need)).all(axis=1)&(paidscore>=goals)
  elif family=='turtle':
   questions=np.minimum(6,np.floor(kill/2)+red+card+1+(x>=1000));info+=w*questions
   if z['level']==1:info=np.maximum(-10,info-2*(f|b))
   chance=np.minimum(1,2**np.minimum(20,info)/(128 if z['level']==0 else 256));guess=w&(B['a'][t]<chance)
   if z['level']<2:state=np.maximum(state,guess);ok=(state>=1)&(wins>=(2 if z['level']==0 else 3))&(paidscore>=goals)
   else:
    if t%2==1:goals+=base*np.where(B['a'][t]<chance,-500,500);info[:]=0
    ok=paidscore>=goals
  elif family=='ancestor':
   unpaid=base&(phase==0)
   if z['level']==1:
    paidscore[unpaid]-=credit[unpaid];pending[unpaid]+=w[unpaid]*x[unpaid];pending[(f|b)&unpaid]=0
   else:pending[unpaid]+=w[unpaid]*x[unpaid];pending[(f|b)&unpaid]=0
   aux[unpaid]+=w[unpaid];aux[(f|b)&unpaid]=0;collect=unpaid&w&(aux>=z['wait'])
   paidscore[collect]+=pending[collect]*(3 if z['level']==1 else 2);phase[collect]=1;ok=(phase>=1)&(paidscore>=goals)
  elif family=='parity':
   good=B['a'][t]<.5
   if z['free_miss']:paidscore-=w*~good*x
   ok=(paidscore>=goals)&w&good
  elif family=='pairs':
   valid=w&(x>=700);redhist+=B['redids'][t]*valid[:,None];lv=z['level']
   if lv<2:
    cells=np.column_stack([redhist[:,j*3:j*3+3].sum(axis=1) for j in range(4)]);enough=(cells>=2).sum(axis=1)>=(1 if lv==0 else 2)
   else:enough=(redhist>=2).sum(axis=1)>=(1 if lv==2 else 2)
   ok=enough&(paidscore>=goals)
  elif family=='hourly':ok=rounds>=3
  else:raise ValueError(family)
  done|=active&((ok&base)|(topping&(paidscore>=goals)))
 net=.90*gross-8*wins-55*fails-35*bags
 r=lambda a:round(float(a),6);ratio=gross/price;nr=net/price
 return dict(mean_gross_per_yuan=r(ratio.mean()),mean_net_per_yuan=r(nr.mean()),median_gross_per_yuan=r(np.median(ratio)),median_net_per_yuan=r(np.median(nr)),
 p10_gross=r(np.quantile(ratio,.1)),p90_gross=r(np.quantile(ratio,.9)),p10_net=r(np.quantile(nr,.1)),p90_net=r(np.quantile(nr,.9)),
 expected_gross_w=r(gross.mean()),expected_net_w=r(net.mean()),mean_rounds=r(rounds.mean()),mean_successes=r(wins.mean()),mean_failures=r(fails.mean()),mean_bags=r(bags.mean()),
 completion_rate=r(done.mean()),capped_rate=r(1-done.mean()),completed_only_mean_gross_per_yuan=r(ratio[done].mean()) if done.any() else None,
 mc_standard_error=r(ratio.std(ddof=1)/math.sqrt(N)),loss_probability=r((net<0).mean()),mean_hours_assumed=1.0 if family=='hourly' else r((wins*25+fails*11+bags*16).mean()/60),
 eligible_for_ranking=bool(done.mean()>=.99 and not z['excluded'] and family!='hourly'))

def audit_tests():
 checks={'thousand_1050_scores_50':max(1050-1000,0)==50,'three_reds_1000_scores_125':1000/2**3==125,'miner_40_red_cells_total':40*100+68*10==4680}
 g=next(x for x in DOC['sections'] if x['name']=='小小巨人');checks['giant_correct_initials_prices']=number(g['tiers'][0][1])==399 and '12' in g['tiers'][0][2] and '30' in g['tiers'][1][2]
 s=SCENARIOS[1];b=bank(s)
 for key in ['red','card','rare','med','fred']:b[key][:]=0
 b['u'][:]=0;b['x'][:]=1000;b['a'][:]=0
 z=dict(family='fixed',price=100,target=1500,mode='绝密',failure_bonus=60,excluded=False);a=simulate(z,s,b)
 checks['fixed_tail_overshoot']=a['expected_gross_w']==2000 and a['mean_rounds']==2
 b['x'][:]=1250;z.update(family='thousand',target=488,failure_bonus=10);a=simulate(z,s,b);checks['thousand_two_1250_complete']=a['expected_gross_w']==2500 and a['mean_rounds']==2
 z.update(family='giant',target=0,price=399,hp=12,hp_cap=25,level=0);a=simulate(z,s,b);checks['giant_12_needs_two_10_damage']=a['mean_rounds']==2
 b['u'][:]=1;z.update(hp=30,hp_cap=None,level=1);a=simulate(z,s,b);checks['all_failure_censor_not_fake_completion']=a['completion_rate']==0 and a['mean_rounds']==H
 assert all(checks.values()),checks
 return checks

def main():
 tests=audit_tests();records=[]
 for section in DOC['sections']:
  for i,t in enumerate(section['tiers']):
   sp=spec_for(section['name'],i,t);records.append(dict(id=f'{section["name"]}::{i}',name=section['name'],tier_index=i,tier=t,model=sp,mechanism=FAMILIES[sp['family']],scenarios={},alternatives={}))
 for s in SCENARIOS:
  print('Generating scenario',s['id'],flush=True);b=bank(s)
  for row in records:
   sp=row['model'];row['scenarios'][s['id']]=simulate(sp,s,b)
   if sp['family']=='miner' and sp['extra_pay']:alt=dict(sp,extra_pay=False);label='988按补差额解释'
   elif sp['family']=='blackhole':
    row['alternatives'][s['id']]={f'q={max(0,min(.98,sp["q"]+d)):.2f}':simulate(dict(sp,q_shift=d),s,b) for d in [-.10,.08]};continue
   elif sp['family']=='bigred' and sp['cells']==368:alt=dict(sp,count_guns=True);label='368格允许枪计入'
   elif sp['family']=='parity':alt=dict(sp,free_miss=True);label='未命中整局免计分'
   elif sp['family']=='ancestor':alt=dict(sp,wait=2);label='等两次连续成功才收菜'
   else:continue
   row['alternatives'][s['id']]={label:simulate(alt,s,b)}
  print('Completed',s['id'],flush=True)
 for row in records:
  vals=[v['mean_gross_per_yuan'] for v in row['scenarios'].values() if v];row['scenario_mean_range']=[min(vals),max(vals)] if vals else None
  for v in row['scenarios'].values():
   if v:
    assert v['p10_gross']<=v['median_gross_per_yuan']<=v['p90_gross'];assert 0<=v['completion_rate']<=1 and v['mean_rounds']<=H;assert v['mean_net_per_yuan']<=v['mean_gross_per_yuan']+.0001
 out=dict(version=VERSION,parameters=PARAMS,tests=tests,records=records,audit_changes=DOC.get('audit_changes',[]),supersedes='v4手工估计值撤回：没有可复算转移模型，原区间不是置信区间，原所谓中位与期望混用。')
 (ROOT/'expected-yield-v5.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 with (ROOT/'expected-yield-v5.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['玩法','档位','价格元/计时按小时','情景','模型','期望毛W/元','估算净W/元','毛中位','毛P10','毛P90','200局结单率','平均局数','备注'])
  for row in records:
   for sid,v in row['scenarios'].items():w.writerow([row['name'],row['tier'][0],row['model']['price'],sid,row['model']['family'],*[v[k] if v else '' for k in ['mean_gross_per_yuan','mean_net_per_yuan','median_gross_per_yuan','p10_gross','p90_gross','completion_rate','mean_rounds']],row['model']['extra']])
 count=sum(r['scenarios']['base'] is not None for r in records)
 summary=dict(version=VERSION,records=len(records),computed_records=count,unmodeled_records=len(records)-count,scenarios=3,repetitions=N,horizon=H,tests=tests,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 (ROOT/'model-v5-report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(summary)
if __name__=='__main__':main()
