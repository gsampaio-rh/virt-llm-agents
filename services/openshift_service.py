from kubernetes import client
from kubernetes.client.rest import ApiException
from typing import List, Dict, Union
import requests


class OpenShiftService:
    """
    This service class handles interactions with the OpenShift (Kubernetes-based) API,
    including retrieving namespaces (projects), checking access, retrieving providers,
    and verifying their readiness.
    """

    def __init__(
        self,
        openshift_config: dict,
    ):
        """
        Initializes the OpenShiftService with API URL, token, and inventory service route,
        and sets up the connection to the OpenShift cluster.
        """
        try:
            api_url = openshift_config["api_url"]
            console_url = openshift_config["console_url"]
            inventory_route = openshift_config["inventory_route"]
            token = openshift_config["token"]

            # Set up the Kubernetes API client configuration
            configuration = client.Configuration()
            configuration.host = api_url
            configuration.verify_ssl = False  # Disable SSL verification if needed
            configuration.api_key = {"authorization": f"Bearer {token}"}

            # Use the custom configuration
            client.Configuration.set_default(configuration)

            self.api_url = api_url
            self.console_url = console_url
            # Create the CoreV1Api and CustomObjectsApi instances for interacting with resources
            self.core_v1_api = client.CoreV1Api()
            self.custom_objects_api = client.CustomObjectsApi()

            # Set the inventory service route and headers
            self.inventory_service_route = inventory_route
            self.headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            }

            # Test connection by fetching namespaces
            self._test_connection()

        except Exception as e:
            print(str(e))
            raise Exception(f"Failed to initialize OpenShiftService: {str(e)}")

    def _test_connection(self):
        """
        Tests the connection by calling the /healthz endpoint.
        This is a quick way to check if the API server is up.
        """
        try:
            url = f"{self.api_url}/healthz"
            response = requests.get(url, headers=self.headers, verify=False)
            if response.status_code == 200 and response.text == "ok":
                print("OpenShift Service connected. API is healthy.")
            else:
                print(f"API health check failed with status: {response.status_code}, response: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error when testing OpenShift API health: {str(e)}")
            raise Exception(f"Failed to connect to OpenShift API: {str(e)}")

    def get_projects(self) -> Union[List[str], str]:
        """
        Retrieves a list of namespaces (projects) available to the logged-in user on OpenShift.

        Returns:
            List[str]: A list of namespace names if successful.
            str: An error message if the operation fails.
        """
        try:
            namespaces = self.core_v1_api.list_namespace()
            project_list = [ns.metadata.name for ns in namespaces.items]
            return project_list
        except ApiException as e:
            return f"Failed to retrieve namespaces: {str(e)}"

    def check_project_access(self, required_projects: List[str]) -> Union[bool, str]:
        """
        Ensures the user has access to the required namespaces.

        Args:
            required_projects (List[str]): A list of namespace names that are needed for migration.

        Returns:
            bool: True if access is confirmed for all required namespaces.
            str: An error message if the operation fails or access is not available.
        """
        try:
            available_projects = self.get_projects()

            if isinstance(available_projects, str):
                # If the function returned an error message, propagate it
                return available_projects

            missing_projects = [
                proj for proj in required_projects if proj not in available_projects
            ]

            if not missing_projects:
                return True
            else:
                return f"Missing access to the following projects: {', '.join(missing_projects)}"

        except ApiException as e:
            return f"Failed to check project access: {str(e)}"

    def get_providers(self, namespace: str = "openshift-mtv") -> Union[List[dict], str]:
        """
        Retrieves the list of Provider resources in the specified namespace.

        Args:
            namespace (str): The namespace where the providers are listed (default: 'openshift-mtv').

        Returns:
            List[dict]: A list of Provider resources if successful.
            str: An error message if the operation fails.
        """
        try:
            providers = self.custom_objects_api.list_namespaced_custom_object(
                group="forklift.konveyor.io",
                version="v1beta1",
                namespace=namespace,
                plural="providers",
            )
            return providers["items"]
        except ApiException as e:
            return f"Failed to retrieve providers: {str(e)}"

    def verify_providers_ready(self, providers: List[dict]) -> Union[bool, str]:
        """
        Verifies that both the VMware and Host providers are listed and their statuses are 'Ready'.

        Args:
            providers (List[dict]): The list of Provider objects retrieved from the OpenShift cluster.

        Returns:
            bool: True if both providers are found and have the 'Ready' status.
            str: An error message if the providers are not ready or not found.
        """
        # Initialize status flags
        vmware_ready = False
        host_ready = False

        # Check each provider for 'vmware' and 'host' and verify 'Ready' status
        for provider in providers:
            provider_name = provider["metadata"]["name"]
            if provider_name in ["vmware", "host"]:
                conditions = provider["status"].get("conditions", [])
                for condition in conditions:
                    if condition["type"] == "Ready" and condition["status"] == "True":
                        if provider_name == "vmware":
                            vmware_ready = True
                        elif provider_name == "host":
                            host_ready = True

        # Verify both providers are ready
        if vmware_ready and host_ready:
            return True
        else:
            missing_providers = []
            if not vmware_ready:
                missing_providers.append("vmware")
            if not host_ready:
                missing_providers.append("host")
            return (
                f"The following providers are not ready: {', '.join(missing_providers)}"
            )

    def create_migration_plan(
        self,
        network_map_uid: str,
        network_map_name: str,
        storage_map_uid: str,
        storage_map_name: str,
        name: str = "default-migration-plan",
        destination: str = "host",
        source: str = "vmware",
        vms: List[Dict[str, str]] = None,
        namespace: str = "openshift-mtv",
    ) -> Union[Dict, str]:
        """
        Creates a migration plan using the forklift.konveyor.io API.

        Args:
            name (str): The name of the migration plan. Default is 'default-migration-plan'.
            destination (str): The destination provider. Default is 'host'.
            source (str): The source provider. Default is 'vmware'.
            vms (List[Dict[str, str]]): A list of VMs to migrate, each VM represented as a dictionary with 'id' and 'name'. Default is None.
            namespace (str): The namespace for the migration plan. Default is 'openshift-mtv'.

        Returns:
            dict: The created migration plan if successful.
            str: An error message if the operation fails.
        """
        if vms is None:
            vms = [
                {"id": "vm-12345", "name": "default-vm"}
            ]  # Default VM if none provided

        n_uid = network_map_uid
        s_uid = storage_map_uid

        openshift_provider_uuid = self.lookup_provider_uuid_by_name(
            provider_name="host", provider_type="openshift"
        )

        vmware_provider_uuid = self.lookup_provider_uuid_by_name(
            provider_name="vmware", provider_type="vsphere"
        )

        try:
            # Prepare the body of the migration plan
            body = {
                "apiVersion": "forklift.konveyor.io/v1beta1",
                "kind": "Plan",
                "metadata": {"name": name, "namespace": namespace},
                "spec": {
                    "map": {
                        "network": {
                            "apiVersion": "forklift.konveyor.io/v1beta1",
                            "kind": "NetworkMap",
                            "name": network_map_name,
                            "namespace": namespace,
                            "uid": n_uid,
                        },
                        "storage": {
                            "apiVersion": "forklift.konveyor.io/v1beta1",
                            "kind": "StorageMap",
                            "name": storage_map_name,
                            "namespace": namespace,
                            "uid": s_uid,
                        },
                    },
                    "provider": {
                        "destination": {
                            "apiVersion": "forklift.konveyor.io/v1beta1",
                            "kind": "Provider",
                            "name": destination,
                            "namespace": namespace,
                            "uid": openshift_provider_uuid,
                        },
                        "source": {
                            "apiVersion": "forklift.konveyor.io/v1beta1",
                            "kind": "Provider",
                            "name": source,
                            "namespace": namespace,
                            "uid": vmware_provider_uuid,
                        },
                    },
                    "targetNamespace": namespace,
                    "vms": vms,
                },
            }

            # Create the migration plan using the Kubernetes custom object API
            api_instance = client.CustomObjectsApi()
            created_plan = api_instance.create_namespaced_custom_object(
                group="forklift.konveyor.io",
                version="v1beta1",
                namespace=namespace,
                plural="plans",
                body=body,
            )

            return created_plan

        except ApiException as e:
            return f"Failed to create migration plan: {str(e)}"

    def get_providers(self, provider_type: str = "vsphere") -> Union[List[Dict], str]:
        """
        Retrieves the list of providers for a specific provider type.

        Args:
            provider_type (str): The type of provider (default: 'vsphere').

        Returns:
            Union[List[Dict], str]: A list of provider details if successful, or an error message if failed.
        """
        url = f"https://{self.inventory_service_route}/providers/{provider_type}"

        try:
            # Make the GET request to fetch the providers
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Failed to retrieve providers: {str(e)}"

    def get_vms_for_migration(
        self, provider_uuid: str, provider_type: str = "vsphere"
    ) -> Union[List[Dict], str]:
        """
        Fetches the list of available VMs for migration from a specific provider in the specified namespace.

        Args:
            provider_type (str): The type of provider (default: 'vsphere').
            provider_uuid (str): The UUID of the provider to fetch VMs for.

        Returns:
            Union[List[Dict], str]: A list of VMs if successful, or an error message if failed.
        """
        # Construct the full API URL dynamically
        url = f"https://{self.inventory_service_route}/providers/{provider_type}/{provider_uuid}/vms?detail=4"

        try:
            # Make the GET request to fetch the VMs
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for non-200 responses

            # Parse the JSON response and return the list of VMs
            return response.json()

        except requests.exceptions.RequestException as e:
            # Return a formatted error message if the request fails
            return f"Failed to retrieve VMs: {str(e)}"

    def lookup_provider_uuid_by_name(
        self, provider_name: str = "vmware", provider_type: str = "vsphere"
    ) -> Union[str, None, str]:
        """
        Looks up the UUID of a provider by its name.

        Args:
            provider_name (str): The name of the provider (default: 'vmware').
            provider_type (str): The type of the provider (default: 'vsphere').

        Returns:
            str: The UUID of the provider if found.
            None: If the provider is not found.
            str: Error message if the API request fails.
        """
        # Construct the URL to retrieve the providers for the specified provider type
        url = f"{self.inventory_service_route}/providers/{provider_type}"

        try:

            # Print the request details for debugging

            # Make the GET request to fetch the providers
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()  # Raise an error for non-200 responses

            # Parse the JSON response to get the list of providers
            providers = response.json()

            # Search for the provider by name and return its UUID
            for provider in providers:
                if provider["name"] == provider_name:
                    return provider["uid"]

            # If no provider with the given name is found, return None
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving provider information: {str(e)}")
            return f"Error retrieving provider information: {str(e)}"

    def lookup_vm_id_by_name(
        self, provider_uuid: str, vm_name: str, provider_type: str = "vsphere"
    ) -> Union[str, None, str]:
        """
        Looks up the ID of a VM by its name within a specific provider.

        Args:
            provider_uuid (str): The UUID of the provider (e.g., VMware).
            vm_name (str): The name of the VM to look up.
            provider_type (str): The type of the provider (default: 'vsphere').

        Returns:
            str: The ID of the VM if found.
            None: If the VM is not found.
            str: Error message if the API request fails.
        """
        # Construct the URL to retrieve the VMs for the specified provider
        url = f"{self.inventory_service_route}/providers/{provider_type}/{provider_uuid}/vms?detail=4"

        try:
            # Make the GET request to fetch the VMs
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()  # Raise an error for non-200 responses

            # Parse the JSON response to get the list of VMs
            vms = response.json()

            # Search for the VM by name and return its ID
            for vm in vms:
                if vm["name"] == vm_name:
                    return vm["id"]

            # If no VM with the given name is found, return None
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving VM information: {str(e)}")
            return f"Error retrieving VM information: {str(e)}"

    def start_migration(
        self, plan_name: str, plan_uid: str, namespace: str = "openshift-mtv"
    ) -> Union[Dict, str]:
        """
        Starts a migration for the given plan by creating a new Migration resource in the specified namespace.

        Args:
            plan_name (str): The name of the migration plan.
            plan_uid (str): The UID of the migration plan.
            namespace (str): The namespace where the migration plan is located. Default is 'openshift-mtv'.

        Returns:
            Dict: The response from the API if successful.
            str: An error message if the operation fails.
        """
        # Define the API URL for creating a migration
        url = f"{self.api_url}/apis/forklift.konveyor.io/v1beta1/namespaces/{namespace}/migrations"

        # Construct the migration payload
        payload = {
            "apiVersion": "forklift.konveyor.io/v1beta1",
            "kind": "Migration",
            "metadata": {
                "generateName": f"{plan_name}-",
                "namespace": namespace,
                "ownerReferences": [
                    {
                        "apiVersion": "forklift.konveyor.io/v1beta1",
                        "kind": "Plan",
                        "name": plan_name,
                        "uid": plan_uid,
                    }
                ],
            },
            "spec": {
                "plan": {"name": plan_name, "namespace": namespace, "uid": plan_uid}
            },
        }

        try:
            # Make the POST request to start the migration
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for non-200 responses

            # Return the JSON response if successful
            return response.json()

        except requests.exceptions.RequestException as e:
            return f"Failed to start migration: {str(e)}"

    def get_migration_plan_by_name(
        self, plan_name: str, namespace: str = "openshift-mtv"
    ) -> Union[Dict, None, str]:
        """
        Retrieves the entire migration plan object by its name.

        Args:
            plan_name (str): The name of the migration plan.
            namespace (str): The namespace where the migration plan is located. Default is 'openshift-mtv'.

        Returns:
            Dict: The full migration plan object if found.
            None: If the migration plan is not found.
            str: Error message if the API request fails.
        """
        # Define the API URL for listing the migration plans
        url = f"{self.api_url}/apis/forklift.konveyor.io/v1beta1/namespaces/{namespace}/plans"

        try:
            # Make the GET request to list the migration plans
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for non-200 responses

            # Parse the JSON response to get the list of migration plans
            plans = response.json().get("items", [])

            # Search for the plan by name and return the full plan object
            for plan in plans:
                if plan["metadata"]["name"] == plan_name:
                    return plan

            # If no plan with the given name is found, return None
            return None

        except requests.exceptions.RequestException as e:
            return f"Error retrieving migration plans: {str(e)}"

    def create_storage_map(
        self,
        source_provider_uid: str = "a1699c04-47c7-4864-852e-f3877bc889e9",
        destination_provider_uid: str = "c07f4f30-c9a4-4c04-894e-5414820311b8",
        source_datastore_id: str = "datastore-1032",
        destination_storage_class: str = "ocs-storagecluster-ceph-rbd",
        namespace: str = "openshift-mtv",
        source_provider_name: str = "vmware",
        destination_provider_name: str = "host",
    ) -> Union[Dict, str]:
        """
        Creates a new storage map in OpenShift.

        Args:
            source_provider_uid (str): The UUID of the source provider (e.g., VMware).
            destination_provider_uid (str): The UUID of the destination provider (e.g., Host).
            source_datastore_id (str): The datastore ID of the source.
            destination_storage_class (str): The storage class of the destination.
            namespace (str): The namespace where the storage map is created (default: 'openshift-mtv').
            source_provider_name (str): The name of the source provider (default: 'vmware').
            destination_provider_name (str): The name of the destination provider (default: 'host').

        Returns:
            Dict: The created storage map if successful.
            str: An error message if the operation fails.
        """
        url = f"{self.api_url}/apis/forklift.konveyor.io/v1beta1/namespaces/{namespace}/storagemaps"

        payload = {
            "apiVersion": "forklift.konveyor.io/v1beta1",
            "kind": "StorageMap",
            "metadata": {
                "namespace": namespace,
                "generateName": f"{source_provider_name}-",
            },
            "spec": {
                "provider": {
                    "source": {
                        "apiVersion": "forklift.konveyor.io/v1beta1",
                        "kind": "Provider",
                        "name": source_provider_name,
                        "namespace": namespace,
                        "uid": source_provider_uid,
                    },
                    "destination": {
                        "apiVersion": "forklift.konveyor.io/v1beta1",
                        "kind": "Provider",
                        "name": destination_provider_name,
                        "namespace": namespace,
                        "uid": destination_provider_uid,
                    },
                },
                "map": [
                    {
                        "source": {"id": source_datastore_id},
                        "destination": {"storageClass": destination_storage_class},
                    }
                ],
            },
        }

        try:
            # Make the POST request to create the storage map
            response = requests.post(
                url, json=payload, headers=self.headers, verify=False
            )
            response.raise_for_status()  # Raise an error for non-200 responses

            created_storage_map = response.json()

            storage_map_uid = created_storage_map["metadata"]["uid"]
            storage_map_name = created_storage_map["metadata"]["name"]

            return created_storage_map, storage_map_uid, storage_map_name

        except requests.exceptions.RequestException as e:
            return f"Failed to create storage map: {str(e)}"

    def create_network_map(
        self,
        source_provider_uid: str = "3442763f-e621-41f9-b2d1-699da301353d",
        destination_provider_uid: str = "81843304-1280-4cee-b50c-e985b7264272",
        source_network_id: str = "dvportgroup-1067",
        destination_type: str = "pod",
        namespace: str = "openshift-mtv",
        source_provider_name: str = "vmware",
        destination_provider_name: str = "host",
    ) -> Union[Dict, str]:
        """
        Creates a new network map in OpenShift.

        Args:
            source_provider_uid (str): The UUID of the source provider (e.g., VMware).
            destination_provider_uid (str): The UUID of the destination provider (e.g., Host).
            source_network_id (str): The network ID of the source.
            destination_type (str): The destination type (default: 'pod').
            namespace (str): The namespace where the network map is created (default: 'openshift-mtv').
            source_provider_name (str): The name of the source provider (default: 'vmware').
            destination_provider_name (str): The name of the destination provider (default: 'host').

        Returns:
            Dict: The created network map if successful.
            str: An error message if the operation fails.
        """
        url = f"{self.api_url}/apis/forklift.konveyor.io/v1beta1/namespaces/{namespace}/networkmaps"

        payload = {
            "apiVersion": "forklift.konveyor.io/v1beta1",
            "kind": "NetworkMap",
            "metadata": {
                "namespace": namespace,
                "generateName": f"{source_provider_name}-",
            },
            "spec": {
                "provider": {
                    "source": {
                        "apiVersion": "forklift.konveyor.io/v1beta1",
                        "kind": "Provider",
                        "name": source_provider_name,
                        "namespace": namespace,
                        "uid": source_provider_uid,
                    },
                    "destination": {
                        "apiVersion": "forklift.konveyor.io/v1beta1",
                        "kind": "Provider",
                        "name": destination_provider_name,
                        "namespace": namespace,
                        "uid": destination_provider_uid,
                    },
                },
                "map": [
                    {
                        "source": {"id": source_network_id},
                        "destination": {"type": destination_type},
                    }
                ],
            },
        }

        try:
            # Make the POST request to create the network map
            response = requests.post(
                url, json=payload, headers=self.headers, verify=False
            )
            response.raise_for_status()  # Raise an error for non-200 responses

            created_network_map = response.json()

            network_map_uid = created_network_map["metadata"]["uid"]
            network_map_name = created_network_map["metadata"]["name"]

            return created_network_map, network_map_uid, network_map_name

        except requests.exceptions.RequestException as e:
            return f"Failed to create network map: {str(e)}"
