"""
API Handler for WS2812 LED Effects Control
This module handles API requests from the web interface and controls LED effects
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

# Version information
APP_VERSION = "1.0.0"
BUILD_DATE = "2026-03-08"
FIRMWARE_VERSION = "1.0.0"

# LED Configuration
LED_CONFIG = {
    "pin": 4,  # GPIO4
    "num_leds": 30,
    "color_order": "GRB",
    "brightness": 100,
    "max_brightness": 255
}

# Available effects
AVAILABLE_EFFECTS = [
    "pulse",
    "rainbow",
    "strobe",
    "scan",
    "twinkle",
    "random"
]

# Color mappings
COLOR_MAP = {
    "red": {"r": 255, "g": 0, "b": 0},
    "green": {"r": 0, "g": 255, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 255},
    "white": {"r": 255, "g": 255, "b": 255},
    "purple": {"r": 255, "g": 0, "b": 255},
    "cyan": {"r": 0, "g": 255, "b": 255},
    "yellow": {"r": 255, "g": 255, "b": 0},
    "orange": {"r": 255, "g": 128, "b": 0}
}

# Current state
current_state = {
    "power": True,
    "effect": "pulse",
    "color": "red",
    "brightness": 100,
    "speed": 50,
    "led_count": 30,
    "led_pin": 4
}

logger = logging.getLogger(__name__)


class LEDController:
    """Main controller for WS2812 LED effects"""

    def __init__(self):
        self.state = current_state.copy()
        self.version = APP_VERSION
        self.build_date = BUILD_DATE
        logger.info(f"LED Controller initialized v{self.version}")

    def handle_command(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle API command from web interface

        Args:
            command: Command type (power, effect, color, brightness, speed, config)
            data: Command data

        Returns:
            Response dictionary with status and result
        """
        try:
            if command == "power":
                return self.set_power(data.get("state"))
            elif command == "effect":
                return self.set_effect(data.get("effect"))
            elif command == "color":
                return self.set_color(data.get("color"))
            elif command == "brightness":
                return self.set_brightness(data.get("brightness"))
            elif command == "speed":
                return self.set_speed(data.get("speed"))
            elif command == "config":
                return self.update_config(data)
            elif command == "status":
                return self.get_status()
            elif command == "info":
                return self.get_info()
            else:
                return {"error": f"Unknown command: {command}"}
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            return {"error": str(e)}

    def set_power(self, state: bool) -> Dict[str, Any]:
        """Set LED power state"""
        self.state["power"] = bool(state)
        logger.info(f"Power set to: {self.state['power']}")
        return {"status": "ok", "power": self.state["power"]}

    def set_effect(self, effect: str) -> Dict[str, Any]:
        """Set LED effect"""
        if effect not in AVAILABLE_EFFECTS:
            return {"error": f"Unknown effect: {effect}. Available: {AVAILABLE_EFFECTS}"}

        self.state["effect"] = effect
        logger.info(f"Effect set to: {effect}")
        return {"status": "ok", "effect": effect}

    def set_color(self, color: str) -> Dict[str, Any]:
        """Set LED color"""
        if color not in COLOR_MAP:
            return {"error": f"Unknown color: {color}. Available: {list(COLOR_MAP.keys())}"}

        self.state["color"] = color
        rgb = COLOR_MAP[color]
        logger.info(f"Color set to: {color} (RGB: {rgb['r']},{rgb['g']},{rgb['b']})")
        return {"status": "ok", "color": color, "rgb": rgb}

    def set_brightness(self, brightness: int) -> Dict[str, Any]:
        """Set LED brightness (0-100)"""
        brightness = max(0, min(100, int(brightness)))
        self.state["brightness"] = brightness
        logger.info(f"Brightness set to: {brightness}%")
        return {"status": "ok", "brightness": brightness}

    def set_speed(self, speed: int) -> Dict[str, Any]:
        """Set effect speed (0-100)"""
        speed = max(0, min(100, int(speed)))
        self.state["speed"] = speed
        logger.info(f"Speed set to: {speed}%")
        return {"status": "ok", "speed": speed}

    def update_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update LED configuration"""
        if "ledCount" in config:
            led_count = max(1, min(1000, int(config["ledCount"])))
            self.state["led_count"] = led_count
            LED_CONFIG["num_leds"] = led_count
            logger.info(f"LED count set to: {led_count}")

        if "ledPin" in config:
            led_pin = max(0, min(39, int(config["ledPin"])))
            self.state["led_pin"] = led_pin
            LED_CONFIG["pin"] = led_pin
            logger.info(f"LED pin set to: {led_pin}")

        return {"status": "ok", "config": self.state}

    def get_status(self) -> Dict[str, Any]:
        """Get current LED status"""
        return {
            "status": "ok",
            "power": self.state["power"],
            "effect": self.state["effect"],
            "color": self.state["color"],
            "brightness": self.state["brightness"],
            "speed": self.state["speed"],
            "led_count": self.state["led_count"],
            "led_pin": self.state["led_pin"]
        }

    def get_info(self) -> Dict[str, Any]:
        """Get device information"""
        return {
            "version": self.version,
            "build_date": self.build_date,
            "firmware_version": FIRMWARE_VERSION,
            "available_effects": AVAILABLE_EFFECTS,
            "available_colors": list(COLOR_MAP.keys()),
            "led_config": LED_CONFIG,
            "uptime": self._get_uptime()
        }

    def _get_uptime(self) -> str:
        """Get device uptime (placeholder)"""
        return "running"


# Global controller instance
controller = LEDController()


def handle_api_request(path: str, method: str, body: str = "") -> Dict[str, Any]:
    """
    Main API request handler

    Args:
        path: Request path
        method: HTTP method
        body: Request body (JSON string)

    Returns:
        Response dictionary
    """
    try:
        if method == "POST" and path == "/api/command":
            data = json.loads(body) if body else {}
            command = data.pop("command", None)

            if not command:
                return {"error": "Missing command"}

            return controller.handle_command(command, data)

        elif method == "GET" and path == "/api/status":
            return controller.get_status()

        elif method == "GET" and path == "/api/info":
            return controller.get_info()

        elif method == "GET" and path == "/api/version":
            return {
                "version": controller.version,
                "build_date": controller.build_date,
                "firmware_version": FIRMWARE_VERSION
            }

        else:
            return {"error": "Not found"}

    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}
    except Exception as e:
        logger.error(f"API Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Test the controller
    logging.basicConfig(level=logging.INFO)

    print("Testing LED Controller API Handler")
    print("=" * 50)

    # Test commands
    print(controller.handle_command("status", {}))
    print(controller.handle_command("power", {"state": True}))
    print(controller.handle_command("effect", {"effect": "rainbow"}))
    print(controller.handle_command("color", {"color": "blue"}))
    print(controller.handle_command("brightness", {"brightness": 75}))
    print(controller.handle_command("info", {}))
