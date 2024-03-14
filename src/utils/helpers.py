from philippine_addresses import ph_address_province_municipalities,ph_address_municipality
import re

# input address should be separated by commas
# street, barangay, municipality, province, country
# suna village, sumpong, malaybalay city, bukidnon, philippines
# suna village, sumpong, makati, bukidnon, philippines
def getProvince(addr:str):

    foundProvince = "";
    provinces = list(ph_address_province_municipalities)
    municipalites = list(ph_address_municipality)

    addresses = addr.split(",")

    for address in addresses:
        capAddress = address.upper()
        isCity = re.search("city", capAddress, re.IGNORECASE) 
        for province in provinces:
            if(re.search(province,capAddress,re.IGNORECASE) and not isCity):
                foundProvince = province + "  address:  "+ address;
                break
        # for municipality in municipalites:
        #     if(re.search(municipalites,capAddress,re.IGNORECASE)):
        #         foundProvince = municipality;
        #         break

        # isCity = re.search("city", address, re.IGNORECASE)
        # if(capAddress in provinces):
        #     foundProvince = "PROVINCELIST: " +  provinces.pop(provinces.index(capAddress)) 
        #     break
        # if(capAddress in municipalites):
        #     foundProvince = "MUNICIPALITY LIST: " + ph_address_municipality[capAddress] 
        #     break
    return foundProvince

    
    
