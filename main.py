import cv2
import pytesseract
import csv

def extract_text_from_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Perform text preprocessing on the image to enhance OCR accuracy
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Use pytesseract to extract text from the preprocessed image
    extracted_text = pytesseract.image_to_string(threshold_image)

    return extracted_text

def save_to_csv(text, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Initialize variables to store extracted fields
        pan_number = ""
        name = ""
        father_name = ""
        dob = ""

        # Split the extracted text into lines and process each line to find the required fields
        lines = text.strip().split('\n')
        for line in lines:
            if "Permanent Account Number" in line:
                pan_number = line.split(':')[-1].strip()
            elif "Name" in line:
                name = line.split(':')[-1].strip()
            elif "Father's Name" in line:
                father_name = line.split(':')[-1].strip()
            elif "Date of Birth" in line:
                dob = line.split(':')[-1].strip()

        # Write the extracted fields to the CSV file
        writer.writerow(["Pan number", "Name", "Father's name", "DOB"])
        writer.writerow([pan_number, name, father_name, dob])

if __name__ == "__main__":
    # Set the Tesseract OCR executable path (update this with the path on your system)
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

    # Path to the input image (PAN card image)
    input_image_path = "/Users/Documents/pan.jpg"

    # Path to the output CSV file
    new_csv_file = "path"

    # Extract text from the image
    extracted_text = extract_text_from_image(input_image_path)

    # Print extracted text for debugging
    print("Out: Pan number, Name, Father's name, DOB")
    print("Out:", extracted_text)

    # Save extracted fields to a CSV file
    save_to_csv(extracted_text, new_csv_file)

    print("Out: Fields extracted and saved to CSV successfully!")
