using System;


// Notes
// Make classes then construct then send to the database 
// So 3 files 1 for class, 1 for constructor, 1 for database connection
public class Detection
{
    public DateTime DetectionTime = DateTime.Now;
    public string Distance { get; set; }

}