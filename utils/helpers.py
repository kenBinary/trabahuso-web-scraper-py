from data.ph_address_municipality import ph_address_municipality
from data.province_list import province_list
from data.municipality_list import municipality_list
from data.job_levels import job_levels
from data.tech_keywords import tech_keywords
import re
import logging

# input address should be separated by commas
# street, barangay, municipality, province, country


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


def get_province(addr: str):

    found_province = ""
    addresses = addr.split(",")

    for address in addresses:

        municipalities = get_municipalities_with_initial(address)
        is_matched = False
        for municipality in municipalities:
            match = re.search(address, municipality, flags=re.IGNORECASE)
            if bool(match):
                found_province = (
                    f"{ph_address_municipality[municipality]}, {municipality}"
                )
                is_matched = True
                break

        if is_matched:
            break

        provinces = get_provinces_with_initial(address)
        for province in provinces:
            match = re.search(address, province, flags=re.IGNORECASE)
            if bool(match):
                found_province = province
                break

    if len(found_province) < 1:
        logging.basicConfig(
            filename="./logs/empty_addresses.log",
            filemode="a",
            format="[%(asctime)s - %(levelname)s]: Location not found during scraping: (%(message)s)",
        )
        logging.warning(addr)

    return found_province


def is_location_remote(job_location: str) -> bool:
    remote_string_patterns = [
        "hybrid work",
        "from home",
        "work from home",
        "hybrid",
        "remote",
    ]
    for remote_string_pattern in remote_string_patterns:
        remote_match = re.search(
            remote_string_pattern, job_location, flags=re.IGNORECASE
        )
        if remote_match:
            return True
    return False


def is_location_unspecified(job_location: str) -> bool:
    country_match = re.search("philippine", job_location, flags=re.IGNORECASE)
    return bool(country_match)


def normalize_scraped_salary(base_salary: int, max_salary: int) -> int:
    return (base_salary + max_salary) / 2


def determine_job_level(string_data: str) -> str:
    for job_level_pattern in job_levels:
        match = re.search(job_level_pattern, string_data, re.IGNORECASE)
        if bool(match):
            return match.group()
    return ""


def normalize_job_level(raw_job_level: str) -> str:

    job_levels: dict = {
        "entry": "entry level",
        "fresh": "fresh graduate",
        "intern": "internship",
        "junior": "junior",
        "jr": "junior",
        "mid": "mid",
        "ojt": "ojt",
        "senior": "senior",
        "sr": "senior",
    }

    for job_level in job_levels:
        if raw_job_level.lower().startswith(job_level):
            return job_levels[job_level]

    logging.basicConfig(
        filename="./logs/invalid_raw_job_level.log",
        filemode="a",
        format="[%(asctime)s - %(levelname)s]: Job level not found during scraping: (%(message)s)",
    )
    logging.warning(raw_job_level)

    return ""


def determine_tech_stack(string_data: str) -> list[str]:

    tech_stack: list[str] = []
    for tech_keyword in tech_keywords:
        special_characters = [
            "#",
            "+",
        ]

        pattern = ""
        if tech_keyword[-1] in special_characters:
            pattern = rf"\b{tech_keyword}\{tech_keyword[-1]}{{1,}}\b,?"
        else:
            pattern = rf"\b{tech_keyword}(?![+#])\b,?"

        match = re.search(pattern, string_data, re.IGNORECASE)
        if bool(match):
            tech_stack.append(tech_keyword)

    return tech_stack
