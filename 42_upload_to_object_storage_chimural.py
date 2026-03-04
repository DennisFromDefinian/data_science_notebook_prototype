# ============================================================
# Upload to OCI Object Storage (Resource Principal)
#
# REQUIRED:
#   BUCKET_NAME: your bucket
# OPTIONAL:
#   PREFIX: "folder" inside bucket
# ============================================================

import os
import oci
from oci.auth import signers

# ===== REQUIRED: set your bucket name =====
BUCKET_NAME = "REPLACE_ME"
# =========================================

PREFIX = "murals/vector-index"  # organize artifacts in your bucket
REGION = os.getenv("OCI_REGION") or "us-ashburn-1"

signer = signers.get_resource_principals_signer()
os_client = oci.object_storage.ObjectStorageClient({"region": REGION}, signer=signer)
NAMESPACE = os_client.get_namespace().data

def upload_file(local_path: str, object_name: str):
    with open(local_path, "rb") as f:
        os_client.put_object(NAMESPACE, BUCKET_NAME, object_name, f)
    print(f"✅ Uploaded: {object_name}")

upload_file(INDEX_PATH, f"{PREFIX}/{INDEX_PATH}")
upload_file(META_PATH,  f"{PREFIX}/{META_PATH}")

print("\nDone. Check your bucket for:")
print(f"  {PREFIX}/{INDEX_PATH}")
print(f"  {PREFIX}/{META_PATH}")