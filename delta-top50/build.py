#!/usr/bin/env python3
"""Render a frozen COMPUTED snapshot, not a new simulation or hand-entered EV model.
The full 152-quote register, six-scene outputs and reproducible engine are supplied
in the research workbook/ZIP. Never reuse this presentation file as model input.
Only writes delta-top50/index.html, top50.csv and audit.json.
"""
from pathlib import Path
import csv,html,json
P=Path(__file__).resolve().parent
VERSION='cross-shop-2026-09-30'
SHOPS={
'X':('西西糖电竞','https://app1.lilihuyu.com/s/pages/7000000005368056#tab=2300021214589087','9月24日核图归档；活动接单与派单质量另核'),
'Y':('游途电竞','https://docs.qq.com/doc/DS0FCYVdtbVhVSktn','9月27日实际读到的四张海报；未宣称读完所有折叠内容'),
'J':('聚琳琅电竞','https://www.jllyx.com/','9月30日实时价格与详情；附加海报未全部逐字核清'),
'M':('鼠鼠学院','https://www.aimouseacademy.com/','公开可检索价目；实时首页需进一步进入，接单条件另核'),
'Z':('战一下电竞','https://zhan1x.com/','9月30日实时全文；旧评论和落款不是近期履约证明'),
'B':('血族电竞','https://xz.sybb.pw/pricing','9月30日实时分类/商品详情；不用过时搜索价或镜像折扣'),
'T':('宅宅鼠电竞','https://zhaizhaishu.com/','9月30日正文；证书日期报错，仅供报价研究，异常页面不要支付或输入账号'),
'L':('裂影电竞','https://lieyingpw.com/#/price','9月30日端游护航分类；不混用手游价')}
RAW='''Z|特调单888|888|2888|14.4|33.5|普通报价|collection
Y|展馆消消乐6格|328|1288|13.7|33.8|普通报价|display
Z|提神醒脑288|288|1488|12.6|27.5|普通报价|collection
Z|提神醒脑388|388|1888|12.0|27.2|普通报价|collection
X|秋日轻享79|79|588|11.5|14.5|活动，续期/派单须确认|fixed
B|体验98|98|788|11.1|11.4|每人限一次|fixed
Y|AZ3不同出生点12个|1688|8888|11.1|18.8|普通报价|spawn
J|环切尔诺贝利12出生点|1688|5188|11.1|18.8|普通报价|spawn
Y|新容器18控制台+10钥匙房|888|2888|10.8|25.8|普通报价|containers
X|千万才是开始388|388|488|10.6|20.8|普通报价|thousand
Z|特调单228|228|1188|10.3|21.3|普通报价|collection
B|核电站88|88|588|10.2|12.1|普通报价|fixed
Y|沙色保险4个/178|178|1000|9.6|15.5|每日一次|sand
J|环切尔诺贝利6出生点|588|1788|9.6|13.1|普通报价|spawn
X|大红爆仓50格|788|3088|9.4|24.3|普通报价|redcells
Y|AZ3不同出生点9个|1088|5688|9.4|13.9|普通报价|spawn
Y|AZ3不同出生点3个|268|1088|9.2|11.9|普通报价|spawn
X|黄金大矿工588|588|0|9.2|18.9|普通报价|miner
Y|沙色保险4个/188|188|1000|9.1|14.7|同日续价|sand
Y|沙色保险6个/308|308|1588|9.1|19.3|普通报价|sand
Y|沙色保险8个/398|398|2188|9.0|19.5|普通报价|sand
Y|新容器2控制台+1钥匙房|158|588|9.0|19.9|普通报价|containers
Y|沙色保险10个/488|488|3000|8.9|19.7|普通报价|sand
X|秋日轻享148|148|1000|8.9|10.5|活动，续期/派单须确认|fixed
X|大红爆仓25格|488|2288|8.9|21.4|普通报价|redcells
J|环切尔诺贝利3出生点|288|888|8.5|11.0|普通报价|spawn
B|周体验128|128|788|8.5|8.7|每周限制|fixed
L|端游护航128|128|788|8.5|8.7|新人每人限1单|fixed
X|秋日轻享268|268|2038|8.5|9.2|活动，续期/派单须确认|fixed
T|护航168|168|1088|8.4|9.5|每日体验一次/监狱+20|fixed
T|每日趣味99|99|2000|8.4|11.1|每日限制|daily
X|千万才是开始888|888|1288|8.4|20.5|普通报价|thousand
Y|新容器5控制台+3钥匙房|388|1288|8.0|19.0|普通报价|containers
Y|展馆消消乐9格|888|3588|8.0|23.0|普通报价|display
Z|绝密保底118|118|700|8.0|9.3|每日体验一次|fixed
J|环切尔诺贝利9出生点|1288|3888|8.0|11.8|普通报价|spawn
X|秋日轻享688|688|5555|7.9|8.4|活动，续期/派单须确认|fixed
M|沙色2个|168|788|7.9|10.4|普通报价|sand
Y|AZ3不同出生点5个|568|3088|7.9|10.5|普通报价|spawn
B|航天138|138|788|7.9|8.1|普通报价|fixed
X|秋日轻享399|399|3000|7.8|8.5|活动，续期/派单须确认|fixed
J|绝密保底258|258|1888|7.8|8.0|普通报价|fixed
X|秋日轻享888|888|7188|7.8|8.2|活动，续期/派单须确认|fixed
M|基础护航158|158|888|7.7|9.1|普通报价|fixed
Z|不出一直打3同红|1488|4888|7.6|20.4|普通报价|pairs
Z|特调单488|488|1888|7.6|16.5|普通报价|collection
X|绝密体验188|188|1088|7.5|8.5|普通报价|fixed
X|秋日轻享1388|1388|10888|7.4|7.8|活动，续期/派单须确认|fixed
Z|不出一直打2同红|688|1688|7.3|19.4|普通报价|pairs
B|巴克什228|228|1488|7.3|7.8|普通报价|fixed'''
METHOD={
'fixed':'累计有效计分达到目标。保留最后一局完整带出，失败补偿是后续义务，不是立即到账。不同价位假设同产能，仅为合同对比，不能证明低价也能派来同水平队伍。',
'collection':'同时满足物品清单和币量目标。物品的实际出货率没有可靠统计；本模型采用明确假设并测试快/慢推进。因任务拖长而排前，不代表真实掉率已被验证。',
'display':'收集红（甲修不算）、金卡和红卡填柜；相同红成对消除；失败保险红也计。模型测试允许拒放重复物与强制消除两种分支，取更低均值。指定地图加价30%尚未计入默认价格。',
'spawn':'不同出生点分别成功撤离一次，重复点不新增进度。游途仅计超过300W；聚琳琅可读文字未明确该门槛，不直接移植。模型假设14个候选类别并测试偏斜/均匀，非官方出生概率。',
'containers':'成功撤离才推进控制台与隐秘钥匙房数量，二类任务与币量均达标才结束。每次成功开多少容器未知，本模型只作速度压力测试，不把地图总容器数当单局可得。',
'thousand':'成功局只计超过1000W的部分，失败+10W目标，丢包流局。388目标488W，888目标1288W。最后一局带出全部归收益账，不截到目标值。',
'sand':'数量任务与币量同时看。游途178/188是摸到即算，308/398/488仅成功计沙色。鼠鼠学院仅公开数量，未明失败资格，保守情景按摸到即计而非宣称真实规则。',
'redcells':'数红的格数不是件数；25/50格档失败塞保险的红也计进度。六套、枪、背包等不自动当任务红；同时完成币量。',
'miner':'累计108格金/红；金每格10W、红每格100W算目标，588收集期收益抵计算保底。打手帮带可推进任务，但不自动把帮带价值全部计入老板收入。',
'daily':'99元不是直接买2000W。每金减目标300、每红减400；失败所获金红按50%抵，失败+60；至少成功一把后才可结束。',
'pairs':'累计任意同种红2个或3个，不可指定。与相同格数、单局同时带出完全不同；同时达到币量目标。24种合成红只是模拟类别，不是真实物品表。'}
SPECIAL={
'特调单888':'清单：香槟4、龙舌兰4、柠檬茶8、可乐8、特色酒杯8；保底2888W。',
'特调单228':'清单：龙舌兰1、柠檬茶3、可乐3；保底1188W。',
'特调单488':'清单：香槟1、龙舌兰1、柠檬茶3、可乐3；保底1888W。',
'提神醒脑288':'清单：咖啡1、挂耳咖啡1、咖啡机1、摩卡咖啡1；保底1488W。',
'提神醒脑388':'清单：高级咖啡豆1、挂耳咖啡1、咖啡机1、摩卡咖啡2；保底1888W。',
'沙色保险4个/178':'每天限一次；4沙色＋1000W；摸到就算，不包全卡。',
'沙色保险4个/188':'同日后续价格；4沙色＋1000W；摸到就算，不包全卡。',
'沙色保险6个/308':'6沙色＋1588W；失败不计沙色；包塔内卡，但未开完不算炸单。',
'沙色保险8个/398':'8沙色＋2188W；失败不计沙色；包塔内卡，但未开完不算炸单。',
'沙色保险10个/488':'10沙色＋3000W；失败不计沙色；包塔内卡，但未开完不算炸单。',
'秋日轻享268':'2038W沿用已归档提取；海报9.1—10.20，实际在售和具体数值付款前再确认。',
'护航168':'每日限一次；仅包过点卡，女护默认机密，监狱加20元。不能把本档默认当同待遇绝密双护。',
'绝密保底258':'聚琳琅价格页258元保1888W；禁止老板私带AW子弹进图。',
'端游护航128':'裂影实时端游新人128保788，每人限1单；不是旧预览中的98。'}
DIRECT={
('B','体验98'):'https://xz.sybb.pw/pricing/product/584323684421',
('B','核电站88'):'https://xz.sybb.pw/pricing/product/981947650693',
('B','周体验128'):'https://xz.sybb.pw/pricing/product/1156412446597',
('B','航天138'):'https://xz.sybb.pw/pricing/product/584323686277',
('B','巴克什228'):'https://xz.sybb.pw/pricing/product/584323685125',
('J','绝密保底258'):'https://www.jllyx.com/#/product/prod-319a33a4'}
def e(v):return html.escape(str(v),quote=True)
records=[]
for i,line in enumerate(RAW.splitlines(),1):
 s,n,p,b,lo,hi,limit,kind=line.split('|');records.append(dict(rank=i,shop_code=s,shop=SHOPS[s][0],name=n,price=float(p),base=float(b),low=float(lo),high=float(hi),limit=limit,kind=kind,rule=SPECIAL.get(n,'')+' '+METHOD[kind],url=DIRECT.get((s,n),'https://www.jllyx.com/#/product/prod-5ccf7ad0' if s=='J' and kind=='spawn' else SHOPS[s][1])))
assert len(records)==50 and len(set((x['shop'],x['name']) for x in records))==50
# The ordering is frozen from unrounded means; do not re-sort rounded presentation values.
cards=[]
for r in records:
 tail='含少量300局仍未结样本，数值是观察窗均值，不是完整订单精确期望。' if r['rank'] in [1,7,8,45] else ''
 unknown='此店完整通用炸补未取得，模型没有虚加赔付；不表示商家实际不赔。' if r['shop_code'] in ['Z','Y','J','B','L'] else '已知炸补按规则加入未来义务；默认同水平打手仅为合同比较。'
 target='108格金红动态计算' if r['kind']=='miner' else f"{r['base']:g}W（计分目标，不必等于仓库净增加）"
 cards.append(f'''<details class="offer" data-shop="{e(r['shop'])}" data-price="{r['price']}" id="rank-{r['rank']}"><summary><span class="rank">{r['rank']:02}</span><div class="name"><small>{e(r['shop'])}</small><b>{e(r['name'])}</b><span>¥{r['price']:g} · {e(r['limit'])}</span></div><div class="metric"><b>{r['low']:.1f}</b><small>万／元 · 情景较低均值</small></div></summary><div class="detail"><p>{e(r['rule'])}</p><div class="facts"><div><small>六组均值范围</small><b>{r['low']:.1f}–{r['high']:.1f} 万／元</b></div><div><small>基础目标</small><b>{e(target)}</b></div></div><p class="warning">{e(unknown)} {e(tail)} 所有掉落、撤离及任务推进参数均为假设；排名不是商家或官方承诺。</p><a href="{e(r['url'])}" target="_blank" rel="noopener noreferrer">查看商家原始价目 ↗</a><p class="muted">{e(SHOPS[r['shop_code']][2])}。本页为规则摘要，完整原文请在来源核对。</p></div></details>''')
css='''
:root{color-scheme:dark;--bg:#0d141a;--card:#16222c;--line:#304351;--muted:#a9bbc7;--green:#ade7bb}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 90% 0,#234138,transparent 45%),var(--bg);color:#edf3f5;font:15px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}.wrap{max-width:1060px;margin:auto;padding:0 18px 50px}header{padding:26px 0}.mast{font-size:12px;letter-spacing:.1em;color:var(--green);border-bottom:1px solid var(--line);padding-bottom:14px}h1{font-size:clamp(33px,6vw,58px);line-height:1.15;letter-spacing:-.04em;margin:25px 0 15px}header p{color:var(--muted);max-width:840px}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:20px}.kpis div{padding:12px;border:1px solid var(--line);border-radius:12px;background:#11201c}.kpis b{display:block;font-size:25px}.kpis span{font-size:11px;color:var(--muted)}.warning{background:#2a2317;color:#ead6af;border-left:3px solid #c2a461;border-radius:8px;padding:13px;font-size:13px}.method{background:#132029;border:1px solid var(--line);border-radius:11px;margin:15px 0}.method>summary{cursor:pointer;padding:13px;font-weight:700}.method>div{padding:0 15px 15px;color:var(--muted);font-size:14px}.toolbar{position:sticky;top:0;z-index:5;background:#0d141af5;backdrop-filter:blur(10px);padding:12px 0}.controls{display:grid;grid-template-columns:1fr 145px 115px;gap:8px}input,select,button{font:inherit;font-size:14px;min-width:0;background:#192d39;color:#edf3f5;border:1px solid #415969;border-radius:10px;padding:10px}.links{display:flex;gap:10px;flex-wrap:wrap;font-size:13px;margin:16px 0}a{color:var(--green);text-underline-offset:4px}.heading{display:flex;align-items:center;justify-content:space-between;margin:20px 0 12px}.heading h2{font-size:21px;margin:0}.heading small{color:var(--muted)}.offer{background:linear-gradient(135deg,#182731,#111b23);border:1px solid var(--line);border-radius:13px;margin:10px 0;overflow:hidden;scroll-margin-top:160px}.offer>summary{display:flex;gap:12px;align-items:center;padding:15px;cursor:pointer;list-style:none}.offer>summary::-webkit-details-marker{display:none}.rank{align-self:flex-start;display:grid;place-items:center;min-width:36px;height:38px;background:#273e4b;color:#c1d3de;font-weight:800;border-radius:9px}.offer:nth-child(-n+3) .rank{color:#f0dc9d;background:#3d3926}.name{flex:1;min-width:0}.name small{display:block;color:var(--muted);font-size:11px}.name b{display:block;font-size:16px}.name span{display:block;color:var(--green);font-size:12px}.metric{text-align:right;flex-shrink:0;max-width:110px}.metric b{display:block;font-size:27px;color:var(--green);line-height:1.2}.metric small{display:block;color:var(--muted);font-size:9px}.detail{padding:3px 16px 16px;border-top:1px solid var(--line)}.facts{display:grid;grid-template-columns:1fr 1fr;gap:8px}.facts>div{padding:10px;border-radius:9px;background:#122b20;border:1px solid #365d45}.facts small{display:block;color:var(--muted);font-size:11px}.facts b{display:block;font-size:14px}.muted{font-size:12px;color:var(--muted)}.sources details{border:1px solid var(--line);border-radius:9px;margin:8px 0;padding:11px}.sources summary{cursor:pointer}.sources p{color:var(--muted);font-size:13px}footer{color:var(--muted);font-size:12px;text-align:center;margin-top:30px}.js-only{display:none}.js .js-only{display:block}[hidden]{display:none!important}:focus-visible{outline:2px solid var(--green);outline-offset:3px}@media(max-width:600px){.controls{grid-template-columns:1fr 1fr}.controls input{grid-column:1/-1;font-size:16px}.offer>summary{padding:12px;gap:8px}.name b{font-size:14px}.metric{max-width:78px}.metric b{font-size:24px}.metric small{font-size:8px}.kpis div{padding:9px}.kpis b{font-size:23px}.facts b{font-size:12px}}
'''
js='''(function(){let q=document.getElementById('q'),s=document.getElementById('shop'),b=document.getElementById('budget'),cards=[...document.querySelectorAll('.offer')];function show(){let n=0;cards.forEach(c=>{let ok=(!q.value||c.textContent.toLowerCase().includes(q.value.toLowerCase()))&&(!s.value||c.dataset.shop===s.value)&&(!b.value||+c.dataset.price<=+b.value);c.hidden=!ok;if(ok)n++;});document.getElementById('count').textContent=n+' / 50';}q.oninput=s.onchange=b.onchange=show;document.documentElement.classList.add('js');show();if(location.hash){let e=document.getElementById(location.hash.slice(1));if(e&&e.classList.contains('offer')){e.open=true;e.scrollIntoView();}}})();'''
options=''.join('<option>'+e(v[0])+'</option>' for v in SHOPS.values())
sources=''.join(f'<details><summary>{e(v[0])}</summary><p>{e(v[2])}</p><a href="{e(v[1])}" target="_blank" rel="noopener">原始价目 ↗</a></details>' for v in SHOPS.values())
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0d141a"><meta name="robots" content="noindex,nofollow"><title>跨店护航Top50｜统一条件比较</title><style>__CSS__</style></head><body data-version="cross-shop-2026-09-30"><div class="wrap"><header><div class="mast">DELTA / CROSS-SHOP RESEARCH · 2026.09.30</div><h1>同一把尺子，<br>比较不同店的护航单。</h1><p>8家公开价目，152条套餐记录。保留价格、任务和失败细则的差异，按六组统一假设的较低平均净收益排序。<strong>这是公开样本的条件比较，不是被统计证明的全网最优。</strong></p><div class="kpis"><div><b>8</b><span>来源店铺</span></div><div><b>152</b><span>报价记录</span></div><div><b>145</b><span>条件测算档位</span></div><div><b>50</b><span>本页比较候选</span></div></div></header><p class="warning"><b>不要把右侧数字当保证收益。</b>单位是万哈夫币／人民币元，来自六组假设中较低的平均值。任务概率、店铺实力和履约情况未经实测验证。相邻差距小于0.5W／元不视为显著。</p><details class="method"><summary>统一标准、关键假设与排除规则</summary><div><p>净收益＝模型新增带出×90%－成功局8W－失败局55W－丢包局35W，再除以人民币价格。90%不是官方税率；不把原有战备重复算收入。</p><p>环境完整撤离率30%／50%／65%，分别测慢／快任务推进，共6组。每组每档1600次，最多300局。同机制跨店参数一致；不使用用户个人对局来校准其他店。</p><p>物品、出生点和任务推进率是明示的合成假设，不是官方掉率。前排特调、咖啡、展柜和容器单尤其敏感。源页面缺少的额外赔付不虚加；不是宣称商家无赔付。</p><p>145档中18档有情景300局完成率不足99%，不进入Top50；另7档缺关键数字或语义不计算。第1、7、8、45项含极少未结样本，数值仍是观察窗均值，不称完整订单精确期望。</p><p>便宜单假设同产能只是合同比较；实际可能派较弱队伍。规则可能允许打手采用最快结单打法。排名没有验证商家资质、账号安全或补偿兑现。</p><p>未把手游、台币占位报价、撞车、账号代打跑刀、过期9.20活动和同品牌镜像混入。长倾圣诞限定等保留为待核线索。没有声称8家已覆盖全互联网。</p><p>完整152档登记、870行情景输出、参数和复算代码，见本次交付的Excel及ZIP。这里是其计算快照，不是重新手填EV。</p></div></details><div class="links"><a href="top50.csv">下载Top50 CSV</a><a href="audit.json">计算审计说明</a><a href="../delta-escort/">西西糖单店原站</a><a href="../delta-youtu/">游途单店原站</a></div><div class="toolbar js-only"><div class="controls"><input id="q" type="search" aria-label="搜索" placeholder="搜玩法、规则或价格"><select id="shop" aria-label="店铺"><option value="">全部店铺</option>__OPTIONS__</select><select id="budget" aria-label="预算"><option value="">不限预算</option><option value="300">300元以内</option><option value="500">500元以内</option><option value="1000">1000元以内</option><option value="2000">2000元以内</option></select></div></div><div class="heading"><h2>统一情景 Top 50</h2><small id="count">50 / 50</small></div><main>__CARDS__</main><noscript>全部数据直接写在网页里，关闭脚本仍可展开规则。</noscript><h2>来源与时效</h2><section class="sources">__SOURCES__</section><footer>2026-09-30计算快照 · 价格以下单确认单为准<br>不因网站自称“纯绿”“100%安全”就作账号安全保证。<br>Firecrawl提示余额偏低，后续大规模批量复核前需补充额度。</footer></div><script>__JS__</script></body></html>'''
page=page.replace('__CSS__',css).replace('__OPTIONS__',options).replace('__CARDS__',''.join(cards)).replace('__SOURCES__',sources).replace('__JS__',js)
assert page.count('class="offer"')==50
assert 'fetch(' not in js
(P/'index.html').write_text(page,encoding='utf-8')
with (P/'top50.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['排名','店铺','具体档位','价格元','基础计分目标W','六情景较低净W/元均值','六情景较高净W/元均值','资格','规则摘要','源页面'])
 for r in records:w.writerow([r['rank'],r['shop'],r['name'],r['price'],r['base'],r['low'],r['high'],r['limit'],r['rule'],r['url']])
audit={'version':VERSION,'shops':8,'quotes_registered':152,'modeled_tiers':145,'critical_unknown_unmodeled':7,'longtail_excluded':18,'top50':50,'scene_count':6,'replications':1600,'horizon':300,'model_sha256':'454a02c2da7778cbbb74d89804af9c765a016fd7b75c5152f657e27987b74619','metric':'minimum of six scenario mean estimated net W/CNY, not a confidence bound or measured expectation','tiny_censor_top50':[1,7,8,45],'result_origin':'computed locally by catalog.py + model.py; workbook and reproducible code delivered separately','checks':{'static_50_rows':True,'eight_shops':len(SHOPS)==8,'old_sites_untouched':True}}
(P/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False))
