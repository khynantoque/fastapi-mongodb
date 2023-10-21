from pytest import fixture
import pdb, requests
import os, sys, json
from assertpy import assert_that

CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import logging as logger, pytest
import lib.common as common
import lib.generate_token as generate_token
from lib.requester import Requester
from lib.mw_sql import execute_query


@pytest.mark.skip(reason="Skipping the entire test suite")
@fixture(scope="module")
def get_admin_token():
    token = generate_token.generate_token(email="adminXYZ@gmail.com", password="Admin123!")
    yield token
    print("\n\n---- Tear Down Test ----\n")

@fixture(scope="module")
def get_staff_token():
    token = generate_token.generate_token(email="staffABC@gmail.com", password="Staff123!")
    yield token
    print("\n\n---- Tear Down Test ----\n")

# --------------------------------
# role: Staff, Admin, Contributor
# page_num:
# page_size:tests/staff_tests/test_staff_login_as_staff.py 
# --------------------------------

@pytest.mark.tc_001
def test_staff_all(get_admin_token):
    req = Requester()
    staff_returned: list = execute_query(
        f"SELECT COUNT(*) FROM mathworld.staff")
    total_staffs: int = staff_returned[0][0]
    header: dict = req.create_basic_headers(token=get_admin_token)
    url = f"{req.base_url}/staff/all"        
    response = requests.request("GET", url, headers=header)
    json_response = json.loads(response.text)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(json_response['total']).is_equal_to(total_staffs)

@pytest.mark.tc_002
def test_staff_all_admin(get_staff_token):
    req = Requester()
    role: str = "Admin" 
    staff_returned: list = execute_query(
        f"SELECT COUNT(*) FROM mathworld.staff")
    total_staffs: int = staff_returned[0][0]
    header: dict = req.create_basic_headers(token=get_staff_token)
    url = f"{req.base_url}/staff/all?{role}"        
    response = requests.request("GET", url, headers=header)
    json_response = json.loads(response.text)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(json_response['total']).is_equal_to(total_staffs)

@pytest.mark.tc_003
def test_staff_all_staff(get_staff_token):
    req = Requester()
    role: str = "Staff"
    staff_returned: list = execute_query(
        f"SELECT COUNT(*) FROM mathworld.staff")
    total_staffs: int = staff_returned[0][0]
    header: dict = req.create_basic_headers(token=get_staff_token)
    url = f"{req.base_url}/staff/all?{role}"        
    response = requests.request("GET", url, headers=header)
    json_response = json.loads(response.text)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(json_response['total']).is_greater_than_or_equal_to(total_staffs)
    