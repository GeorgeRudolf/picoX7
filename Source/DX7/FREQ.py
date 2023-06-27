#!/usr/bin/env python3
#
# Script used to find suitable PLL SYS configs

def pll(refdiv_6, fbdiv_12, post_div1_3, post_div2_3, clk_min, clk_max):
   """ Compute PLL frequency """

   XTAL    =   12000000
   VCO_MIN =  756000000
   VCO_MAX = 1596000000

   ref_freq = XTAL / refdiv_6
   vco_freq = ref_freq * fbdiv_12

   if vco_freq < VCO_MIN or vco_freq > VCO_MAX:
      return False, None, vco_freq

   pll_freq = vco_freq / (post_div1_3 * post_div2_3)

   if pll_freq < clk_min or pll_freq > clk_max:
      return False, pll_freq, vco_freq

   return True, pll_freq, vco_freq


def enumeratePllClockConfigs(clk_min_mhz, clk_max_mhz):
   """ Find all possible configs for a range of target clocks """

   table = {}

   for refdiv in range(1, 32):
      for fbdiv in range(1, 4096):
         for post_div1 in range(1, 8):
            for post_div2 in range(1, 8):
               ok, pll_freq, vco_freq = pll(refdiv, fbdiv, post_div1, post_div2,
                                            clk_min_mhz * 1000000, clk_max_mhz * 1000000)
               if ok:
                  record = { "refdiv"    : refdiv,
                             "fbdiv"     : fbdiv,
                             "post_div1" : post_div1,
                             "post_div2" : post_div2,
                             "vco_freq"  : vco_freq }
                  if pll_freq not in table:
                     table[pll_freq] = record

                  elif record['vco_freq'] > table[pll_freq]['vco_freq']:
                     table[pll_freq] = record

   return dict(sorted(table.items()))


table = enumeratePllClockConfigs(clk_min_mhz = 132, clk_max_mhz = 200)

# For found PLL clock configs filter for those that are exact mutliples
# of frequencies near to the target sample rate of 49096 Hz

for freq in table:
   record = table[freq]
   for f in range(49000, 49200):
       if int(freq) % f == 0:
          print(f'{f} Hz from clock {freq:.3f} Hz with config {record}')
