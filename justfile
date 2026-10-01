set shell := ["bash", "-cu"]

# Directory that holds the .NET collector project.
collector := "Collector"
app := "SonarBackend"

default:
    @just --list

# One-time setup for a fresh machine: install deps and add the user to the
# dialout group for serial port access.
bootstrap:
    brew install just || echo "just already installed"
    brew install dotnet || brew install --cask dotnet-sdk || echo "dotnet already installed (or install manually)"
    dotnet --info | grep -E 'SDK|Version' | head -3
    @echo "Adding current user to 'dialout' group for serial port access..."
    sudo usermod -aG dialout "$USER"
    @echo "Done. Log out and back in for the group change to take effect."
    @echo "Verify with: groups | grep dialout"

# Build the collector for the current platform.
build:
    dotnet build {{collector}}/{{app}}.csproj -c Release

# Run the app (default /dev/ttyACM0, or pass a port: just run /dev/ttyUSB0).
run *port:
    cd {{collector}} && dotnet run --project {{app}}.csproj -c Release -- {{port}}
