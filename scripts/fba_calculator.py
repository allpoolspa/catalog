# run calculate_fees(
#   length,
#   width,
#   height,
#   unit_weight,
#   is_apparel=False,
#   is_media=False,
#   is_pro=True
# )
# Also you can run tests() to perform the examples given on Amazon.
#   *Not all those examples on Amazon are accurate.
#

import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP
from numpy import median


TWO_PLACES = Decimal("0.01")

PICK_PACK = {
    "Standard": Decimal("1.06"),
    "SML_OVER": Decimal("4.09"),
    "MED_OVER": Decimal("5.20"),
    "LRG_OVER": Decimal("8.40"),
    "SPL_OVER": Decimal("10.53"),
}
PACKAGE_WEIGHT = {
    "STND_MEDIA": 0.125,
    "STND_NON_SM": 0.25,
    "STND_NON_LG": 0.25,
    "OVER": 1.00,
    "SPECIAL": 1.00,
}
WEIGHT_HANDLING = {
    "SML_STND_MEDIA": Decimal('0.50'),
    "LRG_STND_MEDIA_1": Decimal('0.85'),
    "LRG_STND_MEDIA_2": Decimal('1.24'),
    "SML_STND_NON": Decimal('0.50'),
    "LRG_STND_NON_1": Decimal('0.96'),
    "LRG_STND_NON_2": Decimal('1.95'),
    "SML_OVER": Decimal('2.06'),
    "MED_OVER": Decimal('2.73'),
    "LRG_OVER": Decimal('63.98'),
    "SPL_OVER": Decimal('124.58'),
}
WEIGHT_HANDLING_MULTIPLIERS = {
    "LRG_STND_MEDIA_2": Decimal('0.41'),
    "LRG_STND_NON_2": Decimal('0.39'),
    "SML_OVER": Decimal('0.39'),
    "MED_OVER": Decimal('0.39'),
    "LRG_OVER": Decimal('0.80'),
    "SPL_OVER": Decimal('0.92'),
}

THRESHOLD = {
    "LRG_STND_MEDIA_2": 2,
    "LRG_STND_NON_2": 2,
    "SML_OVER": 2,
    "MED_OVER": 2,
    "LRG_OVER": 90,
    "SPL_OVER": 90,
}

SML_STND = "SML_STND"
LRG_STND = "LRG_STND"
SPL_OVER = "SPL_OVER"
LRG_OVER = "LRG_OVER"
MED_OVER = "MED_OVER"
SML_OVER = "SML_OVER"

standard = "Standard"
oversize = "Oversize"


def get_30_day(standard_oversize, cubic_foot):
    if standard_oversize == standard:
        return Decimal('0.5525') * normalize(cubic_foot)
    else:
        return Decimal('0.4325') * normalize(cubic_foot)

def get_standard_or_oversize(length, width, height, weight):
    if any(
        [
            (weight > 20),
            (max(length, width, height) > 18),
            (min(length, width, height) > 8),
            (median([length, width, height]) > 14)
        ]
    ):
        return oversize
    return standard

def normalize(data):
    if type(data) != Decimal:
        return Decimal(str(data))
    return data

def get_dimensional_weight(length, width, height):
    dw = Decimal(height * length * width) / Decimal(166.0)
    return Decimal(dw).quantize(TWO_PLACES)

def get_girth_and_length(length, width, height):
    gl = (
        max(length, width, height) +
        (median([length, width, height]) * 2) +
        (min(length, width, height) * 2)
    )
    return Decimal(gl).quantize(Decimal("0.1"))

def get_cost(pick_pack, weight_handling, thirty_day, order_handling, is_apparel, is_pro):
    costs = (
        normalize(pick_pack) +
        normalize(weight_handling) +
        normalize(thirty_day) +
        normalize(order_handling)
    )

    if is_apparel:
        costs += 0.40

    if not is_pro:
        costs += 1.0
    return costs.quantize(TWO_PLACES)

def get_size_tier(standard_oversize, is_media, length,
                  width, height, unit_weight, girth_length):

    if standard_oversize == standard:
        if is_media:
            fee_weight = 14/16.0
        else:
            fee_weight = 12/16.0
        if all(
            [
                (fee_weight >= unit_weight),
                (max(length, width, height) <= 15),
                (min(length, width, height) <= 0.75),
                (median([length, width, height]) <= 12)
            ]
        ):
            size_tier = SML_STND
        else:
            size_tier = LRG_STND
    else:
        if any(
            [
                (girth_length>165),
                (unit_weight > 150),
                (max(length, width, height) > 108),
             ]
        ):
            size_tier = SPL_OVER
        elif girth_length > 130:
            size_tier = LRG_OVER
        elif any(
            [
                (unit_weight > 70),
                (max(length, width, height) > 60),
                (median([length, width, height]) > 30),
            ]
        ):
            size_tier = MED_OVER
        else:
            size_tier = SML_OVER
    return size_tier

def get_outbound_ship_weight(unit_weight, dimensional_weight,
                             standard_oversize, is_media, size_tier):
    """Calculate the outbound shipping weight

    Standard-Size Media
        Packaging weight: 2 (0.125 lb.)
        Rule: unit weight + packaging weight
            *Round up to the nearest whole pound
    Standard-Size Non-Media
        Packaging weight: (1 lb. or less) 4 oz (0.25 lb.)
        Rule: unit weight + packaging weight
            *Round up to the nearest whole pound
    Standard-Size Non-Media (more than 1 lb.)
        Packaging weight: 4 oz (0.25 lb.)
        Rule: max(unit ueight or dimensional weight) + packaging weight
            *Round up to the nearest whole pound
    Small, Medium, and Large Oversize
        Packaging weight: 16 oz (1.00 lb.)
        Rule: max(unit ueight or dimensional weight) + packaging weight
            *Round up to the nearest whole pound
    Special Oversize
        Packaging weight: 16 oz (1.00 lb.)
        Rule: unit weight + packaging weight
            *Round up to the nearest whole pound
    """
    if is_media:
        outbound = Decimal(unit_weight + PACKAGE_WEIGHT['STND_MEDIA'])
    else:
        if standard_oversize == standard:
            if unit_weight <= 1:
                outbound = Decimal(unit_weight + PACKAGE_WEIGHT['STND_NON_SM'])
            else:
                outbound = Decimal(
                    Decimal(max(unit_weight, dimensional_weight)) +
                    Decimal(PACKAGE_WEIGHT['STND_NON_LG'])
                )
        else:
            if size_tier == SPL_OVER:
                outbound = Decimal(unit_weight + PACKAGE_WEIGHT['OVER'])
            else:
                outbound = Decimal(
                    Decimal(max(unit_weight, dimensional_weight)) +
                    Decimal(PACKAGE_WEIGHT['SPECIAL'])
                )
    return outbound.quantize(Decimal('0'), rounding=ROUND_UP)

def get_cubic_foot(length, width, height):
    return Decimal(length * width * height) / Decimal('1728.0')

def get_weight_handling(size_tier, outbound, is_media=False):
    if size_tier == SML_STND:
        return WEIGHT_HANDLING['SML_STND_NON']
    if size_tier == LRG_STND:
        if outbound  <= 1:
            return WEIGHT_HANDLING['LRG_STND_NON_1']
        if is_media:
            if outbound <= 2:
                return WEIGHT_HANDLING['LRG_STND_MEDIA_1']
            else:
                return (
                    WEIGHT_HANDLING['LRG_STND_MEDIA_2'] +
                    (outbound - THRESHOLD['LRG_STND_MEDIA_2']) *
                    WEIGHT_HANDLING_MULTIPLIERS['LRG_STND_MEDIA_2']
                )
        else:
            if outbound <= 2:
                return WEIGHT_HANDLING['LRG_STND_NON_2']
            else:
                return (
                    WEIGHT_HANDLING['LRG_STND_NON_2'] +
                    (outbound - THRESHOLD['LRG_STND_NON_2']) *
                    WEIGHT_HANDLING_MULTIPLIERS['LRG_STND_NON_2']
                )

    if size_tier == SPL_OVER:
        if outbound <= 90:
            return WEIGHT_HANDLING['SPL_OVER']
        else:
            return (
                WEIGHT_HANDLING['SPL_OVER'] +
                (outbound - THRESHOLD['SPL_OVER']) *
                WEIGHT_HANDLING_MULTIPLIERS['SPL_OVER']
            )
    if size_tier == LRG_OVER:
        if outbound <= 90:
            return WEIGHT_HANDLING['LRG_OVER']
        else:
            return (
                WEIGHT_HANDLING['LRG_OVER'] +
                (outbound - THRESHOLD['LRG_OVER']) *
                WEIGHT_HANDLING_MULTIPLIERS['LRG_OVER']
            )

    if size_tier == MED_OVER:
        if outbound <= 2:
            return WEIGHT_HANDLING['MED_OVER']
        else:
            return (
                WEIGHT_HANDLING['MED_OVER'] +
                (outbound - THRESHOLD['MED_OVER']) *
                WEIGHT_HANDLING_MULTIPLIERS['MED_OVER']
            )
    if size_tier == SML_OVER:
        if outbound <= 2:
            return WEIGHT_HANDLING['SML_OVER']
        else:
            return (
                WEIGHT_HANDLING['SML_OVER'] +
                (outbound - THRESHOLD['SML_OVER']) *
                WEIGHT_HANDLING_MULTIPLIERS['SML_OVER']
            )

def calculate_fees(length, width, height, unit_weight,
                   is_apparel=False, is_media=False, is_pro=True):

    dimensional_weight = get_dimensional_weight(
        length, width, height
    )
    girth_length = get_girth_and_length(
        length, width, height
    )
    standard_oversize = get_standard_or_oversize(
        length, width, height, unit_weight
    )
    cubic_foot = get_cubic_foot(length, width, height)

    size_tier = get_size_tier(
        standard_oversize, is_media, length,
        width, height, unit_weight, girth_length
    )
    outbound = get_outbound_ship_weight(
        unit_weight, dimensional_weight,
        standard_oversize, is_media, size_tier
    )

    if is_media or standard_oversize == oversize:
        order_handling = 0
    else:
        order_handling = 1
    pick_pack = PICK_PACK.get(standard_oversize, PICK_PACK.get(size_tier))
    weight_handling = get_weight_handling(size_tier, outbound, is_media).quantize(TWO_PLACES)
    # thirty_day = get_30_day(standard_oversize, cubic_foot)
    # This is not used by the fba_revenue calculator
    thirty_day = 0

    costs = get_cost(
        pick_pack, weight_handling, thirty_day,
        order_handling, is_apparel, is_pro
    )

    return costs


def tests(test=True):
    # The tests.
    print("Testing Small Standard-Size Media")
    l,w,h,wt = [5.6, 4.9, 0.4, 0.3]
    print(float(calculate_fees(l, w, h, wt, is_media=True)) == 1.56)
    print(float(calculate_fees(l, w, h, wt, is_media=True)), '==', 1.56)


    print("Testing Large Standard-Size Media")
    l,w,h,wt = [7.9, 5.1, 1, 0.7]
    print(float(calculate_fees(l, w, h, wt, is_media=True)) == 1.91)
    print(float(calculate_fees(l, w, h, wt, is_media=True)), '==', 1.91)


    print("Testing Small Standard-Size Non-Media")
    l,w,h,wt = [13.8, 9.0, 0.7, 0.7]
    print(float(calculate_fees(l, w, h, wt)) == 2.56)
    print(float(calculate_fees(l, w, h, wt)), '==', 2.56)

    print("Testing Large Standard-Size Non-Media")
    l,w,h,wt = [3.8, 3.7, 1.9, 0.3]
    print(float(calculate_fees(l, w, h, wt)) == 3.02)
    print(float(calculate_fees(l, w, h, wt)), '==', 3.02)

    print("Testing Small Oversize")
    l,w,h,wt = [15.7, 15.0, 0.4, 0.7]
    print(float(calculate_fees(l, w, h, wt)) == 6.15)
    print(float(calculate_fees(l, w, h, wt)), '==', 6.15)

    print("Testing Medium Oversize")
    l,w,h,wt = [63.0, 11.6, 6.3, 46.6]
    print(float(calculate_fees(l, w, h, wt)) == 25.87)
    print(float(calculate_fees(l, w, h, wt)), '==', 25.87)

    print("Testing Large Oversize")
    l,w,h,wt = [50.3, 30.0, 15.0, 146.0]
    print(float(calculate_fees(l, w, h, wt)) == 117.98)
    print(float(calculate_fees(l, w, h, wt)), '==', 117.98)

    print("Testing Special Oversize")
    print("This example is wrong on Amazon. Should be a Large Oversize.")
    l,w,h,wt = [51.6, 35.6, 19.0, 53.5]
    print(float(calculate_fees(l, w, h, wt)) == 135.11)
    print(float(calculate_fees(l, w, h, wt)), '==', 135.11)


