import argparse
import os
import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class LogicProXToolkit:
    def __init__(self, directory: str):
        self.directory = directory

    def scan_files(self) -> List[str]:
        try:
            return [f for f in os.listdir(self.directory) if f.endswith('.logicx')]
        except Exception as e:
            raise RuntimeError(f"Error scanning directory '{self.directory}': {e}")

    def get_file_info(self, filename: str) -> Dict[str, Any]:
        try:
            file_path = os.path.join(self.directory, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()
            info = {
                'name': filename,
                'tempo': root.find('tempo').text,
                'tracks': [track.get('name') for track in root.findall('track')]
            }
            return info
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found in directory '{self.directory}'")
        except Exception as e:
            raise RuntimeError(f"Error reading file '{filename}': {e}")

    def export_data(self, filename: str, format: str) -> None:
        try:
            file_info = self.get_file_info(filename)
            if format.lower() == 'json':
                with open(f"{filename}.json", 'w') as json_file:
                    json.dump(file_info, json_file, indent=4)
            elif format.lower() == 'csv':
                with open(f"{filename}.csv", 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=file_info.keys())
                    writer.writeheader()
                    writer.writerow(file_info)
            else:
                raise ValueError("Format must be 'json' or 'csv'")
        except Exception as e:
            raise RuntimeError(f"Error exporting data for '{filename}': {e}")

    def batch_process(self, format: str) -> None:
        try:
            files = self.scan_files()
            for filename in files:
                self.export_data(filename, format)
                print(f"Processed: {filename}")
        except Exception as e:
            raise RuntimeError(f"Error during batch processing: {e}")

def main():
    parser = argparse.ArgumentParser(description="Logic Pro X Toolkit")
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for Logic Pro X files')
    scan_parser.add_argument('directory', type=str, help='Directory to scan')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific file')
    info_parser.add_argument('directory', type=str, help='Directory containing the Logic Pro X file')
    info_parser.add_argument('filename', type=str, help='Name of the Logic Pro X file')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON/CSV')
    export_parser.add_argument('directory', type=str, help='Directory containing the Logic Pro X file')
    export_parser.add_argument('filename', type=str, help='Name of the Logic Pro X file')
    export_parser.add_argument('format', type=str, choices=['json', 'csv'], help='Export format')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('directory', type=str, help='Directory containing Logic Pro X files')
    batch_parser.add_argument('format', type=str, choices=['json', 'csv'], help='Export format')

    args = parser.parse_args()

    toolkit = LogicProXToolkit(args.directory)

    try:
        if args.command == 'scan':
            files = toolkit.scan_files()
            print(f"Found Logic Pro X files: {files}")
        elif args.command == 'info':
            info = toolkit.get_file_info(args.filename)
            print(json.dumps(info, indent=4))
        elif args.command == 'export':
            toolkit.export_data(args.filename, args.format)
            print(f"Exported {args.filename} to {args.format}")
        elif args.command == 'batch':
            toolkit.batch_process(args.format)
            print(f"Batch processing completed for all files in '{args.directory}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()