# LogSystem Build and Docker Package Script

param(
    [string]$Version = "latest",
    [string]$Registry = "",
    [switch]$SkipBuild,
    [switch]$Push
)

# Color definitions
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

# Project info
$ProjectName = "logsystem"

# Change to project root directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

Write-Host "🚀 LogSystem build and Docker package process started..." -ForegroundColor $Blue
Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor $Blue

# Step 1: Local project build
if (-not $SkipBuild) {
    Write-Host "`n📦 Step 1: Building project locally..." -ForegroundColor $Yellow
    
    # Check and clean existing dist directory
    if (Test-Path "dist") {
        Write-Host "🗑️  Cleaning old build files..." -ForegroundColor $Yellow
        Remove-Item -Recurse -Force "dist"
    }
    
    # Check if dependencies are installed
    if (-not (Test-Path "node_modules")) {
        Write-Host "📥 Installing project dependencies..." -ForegroundColor $Yellow
        pnpm install
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Dependency installation failed" -ForegroundColor $Red
            exit 1
        }
    }
    
    # Execute build
    Write-Host "🔨 Building project..." -ForegroundColor $Yellow
    pnpm build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Project build failed" -ForegroundColor $Red
        exit 1
    }
    
    # Check build artifacts
    if (-not (Test-Path "dist")) {
        Write-Host "❌ Build artifacts not found, please check build configuration" -ForegroundColor $Red
        exit 1
    }
    
    Write-Host "✅ Project build successful!" -ForegroundColor $Green
    
    # Show build artifact info
    $distSize = (Get-ChildItem -Recurse "dist" | Measure-Object -Property Length -Sum).Sum
    $distSizeMB = [math]::Round($distSize / 1MB, 2)
    Write-Host "📊 Build artifact size: $distSizeMB MB" -ForegroundColor $Blue
} else {
    Write-Host "⏭️  Skipping local build step" -ForegroundColor $Yellow
}

# Step 2: Check Docker environment
Write-Host "`n🐳 Step 2: Checking Docker environment..." -ForegroundColor $Yellow

try {
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    Write-Host "✅ Docker environment OK" -ForegroundColor $Green
}
catch {
    Write-Host "❌ Docker not running, please start Docker Desktop first" -ForegroundColor $Red
    exit 1
}

# Step 3: Build Docker image
Write-Host "`n🏗️  Step 3: Building Docker image..." -ForegroundColor $Yellow

# Check if build artifacts exist
if (-not (Test-Path "dist")) {
    Write-Host "❌ dist directory not found, please run local build first" -ForegroundColor $Red
    exit 1
}

# Build Docker image
Write-Host "🔨 Building Docker image: ${ProjectName}:${Version}" -ForegroundColor $Yellow
docker build -t "${ProjectName}:${Version}" -t "${ProjectName}:latest" .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image build successful!" -ForegroundColor $Green
} else {
    Write-Host "❌ Docker image build failed" -ForegroundColor $Red
    exit 1
}

# Step 4: Show image info
Write-Host "`n📋 Step 4: Image information..." -ForegroundColor $Yellow
$images = docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" | Select-String $ProjectName
Write-Host $images -ForegroundColor $Blue

# Step 5: Push image (optional)
if ($Registry -ne "" -and $Push) {
    Write-Host "`n🚀 Step 5: Pushing image to registry..." -ForegroundColor $Yellow
    
    # Tag images
    docker tag "${ProjectName}:${Version}" "${Registry}/${ProjectName}:${Version}"
    docker tag "${ProjectName}:latest" "${Registry}/${ProjectName}:latest"
    
    # Push images
    docker push "${Registry}/${ProjectName}:${Version}"
    docker push "${Registry}/${ProjectName}:latest"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Image push completed!" -ForegroundColor $Green
    } else {
        Write-Host "❌ Image push failed" -ForegroundColor $Red
        exit 1
    }
} elseif ($Registry -ne "") {
    Write-Host "`n💡 Tip: To push image, add -Push parameter" -ForegroundColor $Yellow
}

# Complete
Write-Host "`n🎉 All operations completed!" -ForegroundColor $Green
Write-Host "💡 Usage:" -ForegroundColor $Blue
Write-Host "  Direct run: docker run -d -p 8080:80 ${ProjectName}:${Version}" -ForegroundColor $Yellow
Write-Host "  Use compose: docker-compose up -d" -ForegroundColor $Yellow
Write-Host "  Access URL: http://localhost:8080" -ForegroundColor $Yellow

Write-Host "`n📝 Other useful commands:" -ForegroundColor $Blue
Write-Host "  Check container status: docker ps" -ForegroundColor $Yellow
Write-Host "  View container logs: docker logs [container_id]" -ForegroundColor $Yellow
Write-Host "  Stop container: docker-compose down" -ForegroundColor $Yellow 