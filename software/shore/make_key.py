"""Make the boat's command-signing key: 32 random bytes, printed as 64 hex digits.
Run it once on your own computer. Put the result in the shore server's config.json (boat_key_hex) or the
DRONE_BOAT_KEY_HEX environment variable, and flash the same value into the companion (software/boat/comms/README.md).
Never commit it. Anyone with the key can steer the boat."""
import secrets
print(secrets.token_hex(32))
