#!/usr/bin/env python

def calc_compound_interest(monthly_amt: int, num_years: int,
                           interest: float, start_amt: int=0):
    total = start_amt

    for cur_year in range(1, num_years + 1):
        print(f"Year {cur_year}:")
        for cur_month in range(1, 13):
            total += monthly_amt
            total += total * interest / 100 / 12
            print(f"- Month %2d: %7d - %7d" % (cur_month, int(total),
                                               start_amt + \
                                               monthly_amt * (cur_year -1) * 12 + \
                                               monthly_amt * cur_month))


if __name__ == "__main__":
    calc_compound_interest(800, 30, 10)
