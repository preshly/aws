using Amazon.Lambda.AspNetCoreServer.Hosting;
using Amazon.SimpleNotificationService;
using Amazon.SimpleNotificationService.Model;
using Amazon.Extensions.NETCore.Setup;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDefaultAWSOptions(builder.Configuration.GetAWSOptions());
builder.Services.AddAWSLambdaHosting(LambdaEventSource.HttpApi);
builder.Services.AddAWSService<IAmazonSimpleNotificationService>();

var app = builder.Build();

var snsTopicArn = Environment.GetEnvironmentVariable("SNS_TOPIC_ARN");

app.MapGet("/", () => "Lambda health check API. System running smoothly!");

app.MapGet("/policy", async (IAmazonSimpleNotificationService sns) =>
{
    if (string.IsNullOrEmpty(snsTopicArn))
    {
        Console.WriteLine("SNS Topic ARN not set.");
        return Results.Problem("Something went wrong. Please try again later.");
    }
    var policy = new
    {
        PolicyId = "POL12345",
        Holder = "John Doe",
        Premium = 5000,
        Status = "Active"
    };
    try
    {
        var message = $"Policy details for {policy.PolicyId} were fetched by {policy.Holder} at {DateTime.UtcNow}.";
        await sns.PublishAsync(new PublishRequest
        {
            TopicArn = snsTopicArn,
            Message = message
        });
    }
    catch (Exception e)
    {
        Console.WriteLine($"Error: {e.Message}");
        return Results.Problem("Something went wrong. Please try again later.");
    }
    return Results.Ok(policy);
});

app.Run();
