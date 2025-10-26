#!/usr/bin/env python3
"""
Test Docker connection
"""
import docker
import requests

print("Testing Docker connection...")
print()

# Check what's available
print("Checking installed packages:")
print(f"  docker version: {docker.__version__}")
print(f"  requests version: {requests.__version__}")
print()

try:
    # Test 1: Using APIClient directly
    print("Test 1: Using APIClient directly")
    from docker import APIClient
    client = APIClient(base_url='unix:///var/run/docker.sock')
    version = client.version()
    print(f"✅ Success! Docker version: {version['Version']}")
    print(f"   API version: {version['ApiVersion']}")
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()

print()

try:
    # Test 2: Using DockerClient
    print("Test 2: Using DockerClient")
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    version = client.version()
    print(f"✅ Success! Docker version: {version['Version']}")
    client.close()
except Exception as e:
    print(f"❌ Failed: {e}")

print()
print("Testing complete!")
