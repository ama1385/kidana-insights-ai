@echo off
cd /d "%~dp0"
git init
git add .
git commit -m "🚀 أول رفع لمشروع Kidana Insights AI"
git branch -M main
git remote remove origin
git remote add origin https://github.com/ama1385/kidana-insights-ai.git
git push -u origin main
pause
