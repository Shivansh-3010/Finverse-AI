from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(app, raise_server_exceptions=False)


def test_xirr_endpoint_returns_422_for_incomplete_valuation():
    portfolio_id = uuid4()

    with patch(
        "api.v1.portfolios.router.portfolio_xirr_service.calculate",
        side_effect=ValueError(
            "Portfolio valuation is incomplete; missing market prices for: RELIANCE"
        ),
    ):
        response = client.get(
            f"/api/v1/portfolios/{portfolio_id}/xirr"
        )

    assert response.status_code == 422
    assert "Portfolio valuation is incomplete" in response.json()["detail"]


def test_xirr_endpoint_returns_200_for_successful_calculation():
    portfolio_id = uuid4()
    expected_result = {
        "portfolio_id": str(portfolio_id),
        "cash_flow_count": 2,
        "total_deposited": "1000.00",
        "total_withdrawn": "0.00",
        "terminal_value": "1100.00",
        "xirr": "0.1000",
        "xirr_pct": "10.00",
        "cash_flows": [],
    }

    with patch(
        "api.v1.portfolios.router.portfolio_xirr_service.calculate",
        return_value=expected_result,
    ):
        response = client.get(
            f"/api/v1/portfolios/{portfolio_id}/xirr"
        )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Portfolio XIRR calculated"
    assert response.json()["data"]["xirr_pct"] == "10.00"