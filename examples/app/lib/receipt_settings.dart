// Example writer stub.
await FirebaseFirestore.instance.collection('drivers').doc(email).update({'sms_receipts': value});
