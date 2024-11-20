import cv2
from pyzbar.pyzbar import decode
from fpdf import FPDF
import datetime

# List to hold scanned items and their prices
scanned_items = []

def scan_qr_code():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break
        
        # Decode the QR code
        qr_codes = decode(frame)
        if qr_codes:
            for qr_code in qr_codes:
                # Convert QR code data to string
                qr_data = qr_code.data.decode('utf-8')
                try:
                    # Split data by space to get name and price
                    parts = qr_data.split()
                    if len(parts) >= 2:
                        # Extract name and price
                        name = " ".join(parts[:-1])  # Join all parts except the last as the name
                        price = float(parts[-1])  # Last part is the price
                        scanned_items.append((name, price))
                        print(f"Scanned: {name} - ${price:.2f}")
                    else:
                        print("Error: QR code data format should be 'name price'.")
                except Exception as e:
                    print("Error in QR code format. Use 'name price'.")
                    print(e)

                # Stop scanning after one item
                cap.release()
                cv2.destroyAllWindows()
                return  # Exit the scan function after scanning one item

        # Display the camera feed
        cv2.imshow("QR Code Scanner", frame)

        # Press 'q' to quit scanning manually (just in case)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def generate_pdf_receipt():
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Receipt", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    
    # Add Date and Time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, txt=f"Date: {current_time}", ln=True, align="C")
    
    pdf.ln(10)  # Line break

    # Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(10, 10, "S.No", 1, 0, "C", fill=True)
    pdf.cell(120, 10, "Name", 1, 0, "C", fill=True)
    pdf.cell(40, 10, "Price ($)", 1, 1, "C", fill=True)

    # Add scanned items to the PDF
    total_price = 0
    for idx, (name, price) in enumerate(scanned_items, start=1):
        pdf.cell(10, 10, str(idx), 1, 0, "C")
        pdf.cell(120, 10, name, 1, 0)
        pdf.cell(40, 10, f"{price:.2f}", 1, 1, "R")
        total_price += price

    # Total
    pdf.ln(5)
    pdf.cell(130, 10, "Total", 1, 0)
    pdf.cell(40, 10, f"${total_price:.2f}", 1, 1, "R")

    # Save the PDF
    pdf_filename = "receipt.pdf"
    pdf.output(pdf_filename)
    print(f"\nReceipt generated and saved as {pdf_filename}")

# Main loop
while True:
    print("\nType 'scan' to scan a QR code or 'done' to finish and generate the receipt:")
    user_input = input().lower()
    
    if user_input == "scan":
        scan_qr_code()
    elif user_input == "done":
        if scanned_items:
            generate_pdf_receipt()
        else:
            print("No items scanned. Exiting.")
        break
    else:
        print("Invalid input, please type 'scan' or 'done'.")
