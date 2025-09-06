import os
import argparse
import pydicom
import matplotlib.pyplot as plt


def list_dicom_files(directory):
    #    return [f for f in os.listdir(directory) if f.lower().endswith(".dcm")]
    #  Assume all file are dcms
    return [f for f in os.listdir(directory)]


def choose_file(files):
    print("\nAvailable DICOM files:")
    for i, file in enumerate(files):
        print(f"{i}: {file}")
    choice = int(input("\nEnter the number of the file you want to view: "))
    return files[choice]


def display_dicom_image(filepath):
    ds = pydicom.dcmread(filepath)
    if 'PixelSpacing' in ds:
        spacing = ds.PixelSpacing  # [row spacing, column spacing] in mm
        print(
            f"Pixel spacing: {spacing[0]} mm (row), {spacing[1]} mm (column)")
    else:
        print("Pixel spacing not available.")

    rows = ds.Rows
    columns = ds.Columns

    print(f"Image resolution: {columns} x {rows} (width x height)")

    print("\nMetadata Summary:")
    print(f"Patient Name: {ds.get('PatientName', 'Unknown')}")
    print(f"Study Date: {ds.get('StudyDate', 'Unknown')}")
    print(f"Modality: {ds.get('Modality', 'Unknown')}")
    plt.imshow(ds.pixel_array, cmap='gray')
    plt.title(f"{os.path.basename(filepath)}")
    plt.axis('off')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="DICOM Viewer")
    parser.add_argument(
        "directory", help="Path to directory containing DICOM files")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Invalid directory.")
        return

    dicom_files = list_dicom_files(args.directory)
    if not dicom_files:
        print("No DICOM files found in the directory.")
        return

    selected_file = choose_file(dicom_files)
    filepath = os.path.join(args.directory, selected_file)
    display_dicom_image(filepath)


if __name__ == "__main__":
    main()
