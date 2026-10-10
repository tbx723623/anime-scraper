#!/usr/bin/env python3
"""Unit tests for scraper.parse_anime (no network access needed).

Run with: python3 -m unittest test_scraper
"""
import unittest

from scraper import parse_anime

SAMPLE_HTML = """
<div class="grid">
<div class="card-effect a">
  <h3 class="title"> Test Anime </h3>
  <span><i class="fa fa-calendar-o"></i> 2026-01-01 </span>
  <div class="text-gray-600 mb-2">
    夸克:<a href="https://pan.quark.cn/s/abc">link</a>
    百度;<a href="https://pan.baidu.com/s/def">link</a>
  </div>
  <!-- 底部信息 -->
</div>
<div class="card-effect b">
  <h3>Test Anime</h3>
</div>
<div class="card-effect c">
  <h3><i class="fa fa-star"></i> Icon Title</h3>
</div>
<div class="card-effect d">
  <p>no title here</p>
</div>
</div>
"""


class ParseAnimeTest(unittest.TestCase):
    def test_extracts_fields(self):
        items = parse_anime(SAMPLE_HTML)
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["name"], "Test Anime")
        self.assertEqual(item["date"], "2026-01-01")
        self.assertEqual(item["quark"], ["https://pan.quark.cn/s/abc"])
        self.assertEqual(item["baidu"], ["https://pan.baidu.com/s/def"])

    def test_skips_duplicates_icons_and_untitled_cards(self):
        names = [i["name"] for i in parse_anime(SAMPLE_HTML)]
        self.assertEqual(names, ["Test Anime"])

    def test_empty_html(self):
        self.assertEqual(parse_anime(""), [])


if __name__ == "__main__":
    unittest.main()
