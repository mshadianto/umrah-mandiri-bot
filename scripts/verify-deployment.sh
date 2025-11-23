#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     DEPLOYMENT VERIFICATION SCRIPT                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Enter your Railway backend URL (e.g., https://backend-xxx.railway.app):"
read BACKEND_URL

echo ""
echo "�� Testing backend health..."
HEALTH_CHECK=$(curl -s "${BACKEND_URL}/health")

if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend is healthy!${NC}"
    echo "Response: $HEALTH_CHECK"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    echo "Response: $HEALTH_CHECK"
    exit 1
fi

echo ""
echo "��� Testing backend API endpoints..."

# Test users endpoint
USERS_TEST=$(curl -s -o /dev/null -w "%{http_code}" "${BACKEND_URL}/api/v1/users/health")
if [[ $USERS_TEST == "200" ]]; then
    echo -e "${GREEN}✅ Users API: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Users API: HTTP $USERS_TEST${NC}"
fi

# Test chat endpoint  
CHAT_TEST=$(curl -s -X POST "${BACKEND_URL}/api/v1/chat/health")
if [[ $CHAT_TEST == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Chat API: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Chat API: Check logs${NC}"
fi

# Test advanced endpoint
ADVANCED_TEST=$(curl -s "${BACKEND_URL}/api/v1/advanced/health")
if [[ $ADVANCED_TEST == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Advanced API: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Advanced API: Check logs${NC}"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  BACKEND VERIFICATION COMPLETE                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next: Test your bot in Telegram!"
echo "1. Open Telegram"
echo "2. Find your bot"
echo "3. Send: /start"
echo "4. Click buttons and test features"
echo ""
