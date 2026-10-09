import os
import sys
import time
import socket
import shutil
import platform
import urllib.request
import urllib.error

# Import variables from your unified configuration module
from app.config import COLLECTION_NAME, VECTOR_DB_URL

def get_static_environment_profile():
    # Returns the system infrastructure and hardware topology matrix by pulling safely from sanitized environment variables.
    return {
        "compute_topology": {
            "node_a_core_server": {
                "hardware": os.getenv("SERVER_HARDWARE_NAME", "[Server Hardware Omitted]"),
                "processor": os.getenv("SERVER_CPU_SPEC", "[Server CPU Omitted]"),
                "memory_array": os.getenv("SERVER_RAM_SPEC", "[Server RAM Omitted]"),
                "storage_pool": os.getenv("SERVER_STORAGE_SPEC", "[Server Storage Omitted]"),
                "swap_configuration": os.getenv("SERVER_SWAP_SPEC", "[Server Swap Omitted]"),
                "chassis_state": os.getenv("SERVER_CHASSIS_STATE", "[Server Chassis State Omitted]")
            },
            "node_b_client_workstation": {
                "hardware": os.getenv("CLIENT_HARDWARE_NAME", "[Client Hardware Omitted]"),
                "device_nickname": os.getenv("CLIENT_NICKNAME", "[Client Nickname Omitted]"),
                "processor": os.getenv("CLIENT_CPU_SPEC", "[Client CPU Omitted]"),
                "memory_array": os.getenv("CLIENT_RAM_SPEC", "[Client RAM Omitted]"),
                "storage_pool": os.getenv("CLIENT_STORAGE_SPEC", "[Client Storage Omitted]")
            },
            "node_c_peripheral_utility": {
                "hardware": os.getenv("PERIPHERAL_HARDWARE_NAME", "[Peripheral Omitted]"),
                "state": os.getenv("PERIPHERAL_STATE", "[Peripheral State Omitted]")
            },
            "node_d_mobile_testing": {
                "hardware": os.getenv("PHONE_HARDWARE_NAME", "[Phone Omitted]"),
                "state": os.getenv("PHONE_STATE", "[Phone State Omitted]")
            }
        },
        "virtualization_layer": {
            "hypervisor_host": os.getenv("HYPERVISOR_HOST_SPEC", "[Hypervisor Omitted]"),
            "guest_vm": {
                "hostname": os.getenv("VM_HOSTNAME_MASK", "[VM Hostname Omitted]"),
                "guest_os": os.getenv("VM_OS_SPEC", "[VM OS Omitted]"),
                "provisioned_compute": os.getenv("VM_COMPUTE_ALLOCATION", "[VM Compute Omitted]"),
                "system_rules": os.getenv("VM_SYSTEM_RULES", "[VM Rules Omitted]")
            },
            "containerization": {
                "runtime": "Docker / Podman Engine",
                "base_image": "Python 3.11-slim Linux core",
                "active_containers": ["rag-core (Orchestration)", "qdrant_db (Vector Node)"]
            }
        },
        "network_architecture": {
            "subnet_matrix": {
                "server_static_ip": os.getenv("SERVER_STATIC_IP_MASK", "[Server IP Omitted]"),
                "client_bridge_ip": os.getenv("CLIENT_BRIDGE_IP_MASK", "[Client IP Omitted]"),
                "thunderbolt_bridge_nic1": os.getenv("THUNDERBOLT_NIC_SPEC", "[Thunderbolt Bridge Omitted]"),
                "trusted_isolation_boundary": os.getenv("NETWORK_ISOLATION_SPEC", "[Isolation Boundary Omitted]")
            },
            "overlay_mesh": os.getenv("OVERLAY_MESH_SPEC", "[Mesh Network Omitted]")
        },
        "database_geometry": {
            "instance": "Qdrant Vector Database Cluster",
            "collection_target": COLLECTION_NAME,
            "vector_dimension_bounds": "1536-dimensional float coordinates",
            "distance_metric_logic": "Cosine Distance metric optimization",
            "embedding_source_model": "openai/text-embedding-3-small"
        }
    }

class DiagnosticEngine:
    def __init__(self):
        self.target_api = "openrouter.ai"
        
        # Parse the Qdrant connection endpoint strings from your config file URL, e.g., converts 'http://qdrant_db:6333' into pure host/port primitives
        try:
            url_clean = VECTOR_DB_URL.replace("http://", "").replace("https://", "")
            if ":" in url_clean:
                self.target_db_host, port_str = url_clean.split(":", 1)
                self.target_db_port = int(port_str)
            else:
                self.target_db_host = url_clean
                self.target_db_port = 6333
        except Exception:
            self.target_db_host = "qdrant_db"
            self.target_db_port = 6333

    def execute_self_diagnosis(self):
        # Orchestrates live latency checks and merges them directly with the dynamic profile.
        start_total = time.time()
        
        network_telemetry = self.test_networking()
        static_profile = get_static_environment_profile()
        
        total_runtime = time.time() - start_total
        
        return {
            "diagnostic_metadata": {
                "timestamp_epoch": int(time.time()),
                "total_diagnostic_execution_seconds": round(total_runtime, 4)
            },
            "live_network_latency": network_telemetry,
            "static_environment_matrix": static_profile
        }

    def test_networking(self):
        # Inspects internal DNS resolution, container routing, and upstream handshakes.
        net_stats = {}
        
        # 1. DNS Resolution Trace
        start_dns = time.time()
        try:
            socket.gethostbyname(self.target_api)
            net_stats["dns_resolution_seconds"] = round(time.time() - start_dns, 4)
            net_stats["dns_status"] = "healthy"
        except Exception:
            net_stats["dns_resolution_seconds"] = round(time.time() - start_dns, 4)
            net_stats["dns_status"] = "failed"

        # 2. Inter-Container Database Connectivity Check
        start_db_ping = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)  # Cut off infinite connection delays early
            s.connect((self.target_db_host, self.target_db_port))
            s.close()
            net_stats["db_connection_latency_seconds"] = round(time.time() - start_db_ping, 4)
            net_stats["db_routing_status"] = "connected"
        except Exception as e:
            net_stats["db_connection_latency_seconds"] = round(time.time() - start_db_ping, 4)
            net_stats["db_routing_status"] = "failed"

        # 3. Upstream Gateway Handshake Trace
        url = "https://openrouter.ai"
        start_api = time.time()
        try:
            req = urllib.request.Request(url, data=b"{}", method="POST")
            with urllib.request.urlopen(req, timeout=5) as _:
                pass
        except urllib.error.HTTPError as e:
            net_stats["api_handshake_seconds"] = round(time.time() - start_api, 4)
            net_stats["api_gateway_status"] = f"reachable (Server responded with HTTP {e.code})"
        except Exception as e:
            net_stats["api_handshake_seconds"] = round(time.time() - start_api, 4)
            net_stats["api_gateway_status"] = "unreachable"

        return net_stats
