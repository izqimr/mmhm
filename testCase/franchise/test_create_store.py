import os
from datetime import datetime, timedelta

import pytest

from api.franchise_api import FranchiseApi
from common.db import DB
from common.yml import Yml


class TestCreateStore:
    def test_create_store(self):
        franchise = FranchiseApi()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        yaml_path = os.path.join(base_dir, "data", "franchise", "create_store.yml")
        flow_data = Yml().read_yaml(yaml_path)

        extra_context = {
            "user_id": "1761927782112000871",
            "province_code": "440000",
            "city_code": "440400",
            "province_name": "广东省",
            "city_name": "珠海市",
            "plan_find_shop_date": "TWO_MONTHS",
        }

        first_part = franchise.run_flow(flow_data, extra_context=extra_context, start_index=0, end_index=1)

        assert first_part["results"], "First step was not executed."
        for item in first_part["results"]:
            response_json = item["response"]
            assert response_json.get("success") is True, f"Step failed: {item['step']}, resp={response_json}"

        # context = first_part["context"]
        # intention_no = context.get("intention_no")

        intention_no = "YX2026030600200008288"
        # if not intention_no:
        #     pytest.skip("intention_apply succeeded but no intention_no returned; skip SQL and remaining steps.")

        try:
            db = DB("franchise")
            db.execute(
                "UPDATE t_franchise_intention "
                "SET `status`=%s, `sub_status`=%s "
                "WHERE `intention_no`=%s",
                ("PENDING_INTENTION_AGREEMENT", "PENDING_INTENTION_AGREEMENT", intention_no),
            )
            db.execute(
                "INSERT INTO `store_franchise`.`t_intention_agreement_audit` "
                "(`intention_no`, `audit_status`, `franchisees_id`, `create_id`, `create_name`, `create_time`, `update_id`, `update_name`, `update_time`) "
                "VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, NOW())",
                (intention_no, "PENDING_INTENTION_AGREEMENT", 0, "499999999", "root", "499999999", "root"),
            )
            db.execute(
                "UPDATE `t_intention_gold_audit` "
                "SET `audit_status`=%s "
                "WHERE `intention_no`=%s",
                ("AUDIT_PASS", intention_no),
            )
            db.execute(
                "DELETE FROM `t_franchise_payment_bill` "
                "WHERE `biz_no`=%s",
                (intention_no,),
            )
        except Exception as exc:
            pytest.skip(f"DB not reachable or SQL failed in current env: {exc}")

        second_part = franchise.run_flow(flow_data, extra_context=context, start_index=1)
        assert second_part["results"], "Remaining steps were not executed."
        for item in second_part["results"]:
            response_json = item["response"]
            assert response_json.get("success") is True, f"Step failed: {item['step']}, resp={response_json}"
