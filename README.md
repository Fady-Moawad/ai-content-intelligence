POST /analyze
       ↓
Language Detection
       ↓
Routing
   ┌───┴────┐
Arabic    English
   └───┬────┘
       ↓
   Parallel
 ┌─────┼─────┐
 ↓     ↓     ↓
Summary Sentiment Topics
 └─────┼─────┘
       ↓
 Python Processing
       ↓
 Final Structured Report