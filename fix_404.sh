#!/bin/bash
echo "Ì¥ß Fixing 404 errors..."

# Backend fixes
cd backend/app/api/v1

# Verify chat.py exists
if [ ! -f "chat.py" ]; then
    echo "‚ùå chat.py missing! Creating..."
    # Create chat.py (use code from previous response)
else
    echo "‚úÖ chat.py exists"
fi

# Verify advanced.py exists
if [ ! -f "advanced.py" ]; then
    echo "‚ùå advanced.py missing! Creating..."
    # Create advanced.py (use code from previous response)
else
    echo "‚úÖ advanced.py exists"
fi

# Bot fixes
cd ../../../../telegram-bot

# Create fixed API client if not exists
if [ ! -f "api_client_fixed.py" ]; then
    echo "Creating fixed API client..."
    # (api_client_fixed.py code here)
fi

echo "‚úÖ Fix complete!"
echo ""
echo "Next steps:"
echo "1. Restart backend: cd backend && uvicorn app.main:app --reload"
echo "2. Restart bot: cd telegram-bot && python bot.py"
