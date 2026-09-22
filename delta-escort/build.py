#!/usr/bin/env python3
"""Build only delta-escort/. No changes to the parent blog or Pages settings."""
import concurrent.futures
import hashlib
import html
import json
import os
from pathlib import Path
import re
import time
import urllib.request
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT / 'source-manifest.json').read_text())
DOC = json.loads((ROOT / 'rules.json').read_text())
raw = (ROOT / 'data.js').read_text()
RANKS = json.loads(raw[raw.index('['):].strip().rstrip(';'))
rank_map = {r['name']: r for r in RANKS}
sections = DOC['sections']
assert len(sections) == 39 and len(rank_map) == 36
assert len({x['name'] for x in sections}) == 39
assert all(x['name'] in {a[0] for a in SOURCE['entries']} for x in sections)
POSTERS = ROOT / 'posters'
POSTERS.mkdir(exist_ok=True)
report = {'version': DOC['version'], 'source_snapshot': SOURCE['snapshot'], 'ranking_snapshot': '2026-09-18', 'ranked_games': len(rank_map), 'sections': len(sections), 'tier_records': sum(len(x['tiers']) for x in sections), 'posters': [], 'checks': {}}
asset_map = {}
page_map = {}

# Read only publicly visible catalog image URLs. Expiring query credentials stay in
# memory, never in repository files, logs, or the generated website.
def collect(pw):
    browser = pw.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    context = browser.new_context(viewport={'width': 1280, 'height': 900}, ignore_https_errors=True)
    page = context.new_page()
    page.goto(SOURCE['page'] + '#tab=2300021214589087', wait_until='domcontentloaded', timeout=90000)
    page.wait_for_function('document.querySelectorAll("[role=tab]").length >= 39', timeout=180000)
    found = {}
    aliases = {'一命通关': '一名通关', '我要亿万哈夫币': '我要亿万哈佛币'}
    for name, tab_id, expected in SOURCE['entries']:
        label = aliases.get(name, name)
        ok = page.evaluate('name => { const t = Array.from(document.querySelectorAll("[role=tab]")).find(e => e.textContent.trim() === name); if (!t) return false; t.click(); return true; }', label)
        assert ok, 'Missing catalog tab: ' + name
        page.wait_for_function('expected => Array.from(document.querySelectorAll(".hb-global-image")).some(e => e.src.includes("/" + expected + "/"))', arg=expected[0], timeout=20000)
        page.wait_for_timeout(180)
        urls = page.locator('.hb-global-image').evaluate_all('(els) => els.map(e => e.src)')
        rows = []
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme != 'https' or parsed.hostname != 'hb-v4-attachment-oss.huoban.com':
                raise ValueError('Unexpected source image host')
            m = re.fullmatch(r'/attachment/(\d+)/0', parsed.path)
            if not m:
                raise ValueError('Unexpected source image path')
            rows.append((m.group(1), url))
        assert set(expected).issubset({r[0] for r in rows}), 'Missing image in ' + name
        found[name] = rows
        page_map[name] = SOURCE['page'] + '#tab=' + tab_id
        print('Catalog:', name, len(rows), 'image(s)', flush=True)
    context.close()
    browser.close()
    return found

def download(item):
    asset_id, url = item
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': SOURCE['page']})
            with urllib.request.urlopen(req, timeout=45) as resp:
                blob = resp.read(30_000_001)
            if len(blob) > 30_000_000:
                raise ValueError('Image too large')
            if blob.startswith(b'\xff\xd8\xff'):
                ext = '.jpg'
            elif blob.startswith(b'\x89PNG\r\n\x1a\n'):
                ext = '.png'
            else:
                raise ValueError('Source did not return an original image')
            name = asset_id + ext
            (POSTERS / name).write_bytes(blob)
            return asset_id, {'file': 'posters/' + name, 'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}
        except Exception as exc:
            if attempt == 2:
                raise RuntimeError('Could not archive poster ' + asset_id + ': ' + type(exc).__name__) from None
            time.sleep(1 + attempt)

with sync_playwright() as pw:
    if os.environ.get('ESCORT_USE_ARCHIVED') == '1':
        for name, tab_id, ids in SOURCE['entries']:
            page_map[name] = SOURCE['page'] + '#tab=' + tab_id
            asset_map[name] = []
            for aid in ids:
                matches = list(POSTERS.glob(aid + '.*'))
                assert len(matches) == 1
                blob = matches[0].read_bytes()
                row = {'file': 'posters/' + matches[0].name, 'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}
                asset_map[name].append(row)
                report['posters'].append(row)
    else:
        found = collect(pw)
        work = {aid: url for pairs in found.values() for aid, url in pairs}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            saved = dict(pool.map(download, work.items()))
        for name, pairs in found.items():
            asset_map[name] = [saved[aid] for aid, _ in pairs]
        report['posters'] = list(saved.values())
    assert len(report['posters']) >= 40

    def e(value):
        return html.escape(str(value or ''), quote=True)

    ordered = sorted(sections, key=lambda s: rank_map.get(s['name'], {}).get('rank', 1000))
    cards = []
    for idx, section in enumerate(ordered):
        name = section['name']
        analysis = rank_map.get(name, {})
        rank = analysis.get('rank')
        ident = 'play-' + str(rank or (idx + 1))
        prices = [float(m.group()) for t in section['tiers'] for m in [re.search(r'\d+(?:\.\d+)?', str(t[1]))] if m]
        minimum = min(prices) if prices else 999999
        # Filter refers to any recorded tier, not the price of an inferred favourite.
        meta = f'<span>{e(section.get("map"))}</span><span>{len(section["tiers"])} 档记录</span><span>原图 {len(asset_map[name])} 张</span>'
        title = f'<span class="rank">{str(rank).zfill(2) if rank else "附"}</span><span class="card-head"><span class="name">{e(name)}</span><span class="pick">{e("参考首选：" + analysis.get("pick", "") if rank else "全店规则／储值权益，不参与排名")}</span></span><span class="arrow" aria-hidden="true">＋</span>'
        tier_html = ''
        for t in section['tiers']:
            tier_html += f'<div class="tier"><div class="tier-top"><h4>{e(t[0])}</h4><b>{e(t[1])}</b></div><p class="goal">目标／保底：{e(t[2])}</p><p>{e(t[3])}</p></div>'
        rules_html = ''.join('<li>' + e(x) + '</li>' for x in section['rules'])
        warns = ''.join('<p>' + e(w) + '</p>' for w in section.get('warnings', []))
        if section.get('activity'):
            warns = '<p>' + e(section['activity']) + '</p>' + warns
        images = ''
        for n, poster in enumerate(asset_map[name], 1):
            src = e(poster['file'])
            images += f'<figure><figcaption>商家原文海报 {n} · 点击图片可在新页放大</figcaption><a href="{src}" target="_blank" rel="noopener"><img src="{src}" loading="lazy" decoding="async" alt="{e(name)}：完整商家规则原图第{n}张"></a><a class="text-link" href="{src}" target="_blank" rel="noopener">打开完整原图 ↗</a></figure>'
        analysis_html = ''
        if rank:
            analysis_html = f'<details class="analysis"><summary>参考排名理由 · 非商家规则</summary><div><p>{e(analysis.get("why", analysis.get("mechanism")))}</p><h4>同玩法档位优先顺序</h4><p>{e(analysis.get("tierOrder"))}</p><h4>判断把握：{e(analysis.get("confidence"))}</h4><p>{e(analysis.get("caveat"))}</p><p class="muted">沿用2026-09-18分析，属于主观概率判断；不是实测收益，也不是2026-09-22重新核定的购买结论。</p></div></details>'
        example = f'<div class="example"><strong>算例，不是收益承诺</strong><p>{e(section["example"])}</p></div>' if section.get('example') else ''
        cards.append(f'''<details class="play" id="{ident}" data-rank="{rank or 999}" data-minprice="{minimum}" data-name="{e(name)}" data-kind="{'rank' if rank else 'extra'}">
<summary>{title}</summary><div class="card-preview"><p>{e(section['plain'])}</p><div class="meta">{meta}</div></div>
<div class="detail"><div class="detail-actions enhanced-only"><button type="button" class="save" aria-pressed="false">☆ 收藏</button><button type="button" class="copy">复制规则</button><button type="button" class="jump-source">看商家原文 ↓</button></div>
<p class="read-note">下面是规则整理版，不是逐字引文。完整原文请看本条目下方的商家海报；我的分析单独收在最后。</p>
{('<div class="warning"><strong>日期／待核条款</strong>' + warns + '</div>') if warns else ''}
<h3>各价位到底有什么区别</h3><div class="tiers">{tier_html or '<p>本栏目没有独立价格套餐。</p>'}</div>
<h3>具体玩法与结单规则</h3><ol class="rule-list">{rules_html}</ol>{example}
{('<p class="muted">未单独写明的权益，请同时阅读 <a href="#play-37" class="open-general">全店下单须知</a>；不把通用条款自动覆盖套餐例外。</p>') if rank else ''}
<details class="source-block"><summary>商家原文 · 完整海报原图（{len(asset_map[name])}张）</summary><div class="source-content"><p class="muted">来自商家公开页面，2026-09-22抓取的原始图片，未重写图片文字。海报仍展示不代表活动仍有效。</p>{images}<a class="text-link" href="{e(page_map[name])}" target="_blank" rel="noopener">回商家对应栏目核对当前版本 ↗</a></div></details>
{analysis_html}<p class="muted source-foot">规则整理记录：2026-09-16／18；原图归档：2026-09-22。W＝万哈夫币，R／元＝人民币；保底可能只是计分目标。</p></div></details>''')

    css = '''
:root{color-scheme:dark;--bg:#0b1116;--panel:#131c24;--line:#2b3a46;--muted:#afbdc9;--green:#a6e6bc;--text:#f1f5f7}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}a{color:var(--green);text-underline-offset:4px}button,input,select{font:inherit}button,summary{touch-action:manipulation}button{cursor:pointer}button:focus-visible,summary:focus-visible,input:focus-visible,a:focus-visible{outline:2px solid var(--green);outline-offset:4px}button{border:1px solid var(--line);border-radius:10px;padding:9px 12px;background:#1a2832;color:var(--text)}.wrap{max-width:1120px;margin:auto;padding:0 18px 65px}.mast{display:flex;justify-content:space-between;align-items:center;padding:22px 0 14px;border-bottom:1px solid var(--line);font-size:13px;color:var(--muted)}.mast b{color:var(--green);letter-spacing:.12em}.hero{padding:27px 0 22px}.eyebrow{font-size:12px;color:var(--green);letter-spacing:.13em}.hero h1{font-size:clamp(30px,5vw,48px);line-height:1.25;margin:10px 0 14px;letter-spacing:-.04em}.hero p{max-width:810px;color:var(--muted);margin:0}.stats{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}.stats span{padding:8px 13px;border:1px solid var(--line);border-radius:10px;color:var(--muted);font-size:13px}.stats b{color:#fff;font-size:18px;margin-right:5px}.notice{border-left:3px solid #bd9752;background:#241e15;padding:12px 15px;font-size:13px;color:#e9d6b3;margin:0 0 20px}.toolbar{position:sticky;top:0;z-index:5;background:rgba(11,17,22,.97);padding:12px 0;border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}.search-row{display:flex;gap:8px}.search-row input{background:#14202a;border:1px solid #39505e;border-radius:12px;color:white;padding:12px;width:100%;min-width:0;font-size:16px}.search-row button{white-space:nowrap}.filters{display:flex;gap:7px;overflow-x:auto;padding:10px 0 1px;scrollbar-width:thin}.filters button{white-space:nowrap;font-size:13px;border-radius:999px;padding:7px 12px}.filters button[aria-pressed=true]{background:#254633;border-color:#64876f;color:#d9f5e2}.section-heading{display:flex;align-items:center;justify-content:space-between;margin:24px 0 13px}.section-heading h2{font-size:18px;margin:0}.section-heading span{font-size:12px;color:var(--muted)}.grid{display:grid;grid-template-columns:1fr;gap:12px}.play{background:var(--panel);border:1px solid var(--line);border-radius:15px;overflow:hidden;scroll-margin-top:155px;align-self:start;min-width:0}.play>summary{list-style:none;display:flex;gap:12px;align-items:center;padding:17px 15px 10px;cursor:pointer}.play>summary::-webkit-details-marker{display:none}.rank{display:grid;place-items:center;flex:0 0 39px;height:40px;border-radius:10px;color:var(--muted);font-weight:800;font-size:18px;background:#21303b}.play[data-rank="1"] .rank{background:#3e3520;color:#f9d888}.play[data-rank="2"] .rank{color:#e0e9ed}.play[data-rank="3"] .rank{color:#efcbb2}.card-head{display:block;flex:1;min-width:0}.name{display:block;font-size:18px;font-weight:750}.pick{display:block;color:var(--green);font-size:13px;margin-top:3px;overflow-wrap:anywhere}.arrow{color:#9bb5a5;font-size:23px}.play[open]>.summary .arrow{transform:rotate(45deg)}.card-preview{padding:0 15px 15px}.card-preview p{font-size:14px;color:var(--muted);margin:0 0 9px}.meta{display:flex;gap:6px;flex-wrap:wrap}.meta span{font-size:11px;color:#bdcad3;padding:3px 7px;background:#1e2d37;border-radius:6px}.play:not([open])>.card-preview{display:block}.play[open]{border-color:#668574}.detail{padding:0 16px 20px;border-top:1px solid var(--line)}.detail-actions{display:flex;gap:7px;flex-wrap:wrap;padding-top:14px}.detail-actions button{font-size:13px}.detail-actions .save[aria-pressed=true]{color:#f5d480;border-color:#b58e45}.read-note{font-size:13px;color:#c5d4dc;margin:16px 0}.warning{background:#2c2418;border:1px solid #695337;border-radius:10px;padding:12px;color:#ebd3ae;font-size:14px}.warning p{margin:7px 0 0}h3{font-size:16px;margin:23px 0 12px;color:#e0ede5}h4{font-size:14px;margin:0}.tiers{display:grid;gap:8px;grid-template-columns:1fr}.tier{background:#0e171e;border:1px solid #2c3c46;border-radius:10px;padding:12px}.tier-top{display:flex;gap:12px;align-items:baseline;justify-content:space-between}.tier-top b{color:var(--green);white-space:normal;text-align:right;font-size:14px}.tier p{font-size:13px;color:var(--muted);margin:5px 0 0}.tier p.goal{color:#e0e8ed}.rule-list{padding-left:24px;margin:0}.rule-list li{padding:5px 0 7px 4px;font-size:15px;overflow-wrap:anywhere}.rule-list li::marker{color:var(--green);font-weight:700}.muted{color:var(--muted);font-size:13px;overflow-wrap:anywhere}.example{padding:13px;background:#163325;border-radius:10px;margin:14px 0;font-size:14px}.example p{margin-bottom:0}.source-block,.analysis{margin-top:20px;border:1px solid #476478;border-radius:10px;background:#101c26}.source-block>summary,.analysis>summary{padding:13px 15px;cursor:pointer;font-weight:700;font-size:14px;scroll-margin-top:155px}.source-content,.analysis>div{padding:0 15px 17px}.source-content figure{margin:18px 0}.source-content figcaption{font-size:12px;color:#b7c7d2;margin-bottom:8px}.source-content img{display:block;width:100%;max-width:850px;height:auto;margin:0 auto 12px;border-radius:6px;background:#1c2932}.text-link{font-size:14px}.analysis{border-color:#405a49;background:#14231b}.analysis p{font-size:14px}.analysis h4{margin-top:15px;color:#abd9bb}.source-foot{border-top:1px solid var(--line);padding-top:12px;margin-top:18px}.footer{text-align:center;color:#9aadb9;font-size:12px;margin:35px 0 0}.enhanced-only{display:none}.js .enhanced-only{display:flex}.js .toolbar.enhanced-only{display:block}[hidden]{display:none!important}.empty{border:1px dashed var(--line);padding:24px;text-align:center;border-radius:12px}.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#d5f1df;color:#14291d;padding:10px 18px;border-radius:10px;z-index:20;max-width:90vw;font-size:14px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}@media(min-width:780px){.wrap{padding-left:26px;padding-right:26px}.grid{grid-template-columns:1fr 1fr}.play[open]{grid-column:1/-1}.tiers{grid-template-columns:repeat(2,minmax(0,1fr))}.hero{padding-top:38px}.detail{padding:0 24px 24px}.rule-list{max-width:940px}}@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}@media print{.toolbar,.detail-actions,.mast{display:none!important}.grid{display:block}.play{break-inside:avoid;margin-bottom:12px}}
'''
    js = '''
(function(){'use strict';
var cards=Array.from(document.querySelectorAll('details.play'));var q=document.getElementById('q');var count=document.getElementById('count');var empty=document.getElementById('empty');var mode='all';var saved=new Set();
try{var value=JSON.parse(localStorage.getItem('escortFavs')||'[]');if(Array.isArray(value))saved=new Set(value.filter(function(x){return typeof x==='string';}));}catch(err){}
var corpus=cards.map(function(c){return c.textContent.toLowerCase();});
function toast(t){var el=document.getElementById('toast');el.textContent=t;el.hidden=false;clearTimeout(window.__escortToast);window.__escortToast=setTimeout(function(){el.hidden=true;},2200);}
function filter(){var text=q.value.trim().toLowerCase(),n=0;cards.forEach(function(c,i){var ok=!text||corpus[i].includes(text);if(mode==='top10')ok=ok&&Number(c.dataset.rank)<=10;if(mode==='budget')ok=ok&&Number(c.dataset.minprice)<=500;if(mode==='saved')ok=ok&&saved.has(c.dataset.name);if(mode==='extra')ok=ok&&c.dataset.kind==='extra';c.hidden=!ok;if(ok)n++;});count.textContent='显示 '+n+' / '+cards.length+' 个栏目';empty.hidden=n!==0;}
q.addEventListener('input',filter);document.getElementById('clear').addEventListener('click',function(){q.value='';q.focus();filter();});
document.querySelectorAll('[data-filter]').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});filter();});});
cards.forEach(function(c){var b=c.querySelector('.save');b.setAttribute('aria-pressed',String(saved.has(c.dataset.name)));b.textContent=saved.has(c.dataset.name)?'★ 已收藏':'☆ 收藏';b.addEventListener('click',function(){if(saved.has(c.dataset.name))saved.delete(c.dataset.name);else saved.add(c.dataset.name);b.setAttribute('aria-pressed',String(saved.has(c.dataset.name)));b.textContent=saved.has(c.dataset.name)?'★ 已收藏':'☆ 收藏';try{localStorage.setItem('escortFavs',JSON.stringify(Array.from(saved)));}catch(err){toast('当前浏览器无法保存收藏，页面仍可正常阅读');}filter();});
c.querySelector('.copy').addEventListener('click',function(){var t=c.querySelector('.name').textContent+'\\n'+c.querySelector('.card-preview p').textContent+'\\n'+c.querySelector('.tiers').innerText+'\\n'+c.querySelector('.rule-list').innerText+'\\n整理版非逐字原文；请同时核对商家海报。';if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){toast('规则已复制');},function(){toast('复制受限，请长按文字选择复制');});}else toast('请长按规则文字选择复制');});
c.querySelector('.jump-source').addEventListener('click',function(){var d=c.querySelector('.source-block');d.open=true;d.scrollIntoView({block:'start'});});});
function deepLink(){var id=decodeURIComponent(location.hash.slice(1));var target=document.getElementById(id);if(target&&target.classList.contains('play')){target.open=true;target.hidden=false;target.scrollIntoView({block:'start'});}}
window.addEventListener('hashchange',deepLink);document.documentElement.classList.add('js');filter();if(location.hash)setTimeout(deepLink,50);
})();
'''
    content = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0b1116"><meta name="robots" content="noindex,nofollow"><meta name="description" content="三角洲端游护航参考排行榜，39个栏目、逐档规则与完整商家海报原文。"><title>三角洲护航指南｜排行榜、完整规则与原文</title><style>__CSS__</style></head><body data-version="2026-09-22-r2"><div class="wrap"><div class="mast"><b>DELTA / FIELD GUIDE</b><span>规则阅读版 · v2</span></div><header class="hero"><span class="eyebrow">端游 · 接受跨天 · 参考分析</span><h1>先看懂玩法，<br>再选护航单。</h1><p>排行榜只是参考。每个条目都附有<strong>各价位差异、具体结单规则和商家原文海报</strong>，点开即可逐条核对。</p><div class="stats"><span><b>36</b>参考排名</span><span><b>39</b>规则栏目</span><span><b>__TIERS__</b>档位记录</span><span><b>__IMAGES__</b>商家原图</span></div></header><div class="notice">排名沿用2026-09-18的主观概率判断，未掌握商家订单流水。文字规则为整理版，原文以完整海报为准；不清楚的数字保留“待核”。原图归档于2026-09-22，活动仍展示不代表仍有效。本页不是商家或游戏官方页面。</div><div class="toolbar enhanced-only"><label class="sr-only" for="q">搜索玩法、价格或规则</label><div class="search-row"><input id="q" type="search" placeholder="搜玩法、价格、规则：AW / 无赖子 / 488" autocomplete="off"><button id="clear" type="button">清空</button></div><nav class="filters" aria-label="排行榜筛选"><button data-filter="all" aria-pressed="true">全部栏目</button><button data-filter="top10" aria-pressed="false">Top 10</button><button data-filter="budget" aria-pressed="false">有500元内档</button><button data-filter="saved" aria-pressed="false">我的收藏</button><button data-filter="extra" aria-pressed="false">全店须知／储值</button></nav></div><div class="section-heading"><h2>参考排行榜与玩法规则</h2><span id="count" aria-live="polite">39 个栏目 · 点开阅读</span></div><p class="muted">先选玩法，再看该玩法的不同档位。前36项按旧版参考名次排列，末3项为全店须知与储值说明。</p><main class="grid" id="list">__CARDS__</main><div id="empty" class="empty" hidden>没有符合条件的栏目。清空搜索或切回“全部栏目”。</div><noscript><p class="notice">浏览器未启用脚本：全部排行榜、规则和原图仍可直接展开阅读，仅搜索与收藏不可用。</p></noscript><footer class="footer">版本 2026-09-22-r2 · 内容直接写入页面，不依赖外部数据脚本<br>商家原文归原发布方所有，本页仅用于个人对照阅读。<br><a href="./source-manifest.json">来源栏目索引</a> · <a href="./build-report.json">构建与完整性校验</a></footer></div><div id="toast" class="toast" role="status" hidden></div><script>__JS__</script></body></html>'''
    content = content.replace('__CSS__', css).replace('__CARDS__', '\n'.join(cards)).replace('__TIERS__', str(report['tier_records'])).replace('__IMAGES__', str(len(report['posters']))).replace('__JS__', js)
    assert content.count('class="play"') == 39
    assert content.count('class="source-block"') == 39
    assert './data.js' not in content
    (ROOT / 'index.html').write_text(content, encoding='utf-8')

    # Verify both enhanced mobile view and script-disabled static fallback.
    browser = pw.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    context = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto((ROOT / 'index.html').as_uri())
    assert page.locator('details.play').count() == 39
    assert page.locator('details.play[data-kind=rank]').count() == 36
    assert page.locator('.tier').count() == report['tier_records']
    assert page.locator('html.js').count() == 1
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
    page.screenshot(path='/tmp/escort-verified-mobile.png', full_page=False)
    page.locator('[data-filter=top10]').click()
    assert page.locator('details.play:not([hidden])').count() == 10
    page.locator('[data-filter=all]').click()
    page.locator('#q').fill('千万才是开始')
    assert page.locator('details.play:not([hidden])').count() == 1
    page.locator('#clear').click()
    page.locator('#play-1 > summary').click()
    assert page.locator('#play-1').get_attribute('open') is not None
    page.locator('#play-1 .jump-source').click()
    page.locator('#play-1 .source-block img').wait_for()
    page.wait_for_function('document.querySelector("#play-1 .source-block img").naturalWidth > 0')
    page.locator('#play-1 .source-block').evaluate('(e)=>e.open=false')
    page.locator('#play-1').scroll_into_view_if_needed()
    page.screenshot(path='/tmp/escort-verified-mobile-rules.png', full_page=False)
    page.locator('#play-1 .save').click()
    page.locator('[data-filter=saved]').click()
    assert page.locator('details.play:not([hidden])').count() == 1
    page.locator('[data-filter=all]').click()
    page.locator('#play-1 .save').click()
    page.locator('#play-1').evaluate('(e)=>e.open=false')
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.evaluate('scrollTo(0,0)')
    page.screenshot(path='/tmp/escort-verified-desktop.png')
    assert not errors, 'JavaScript errors: ' + str(errors)
    context.close()
    context = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto((ROOT / 'index.html').as_uri())
    assert page.locator('details.play').count() == 39
    page.locator('#play-1 > summary').click()
    assert page.locator('#play-1 .rule-list').is_visible()
    context.close()
    browser.close()
    report['checks'] = {'javascript_errors': errors, 'mobile_390px': 'passed', 'desktop_1440px': 'passed', 'search': 'passed', 'top10': 'passed', 'favorites': 'passed', 'original_poster_load': 'passed', 'javascript_disabled_fallback': 'passed'}
    (ROOT / 'build-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'posters'}, ensure_ascii=False), flush=True)
