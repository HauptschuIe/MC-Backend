from ast import Raise
import datetime
import re

def transformTotalVisitorsToInt(totalVisitorsStr):
    #Lookup between character and numeric value
    #Mabye we should put the lookup into the DB?
    if totalVisitorsStr is not None:
        tempDict = {"K": 1e3,
            "M": 1e6,
            "G": 1e9}

        try:
            return float(totalVisitorsStr[:-1])*tempDict[totalVisitorsStr[-1]]
        except:
            try:
                #If you can convert it into a float right away, everything is fine
                return float(totalVisitorsStr)
            except:
                #Is ValueError the correct type of exception?
                raise ValueError('Exception during Transformation. Check the input string and lookup table for total visitor number transformation.')
    else:
        return None

def transformAvgVisitDurationToSeconds(avgVisitDurationStr):
    #Example: 00:04:18
    #Check whether it's a legitimate format (e.g. not 70 seconds)
    if avgVisitDurationStr is not None:
        datetime.datetime.strptime(avgVisitDurationStr, "%H:%M:%S")
        (h, m, s) = avgVisitDurationStr.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        return None

def transformShareToFloat(share):
    #Returns: float
    if share is not None:
        share = share.replace("undefined", "")
        share = share.replace(",", ".")
        share = share.replace("%", "")
        share = share.strip()
        share = float(share)
        return share
    else:
        return None

def transformJumpOffRateToFloat(jumpOffRateStr):
    if jumpOffRateStr is not None:
        return float(jumpOffRateStr[:-1])
    else:
        return None

def transformStringToFLoat(string):
    return string.replace(",", ".")

def transformkAToNull(string):
    return string.replace("k. A.", "Null")

def removeStringFirstChar(string):
    return string[1:]

def replacePoint(string):
    return string.replace(".", "")

def transformSplitStringSpace(string):
    return string.split(" ")

def removeStringLastChar(string):
    return string[:-1]

def removeStringTwoChar(string):
    return string[:-2]

def transformPriceToFloat(product_price):
    #Returns: float
    if product_price is not None:
        product_price = product_price.replace("undefined", "")
        product_price = product_price.replace(",", ".")
        product_price = product_price.replace("€", "")
        product_price = product_price.replace("*", "")
        product_price = product_price.replace("–", "")
        product_price = product_price.replace("-", "")
        product_price = product_price.strip()
        product_price = float(product_price)
        return product_price
    else:
        return None

def transformPriceToFloatEuronics(product_price):
    #Returns: float
    if product_price is not None:
        product_price = product_price.replace(".", "")
        product_price = product_price.replace(",", ".")
        product_price = product_price.replace("€", "")
        product_price = product_price.replace("*", "")
        product_price = product_price.replace("\xa0", "")
        product_price = product_price.strip()
        product_price = float(product_price)
        return product_price
    else:
        return None

#Example: Februar 2022; used for similarweb visitors scraper
def transformMonthYearToTimestamp(month_year):

    month_dict = {
        "Januar": "01", "January": "01",
        "Februar": "02", "February": "02",
        "März": "03", "March": "03",
        "April": "04", "April": "04",
        "Mai": "05", "May": "05",
        "Juni": "06", "June": "06",
        "Juli": "07", "July": "07",
        "August": "08", "August": "08",
        "September": "09", "September": "09",
        "Oktober": "10", "October": "10",
        "November": "11", "November": "11",
        "Dezember": "12", "December": "12"
    }

    regex_match = re.search("([^ ]*) ([0-9]{4})", month_year, re.IGNORECASE)

    if month_year is not None:
        if regex_match:
            month_str = regex_match.group(1)
            year = regex_match.group(2)
            numeric_month_str = month_dict[month_str]
            return datetime.datetime.strptime(numeric_month_str + "/" + year, "%m/%Y")
        else:
            raise ValueError("input string is not in the right format.")
    else:
        return None
    
def transformMonth(string):
    if(string=="january"):
        month = 1
    elif (string=="february"):
        month = 2
    elif (string=="march"):
        month = 3
    elif (string=="april"):
        month = 4
    elif (string=="may"):
        month = 5
    elif (string=="june"):
        month = 6
    elif (string=="july"):
        month = 7
    elif (string=="august"):
        month = 8
    elif (string=="september"):
        month = 9
    elif (string=="october"):
        month = 10
    elif (string=="november"):
        month = 11
    elif (string=="december"):
        month = 12
    return month