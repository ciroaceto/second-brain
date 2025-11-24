#!/bin/bash

# Setup OpenTelemetry Observability with Jaeger
# This script starts Jaeger for trace visualization

set -e

echo "🔍 Setting up OpenTelemetry Observability..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker daemon is running${NC}"
echo ""

# Container name
CONTAINER_NAME="jaeger"

# Check if Jaeger container exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "📦 Jaeger container already exists"
    
    # Check if it's running
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${GREEN}✓ Jaeger is already running${NC}"
    else
        echo "🔄 Starting existing Jaeger container..."
        docker start ${CONTAINER_NAME}
        echo -e "${GREEN}✓ Jaeger started${NC}"
    fi
else
    echo "🚀 Creating and starting Jaeger container..."
    docker run -d --name ${CONTAINER_NAME} \
        -p 16686:16686 \
        -p 4317:4317 \
        -p 4318:4318 \
        jaegertracing/all-in-one:latest
    
    echo -e "${GREEN}✓ Jaeger container created and started${NC}"
fi

echo ""

# Wait a moment for Jaeger to fully start
echo "⏳ Waiting for Jaeger to be ready..."
sleep 3

# Verify Jaeger is accessible
if curl -s http://localhost:16686 > /dev/null; then
    echo -e "${GREEN}✓ Jaeger is accessible${NC}"
else
    echo -e "${YELLOW}⚠ Jaeger may still be starting up...${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 Observability Setup Complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Access Jaeger UI at:"
echo -e "   ${GREEN}http://localhost:16686${NC}"
echo ""
echo "🔌 OTLP Endpoints:"
echo "   gRPC: http://localhost:4317"
echo "   HTTP: http://localhost:4318"
echo ""
echo "🧪 Test your traces:"
echo "   uv run python main.py query \"test observability\""
echo ""
echo "🛑 Stop Jaeger:"
echo "   docker stop ${CONTAINER_NAME}"
echo ""
echo "🔄 Restart Jaeger:"
echo "   docker restart ${CONTAINER_NAME}"
echo ""
echo "🗑️  Remove Jaeger:"
echo "   docker rm -f ${CONTAINER_NAME}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

