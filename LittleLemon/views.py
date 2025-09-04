from django.http import HttpResponse
from django.shortcuts import render, redirect

def home_view(request):
    """Simple home page that redirects to API"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Little Lemon Restaurant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .logo {
                font-size: 3em;
                margin-bottom: 20px;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            .description {
                color: #7f8c8d;
                font-size: 1.1em;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .links {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
                font-weight: bold;
            }
            .btn:hover {
                background: #2980b9;
            }
            .btn.admin {
                background: #e74c3c;
            }
            .btn.admin:hover {
                background: #c0392b;
            }
            .endpoints {
                margin-top: 30px;
                text-align: left;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
            }
            .endpoints h3 {
                margin-top: 0;
                color: #2c3e50;
            }
            .endpoints ul {
                list-style: none;
                padding: 0;
            }
            .endpoints li {
                margin: 8px 0;
                padding: 8px;
                background: white;
                border-radius: 3px;
                border-left: 4px solid #3498db;
            }
            .endpoints a {
                color: #2c3e50;
                text-decoration: none;
            }
            .endpoints a:hover {
                color: #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🍋</div>
            <h1>Welcome to Little Lemon Restaurant</h1>
            <p class="description">
                Your favorite Mediterranean restaurant is now online! 
                Explore our delicious menu, read reviews, and discover what makes our food special.
            </p>
            
            <div class="links">
                <a href="/api/" class="btn">🚀 Explore API</a>
                <a href="/admin/" class="btn admin">👨‍💼 Admin Panel</a>
            </div>
            
            <div class="endpoints">
                <h3>🔗 Quick Links</h3>
                <ul>
                    <li><a href="/api/">📋 API Documentation</a></li>
                    <li><a href="/api/categories/">📂 View Categories</a></li>
                    <li><a href="/api/menu-items/">🍽️ Browse Menu Items</a></li>
                    <li><a href="/api/ratings/">⭐ Customer Ratings</a></li>
                </ul>
            </div>
            
            <div style="margin-top: 30px; color: #7f8c8d; font-size: 0.9em;">
                <p>💡 <strong>Tip:</strong> Try the API endpoints above to see our restaurant data in action!</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
