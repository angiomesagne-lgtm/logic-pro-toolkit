import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class Track:
    name: str
    channel: int
    midi_data: List[int] = field(default_factory=list)

@dataclass
class LogicProXProject:
    name: str
    bpm: int
    tracks: List[Track] = field(default_factory=list)

class LogicProXParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.project: Optional[LogicProXProject] = None

    def parse(self) -> LogicProXProject:
        """Parse a Logic Pro X project file and return a LogicProXProject instance."""
        if not os.path.exists(self.file_path):
            logging.error("File not found: %s", self.file_path)
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            logging.info("Parsing project file: %s", self.file_path)
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            project_name = root.find('name').text
            bpm = int(root.find('bpm').text)
            tracks = self._parse_tracks(root.findall('tracks/track'))
            self.project = LogicProXProject(name=project_name, bpm=bpm, tracks=tracks)
            logging.info("Project parsed successfully: %s", self.project)
            return self.project
        except ET.ParseError as e:
            logging.error("Failed to parse XML: %s", e)
            raise ValueError("Failed to parse XML") from e
        except Exception as e:
            logging.error("An error occurred while parsing the project: %s", e)
            raise

    def _parse_tracks(self, track_elements) -> List[Track]:
        """Parse track elements from the XML and return a list of Track instances."""
        tracks = []
        for track_elem in track_elements:
            name = track_elem.find('name').text
            channel = int(track_elem.find('channel').text)
            midi_data = [int(note.text) for note in track_elem.findall('midi_data/note')]
            track = Track(name=name, channel=channel, midi_data=midi_data)
            tracks.append(track)
            logging.info("Parsed track: %s", track)
        return tracks

class LogicProXExporter:
    def __init__(self, project: LogicProXProject):
        self.project = project

    def export_to_xml(self, output_path: str) -> None:
        """Export the LogicProXProject to an XML file."""
        logging.info("Exporting project to XML: %s", output_path)
        root = ET.Element("project")
        ET.SubElement(root, "name").text = self.project.name
        ET.SubElement(root, "bpm").text = str(self.project.bpm)

        tracks_elem = ET.SubElement(root, "tracks")
        for track in self.project.tracks:
            track_elem = ET.SubElement(tracks_elem, "track")
            ET.SubElement(track_elem, "name").text = track.name
            ET.SubElement(track_elem, "channel").text = str(track.channel)
            midi_data_elem = ET.SubElement(track_elem, "midi_data")
            for note in track.midi_data:
                note_elem = ET.SubElement(midi_data_elem, "note")
                note_elem.text = str(note)

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        logging.info("Project exported successfully to: %s", output_path)