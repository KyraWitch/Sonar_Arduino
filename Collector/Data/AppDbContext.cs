using Microsoft.EntityFrameworkCore;
using MyApi.Models;

namespace MyApi.Data;

public class AppDbContext : DbContext
{
    private static readonly Lazy<AppDbContext> _instance =
        new(() => new AppDbContext());

    public static AppDbContext Instance => _instance.Value;

    private AppDbContext()
        : base(new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite("Data Source=database.sqlite")
            .Options)
    {
        Database.EnsureCreated();
    }

    public DbSet<Reading> Readings => Set<Reading>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Reading>().HasKey(e => e.Id);
    }
}
