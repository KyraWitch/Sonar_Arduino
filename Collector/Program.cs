using System.IO.Ports;
using System.Text;
using MyApi.Data;
using MyApi.Models;

// =============================================================================
//  SonarBackend - a CLI that reads sonar readings from the Arduino over
//  USB-C serial and stores them in a local SQLite database.
//
//  DATA FLOW
//    Arduino --(USB-C serial, 9600 baud)--> /dev/ttyACM0 --> this program --> database.sqlite
//
//  The Arduino sketch (Arduino/Sketches/) sends one reading per line, in the
//  form:  <angle>,<distance>.
//  e.g.   125,45.
//  The "." is the terminator that tells us a complete reading has arrived.
//
//  ----------------------------------------------------------------------------
//  NOTE FOR LATER: switching from USB cable to BLUETOOTH
//  ----------------------------------------------------------------------------
//  Right now the transport is a USB-C serial cable, opened via System.IO.Ports
//  (the "SerialPort" class below). The only place that matters for the
//  transport is the section marked  [TRANSPORT]  further down - everything
//  after it (parsing, saving to the database) does not care how the bytes
//  arrived.
//
//  When you move to Bluetooth you will replace the [TRANSPORT] section with a
//  Bluetooth connection instead of a SerialPort. You do NOT need to touch the
//  parsing or the database code - it will keep receiving the same
//  "angle,distance." text, just from a different source.
//
//  Libraries to look at for the Bluetooth side (not installed yet):
//    - UdpSharp / BluetoothSerial style: the Arduino exposes itself as a
//      "serial over Bluetooth" (SPP) device. On Linux that often still shows
//      up as a serial port (e.g. /dev/rfcomm0 or /dev/ttyUSB0), in which case
//      System.IO.Ports keeps working and you only change the device path.
//    - System.IO.Ports - the current serial transport (what we use today).
//    - If you go a "real" BLE route instead of classic BT serial, look at:
//        * BleLib  (https://github.com/davidfowl/blelib)
//        * Nordic's nRF Connect SDK on the Arduino/board side for the BLE GATT
//          service that would carry the readings.
//    The key idea: keep the "angle,distance." line format identical, so the
//    parsing code below keeps working no matter the transport.
// =============================================================================

const int baudRate = 9600;
var serialPath = args.Length > 0 ? args[0] : "/dev/ttyACM0";

// The database is a single shared instance (a singleton). We create it once and
// reuse it everywhere - see AppDbContext for how it is set up.
var db = AppDbContext.Instance;

// -----------------------------------------------------------------------------
//  [TRANSPORT] - open the connection to the Arduino.
//  TODAY: a USB-C serial cable, accessed as a serial port on the filesystem.
//  LATER: swap this block for a Bluetooth connection (see note at top).
// -----------------------------------------------------------------------------
SerialPort? port;
try
{
    // SerialPort(path, baudRate, parity, dataBits, stopBits)
    port = new SerialPort(serialPath, baudRate, Parity.None, 8, StopBits.One);
    port.ReadTimeout = 500; // don't block forever waiting for data
    port.Open();
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Could not open serial port '{serialPath}': {ex.Message}");
    Console.Error.WriteLine("Hint: run 'sudo usermod -aG dialout $USER', then log out and back in.");
    return 1;
}

Console.WriteLine($"Listening on {serialPath} @ {baudRate} baud. Ctrl+C to stop.");

// Lets Ctrl+C stop the loop cleanly instead of killing the process mid-write.
using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cts.Cancel(); };

// Bytes arrive in chunks, so we accumulate them until we see the "." terminator.
var buffer = new StringBuilder();
var lineCount = 0;

try
{
    while (!cts.IsCancellationRequested)
    {
        string chunk;
        try { chunk = port.ReadExisting(); }
        catch (TimeoutException) { continue; }             // no data yet, keep waiting
        catch (InvalidOperationException) { break; }       // port closed

        foreach (var c in chunk)
        {
            if (c is '\r' or '\n') continue; // ignore line endings

            if (c == '.')
            {
                // "." means we have a complete reading like "125,45."
                var line = buffer.ToString().Trim();
                buffer.Clear();
                if (line.Length == 0) continue;

                // A reading is exactly two numbers separated by a comma.
                var parts = line.Split(',');
                if (parts.Length != 2 ||
                    !double.TryParse(parts[0], out var angle) ||
                    !double.TryParse(parts[1], out var distance))
                {
                    Console.Error.WriteLine($"  ! unrecognized reading: '{line}'");
                    continue;
                }

                // Persist the reading to SQLite and echo it to the console.
                var reading = new Reading { Timestamp = DateTime.UtcNow, Angle = angle, Distance = distance };
                db.Readings.Add(reading);
                db.SaveChanges();
                lineCount++;

                Console.WriteLine($"[{reading.Timestamp:O}] angle={angle,8:F3}  distance={distance,8:F3} cm");
            }
            else
            {
                buffer.Append(c);
            }
        }
    }
}
finally
{
    port.Close();
    Console.WriteLine($"\nStopped. {lineCount} new readings this session, {db.Readings.Count()} total in database.sqlite");
}

return 0;
