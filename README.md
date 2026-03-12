# Logic Pro Toolkit

![Banner](assets/banner.png)


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/logic-pro-toolkit.svg)](https://pypi.org/project/logic-pro-toolkit/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/logic-pro-toolkit/tests.yml?branch=main)](https://github.com/yourusername/logic-pro-toolkit/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

Logic Pro Toolkit is a comprehensive Python library for working with Logic Pro X project files, MIDI data, and audio production assets. It enables developers and music producers to programmatically parse `.logicx` projects, extract and manipulate MIDI information, manage instrument presets, and automate complex music production workflows without opening the DAW.

## Features

- **Project File Parsing**: Read and extract data from Logic Pro X project bundles
- **MIDI Data Extraction**: Parse, analyze, and export MIDI tracks and events
- **Preset Management**: Access and organize instrument and effect presets
- **Automation Data**: Extract and modify automation curves and parameters
- **Metadata Handling**: Read and modify project metadata, tags, and markers
- **Batch Processing**: Process multiple projects with automated workflows
- **XML Manipulation**: Direct access to underlying project XML structure
- **Type Safety**: Full type hints for better IDE support and code reliability

## Installation

Install via pip:

```bash
pip install logic-pro-toolkit
```

Or install from source:

```bash
git clone https://github.com/yourusername/logic-pro-toolkit.git
cd logic-pro-toolkit
pip install -e .
```

## Quick Start

```python
from logic_pro_toolkit import LogicProject

# Open a Logic Pro X project
project = LogicProject("path/to/your/project.logicx")

# Extract basic project information
print(f"Project: {project.name}")
print(f"Tempo: {project.tempo} BPM")
print(f"Time Signature: {project.time_signature}")
print(f"Total Tracks: {len(project.tracks)}")

# List all tracks
for track in project.tracks:
    print(f"Track: {track.name} ({track.track_type})")
```

## Usage Examples

### Extracting MIDI Data

```python
from logic_pro_toolkit import LogicProject
from logic_pro_toolkit.midi import MidiExporter

# Open project and access MIDI tracks
project = LogicProject("myproject.logicx")

# Get all MIDI tracks
midi_tracks = [t for t in project.tracks if t.track_type == "MIDI"]

# Extract MIDI events from a track
for track in midi_tracks:
    events = track.get_midi_events()
    
    for event in events:
        print(f"Note: {event.pitch}, Velocity: {event.velocity}, "
              f"Position: {event.start_time}, Duration: {event.duration}")

# Export MIDI to standard format
exporter = MidiExporter(project)
exporter.export_track(midi_tracks[0], "output.mid")
```

### Parsing Markers and Regions

```python
from logic_pro_toolkit import LogicProject

project = LogicProject("myproject.logicx")

# Access project markers
for marker in project.markers:
    print(f"Marker: {marker.name} at {marker.position} beats")

# Work with regions
for region in project.regions:
    print(f"Region: {region.name}")
    print(f"  Start: {region.start_time}")
    print(f"  Length: {region.length}")
    print(f"  Track: {region.track.name}")
```

### Managing Presets

```python
from logic_pro_toolkit import LogicProject
from logic_pro_toolkit.presets import PresetManager

project = LogicProject("myproject.logicx")
preset_mgr = PresetManager(project)

# List all presets in use
presets = preset_mgr.get_active_presets()
for preset in presets:
    print(f"{preset.instrument}: {preset.name}")

# Search for specific presets
synth_presets = preset_mgr.search(instrument="Alchemy", category="Synth")
for preset in synth_presets:
    print(f"Found: {preset.name}")

# Export preset settings
settings = preset_mgr.export_preset(preset)
print(settings)
```

### Batch Processing Projects

```python
from logic_pro_toolkit import LogicProject
from logic_pro_toolkit.batch import BatchProcessor
from pathlib import Path

# Process multiple projects
projects_dir = Path("./my_projects")
processor = BatchProcessor()

def analyze_project(project_path):
    """Custom analysis function"""
    project = LogicProject(project_path)
    return {
        "name": project.name,
        "tracks": len(project.tracks),
        "duration": project.duration,
        "tempo": project.tempo
    }

results = processor.process_directory(
    projects_dir,
    analyze_project,
    pattern="*.logicx"
)

for result in results:
    print(result)
```

### Extracting Automation Data

```python
from logic_pro_toolkit import LogicProject

project = LogicProject("myproject.logicx")

# Access automation for a track
track = project.tracks[0]

for automation in track.automations:
    print(f"Parameter: {automation.parameter_name}")
    
    for point in automation.points:
        print(f"  Time: {point.time}, Value: {point.value}")

# Export automation to JSON
import json
automation_data = track.export_automations_to_dict()
with open("automation.json", "w") as f:
    json.dump(automation_data, f, indent=2)
```

## Requirements

| Requirement | Version | Notes |
|------------|---------|-------|
| Python | 3.8+ | Core language requirement |
| plistlib | Built-in | For XML property list parsing |
| zipfile | Built-in | For project bundle extraction |
| music21 | 7.0+ | Optional, for advanced MIDI analysis |
| lxml | 4.6+ | Optional, for enhanced XML processing |
| pydantic | 1.8+ | For data validation |

### Installation of Optional Dependencies

```bash
# For advanced MIDI analysis
pip install logic-pro-toolkit[music21]

# For enhanced XML processing
pip install logic-pro-toolkit[xml]

# All optional features
pip install logic-pro-toolkit[all]
```

## API Reference

Full API documentation is available at [https://logic-pro-toolkit.readthedocs.io](https://logic-pro-toolkit.readthedocs.io)

### Main Classes

- **LogicProject**: Main class for working with Logic Pro X projects
- **Track**: Represents an individual track in a project
- **MidiEvent**: Represents a single MIDI note or event
- **Marker**: Project markers and locators
- **Automation**: Track and plugin automation data
- **Preset**: Instrument and effect preset information

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/logic-pro-toolkit.git
cd logic-pro-toolkit

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black . --check
flake8 .

# Build documentation
cd docs
make html
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=logic_pro_toolkit

# Run specific test file
pytest tests/test_project_parsing.py -v
```

## Known Limitations

- Requires access to Logic Pro X project files (`.logicx`)
- Some advanced plugin parameters may not be fully supported
- Requires macOS for full project compatibility
- Real-time playback is not supported; this is a file manipulation toolkit

## Roadmap

- [ ] Support for Logic Pro 11.x projects
- [ ] Enhanced plugin parameter support
- [ ] Audio file analysis integration
- [ ] Web-based project viewer
- [ ] Collaborative project editing


## Screenshots

![Screenshot 1](assets/screenshots/screenshot-1.png)
![Screenshot 2](assets/screenshots/screenshot-2.png)
![Screenshot 3](assets/screenshots/screenshot-3.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This toolkit is designed for working with Logic Pro X project files you own or have permission to modify. Users are responsible for ensuring compliance with applicable software licenses and copyright regulations.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/logic-pro-toolkit/issues)
- **Documentation**: [Read the Docs](https://logic-pro-toolkit.readthedocs.io)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/logic-pro-toolkit/discussions)

## Authors

- Your Name ([@yourusername](https://github.com/yourusername))
- Contributors: [See CONTRIBUTORS.md](CONTRIBUTORS.md)

---

**Made with ♪ for music producers and developers**