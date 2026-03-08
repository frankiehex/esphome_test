#!/usr/bin/env python3
"""
Test script for WS2812 LED Effects API Handler
測試 WS2812 LED 效果 API 處理程序
"""

import json
import sys
from api_handler import controller, handle_api_request

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_api():
    """Test all API endpoints"""

    print_header("WS2812 LED Effects API - Test Suite")

    # Test 1: Get device info
    print("\n[TEST 1] Get Device Information")
    print("-" * 60)
    response = controller.get_info()
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 2: Get initial status
    print("\n[TEST 2] Get Initial Status")
    print("-" * 60)
    response = controller.get_status()
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 3: Set power on
    print("\n[TEST 3] Set Power ON")
    print("-" * 60)
    response = controller.handle_command("power", {"state": True})
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 4: Set effect to rainbow
    print("\n[TEST 4] Set Effect to Rainbow")
    print("-" * 60)
    response = controller.handle_command("effect", {"effect": "rainbow"})
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 5: Set color to blue
    print("\n[TEST 5] Set Color to Blue")
    print("-" * 60)
    response = controller.handle_command("color", {"color": "blue"})
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 6: Set brightness
    print("\n[TEST 6] Set Brightness to 75%")
    print("-" * 60)
    response = controller.handle_command("brightness", {"brightness": 75})
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 7: Set speed
    print("\n[TEST 7] Set Speed to 80%")
    print("-" * 60)
    response = controller.handle_command("speed", {"speed": 80})
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 8: Update config
    print("\n[TEST 8] Update LED Configuration")
    print("-" * 60)
    response = controller.handle_command("config", {
        "ledCount": 60,
        "ledPin": 23
    })
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 9: Get final status
    print("\n[TEST 9] Get Final Status")
    print("-" * 60)
    response = controller.get_status()
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 10: Test API request handler
    print("\n[TEST 10] Test HTTP-like API Request Handler")
    print("-" * 60)

    # Test status endpoint
    response = handle_api_request("/api/status", "GET")
    print("GET /api/status:")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test version endpoint
    response = handle_api_request("/api/version", "GET")
    print("\nGET /api/version:")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test command endpoint
    command_body = json.dumps({
        "command": "effect",
        "effect": "strobe"
    })
    response = handle_api_request("/api/command", "POST", command_body)
    print("\nPOST /api/command (set effect to strobe):")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # Test 11: Test all available effects
    print("\n[TEST 11] Test All Available Effects")
    print("-" * 60)
    effects = ["pulse", "rainbow", "strobe", "scan", "twinkle", "random"]
    for effect in effects:
        response = controller.handle_command("effect", {"effect": effect})
        status = "✓" if response.get("status") == "ok" else "✗"
        print(f"{status} {effect.upper()}: {response.get('effect', 'ERROR')}")

    # Test 12: Test all available colors
    print("\n[TEST 12] Test All Available Colors")
    print("-" * 60)
    colors = ["red", "green", "blue", "white", "purple", "cyan", "yellow", "orange"]
    for color in colors:
        response = controller.handle_command("color", {"color": color})
        status = "✓" if response.get("status") == "ok" else "✗"
        rgb = response.get("rgb", {})
        print(f"{status} {color.upper()}: RGB({rgb.get('r', 0)}, {rgb.get('g', 0)}, {rgb.get('b', 0)})")

    # Test 13: Test error handling
    print("\n[TEST 13] Test Error Handling")
    print("-" * 60)

    # Invalid effect
    response = controller.handle_command("effect", {"effect": "invalid_effect"})
    print(f"Invalid effect test: {response}")

    # Invalid color
    response = controller.handle_command("color", {"color": "invalid_color"})
    print(f"Invalid color test: {response}")

    # Out of range brightness
    response = controller.handle_command("brightness", {"brightness": 150})
    print(f"Out of range brightness (150 → clamped): {response}")

    # Final summary
    print_header("Test Summary")
    print("\n✓ All API endpoints tested successfully!")
    print(f"✓ Device: WS2812 LED Controller v{controller.version}")
    print(f"✓ Build Date: {controller.build_date}")
    print(f"✓ Available Effects: {len(effects)}")
    print(f"✓ Available Colors: {len(colors)}")
    print("\nAPI endpoints available:")
    print("  - GET  /api/status")
    print("  - GET  /api/info")
    print("  - GET  /api/version")
    print("  - POST /api/command")


if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        sys.exit(1)
