#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import sys
import math

bench_pattern = re.compile("^test bench_([^ ]+) *\.\.\. bench: +([^ ]+) ns/iter.*$")

mem_benches = {}
safe_benches = {}

def parse_number(with_commas):
    return int(with_commas.replace(",", ""), 10)

def split_bench(bench):
    safe = False
    tail = None
    if bench.startswith("safe_mem_"):
        safe = True
        tail = bench[len("safe_mem_"):]
    else:
        tail = bench[len("mem_"):]
    under = tail.rfind("_")
    name = tail[:under]
    length = tail[under+1:]
    return (safe, name, length)

def read_file(file_name):
    f = open(file_name)
    for line in f:
        match = bench_pattern.match(line)
        if match:
            try:
                (safe, name, length) = split_bench(match.group(1))
                time = parse_number(match.group(2))
                if safe:
                    if not safe_benches.has_key(name):
                        safe_benches[name] = {}
                    safe_benches[name][length] = time
                else:
                    if not mem_benches.has_key(name):
                        mem_benches[name] = {}
                    mem_benches[name][length] = time
            except:
                pass

def colorize(baseline_result, comparison_result):
    (hue, factor) = (0, baseline_result / comparison_result) if baseline_result < comparison_result else (120, comparison_result / baseline_result)
    return "%d, %0.6f%%" % (hue, pow((1.0 - factor), 0.75) * 100)

read_file(sys.argv[1])

out = sys.stdout
out.write("<table>\n")
out.write("<thead>\n")
out.write("<tr><td></td><th colspan=6>Length</th></tr>\n")
out.write("<tr><th>Operation</th><th>1</th><th>3</th><th>15</th><th>16</th><th>30</th><th>1000</th></tr>\n")
out.write("</thead><tbody>\n")
for name in mem_benches.keys():
    out.write("<tr>\n")
    out.write("<th>\n")
    out.write(name)
    out.write("</th>\n")
    for length in ["1", "3", "15", "16", "30", "1000"]:
        baseline_result = float(safe_benches[name][length])
        comparison_result = float(mem_benches[name][length])
        factor = baseline_result / comparison_result
        if math.isnan(factor):
            out.write("<td></td>\n")
        else:
            out.write("<td style='background-color: hsl(%s, 65%%);'>%0.2f</td>\n" % (colorize(baseline_result, comparison_result), factor))
    out.write("</tr>\n")
out.write("</tbody>\n")
out.write("</table>\n")

