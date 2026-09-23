#!/usr/bin/env python3
"""Apply narrow, idempotent reader corrections before building the static site.
Only Little Giant records are edited. Prices, other games, source posters and
ranking numbers are preserved. The original poster remains the source of truth.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
NAME = '小小巨人'
NOTE = '2026-09-23阅读校正：Part 1初始12滴，上限25滴；Part 2初始30滴，无上限。先前把Part 1误读为1滴，由此产生的“低初始血量容易一把结单”判断作废。本次不修改其他价格、扣血规则或凭两项血量直接重排名次。'


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def replace_record(path, collection, mutate, js=False):
    """Replace just the matching JSON object, leaving all surrounding bytes intact."""
    original = path.read_text(encoding='utf-8')
    payload = original[original.index('['):].strip().removesuffix(';') if js else original
    doc = json.loads(payload)
    items = doc if collection is None else doc[collection]
    matches = [i for i in items if i.get('name') == NAME]
    assert len(matches) == 1, (path.name, 'expected exactly one Little Giant record')
    item = matches[0]
    old_item = json.loads(json.dumps(item, ensure_ascii=False))
    needle = compact(item)
    assert original.count(needle) == 1, (path.name, 'source formatting changed; refusing broad rewrite')
    mutate(item)
    if item == old_item:
        return
    revised = original.replace(needle, compact(item), 1)
    new_payload = revised[revised.index('['):].strip().removesuffix(';') if js else revised
    new_doc = json.loads(new_payload)
    new_items = new_doc if collection is None else new_doc[collection]
    assert [x for x in new_items if x.get('name') != NAME] == [x for x in items if x.get('name') != NAME]
    path.write_text(revised, encoding='utf-8')
    print('Corrected:', path.name)


def rules_update(item):
    tiers = {t[0]: t for t in item['tiers']}
    assert tiers['Part 1'][2] in ('旧读初始1滴，上限25滴', '初始12滴，上限25滴')
    assert tiers['Part 2'][2] in ('初始血量待核，无上限', '初始30滴，无上限')
    tiers['Part 1'][2] = '初始12滴，上限25滴'
    tiers['Part 1'][3] = '有效撤离门槛约700W；初始血量已校正为12滴，扣血表见原图'
    tiers['Part 2'][2] = '初始30滴，无上限'
    tiers['Part 2'][3] = '有效撤离门槛约800W；初始血量已校正为30滴，逐档扣血表见原图'
    item['rules'] = [r.replace('血条清空则结单。完整数字表、首档价格、初始血量在旧提取中不稳定，本版保留原海报供直接查看。',
                              '血条清空则结单。Part 1初始12滴、上限25滴；Part 2初始30滴、无上限。首档价格及部分扣血／回血数字仍待核，请查看完整原海报。')
                     for r in item['rules']]
    if NOTE not in item['warnings']:
        item['warnings'].insert(0, NOTE)


def current_ranking_update(item):
    # Retain its old numeric position, but label this item pending reassessment.
    item['pick'] = '初始血量已更正：12／30滴；原排名位置保留，档位待重评'
    item['tierOrder'] = 'Part 1初始12滴（上限25），Part 2初始30滴（无上限）；不再沿用1滴假设。价格与逐档扣血／回血规则尚未全部核清，暂不据此给出新的档位胜负。'
    item['why'] = '初始血量已经修正为12／30滴，旧的1滴快速结单推断作废。结单仍由成功扣血、失败回血、物品回血及上限共同决定，不能把初始血量增加倍数直接当收益增加倍数。本项原位置只为保留导航，未依据修正后的完整规则重新计算名次。'
    item['confidence'] = '初始血量已校正；性价比待重评'
    item['caveat'] = 'Part 1初始12滴、Part 2初始30滴已按读者纠正更新；不再标作未知。首档价格及部分扣血数字仍待核；高装头甲不自动视为医疗收藏品回血。'


def legacy_update(item):
    item['pick'] = '初始血量已校正；旧档位推荐撤回，待重评'
    item['tierOrder'] = 'Part 1初始12滴，Part 2初始30滴；旧的2999优先顺序未按修正后完整规则重算，不继续作为推荐。'
    reason = 'Part 1初始12滴、Part 2初始30滴，不再沿用1滴易结单的错误假设；需结合各档扣血、回血和上限重新评估，不能只按初始血量倍数估算收益。'
    item['why'] = reason
    item['mechanism'] = reason
    item['caveat'] = '前两档初始血量已纠正；首档价格和部分扣血／回血规则仍以商家原图核对。'


def check_page():
    text = (ROOT / 'index.html').read_text(encoding='utf-8')
    start = text.index('data-name="小小巨人"')
    end = text.find('<details class="play"', start + 1)
    section = text[start:end if end != -1 else len(text)]
    assert '初始12滴，上限25滴' in section
    assert '初始30滴，无上限' in section
    assert '旧读初始1滴' not in section
    assert '初始血量待核，无上限' not in section
    assert '初始数字请直接核图' not in section
    assert '原排名位置保留' in section
    assert '低初始血可能一把结束' not in section
    path = ROOT / 'build-report.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    report.setdefault('checks', {})['little_giant_initial_hp_12_30'] = 'passed'
    report['content_corrections'] = [{'game': NAME, 'date': '2026-09-23', 'part1_initial_hp': 12,
                                      'part2_initial_hp': 30, 'source': 'reader correction',
                                      'ranking_recomputed': False, 'posters_modified': False}]
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Verified: Part 1=12, Part 2=30; stale claims removed; original posters unchanged.')


if __name__ == '__main__':
    if '--check-page' in sys.argv:
        check_page()
    else:
        replace_record(ROOT / 'rules.json', 'sections', rules_update)
        replace_record(ROOT / 'ranking-v3.json', 'ranking', current_ranking_update)
        replace_record(ROOT / 'data.js', None, legacy_update, js=True)
