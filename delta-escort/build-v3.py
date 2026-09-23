#!/usr/bin/env python3
"""Calibrate the existing static reference build; retain source posters and URLs.
Only anonymous aggregates are rendered, never user photos or account identifiers.
"""
from pathlib import Path
import hashlib
import html
import json
import math
import os

ROOT = Path(__file__).resolve().parent
CAL = json.loads((ROOT / 'ranking-v3.json').read_text(encoding='utf-8'))
assert CAL['version'] == '2026-09-23-r4'\nYIELD = json.loads((ROOT / 'expected-yield-v4.json').read_text(encoding='utf-8'))\nYIELD_MAP = {x['name']: x for x in YIELD['items']}\nassert len(YIELD_MAP)==36
assert sorted(x['rank'] for x in CAL['ranking']) == list(range(1, 37))
assert len({x['name'] for x in CAL['ranking']}) == 36
case = CAL['case']
assert sum(x['rounds'] for x in case['days']) == 26
assert sum(x['reported_valid_extractions'] for x in case['days']) == 4
assert math.isclose(sum(case['clearly_identified_full_values_w']), 4362.555, abs_tol=1e-6)
assert math.isclose(sum(case['clearly_identified_full_values_w']) + sum(case['additional_ui_success_values_w']), 5307.9787, abs_tol=1e-6)
assert math.isclose(sum(max(v - 1000, 0) for v in case['clearly_identified_full_values_w']), 1484.9128, abs_tol=1e-6)
assert math.isclose(1484.9128 - (1288 + 19*10), 6.9128, abs_tol=1e-6)
assert math.isclose(1484.9128 - (1288 + 22*10), -23.0872, abs_tol=1e-6)
poster_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'posters').iterdir() if p.is_file()}
assert len(poster_hashes) == 40

def esc(v):
    return html.escape(str(v), quote=True)

rows = ''.join('<tr><th>'+esc(d['label'])+'</th><td>'+str(d['rounds'])+'</td><td>'+str(d['reported_valid_extractions'])+'</td><td>'+esc(d['notes'])+'</td></tr>' for d in case['days'])
scenarios = ''.join('<div class="scenario"><h4>'+esc(a)+'</h4><p>'+esc(b)+'</p></div>' for a,b in CAL['account_effect']['scenarios'])
links = ''.join('<li><a href="'+esc(r['url'])+'" target="_blank" rel="noopener">'+esc(r['label'])+'</a><p>'+esc(r['note'])+'</p></li>' for r in CAL['references'])
CASE_HTML = '''
<section class="case-panel" aria-labelledby="case-heading">
<div class="case-heading"><span class="eyebrow">NEW · 2026-09-23</span><h2 id="case-heading">这次按「高压装备局」重新排</h2><p>用一张388元订单校准，而不是把失败多、装备贵，直接等同于性价比高。</p></div>
<div class="case-metrics"><div><b>26</b><span>口述总局数 · 4天</span></div><div><b>4</b><span>口述有效撤离</span></div><div><b>15.4%</b><span>本单样本比例，非固定胜率</span></div><div><b>5把AWM</b><span>只确认结单这一局</span></div></div>
<p class="case-key">核心修正：<strong>贵枪 ≠ 多个合格红；容易缴枪 ≠ 容易拿齐15张狗牌；接受跨天 ≠ 值得为反复清零付溢价。</strong></p>
<details class="case-review"><summary>四天订单复盘 · 看计分、带出与口径差异</summary><div class="case-body">
<div class="table-scroll"><table class="evidence-table"><thead><tr><th>阶段</th><th>局数</th><th>有效撤离（口述）</th><th>依据与不确定性</th></tr></thead><tbody>__DAY_ROWS__</tbody></table></div>
<div class="warning"><strong>先避免重复计算</strong><p>__COUNT_WARNING__</p></div>
<h3>三种带出显示值口径，不能相加</h3><div class="table-scroll"><table class="evidence-table"><thead><tr><th>口径</th><th>合计显示价值</th><th>含义</th></tr></thead><tbody>
<tr><td>三次明确点名、图中可核的完整撤离</td><td>4362.56W</td><td>1372.0399＋877.6422＋2112.8729；不含其余记录</td></tr>
<tr><td>截图可辨认的五条成功记录</td><td>5307.98W</td><td>再含558.2213、387.2024；可能含丢包撤，并非五次有效满包</td></tr>
<tr><td>口述第三天970W若确实另行带出</td><td>5332.56W</td><td>前三个点名值＋970；不再叠加可能重合的558与387</td></tr>
</tbody></table></div>
<p class="read-note">__VALUE_WARNING__</p>
<p>仅按截图五条显示值除388元为<strong>13.68W／元毛显示值</strong>，不是净币价比。总在线小时未知，不能把4个自然日当4×24小时，也不能据此计算净时薪。</p>
<h3>为什么不建议看到打得久就升888？</h3>
<p>两次明确超过1000W的计分为<strong>372.0399＋1112.8729＝1484.9128W</strong>。如果19次失败需要加10W，388档目标678W、888档目标1478W，两档可能同一最后局结束；若22次都加，则888档还差23.0872W。真实补偿次数未确认。</p>
<p class="muted">这是同路径的静态重放，不是认为换套餐后打手必然采取同样打法。丢包、个人失误等可能有不同补偿口径；“970万本来能撤”若未实际带出，不进入实得统计。</p>
<div class="example"><strong>这单证明了什么，没有证明什么</strong><p>证明这个组合在这单有效撤离少，且至少一个成功局有集中AWM枪源。不证明账号被永久锁定高强度、不证明所有成功局都有5把AWM、不证明全店长期撤离率是15.4%。结单大胜本身受到停止条件选择。</p></div>
</div></details>
<details class="case-review"><summary>打手换号能控强度？本次如何纳入判断</summary><div class="case-body"><p>__ACCOUNT_TEXT__</p><div class="scenario-grid">__SCENARIOS__</div><p class="muted">__ACCOUNT_VERIFY__</p></div></details>
<details class="case-review"><summary>档位为什么变了 · 矿工、爬塔、AW单的敏感性</summary><div class="case-body"><h3>黄金588与988：额外补是真的，也不是无条件选988</h3><p>__MINER__</p><h3>永恒之塔：低撤离可能只增加长尾，不增加实际收益</h3><p>__TOWER__</p><h3>战争1088：撤销把三AW视为稳定稀缺条件的溢价</h3><p>__WAR__</p></div></details>
<details class="case-review"><summary>证据边界与来源</summary><div class="case-body"><p>__METHOD__</p><p>__SCOPE__</p><ul class="case-links">__LINKS__</ul><p class="muted">__PRIVACY__</p></div></details></section>
'''
for key,value in {
    '__DAY_ROWS__':rows,'__COUNT_WARNING__':esc(case['count_warning']),'__VALUE_WARNING__':esc(case['value_warning']),
    '__ACCOUNT_TEXT__':esc(CAL['account_effect']['text']),'__SCENARIOS__':scenarios,'__ACCOUNT_VERIFY__':esc(CAL['account_effect']['verification']),
    '__MINER__':esc(CAL['sensitivity']['miner']),'__TOWER__':esc(CAL['sensitivity']['tower']),'__WAR__':esc(CAL['sensitivity']['war']),
    '__METHOD__':esc(CAL['method']),'__SCOPE__':esc(CAL['scope']),'__LINKS__':links,'__PRIVACY__':esc(case['privacy'])
}.items():
    CASE_HTML=CASE_HTML.replace(key,value)
EXTRA_CSS='''
.case-panel{margin:20px 0 22px;border:1px solid #496556;background:#111f18;border-radius:15px;padding:19px}.case-heading h2{font-size:22px;margin:5px 0 9px;line-height:1.4}.case-heading p{color:#c0d1c5;font-size:14px;margin:0}.case-metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:17px 0}.case-metrics>div{border:1px solid #365241;border-radius:10px;padding:11px;background:#14271b}.case-metrics b{display:block;font-size:23px;color:#c5f0cd;line-height:1.3}.case-metrics span{font-size:11px;color:#b4c6b8;display:block;margin-top:5px}.case-key{font-size:14px;color:#d2e8d9}.case-review{border:1px solid #3b4e41;background:#101a14;border-radius:10px;margin:10px 0}.case-review>summary{cursor:pointer;padding:12px 13px;font-size:14px;font-weight:650;scroll-margin-top:160px}.case-body{padding:0 14px 16px}.case-body p{font-size:14px;overflow-wrap:anywhere}.table-scroll{overflow-x:auto;width:100%;margin:15px 0}.evidence-table{border-collapse:collapse;width:100%;font-size:12px;line-height:1.65;min-width:400px}.evidence-table th,.evidence-table td{border-bottom:1px solid #354c3f;padding:9px 8px;text-align:left;vertical-align:top}.evidence-table th{color:#c7e7d0}.scenario-grid{display:grid;gap:9px}.scenario{border:1px solid #344f3c;border-radius:10px;padding:12px}.scenario h4{color:#b1e5c2}.scenario p{margin:8px 0 0}.case-links{padding-left:20px}.case-links p{font-size:12px}.yield-tag{font-size:11px;border:1px solid #4c6b5c;background:#173226;border-radius:5px;padding:3px 6px;color:#b9f0ca;font-weight:700}.yield-box{margin:14px 0;background:#14291e;border:1px solid #3b664c;border-radius:11px;padding:13px}.yield-box strong{color:#c4f0d1}.yield-box p{margin:6px 0;font-size:13px}.yield-box small{color:#91aa99}.change-tag{font-size:11px;border:1px solid #4a6252;background:#213a29;border-radius:5px;padding:3px 6px;color:#c3ddca}.account-note{background:#18292b;border-left:3px solid #6d9e9a;padding:10px 12px;font-size:13px;color:#c7dddd;margin:12px 0}@media(min-width:780px){.case-metrics{grid-template-columns:repeat(4,minmax(0,1fr))}.scenario-grid{grid-template-columns:1fr 1fr}.case-panel{padding:23px}.case-heading h2{font-size:25px}}
'''
source_path=ROOT/'build.py'
code=source_path.read_text(encoding='utf-8')
def patch(old,new,expected=1):
    global code
    n=code.count(old)
    if expected is not None and n!=expected:
        raise RuntimeError('Base build changed: '+str(n)+' occurrence(s) of '+old[:85])
    code=code.replace(old,new)
patch("rank_map = {r['name']: r for r in RANKS}","""rank_map = {r['name']: r for r in RANKS}
calibration = json.loads((ROOT / 'ranking-v3.json').read_text(encoding='utf-8'))
previous_ranks = {r['name']: r['rank'] for r in RANKS}
assert set(previous_ranks) == {r['name'] for r in calibration['ranking']}
for updated in calibration['ranking']:
    item = dict(rank_map[updated['name']])
    item.update(updated)
    item['previousRank'] = previous_ranks[item['name']]
    rank_map[item['name']] = item
for name,item in rank_map.items():
    if name in YIELD_MAP:
        item['yield'] = YIELD_MAP[name]
DOC['version'] = YIELD['version']
""")
patch("'ranking_snapshot': '2026-09-18'","'ranking_snapshot': '2026-09-23'")
patch("ident = 'play-' + str(rank or (idx + 1))","ident = 'play-' + str(analysis.get('previousRank', rank) or (idx + 1))")
patch("        title = f'<span class=\"rank\">","""        if rank:
            meta += f'<span class="change-tag">旧版 {analysis["previousRank"]} → 本版 {rank}</span>'
        title = f'<span class="rank">""")
patch('data-rank="{rank or 999}" data-minprice=','data-rank="{rank or 999}" data-oldrank="{analysis.get(\'previousRank\', rank) or 999}" data-minprice=')
patch('<h4>同玩法档位优先顺序</h4>','<div class="account-note"><strong>账号／队伍变化后的敏感性</strong><p>{e(analysis.get("accountSensitivity"))}</p></div><h4>本次档位优先顺序</h4>')
patch('沿用2026-09-18分析，属于主观概率判断；不是实测收益，也不是2026-09-22重新核定的购买结论。','2026-09-23按一单实战重新判断；新增“万哈夫币/元”毛收益模型。只有千万388有本次样本，其余为规则+概率假设的模型估值，不是商家承诺。')
patch('规则阅读版 · v2','期望收益版 · v4')
patch('先看懂玩法，<br>再选护航单。','每一块钱，<br>大概能吃多少万？')
patch('排行榜只是参考。每个条目都附有<strong>各价位差异、具体结单规则和商家原文海报</strong>，点开即可逐条核对。','新增<strong>期望毛收益（万哈夫币/元）</strong>：每个玩法给中位估值、保守—乐观区间和置信度；规则、原图与实战复盘继续保留。')
patch('排名沿用2026-09-18的主观概率判断，未掌握商家订单流水。文字规则为整理版，原文以完整海报为准；不清楚的数字保留“待核”。原图归档于2026-09-22，活动仍展示不代表仍有效。本页不是商家或游戏官方页面。','期望收益口径＝老板最终实际带出毛价值÷人民币价格，单位万哈夫币/元。区间表达掉落、撤离、任务推进、打手打法等不确定性；暂未扣战备、药弹、维修、交易损耗。不是商家承诺或长期实测。')
patch('前36项按旧版参考名次排列，末3项为全店须知与储值说明。','前36项按本次高压装备局购买优先级排列，卡片标出旧→新名次；末3项为须知与储值。35／36项因报价或活动状态未确认，仅保留观察，不代表确认可下单。')
patch('2026-09-22-r2','2026-09-23-r3',expected=None)
patch("    assert content.count('class=\"play\"') == 39","""    content = content.replace('<div class="toolbar enhanced-only">', CASE_HTML + '<div class="toolbar enhanced-only">', 1)
    content = content.replace('</style>', EXTRA_CSS + '</style>', 1)
    assert content.count('class="play"') == 39""")
patch("    (ROOT / 'build-report.json').write_text","""    report['calibration'] = {'anonymous_cases': 1, 'reported_rounds': 26, 'reported_valid_extractions': 4, 'count_discrepancy_disclosed': True, 'actual_profit_unknown': True, 'account_matchmaking_unverified': True, 'user_photos_published': False, 'previous_anchors_preserved': True}
    (ROOT / 'build-report.json').write_text""")
os.environ['ESCORT_USE_ARCHIVED']='1'
exec(compile(code,str(source_path),'exec'),{'__file__':str(source_path),'__name__':'__main__','CASE_HTML':CASE_HTML,'EXTRA_CSS':EXTRA_CSS})
assert poster_hashes == {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'posters').iterdir() if p.is_file()}
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
    for width in [360,390,1440]:
        context=browser.new_context(viewport={'width':width,'height':900})
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto((ROOT/'index.html').as_uri())
        assert page.locator('body').get_attribute('data-version')==YIELD['version']
        assert page.locator('#play-2').get_attribute('data-rank')=='25'
        assert page.locator('#play-6').get_attribute('data-name')=='小香手'
        assert page.locator('#play-6').get_attribute('data-rank')=='18'
        assert page.locator('.change-tag').count()==36
        assert page.locator('.source-block img').count()==40
        order=page.locator('details.play[data-kind=rank]').evaluate_all('(els)=>els.map(e=>Number(e.dataset.rank))')
        assert order==list(range(1,37))
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
        page.screenshot(path=f'/tmp/escort-verified-v3-{width}.png')
        page.locator('.case-review').first.locator('summary').click()
        assert page.locator('.evidence-table').first.is_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
        page.locator('.case-review').first.scroll_into_view_if_needed()
        page.screenshot(path=f'/tmp/escort-verified-v3-case-{width}.png')
        assert not errors
        context.close()
    browser.close()
report_path=ROOT/'build-report.json'
report=json.loads(report_path.read_text())
report['checks'].update({'mobile_360px':'passed','calibration_panel':'passed','all_36_ranks_reordered':'passed','old_deep_links_preserved':'passed','40_original_posters_unchanged':'passed'})
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('V4 passed: 36 new ranks, 39 sections, 170 tier records, 40 unchanged source posters; no uploaded user images.')
