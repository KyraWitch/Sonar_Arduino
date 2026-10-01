namespace MyApi.Models;

public class Reading
{
    public int Id { get; set; }
    public DateTime Timestamp { get; set; }
    public double Angle { get; set; }
    public double Distance { get; set; }
}