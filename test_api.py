import json
import requests

BASE_URL = "http://127.0.0.1:8000"


def test_root_endpoint():
    print("=== TEST 1: GET / ===")
    res = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {res.status_code}")
    print(f"Response:\n{json.dumps(res.json(), indent=2)}\n")


def test_health_endpoint():
    print("=== TEST 2: GET /health ===")
    res = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {res.status_code}")
    print(f"Response:\n{json.dumps(res.json(), indent=2)}\n")


def test_predict_valid_inputs():
    print("=== TEST 3: POST /predict (Valid Inputs) ===")
    test_cases = [
        "Hello world, welcome to Computational Thinking practice!",
        "FastAPI makes building Web APIs quick and efficient.",
    ]

    for text in test_cases:
        payload = {"message": text}
        res = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Input: {text}")
        print(f"Status Code: {res.status_code}")
        print(f"Output:\n{json.dumps(res.json(), ensure_ascii=False, indent=2)}\n")


def test_predict_invalid_inputs():
    print("=== TEST 4: POST /predict (Validation Error Handling) ===")
    payload = {"message": "   "}  # Empty string/whitespace test
    res = requests.post(f"{BASE_URL}/predict", json=payload)
    print("Input: [Whitespace Only]")
    print(f"Status Code: {res.status_code}")
    print(f"Response Error:\n{json.dumps(res.json(), indent=2)}\n")


if __name__ == "__main__":
    try:
        test_root_endpoint()
        test_health_endpoint()
        test_predict_valid_inputs()
        test_predict_invalid_inputs()
    except requests.exceptions.ConnectionError:
        print("[ERROR]: Could not connect to FastAPI server. Ensure 'uvicorn main:app --reload' is running.")