from philippine_addresses import (
    ph_address_province_municipalities,
    ph_address_municipality,
    province_list,
    municipality_list,
)
import re

# input address should be separated by commas
# street, barangay, municipality, province, country
# suna village, sumpong, malaybalay city, bukidnon, philippines
# suna village, sumpong, makati, bukidnon, philippines


# performs a binary search on province/municipality list
def get_index_of_string(address_list: list[str], initial: str) -> int:

    if len(address_list) < 1:
        return -1

    left = 0
    right = len(address_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if address_list[mid][0] == initial:
            return mid
        elif address_list[mid][0] < initial:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# performs a linear search both ways
def get_provinces_with_initial(targetString: str) -> list[str]:

    initial = targetString[0].upper()
    province_list_subset: list[str] = []

    if len(targetString) < 1 or len(initial) < 1:
        return province_list_subset

    target_string_index = get_index_of_string(province_list, initial)
    province_list_subset.append(province_list[target_string_index])

    search_state = 0
    search_pointer = target_string_index + 1
    while search_state < 2:

        # check if index is at start or end of list
        if search_pointer > (len(province_list) - 1):
            search_state += 1
            search_pointer = target_string_index - 1

        if search_pointer < 0:
            search_state += 1

        province_at_index = province_list[search_pointer]

        # check when value at index is not equal to initial
        if province_at_index[0] != initial and search_state == 0:
            search_state += 1
            search_pointer = target_string_index - 1
        elif province_at_index[0] != initial:
            search_state += 1

        if province_at_index[0] == initial and search_state == 0:
            province_list_subset.append(province_at_index)
            search_pointer += 1
        elif province_at_index[0] == initial and search_state == 1:
            province_list_subset.append(province_at_index)
            search_pointer -= 1

    return sorted(province_list_subset)


def get_municipalities_with_initial(targetString: str) -> list[str]:

    initial = targetString[0].upper()
    municipality_list_subset: list[str] = []

    if len(targetString) < 1 or len(initial) < 1:
        return municipality_list_subset

    target_string_index = get_index_of_string(municipality_list, initial)
    municipality_list_subset.append(municipality_list[target_string_index])

    search_state = 0
    search_pointer = target_string_index + 1
    while search_state < 2:

        # check if index is at start or end of list
        if search_pointer > (len(municipality_list) - 1):
            search_state += 1
            search_pointer = target_string_index - 1

        if search_pointer < 0:
            search_state += 1

        province_at_index = municipality_list[search_pointer]

        # check when value at index is not equal to initial
        if province_at_index[0] != initial and search_state == 0:
            search_state += 1
            search_pointer = target_string_index - 1
        elif province_at_index[0] != initial:
            search_state += 1

        if province_at_index[0] == initial and search_state == 0:
            municipality_list_subset.append(province_at_index)
            search_pointer += 1
        elif province_at_index[0] == initial and search_state == 1:
            municipality_list_subset.append(province_at_index)
            search_pointer -= 1

    return sorted(municipality_list_subset)


def getProvince(addr: str):

    foundProvince = ""
    provinces = list(ph_address_province_municipalities)
    municipalites = list(ph_address_municipality)

    addresses = addr.split(",")

    for address in addresses:
        capAddress = address.upper()
        isCity = re.search("city", capAddress, re.IGNORECASE)
        for province in provinces:
            if re.search(province, capAddress, re.IGNORECASE) and not isCity:
                foundProvince = province + "  address:  " + address
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
