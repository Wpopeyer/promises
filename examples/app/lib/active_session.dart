// Example writer stub.
await FirebaseFirestore.instance.collection('sessions').doc(plate).set({
  'is_parked': endedAt == null,
  'zone_type': resolveZoneType(tariffCode),
});
