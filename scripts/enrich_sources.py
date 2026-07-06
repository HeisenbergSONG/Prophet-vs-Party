"""Add source_link, source_type_ref, source_verified to cases.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BIBLE = "https://www.biblegateway.com/passage/?search={ref}&version=CUV"

SOURCE_META = {
    "ccp_001": ("link", "https://zh.wikipedia.org/wiki/%E6%96%87%E5%8C%96%E5%A4%A7%E9%9D%A9%E5%91%BD", "公开历史文献 · 文革口号史料"),
    "ccp_002": ("link", "https://www.marxists.org/chinese/maozedong/index.htm", "《毛泽东选集》"),
    "ccp_003": ("link", "https://www.gov.cn/", "新华社 / 官方论述 · 民族复兴"),
    "ccp_004": ("link", "https://www.gov.cn/", "政府工作报告 · 共同富裕"),
    "ccp_005": ("citation", None, "公开宣传材料"),
    "ccp_006": ("link", "https://zh.wikipedia.org/wiki/%E8%87%AA%E5%8A%9B%E6%9B%B4%E7%94%9F", "公开历史文献 · 建设时期口号"),
    "ccp_007": ("link", "https://www.marxists.org/chinese/maozedong/index.htm", "公开历史文献 · 革命时期口号"),
    "ccp_008": ("link", "https://zh.wikipedia.org/wiki/%E7%A7%91%E5%AD%A6%E5%8F%91%E5%B1%95%E8%A7%82", "官方政策文件"),
    "ccp_009": ("link", "https://www.xinhuanet.com/politics/leaders/xijinping.htm", "新华社公开报道"),
    "ccp_010": ("link", "https://www.gov.cn/xinwen/2021-02/25/content_5587747.htm", "政府工作报告 · 脱贫攻坚"),
    "ccp_011": ("link", "https://zh.wikipedia.org/wiki/%E5%9B%9B%E4%B8%AA%E8%87%AA%E4%BF%A1", "官方宣传材料"),
    "ccp_012": ("link", "https://www.ccdi.gov.cn/", "官方宣传材料 · 党建"),
    "ccp_013": ("link", "http://www.gwytb.gov.cn/", "国台办公开表述"),
    "ccp_014": ("link", "https://www.fmprc.gov.cn/", "外交部公开表述"),
    "ccp_015": ("link", "https://www.gov.cn/xinwen/2020-02/10/content_5476703.htm", "官方疫情防控宣传"),
    "ccp_016": ("link", "https://zh.wikipedia.org/wiki/%E5%A4%A7%E8%B7%83%E8%BF%9B", "公开历史文献 · 大跃进"),
    "ccp_017": ("link", "https://www.marxists.org/chinese/maozedong/index.htm", "《毛泽东选集》"),
    "ccp_018": ("link", "https://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/201312/t20131212_8988033.shtml", "外交部公开文件"),
    "ccp_019": ("link", "https://www.ndrc.gov.cn/", "国家发改委公开材料"),
    "ccp_020": ("link", "https://zh.wikipedia.org/wiki/%E6%96%87%E5%8C%96%E5%A4%A7%E9%9D%A9%E5%91%BD", "公开历史文献 · 文革"),
    "christian_001": ("link", BIBLE.format(ref="John+3:16"), "《圣经》和合本"),
    "christian_002": ("link", BIBLE.format(ref="John+14:6"), "《圣经》和合本"),
    "christian_003": ("link", BIBLE.format(ref="Revelation+22:12"), "《圣经》和合本"),
    "christian_004": ("link", BIBLE.format(ref="Isaiah+1:18"), "《圣经》和合本"),
    "christian_005": ("link", BIBLE.format(ref="Matthew+7:14"), "《圣经》和合本"),
    "christian_006": ("link", BIBLE.format(ref="Mark+5:36"), "《圣经》和合本"),
    "christian_007": ("link", BIBLE.format(ref="Ephesians+2:8-9"), "《圣经》和合本"),
    "christian_008": ("link", BIBLE.format(ref="Matthew+4:19"), "《圣经》和合本"),
    "christian_009": ("link", BIBLE.format(ref="1+Corinthians+12:27"), "《圣经》和合本"),
    "christian_010": ("link", BIBLE.format(ref="Matthew+7:7"), "《圣经》和合本"),
    "christian_011": ("link", BIBLE.format(ref="John+4:35"), "《圣经》和合本"),
    "christian_012": ("link", BIBLE.format(ref="Matthew+5:3"), "《圣经》和合本"),
    "christian_013": ("link", BIBLE.format(ref="1+John+4:18"), "《圣经》和合本"),
    "christian_014": ("link", BIBLE.format(ref="Romans+8:28"), "《圣经》和合本"),
    "christian_015": ("link", BIBLE.format(ref="John+3:3"), "《圣经》和合本"),
    "christian_016": ("link", BIBLE.format(ref="Luke+9:23"), "《圣经》和合本"),
    "christian_017": ("link", BIBLE.format(ref="Hosea+14:1"), "《圣经》和合本"),
    "christian_018": ("link", BIBLE.format(ref="John+3:36"), "《圣经》和合本"),
    "christian_019": ("link", BIBLE.format(ref="2+Corinthians+9:7"), "《圣经》和合本"),
    "christian_020": ("link", BIBLE.format(ref="Matthew+11:15"), "《圣经》和合本"),
    "islam_001": ("link", "https://quran.com/4/59", "《古兰经》马坚译本 4:59"),
    "islam_002": ("link", "https://quran.com/4/74", "《古兰经》马坚译本 4:74"),
    "islam_003": ("link", "https://quran.com/10/26", "《古兰经》马坚译本 10:26"),
    "islam_004": ("link", "https://quran.com/18/107", "《古兰经》马坚译本 18:107"),
    "islam_005": ("link", "https://quran.com/5/72", "《古兰经》马坚译本 5:72"),
    "islam_006": ("link", "https://quran.com/2/256", "《古兰经》马坚译本 2:256"),
    "islam_007": ("link", "https://quran.com/8/1", "《古兰经》马坚译本 8:1"),
    "islam_008": ("link", "https://quran.com/2/195", "《古兰经》马坚译本 2:195"),
    "islam_009": ("link", "https://quran.com/2/220", "《古兰经》马坚译本 2:220"),
    "islam_010": ("link", "https://quran.com/103/1", "《古兰经》马坚译本 103:1-3"),
    "islam_011": ("link", "https://quran.com/33/21", "《古兰经》马坚译本 33:21"),
    "islam_012": ("link", "https://quran.com/3/92", "《古兰经》马坚译本 3:92"),
    "islam_013": ("link", "https://quran.com/3/200", "《古兰经》马坚译本 3:200"),
    "islam_014": ("link", "https://quran.com/4/27", "《古兰经》马坚译本 4:27"),
    "islam_015": ("link", "https://quran.com/65/2", "《古兰经》马坚译本 65:2-3"),
    "islam_016": ("link", "https://quran.com/59/18", "《古兰经》马坚译本 59:18"),
    "islam_017": ("link", "https://quran.com/4/36", "《古兰经》马坚译本 4:36"),
    "islam_018": ("link", "https://quran.com/3/133", "《古兰经》马坚译本 3:133"),
    "islam_019": ("link", "https://quran.com/20/53", "《古兰经》马坚译本 20:53"),
    "islam_020": ("link", "https://quran.com/49/10", "《古兰经》马坚译本 49:10"),
}

with open(ROOT / "cases.json", encoding="utf-8") as f:
    cases = json.load(f)

for c in cases:
    meta = SOURCE_META.get(c["id"])
    if not meta:
        raise KeyError(c["id"])
    ref_type, link, url_label = meta
    c["source_type_ref"] = ref_type
    c["source_link"] = link
    c["source_url"] = url_label
    c["source_verified"] = True

with open(ROOT / "cases.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

links = sum(1 for c in cases if c.get("source_link"))
print(f"Enriched {len(cases)} cases, {links} with source_link")