from decimal import Decimal

def test_search_returns_empty_when_no_matches(client, seed_data):
    resp = client.get("/products/search", params={"title": "Should not exist"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 0

def test_search_no_filters_returns_all(client, seed_data):
    resp = client.get("/products/search", params={"limit": 100, "offset": 0})
    assert resp.status_code == 200

    skus = {p["sku"] for p in resp.json()}
    assert skus == {"SKU-CASE-001", "SKU-PHONE-001", "SKU-TSHIRT-001"}

def test_search_by_title_match(client, seed_data):
    resp = client.get("/products/search", params={"title": "Smart Phone"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-PHONE-001"

def test_search_by_partial_title_case_insensitive(client, seed_data):
    resp = client.get("/products/search", params={"title": "PHONE"})
    assert resp.status_code == 200
    skus = {p["sku"] for p in resp.json()}
    assert skus == {"SKU-PHONE-001", "SKU-CASE-001"}

def test_search_by_sku_exact_match(client, seed_data):
    resp = client.get("/products/search", params={"sku": "SKU-CASE-001"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-CASE-001"

def test_search_by_min_price_inclusive(client, seed_data):
    resp = client.get("/products/search", params={"min_price": 25})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    skus = {p["sku"] for p in data}
    assert skus == {"SKU-PHONE-001", "SKU-TSHIRT-001"}

def test_search_by_max_price_inclusive(client, seed_data):
    resp = client.get("/products/search", params={"max_price": 25})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    skus = {p["sku"] for p in data}
    assert skus == {"SKU-CASE-001", "SKU-TSHIRT-001"}
    prices = {Decimal(p["price"]) for p in data}
    for price in prices:
        assert price <= Decimal("25.00")


def test_search_by_min_and_max_price_inclusive(client, seed_data):
    resp = client.get("/products/search", params={"min_price": 10, "max_price": 25})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    skus = {p["sku"] for p in data}
    assert skus == {"SKU-CASE-001", "SKU-TSHIRT-001"}
    prices = {Decimal(p["price"]) for p in data}
    for price in prices:
        assert price <= Decimal("25.00")
        assert price >= Decimal("10.00")

def test_search_by_category_id(client, seed_data):
    electronics_id = seed_data["categories"]["electronics"].id

    resp = client.get("/products/search", params={"category_id": electronics_id})
    assert resp.status_code == 200

    skus = {p["sku"] for p in resp.json()}
    assert skus == {"SKU-CASE-001", "SKU-PHONE-001"}

def test_search_by_invalid_category_id(client, seed_data):
    invalid_id = 100000000

    resp = client.get("/products/search", params={"category_id": invalid_id})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 0

def test_search_combined_filters(client, seed_data):
    electronics_id = seed_data["categories"]["electronics"].id

    resp = client.get(
        "/products/search",
        params={"title": "phone", "category_id": electronics_id, "min_price": 100},
    )
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-PHONE-001"

def test_search_invalid_price_range_message(client):
    resp = client.get("/products/search", params={"min_price": 100, "max_price": 10})
    assert resp.status_code in (400, 422)
    body = resp.json()
    assert "detail" in body

def test_search_pagination_limit_offset(client, seed_data):
    # ask for 1 item at a time
    r1 = client.get("/products/search", params={"limit": 1, "offset": 0})
    r2 = client.get("/products/search", params={"limit": 1, "offset": 1})

    assert r1.status_code == 200
    assert r2.status_code == 200

    a = r1.json()
    b = r2.json()
    assert len(a) == 1
    assert len(b) == 1

    assert a[0]["sku"] != b[0]["sku"]