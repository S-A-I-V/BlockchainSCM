
def generate_qr_code_representation(transaction):
    qr_data = {
        'Manufacturer': transaction.manufacturer,
        'Distributor': transaction.distributor,
        'Client': transaction.client,
        'Timestamps': transaction.timestamps
    }
    qr_string = "QR_CODE[" + str(qr_data) + "]"
    return qr_string
