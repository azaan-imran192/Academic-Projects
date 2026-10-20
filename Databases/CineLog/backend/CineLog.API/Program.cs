using CineLog.BLL;
using CineLog.BLL.Services;
using CineLog.Data.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
if (string.IsNullOrWhiteSpace(connectionString))
    throw new InvalidOperationException("Set ConnectionStrings__DefaultConnection to your local CineLog database connection string.");
builder.Services.AddDbContext<CineLogContext>(options => options.UseSqlServer(connectionString));

builder.Services.AddScoped<ICineLogService>(provider =>
{
    var context = provider.GetRequiredService<CineLogContext>();
    return CineLogServiceFactory.Create(context);
});

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();