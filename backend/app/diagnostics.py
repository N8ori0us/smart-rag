import os
import sys
import time
import socket
import shutil
import platform
import urllib.request
import urllib.error

# Pull centralized environment hooks from your configuration module
from app.config import COLLECTION_NAME, VECTOR_DB_URL, API_URL

def discover_system_hardware():
    """Queries the host operating system at runtime to dynamically assemble a

    universal hardware and virtualization signature.
    """
    stats = {}
    try:
        # Dynamic Compute Discovery
        stats["logical_cpu_cores"] = os.cpu_count() or 0
        stats["cpu_architecture"] = platform.machine()
        stats["processor_type"] = platform.processor()
        
        # Dynamic Linux cgroup Container RAM Discovery (Supports both v1 and v2)
        ram_limit = None
        cgroup_v2_path = "/sys/fs/cgroup/memory.max"
        cgroup_v1_path = "/sys/fs/cgroup/memory/memory.limit_in_bytes"
        
        if os.path.exists(cgroup_v2_path):
            with open(cgroup_v2_path, "r") as f:
                val = f.read().strip()
                if val != "max":  # cgroups v2 returns literal 'max' if unlimited
                    ram_limit = int(val)
        elif os.path.exists(cgroup_v1_path):
            with open(cgroup_v1_path, "r") as f:
                ram_limit = int(f.read().strip())
                
        if ram_limit:
            stats["active_container_ram_limit_bytes"] = ram_limit
        
        # Dynamic Storage Volume Calculations
        total, used, free = shutil.disk_usage("/")
        stats["storage_total_gb"] = round(total / (1024**3), 2)
        stats["storage_used_gb"] = round(used / (1024**3), 2)
        stats["storage_free_gb"] = round(free / (1024**3), 2)
        stats["storage_utilization_pct"] = round((used / total) * 100, 2)
        
        # Dynamic OS Kernel Environment Metadata
        stats["host_os_platform"] = platform.system()
        stats["host_os_release"] = platform.release()
        stats["runtime_python_version"] = sys.version.split()[0]
    except Exception as e:
        stats["probe_error"] = f"Runtime hardware discovery failed: {str(e)}"
    return stats

def get_environment_identity():
    """Extracts custom environment descriptors from memory variables, providing

    local context without hardcoding text fields into version control.
    """
    return {
        "node_assignments": {
            "active_role": os.getenv("SERVER_HARDWARE_NAME", "Generic Linux Node"),
            "chassis_state": os.getenv("SERVER_CHASSIS_STATE", "Default Headless Deployment"),
            "client_workstation_peer": os.getenv("CLIENT_HARDWARE_NAME", "Unknown Client Base"),
            "client_nickname": os.getenv("CLIENT_NICKNAME", "Unassigned"),
            "peripheral_utility_nodes": os.getenv("PERIPHERAL_HARDWARE_NAME", "None Configured"),
            "mobile_testing_nodes": os.getenv("PHONE_HARDWARE_NAME", "None Configured")
        },
        "virtualization_context": {
            "hypervisor_layer": os.getenv("HYPERVISOR_HOST_SPEC", "Bare-metal / Native OS"),
            "target_guest_hostname": os.getenv("VM_HOSTNAME_MASK", "localhost"),
            "guest_os_profile": os.getenv("VM_OS_SPEC", "Standard Linux Distribution"),
            "allocated_compute_claim": os.getenv("VM_COMPUTE_ALLOCATION", "Default Allocation")
        },
        "network_topology_context": {
            "uplink_static_bridge": os.getenv("SERVER_STATIC_IP_MASK", "DHCP Addressing"),
            "client_bridge_ip": os.getenv("CLIENT_BRIDGE_IP_MASK", "Unassigned"),
            "thunderbolt_bridge_nic": os.getenv("THUNDERBOLT_NIC_SPEC", "No Thunderbolt NIC Detected"),
            "network_isolation_boundary": os.getenv("NETWORK_ISOLATION_SPEC", "Default Shared Routing")
        }
    }

class DiagnosticEngine:
    def __init__(self):
        # Safely convert configuration URLs into pure network host and port primitives
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
        """Orchestrates dynamic probes, identity lookups, and connection tracking metrics."""
        start_total = time.time()
        
        live_networking = self.test_networking()
        live_hardware = discover_system_hardware()
        identity_profile = get_environment_identity()
        
        total_runtime = time.time() - start_total
        
        return {
            "diagnostic_metadata": {
                "timestamp_epoch": int(time.time()),
                "total_diagnostic_execution_seconds": round(total_runtime, 4)
            },
            "live_network_latency": live_networking,
            "live_hardware_discovery": live_hardware,
            "configured_identity_matrix": identity_profile,
            "database_geometry": {
                "instance": "Qdrant Vector Database Cluster",
                "collection_target": COLLECTION_NAME,
                "vector_dimension_bounds": "1536-dimensional float coordinates",
                "distance_metric_logic": "Cosine Distance metric optimization"
            }
        }

    def test_networking(self):
        """Measures active internal and external communication path execution timings."""
        net_stats = {}
        
        # 1. Dynamically parse target host from your central API_URL parameter
        try:
            target_api_host = API_URL.replace("http://", "").replace("https://", "").split("/")[0]
        except Exception:
            target_api_host = "openrouter.ai"

        # 2. DNS Resolution Trace
        start_dns = time.time()
        try:
            socket.gethostbyname(target_api_host)
            net_stats["dns_resolution_seconds"] = round(time.time() - start_dns, 4)
            net_stats["dns_status"] = "healthy"
        except Exception:
            net_stats["dns_resolution_seconds"] = round(time.time() - start_dns, 4)
            net_stats["dns_status"] = "failed"

        # 3. Inter-Container Database Connectivity Check
        start_db_ping = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            s.connect((self.target_db_host, self.target_db_port))
            s.close()
            net_stats["db_connection_latency_seconds"] = round(time.time() - start_db_ping, 4)
            net_stats["db_routing_status"] = "connected"
        except Exception:
            net_stats["db_connection_latency_seconds"] = round(time.time() - start_db_ping, 4)
            net_stats["db_routing_status"] = "failed"

        # 4. Upstream Gateway Handshake Trace via Central API_URL
        start_api = time.time()
        try:
            req = urllib.request.Request(API_URL, data=b"{}", method="POST")
            with urllib.request.urlopen(req, timeout=5) as _:
                pass
        except urllib.error.HTTPError as e:
            net_stats["api_handshake_seconds"] = round(time.time() - start_api, 4)
            net_stats["api_gateway_status"] = f"reachable (Server responded with HTTP {e.code})"
        except Exception:
            net_stats["api_handshake_seconds"] = round(time.time() - start_api, 4)
            net_stats["api_gateway_status"] = "unreachable"

        return net_stats
