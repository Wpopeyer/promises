# Example writer stub.
def mirror_zone(zone):
    firestore.collection("zones").document(f"{zone.city_id},{zone.id}").set({"is_active": not zone.decommissioned})
