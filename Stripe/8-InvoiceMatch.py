def parse_payment(payment_str):
    payment_name, payment_amount_str, memo = [part.strip() for part in payment_str.split(",")]
    return {
        "payment_name": payment_name,
        "payment_amount": int(payment_amount_str),
        "memo": memo,
    }


def parse_invoice(invoice_str):
    invoice_id, due_date, amount_str = [part.strip() for part in invoice_str.split(",")]
    return {
        "invoice_id": invoice_id,
        "due_date": due_date,
        "amount": int(amount_str),
    }


def parse_invoices(invoice_strs):
    return [parse_invoice(invoice_str) for invoice_str in invoice_strs]


def extract_invoice_id_from_memo(memo):
    for token in memo.split():
        if token.startswith("XXXX:"):
            return token[len("XXXX:"):]
    return None


def find_invoice_by_id(invoices, invoice_id):
    if invoice_id is None:
        return None

    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice

    return None


def find_invoice_by_amount(invoices, payment_amount):
    matches = [
        invoice for invoice in invoices
        if invoice["amount"] == payment_amount
    ]
    if not matches:
        return None

    return min(matches, key=lambda invoice: invoice["due_date"])


def find_invoice_by_amount_with_forgiveness(invoices, payment_amount, forgiveness):
    matches = [
        invoice for invoice in invoices
        if abs(invoice["amount"] - payment_amount) <= forgiveness
    ]
    if not matches:
        return None

    return min(matches, key=lambda invoice: invoice["due_date"])


def format_summary(payment, invoice, include_difference=False):
    summary = {
        "payment_name": payment["payment_name"],
        "payment_amount": payment["payment_amount"],
        "due_date": invoice["due_date"],
        "invoice_id": invoice["invoice_id"],
    }

    if include_difference:
        summary["difference"] = payment["payment_amount"] - invoice["amount"]

    return summary


def payment_summary(payment_str, invoice_strs, forgiveness=0):
    payment = parse_payment(payment_str)
    invoices = parse_invoices(invoice_strs)

    invoice_id = extract_invoice_id_from_memo(payment["memo"])
    matched_invoice = find_invoice_by_id(invoices, invoice_id)

    if matched_invoice is None:
        if forgiveness > 0:
            matched_invoice = find_invoice_by_amount_with_forgiveness(
                invoices, payment["payment_amount"], forgiveness
            )
        else:
            matched_invoice = find_invoice_by_amount(
                invoices, payment["payment_amount"]
            )

    if matched_invoice is None:
        return None

    return format_summary(payment, matched_invoice, include_difference=(forgiveness > 0))

payment = "alice, 97, no reference"
invoices = [
    "INV-100, 2025-01-10, 100",
    "INV-101, 2025-01-05, 95",
    "INV-200, 2025-01-07, 150"
]
forgiveness = 3

print(payment_summary(payment, invoices, forgiveness))