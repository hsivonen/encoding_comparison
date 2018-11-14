#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import sys
import math

bench_pattern = re.compile("^test bench_([^ ]+) *\.\.\. bench: +([^ ]+) ns/iter.*$")

encodings = [
    "ar",
    "cs",
    "de",
    "el",
    "en",
    "jquery",
    "fr",
    "he",
    "pt",
    "ru",
    "th",
    "tr",
    "vi",
    "zh_cn",
    "zh_tw",
    "ja",
    "ko",
    "ar_windows_1256",
    "cs_windows_1250",
    "de_windows_1252",
    "el_windows_1253",
    "en_windows_1252",
    "fr_windows_1252",
    "he_windows_1255",
    "pt_windows_1252",
    "ru_windows_1251",
    "th_windows_874",
    "tr_windows_1254",
    "vi_windows_1258",
    "zh_cn_gb18030",
    "zh_tw_big5",
    "ja_euc_jp",
    "ja_iso_2022_jp",
    "ja_shift_jis",
    "ko_euc_kr",
    "user_defined",
    "ar_utf_16le",
    "cs_utf_16le",
    "de_utf_16le",
    "el_utf_16le",
    "en_utf_16le",
    "fr_utf_16le",
    "he_utf_16le",
    "pt_utf_16le",
    "ru_utf_16le",
    "th_utf_16le",
    "tr_utf_16le",
    "vi_utf_16le",
    "zh_cn_utf_16le",
    "zh_tw_utf_16le",
    "ja_utf_16le",
    "ko_utf_16le",
    "ar_utf_16be",
    "cs_utf_16be",
    "de_utf_16be",
    "el_utf_16be",
    "en_utf_16be",
    "fr_utf_16be",
    "he_utf_16be",
    "pt_utf_16be",
    "ru_utf_16be",
    "th_utf_16be",
    "tr_utf_16be",
    "vi_utf_16be",
    "zh_cn_utf_16be",
    "zh_tw_utf_16be",
    "ja_utf_16be",
    "ko_utf_16be",
]

language_names = {
    "ar": "Arabic",
    "cs": "Czech",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "jquery": "JavaScript",
    "fr": "French",
    "he": "Hebrew",
    "pt": "Portuguese",
    "ru": "Russian",
    "th": "Thai",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "zh_cn": "Simplified Chinese",
    "zh_tw": "Traditional Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}

encoding_names = {
    "_windows_1250": "windows-1250",
    "_windows_1251": "windows-1251",
    "_windows_1252": "windows-1252",
    "_windows_1253": "windows-1253",
    "_windows_1254": "windows-1254",
    "_windows_1255": "windows-1255",
    "_windows_1256": "windows-1256",
    "_windows_1258": "windows-1258",
    "_windows_874": "windows-874",
    "_gb18030": "gb18030",
    "_big5": "Big5",
    "_iso_2022_jp": "ISO-2022-JP",
    "_euc_jp": "EUC-JP",
    "_shift_jis": "Shift_JIS",
    "_euc_kr": "EUC-KR",
    "_utf_16be": "UTF-16BE",
    "_utf_16le": "UTF-16LE",
}

categories = [
    "uconv_to_utf16_",
    "icu_to_utf16_",
    "windows_to_utf16_",
    "webkit_to_utf16_",
    "kewb_to_utf16_",
    "std_validation_",
    "rust_to_string_",
    "iconv_to_utf8_",
    "uconv_from_utf16_",
    "icu_from_utf16_",
    "windows_from_utf16_",
    "webkit_from_utf16_",
    "rust_to_vec_",
    "iconv_from_utf8_",
]

category_names = {
    "uconv_to_utf16_": "uconv",
    "icu_to_utf16_": "ICU",
    "windows_to_utf16_": "kernel32",
    "webkit_to_utf16_": "WebKit",
    "kewb_to_utf16_": "kewb",
    "std_validation_": "stdlib",
    "rust_to_string_": "rust-encoding",
    "iconv_to_utf8_": "glibc",
    "uconv_from_utf16_": "uconv",
    "icu_from_utf16_": "ICU",
    "windows_from_utf16_": "kernel32",
    "webkit_from_utf16_": "WebKit",
    "rust_to_vec_": "rust-encoding",
    "iconv_from_utf8_":"glibc",
}

baseline_results = {
#    "decode_to_string_": {},
#    "decode_to_utf16_": {},
#    "decode_to_utf8_": {},
#    "encode_from_utf16_": {},
#    "encode_from_utf8_": {},
#    "encode_to_vec_": {},
    "icu_from_utf16_": {},
    "icu_to_utf16_": {},
    "iconv_from_utf8_": {},
    "iconv_to_utf8_": {},
    "rust_to_string_": {},
    "rust_to_vec_": {},
    "std_validation_": {},
    "uconv_from_utf16_": {},
    "uconv_to_utf16_": {},
    "windows_from_utf16_": {},
    "windows_to_utf16_": {},
    "webkit_from_utf16_": {},
    "webkit_to_utf16_": {},
    "kewb_to_utf16_": {},
}

comparison_results = {
    "decode_to_string_": {},
    "decode_to_utf16_": {},
    "decode_to_utf8_": {},
    "encode_from_utf16_": {},
    "encode_from_utf8_": {},
    "encode_to_vec_": {},
}

pairings = {
    "decode_to_string_": "decode_to_string_",
    "decode_to_utf16_": "decode_to_utf16_",
    "decode_to_utf8_": "decode_to_utf8_",
    "encode_from_utf16_": "encode_from_utf16_",
    "encode_from_utf8_": "encode_from_utf8_",
    "encode_to_vec_": "encode_to_vec_",
    "iconv_from_utf8_": "encode_from_utf8_",
    "iconv_to_utf8_": "decode_to_utf8_",
    "icu_from_utf16_": "encode_from_utf16_",
    "icu_to_utf16_": "decode_to_utf16_",
    "rust_to_string_": "decode_to_string_",
    "rust_to_vec_": "encode_to_vec_",
    "std_validation_": "decode_to_string_",
    "uconv_from_utf16_": "encode_from_utf16_",
    "uconv_to_utf16_": "decode_to_utf16_",
    "windows_from_utf16_": "encode_from_utf16_",
    "windows_to_utf16_": "decode_to_utf16_",
    "webkit_from_utf16_": "encode_from_utf16_",
    "webkit_to_utf16_": "decode_to_utf16_",
    "kewb_to_utf16_": "decode_to_utf16_",
}

def parse_number(with_commas):
    return int(with_commas.replace(",", ""), 10)

def split_bench(name, benches):
    for bench in benches:
        if name.startswith(bench):
            return (name[:len(bench)], name[len(bench):])
    raise Error

def read_file(file_name, results):
    benches = results.keys()
    f = open(file_name)
    for line in f:
        match = bench_pattern.match(line)
        if match:
            try:
                (category, lang_encoding) = split_bench(match.group(1), benches)
                time = parse_number(match.group(2))
                results[category][lang_encoding] = time
            except:
                pass

def read_float(results, category, lang_encoding):
     if not results[category].has_key(lang_encoding):
         return float("nan")
     return float(results[category][lang_encoding])

def format_encoding(lang_encoding):
    if "user_defined" == lang_encoding:
        return "x-user-defined"
    if language_names.has_key(lang_encoding):
        return language_names[lang_encoding] + ", UTF-8"
    for lang in language_names.keys():
        if lang_encoding.startswith(lang):
            return "%s, %s" % (language_names[lang], encoding_names[lang_encoding[len(lang):]])

def colorize(baseline_result, comparison_result):
    (hue, factor) = (0, baseline_result / comparison_result) if baseline_result < comparison_result else (120, comparison_result / baseline_result)
    return "%d, %0.6f%%" % (hue, pow((1.0 - factor), 0.75) * 100)

read_file(sys.argv[1], baseline_results)
read_file(sys.argv[2], comparison_results)

out = sys.stdout
out.write("<table>\n")
out.write("<thead>\n")
out.write("<tr><td rowspan=3></td><th colspan=8>Decode</th><th colspan=6>Encode</th></tr>\n")
out.write("<tr><th colspan=5>UTF-16</th><th colspan=3>UTF-8</th><th colspan=4>UTF-16</th><th colspan=2>UTF-8</th></tr>\n")
out.write("<tr>\n")
for category in categories:
    out.write("<th>\n")
    out.write(category_names[category])
    out.write("</th>\n")
out.write("</tr>\n")
out.write("</thead><tbody>\n")
for lang_encoding in encodings:
    out.write("<tr>\n")
    out.write("<th>\n")
    out.write(format_encoding(lang_encoding))
    out.write("</th>\n")
    for category in categories:
        paired = pairings[category]
        baseline_result = read_float(baseline_results, category, lang_encoding)
        comparison_result = read_float(comparison_results, paired, lang_encoding)
        factor = baseline_result / comparison_result
        if math.isnan(factor):
            out.write("<td></td>\n")
        else:
            out.write("<td style='background-color: hsl(%s, 65%%);'>%0.2f</td>\n" % (colorize(baseline_result, comparison_result), factor))
    out.write("</tr>\n")
out.write("</tbody>\n")
out.write("</table>\n")

