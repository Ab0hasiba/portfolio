# Email System Test Script for PowerShell

Write-Host "Email System Test" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

# Test data
$testData = @{
    name = "Test User"
    email = "test@example.com"
    message = "This is a test message from PowerShell script"
} | ConvertTo-Json

Write-Host "`nTesting email endpoint..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:5000/send-email"
Write-Host "Data: $testData"

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/send-email" -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 10
    
    Write-Host "`n✅ Response received:" -ForegroundColor Green
    Write-Host "Success: $($response.success)"
    Write-Host "Message: $($response.message)"
    
    if ($response.success) {
        Write-Host "`n🎉 Email test successful!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Email test failed: $($response.message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "`n❌ Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Message -like "*Connection*") {
        Write-Host "`n💡 Make sure the Flask server is running:" -ForegroundColor Yellow
        Write-Host "   cd backend" -ForegroundColor White
        Write-Host "   python app.py" -ForegroundColor White
    }
}

Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "Test completed!" -ForegroundColor Cyan
