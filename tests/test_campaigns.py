def test_get_summary(test_client):
    response = test_client.get("/campaigns/summary?start_date=2023-04-20&end_date=2023-04-30")
    assert response.status_code == 200
    data = response.json()
    
    assert "campaignCard" in data
    assert data["campaignCard"]["campaignName"] == "All"
    assert data["campaignCard"]["range"] == "20 Apr - 30 Apr"
    assert data["campaignCard"]["days"] == 11

    assert "performanceMetrics" in data
    assert "currentMetrics" in data["performanceMetrics"]
    assert data["performanceMetrics"]["currentMetrics"]["impressions"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["clicks"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["views"] > 0

    assert "volumeUnitCostTrend" in data
    assert "impressionsCpm" in data["volumeUnitCostTrend"]
    assert "impression" in data["volumeUnitCostTrend"]["impressionsCpm"]
    assert "cpm" in data["volumeUnitCostTrend"]["impressionsCpm"]

def test_invalid_date_range(test_client):
    response = test_client.get("/campaigns/summary?start_date=2023-04-30&end_date=2023-04-20")
    assert response.status_code == 422

def test_get_summary_with_campaign_id(test_client):
    response = test_client.get("/campaigns/summary?campaign_id=f9bedbbf3c17d&start_date=2023-04-20&end_date=2023-04-30")
    assert response.status_code == 200
    data = response.json()
    
    assert "campaignCard" in data
    assert data["campaignCard"]["campaignName"] == "Crypto Analysis"
    assert data["campaignCard"]["range"] == "20 Apr - 30 Apr"
    assert data["campaignCard"]["days"] == 11

    assert "performanceMetrics" in data
    assert "currentMetrics" in data["performanceMetrics"]
    assert data["performanceMetrics"]["currentMetrics"]["impressions"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["clicks"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["views"] > 0

    assert "volumeUnitCostTrend" in data
    assert "impressionsCpm" in data["volumeUnitCostTrend"]
    assert "impression" in data["volumeUnitCostTrend"]["impressionsCpm"]
    assert "cpm" in data["volumeUnitCostTrend"]["impressionsCpm"]

def test_get_summary_without_date_range(test_client):
    response = test_client.get("/campaigns/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert "campaignCard" in data
    assert data["campaignCard"]["campaignName"] == "All"

    assert "performanceMetrics" in data
    assert "currentMetrics" in data["performanceMetrics"]
    assert data["performanceMetrics"]["currentMetrics"]["impressions"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["clicks"] > 0
    assert data["performanceMetrics"]["currentMetrics"]["views"] > 0

    assert "volumeUnitCostTrend" in data
    assert "impressionsCpm" in data["volumeUnitCostTrend"]
    assert "impression" in data["volumeUnitCostTrend"]["impressionsCpm"]
    assert "cpm" in data["volumeUnitCostTrend"]["impressionsCpm"]
