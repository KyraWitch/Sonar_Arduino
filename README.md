# Sonar_Arduino

Project and repository for the sonar arduino project.

This project is currently under development by Eden Hviid.

## Overview

The sonar board (Arduino) sweeps an ultrasonic sensor with a servo and streams
each reading over USB-C serial. The `Collector` CLI (C# / .NET 10) listens on
the serial port, parses each reading, and stores it in a SQLite database
(`Collector/database.sqlite`).

```
Arduino (USB-C)  --Serial 9600-->  /dev/ttyACM0  -->  SonarBackend (C#)  -->  database.sqlite
```

Wire protocol (emitted by the sketch's `sendData()`):

```
<angle>,<distance>.
```

Example: `125,45.`  (125 degrees, 45 cm). The `.` terminates a reading.

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download)
- [just](https://github.com/casey/just) — command runner (used in place of shell scripts)
- Arduino IDE (or `arduino-cli`) to flash the sketch

Install via Homebrew:

```sh
brew install --cask dotnet-sdk   # or: brew install dotnet
brew install just
```

## Serial port permissions (Linux)

The Arduino shows up as a serial device (e.g. `/dev/ttyACM0`) owned by the
`dialout` group. Your user must be in that group to read it, otherwise opening
the port fails with "Permission denied".

One-time setup:

```sh
sudo usermod -aG dialout "$USER"
```

Then **log out and back in** (group membership applies at next login). Verify:

```sh
groups | grep dialout
ls -l /dev/ttyACM0        # should show: crw-rw---- root dialout
```

> Note: which device node appears depends on your board's USB-serial chip.
> `ttyACM*` is typical for CDC-ACM (native USB) boards; `ttyUSB*` for
> FTDI/CH340/CP210x adapters. Check `ls /dev/ttyACM* /dev/ttyUSB*` after
> plugging in, and pass the right one to the app if it isn't the default.

## Usage

All commands are driven by [just](https://github.com/casey/just). Run `just`
with no arguments to list available recipes.

| Command            | What it does                                              |
| ------------------ | --------------------------------------------------------- |
| `just bootstrap`   | Installs deps (dotnet, just) + sets up serial permissions |
| `just build`       | Builds the collector for the current platform             |
| `just run`         | Runs the app, listening on `/dev/ttyACM0`                 |
| `just run <port>`  | Runs the app on a specific port, e.g. `just run /dev/ttyUSB0` |

### Typical flow

```sh
just bootstrap     # new machine
just build
just run           # plug in the Arduino, start capturing readings
```

Readings print to the console as they land and are written to
`Collector/database.sqlite` (created automatically on first run).

### Inspecting the database

```sh
sqlite3 Collector/database.sqlite 'SELECT * FROM Readings ORDER BY Id DESC LIMIT 10;'
```

## Arduino sketch

See `Arduino/Sketches/`. Flash the sketch with the Arduino IDE, making sure
`BAUD_RATE` (9600) matches the collector. The sketch currently has a few WIP
compile errors (see notes below) that must be fixed before it will upload.

## Project layout

```
Collector/
  Program.cs              # serial listener + entry point
  Data/AppDbContext.cs    # EF Core DbContext (SQLite singleton)
  Models/Reading.cs       # reading entity (Timestamp, Angle, Distance)
  SonarBackend.csproj     # .NET 10 console project
Arduino/
  Sketches/               # the sonar board firmware
  Cad/                    # printed parts (STL)
  python_cad/             # CAD generation scripts
docs/                     # design docs + diagrams
```
